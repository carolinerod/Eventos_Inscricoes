from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Evento, Participante, Inscricao
from .forms import EventoForm, ParticipanteForm

class EventoListView(ListView):
    model = Evento
    template_name = 'eventos/evento_list.html'
    context_object_name = 'eventos'


class EventoCreateView(CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento-list')


class EventoUpdateView(UpdateView):
    model = Evento
    fields = ['titulo', 'descricao', 'data', 'local', 'imagem']
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento-list')


class EventoDeleteView(DeleteView):
    model = Evento
    template_name = 'eventos/evento_confirm_delete.html'
    success_url = reverse_lazy('evento-list')


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
        Inscricao.objects.create(evento=self.evento, participante=participante)

        send_mail(
            subject='Confirmação de Inscrição',
            message=f'Olá {participante.nome}, sua inscrição no evento "{self.evento.titulo}" foi confirmada!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[participante.email],
            fail_silently=False,
        )

        
        send_mail(
            subject='Nova Inscrição Recebida',
            message=f'{participante.nome} se inscreveu no evento "{self.evento.titulo}".',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        messages.success(self.request, "Inscrição realizada com sucesso!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('evento-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evento'] = self.evento
        return context
