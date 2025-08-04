from django.contrib import admin
from .models import Evento, Participante, Inscricao

admin.site.register(Evento)
admin.site.register(Participante)
admin.site.register(Inscricao)

