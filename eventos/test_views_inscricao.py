# eventos/tests/test_views_inscricao.py
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core import mail

from eventos.models import Evento, Participante, Inscricao


class InscricaoViewTests(TestCase):
    def setUp(self):
        self.evento = Evento.objects.create(
            titulo="Minicurso Python",
            tipo="MINICURSO",
            data=timezone.now(),
            local="Lab 2",
            descricao="Aulas práticas",
            capacidade=1,  # intencional para testar fluxo de capacidade/duplicidade
        )
        # URL conforme seu urls.py
        self.url_inscricao = reverse('evento-inscricao', args=[self.evento.pk])

    def test_inscricao_sucesso_envia_email_html_uma_vez(self):
        """Primeira inscrição deve criar, renderizar página e enviar 1 e-mail (participante)."""
        form_data = {
            'nome': 'Ana',
            'email': 'ana@example.com',
            'telefone': '333',
            'assistencia': 'NENHUMA',
            'assistencia_detalhes': '',
        }
        resp = self.client.post(self.url_inscricao, data=form_data, follow=True)
        self.assertEqual(resp.status_code, 200)

        # A view envia e-mail do participante e SÓ envia ao organizador se SEND_ORGANIZER_EMAIL=True.
        # Como a flag default é False, esperamos 1 e-mail.
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('ana@example.com', mail.outbox[0].to)

        # Deve ter sido criada exatamente uma inscrição
        self.assertEqual(Inscricao.objects.filter(evento=self.evento).count(), 1)

    def test_nao_permite_duplicidade_mesmo_email_mesmo_evento(self):
        """Com a lógica nova: duplicidade é verificada antes da capacidade -> mensagem correta."""
        # Cria a primeira inscrição
        p = Participante.objects.create(
            nome='Ana', email='ana@example.com', telefone='333', assistencia='NENHUMA'
        )
        Inscricao.objects.create(evento=self.evento, participante=p)

        # Tenta inscrever o mesmo e-mail de novo
        form_data = {
            'nome': 'Ana',
            'email': 'ana@example.com',
            'telefone': '333',
            'assistencia': 'NENHUMA',
            'assistencia_detalhes': '',
        }
        resp = self.client.post(self.url_inscricao, data=form_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Você já está inscrito neste evento.")

        # Continua existindo apenas 1 inscrição
        self.assertEqual(Inscricao.objects.filter(evento=self.evento).count(), 1)

        # Não deve disparar novo e-mail
        self.assertEqual(len(mail.outbox), 0)
