from django.urls import path
from .views import (
    EventoListView,
    EventoCreateView,
    EventoUpdateView,
    EventoDeleteView,
    InscricaoCreateView,
)

urlpatterns = [
    path('', EventoListView.as_view(), name='evento-list'),
    path('novo/', EventoCreateView.as_view(), name='evento-create'),
    path('editar/<int:pk>/', EventoUpdateView.as_view(), name='evento-update'),
    path('<int:pk>/excluir/', EventoDeleteView.as_view(), name='evento-delete'),
    path('evento/<int:pk>/inscrever/', InscricaoCreateView.as_view(), name='evento-inscricao'),
]
