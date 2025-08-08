# eventos/test_views_export.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from eventos.models import Evento, Participante, Inscricao

User = get_user_model()


class ExportCsvTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # usuário para passar pelo @login_required das views
        cls.user = User.objects.create_user(
            username='admin', password='x', is_staff=True
        )

    def setUp(self):
        self.client.force_login(self.user)

        self.evento = Evento.objects.create(
            titulo="Minicurso Python",
            tipo="MINICURSO",
            data=timezone.now(),
            local="Lab 2",
            descricao="Conteúdo prático",
            capacidade=10,
        )
        self.p1 = Participante.objects.create(
            nome="Ana",
            email="ana@example.com",
            telefone="333",
            assistencia="NENHUMA",
            assistencia_detalhes="—",
        )
        self.p2 = Participante.objects.create(
            nome="Bruno",
            email="bruno@example.com",
            telefone="444",
            assistencia="NENHUMA",
            assistencia_detalhes="Precisa de tomada próxima",
        )
        Inscricao.objects.create(evento=self.evento, participante=self.p1)
        Inscricao.objects.create(evento=self.evento, participante=self.p2)

    def test_exportar_inscritos_evento_csv(self):
        """
        Exporta inscritos de um evento específico.
        URL: 'evento-inscritos-exportar', args=[evento.pk]
        Cabeçalho esperado: ['Evento','Data/Hora','Participante','Email','Telefone','Observações','Data inscrição']
        """
        url = reverse('evento-inscritos-exportar', args=[self.evento.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        content = resp.content.decode('utf-8')
        # Cabeçalho
        self.assertIn("Evento,Data/Hora,Participante,Email,Telefone,Observações,Data inscrição", content)
        # Conteúdo básico
        self.assertIn("Minicurso Python", content)
        self.assertIn("Ana", content)
        self.assertIn("Bruno", content)
        # Observações vêm de assistencia_detalhes
        self.assertIn("Precisa de tomada próxima", content)

    def test_exportar_inscricoes_filtradas_csv(self):
        """
        Exporta inscrições filtradas por evento (querystring ?evento=<id>).
        URL: 'inscricoes-exportar'
        Cabeçalho esperado: ['Evento','Data/Hora','Participante','Email','Telefone','Observações','Data inscrição']
        """
        url = reverse('inscricoes-exportar')
        resp = self.client.get(url, {'evento': self.evento.pk})
        self.assertEqual(resp.status_code, 200)

        content = resp.content.decode('utf-8')
        # Cabeçalho
        self.assertIn("Evento,Data/Hora,Participante,Email,Telefone,Observações,Data inscrição", content)
        # Conteúdo básico
        self.assertIn("Minicurso Python", content)
        self.assertIn("Ana", content)
        self.assertIn("Bruno", content)
        # Observações vêm de assistencia_detalhes
        self.assertIn("Precisa de tomada próxima", content)
