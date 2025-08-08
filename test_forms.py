from django.test import TestCase
from django.utils import timezone
from eventos.models import Evento, Participante, Inscricao

class ModelTests(TestCase):
    def setUp(self):
        self.evento = Evento.objects.create(
            titulo="Workshop SQL",
            tipo="WORKSHOP",
            data=timezone.now(),  # DateTimeField ok
            local="Sala 101",
            descricao="Intensivo SQL",
            capacidade=2,
        )
        self.part = Participante.objects.create(
            nome="Ana",
            email="ana@example.com",
            telefone="11999990000",
            assistencia="NENHUMA",
        )

    def test_total_inscritos(self):
        # precisa existir um método total_inscritos no model Evento
        # ex: return self.inscricoes.count()
        self.assertEqual(self.evento.total_inscritos(), 0)
        Inscricao.objects.create(evento=self.evento, participante=self.part)
        self.assertEqual(self.evento.total_inscritos(), 1)

    def test_strs(self):
        self.assertIn("Workshop SQL", str(self.evento))
        insc = Inscricao.objects.create(evento=self.evento, participante=self.part)
        self.assertIn("Ana", str(insc))
