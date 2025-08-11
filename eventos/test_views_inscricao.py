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
            capacidade=1,  
        )
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

        
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('ana@example.com', mail.outbox[0].to)

        self.assertEqual(Inscricao.objects.filter(evento=self.evento).count(), 1)

    def test_nao_permite_duplicidade_mesmo_email_mesmo_evento(self):
        """Com a lógica nova: duplicidade é verificada antes da capacidade -> mensagem correta."""
        # Cria a primeira inscrição
        p = Participante.objects.create(
            nome='Ana', email='ana@example.com', telefone='333', assistencia='NENHUMA'
        )
        Inscricao.objects.create(evento=self.evento, participante=p)

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

        self.assertEqual(Inscricao.objects.filter(evento=self.evento).count(), 1)

        self.assertEqual(len(mail.outbox), 0)
