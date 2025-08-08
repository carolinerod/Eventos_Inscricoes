from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.db.models import Q, Count
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
import csv

from .models import Evento, Participante, Inscricao
from .forms import EventoForm, ParticipanteForm


class EventoListView(ListView):
    model = Evento
    template_name = 'eventos/evento_list.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        qs = super().get_queryset().order_by('data')
        data_str = self.request.GET.get('data')
        local = self.request.GET.get('local')
        if data_str:
            qs = qs.filter(data__date=data_str)
        if local:
            qs = qs.filter(local__icontains=local.strip())
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['f_data'] = self.request.GET.get('data', '')
        ctx['f_local'] = self.request.GET.get('local', '')
        return ctx


class EventoCreateView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento-list')
    login_url = 'login'

    def form_invalid(self, form):
        messages.error(self.request, "Há erros no formulário. Por favor, corrija os campos destacados.")
        return super().form_invalid(form)


class EventoUpdateView(LoginRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento-list')
    login_url = 'login'

    def form_invalid(self, form):
        messages.error(self.request, "Há erros no formulário. Por favor, corrija os campos destacados.")
        return super().form_invalid(form)


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

    def form_invalid(self, form):
        messages.error(self.request, "Há erros no formulário. Verifique os campos e tente novamente.")
        return super().form_invalid(form)

    def form_valid(self, form):
        cd = form.cleaned_data
        email = (cd.get('email') or '').strip()

        if Inscricao.objects.filter(evento=self.evento, participante__email__iexact=email).exists():
            messages.warning(self.request, "Você já está inscrito neste evento.")
            return self.form_invalid(form)

        if self.evento.inscricoes.count() >= self.evento.capacidade:
            messages.error(self.request, "Evento esgotado.")
            return self.form_invalid(form)

        participante = Participante.objects.filter(email__iexact=email).first()
        if not participante:
            participante = Participante(email=email)

        # Atualiza dados sempre
        participante.nome = cd.get('nome')
        participante.telefone = cd.get('telefone')
        participante.assistencia = cd.get('assistencia')
        participante.assistencia_detalhes = cd.get('assistencia_detalhes')
        participante.save()

        # 4) Cria Inscrição
        inscricao = Inscricao.objects.create(evento=self.evento, participante=participante)

        # 5) E-mail HTML para o participante
        contexto_email = {
            'inscricao': inscricao,
            'evento': self.evento,
            'url_ingresso': self.request.build_absolute_uri(
                reverse('ingresso-detail', args=[inscricao.pk])
            ),
        }
        html_content = render_to_string('eventos/ingresso_email.html', contexto_email)

        email_msg = EmailMultiAlternatives(
            subject=f'Confirmação de Inscrição: {self.evento.titulo}',
            body="Sua inscrição foi confirmada.",
            from_email=settings.EMAIL_HOST_USER,
            to=[participante.email],
        )
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()

        if getattr(settings, 'SEND_ORGANIZER_EMAIL', False):
            send_mail(
                subject='Nova Inscrição Recebida',
                message=f'{participante.nome} se inscreveu no evento "{self.evento.titulo}".',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

        messages.success(self.request, "Inscrição realizada com sucesso! Verifique seu e-mail.")
        self.inscricao = inscricao
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('evento-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evento'] = self.evento
        context['inscricao'] = getattr(self, 'inscricao', None)
        return context


class IngressoDetailView(DetailView):
    model = Inscricao
    template_name = 'eventos/ingresso.html'
    context_object_name = 'inscricao'


class ListaInscritosView(LoginRequiredMixin, DetailView):
    """Lista inscritos de um evento específico, com busca."""
    model = Evento
    template_name = 'eventos/inscritos_list.html'
    context_object_name = 'evento'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        inscricoes = self.object.inscricoes.select_related('participante').all()
        if q:
            inscricoes = inscricoes.filter(
                Q(participante__nome__icontains=q) |
                Q(participante__email__icontains=q) |
                Q(participante__telefone__icontains=q)
            )
        ctx['q'] = q
        ctx['inscricoes'] = inscricoes
        return ctx


class InscricoesAdminListView(LoginRequiredMixin, ListView):
    """Página geral de inscrições com filtro por evento e busca."""
    model = Inscricao
    template_name = 'eventos/inscricoes_admin_list.html'
    context_object_name = 'inscricoes'
    paginate_by = 20
    login_url = 'login'

    def get_queryset(self):
        qs = super().get_queryset().select_related('evento', 'participante').order_by('-data_inscricao')
        evento_id = self.request.GET.get('evento')
        q = self.request.GET.get('q')

        if evento_id:
            qs = qs.filter(evento_id=evento_id)
        if q:
            qs = qs.filter(
                Q(participante__nome__icontains=q) |
                Q(participante__email__icontains=q) |
                Q(participante__telefone__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['eventos'] = Evento.objects.annotate(total=Count('inscricoes')).order_by('data')
        ctx['selected_evento'] = self.request.GET.get('evento') or ''
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


@login_required(login_url='login')
def exportar_inscritos_evento_csv(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    inscricoes = evento.inscricoes.select_related('participante').order_by('data_inscricao')

    response = HttpResponse(content_type='text/csv')
    filename = f'inscritos_{evento.titulo}_{evento.data.strftime("%Y%m%d_%H%M")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Evento', 'Data/Hora', 'Participante', 'Email', 'Telefone', 'Observações', 'Data inscrição'])

    for ins in inscricoes:
        p = ins.participante
        writer.writerow([
            smart_str(evento.titulo),
            evento.data.strftime('%d/%m/%Y %H:%M'),
            smart_str(p.nome),
            p.email,
            smart_str(p.telefone),
            smart_str(getattr(p, 'assistencia_detalhes', '') or ''),
            ins.data_inscricao.strftime('%d/%m/%Y %H:%M'),
        ])

    return response


@login_required(login_url='login')
def exportar_inscricoes_csv(request):
    qs = Inscricao.objects.select_related('evento', 'participante').order_by('-data_inscricao')
    evento_id = request.GET.get('evento')
    q = request.GET.get('q')

    if evento_id:
        qs = qs.filter(evento_id=evento_id)
    if q:
        qs = qs.filter(
            Q(participante__nome__icontains=q) |
            Q(participante__email__icontains=q) |
            Q(participante__telefone__icontains=q)
        )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inscricoes_filtradas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Evento', 'Data/Hora', 'Participante', 'Email', 'Telefone', 'Observações', 'Data inscrição'])

    for ins in qs:
        p = ins.participante
        writer.writerow([
            smart_str(ins.evento.titulo),
            ins.evento.data.strftime('%d/%m/%Y %H:%M'),
            smart_str(p.nome),
            p.email,
            smart_str(p.telefone),
            smart_str(getattr(p, 'assistencia_detalhes', '') or ''),
            ins.data_inscricao.strftime('%d/%m/%Y %H:%M'),
        ])

    return response


class OrganizadorLoginView(LoginView):
    template_name = 'eventos/login.html'


class OrganizadorLogoutView(LogoutView):
    next_page = reverse_lazy('evento-list')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'eventos/dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['eventos'] = Evento.objects.annotate(total=Count('inscricoes')).order_by('-data')
        ctx['totais'] = {
            'eventos': Evento.objects.count(),
            'inscricoes': Inscricao.objects.count(),
            'participantes': Participante.objects.count(),
        }
        return ctx
