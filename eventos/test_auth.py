from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from eventos.models import Evento

class AuthRequiredViewsTests(TestCase):
    def setUp(self):
        self.evento = Evento.objects.create(
            titulo="Palestra A",
            tipo="PALESTRA",
            data=timezone.now(),
            local="Auditório",
            descricao="Tema A",
            capacidade=10
        )

    def test_crud_evento_requires_login(self):
        resp = self.client.get(reverse('evento-create'))
        self.assertEqual(resp.status_code, 302)  # redirect to login

        # Após login
        User.objects.create_user('org', 'org@example.com', '123456')
        self.client.login(username='org', password='123456')

        self.assertEqual(self.client.get(reverse('evento-create')).status_code, 200)
        self.assertEqual(self.client.get(reverse('evento-update', args=[self.evento.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse('evento-delete', args=[self.evento.pk])).status_code, 200)
