from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField

class Evento(models.Model):
    TIPO_CHOICES = [
        ('PALESTRA', 'Palestra'),
        ('WORKSHOP', 'Workshop'),
        ('MINICURSO', 'Minicurso'),
        ('NETWORK', 'Networking'),
        ('OUTRO', 'Outro'),
    ]

    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='PALESTRA')
    data = models.DateTimeField()
    local = models.CharField(max_length=100)
    descricao = models.TextField()
    observacao_organizador = models.TextField(blank=True, null=True)
    capacidade = models.PositiveIntegerField()
    imagem = CloudinaryField('imagem', blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.data.strftime('%d/%m/%Y %H:%M')}"

    def total_inscritos(self):
        return self.inscricoes.count()

class Participante(models.Model):
    ASSISTENCIA_CHOICES = [
        ('NENHUMA', 'Não preciso de assistência'),
        ('LOCOMOCAO', 'Assistência de locomoção'),
        ('AUDIOVISUAL', 'Apoio audiovisual (ex.: legendas, intérprete)'),
        ('OUTRA', 'Outro (descrever)'),
    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    assistencia = models.CharField(max_length=20, choices=ASSISTENCIA_CHOICES, default='NENHUMA')
    assistencia_detalhes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Inscricao(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes')
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='inscricoes')
    data_inscricao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.participante.nome} em {self.evento.titulo}"
