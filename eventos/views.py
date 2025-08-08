from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin  
from django.template.loader import render_to_string
from .models import Evento, Participante, Inscricao
from .forms import EventoForm, ParticipanteForm


class EventoListView(ListView):
    model = Evento
    template_name = 'eventos/evento_list.html'
    context_object_name = 'eventos'


class EventoCreateView(LoginRequiredMixin, CreateView): 
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento-list')
    login_url = 'login'  


class EventoUpdateView(LoginRequiredMixin, UpdateView):  
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento-list')
    login_url = 'login'


class EventoDeleteView(LoginRequiredMixin, DeleteView):  
    model = Evento
    template_name = 'eventos/evento_confirm_delete.html'
    success_url = reverse_lazy('evento-list')
    login_url = 'login'


class InscricaoCreateView(FormView):  
    template_name = 'eventos/inscricao_form.html'
    form_class = ParticipanteForm

    def dispatch(self, request, *args, **kwargs):
        self.evento = get_object_or_404(Evento, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.evento.inscricoes.count() >= self.evento.capacidade:
            messages.error(self.request, "Evento esgotado.")
            return self.form_invalid(form)

        participante = form.save()

        if Inscricao.objects.filter(evento=self.evento, participante__email=participante.email).exists():
            messages.warning(self.request, "Você já está inscrito neste evento.")
            return self.form_invalid(form)

        inscricao = Inscricao.objects.create(evento=self.evento, participante=participante)

        contexto_email = {
            'inscricao': inscricao,
            'evento': self.evento,
            'url_ingresso': self.request.build_absolute_uri(reverse('ingresso-detail', args=[inscricao.pk]))
        }
        html_content = render_to_string('eventos/ingresso_email.html', contexto_email)

        email = EmailMultiAlternatives(
            subject=f'Confirmação de Inscrição: {self.evento.titulo}',
            body="Sua inscrição foi confirmada.",
            from_email=settings.EMAIL_HOST_USER,
            to=[participante.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        send_mail(
            subject='Nova Inscrição Recebida',
            message=f'{participante.nome} se inscreveu no evento "{self.evento.titulo}".',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        messages.success(self.request, "Inscrição realizada com sucesso! Verifique seu e-mail.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('evento-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evento'] = self.evento
        return context


class IngressoDetailView(DetailView):
    model = Inscricao
    template_name = 'eventos/ingresso.html'
    context_object_name = 'inscricao'


class OrganizadorLoginView(LoginView):
    template_name = 'eventos/login.html'


class OrganizadorLogoutView(LogoutView):
    next_page = reverse_lazy('evento-list')
