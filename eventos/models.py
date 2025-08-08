from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField  # ✅ Para armazenar imagens no Cloudinary

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    data = models.DateTimeField()  # ✅ Já armazena data + hora
    local = models.CharField(max_length=100)
    descricao = models.TextField()
    capacidade = models.PositiveIntegerField()
    imagem = CloudinaryField('imagem', blank=True, null=True)  # ✅ Imagem do evento para usar no ingresso

    def __str__(self):
        return f"{self.titulo} - {self.data.strftime('%d/%m/%Y %H:%M')}"

    def total_inscritos(self):
        return self.inscricoes.count()  # ✅ Facilita ver o total de inscritos no admin ou no template


class Participante(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Inscricao(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes')
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='inscricoes')
    data_inscricao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.participante.nome} em {self.evento.titulo}"
