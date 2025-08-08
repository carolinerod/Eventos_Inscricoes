from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    EventoListView,
    EventoCreateView,
    EventoUpdateView,
    EventoDeleteView,
    InscricaoCreateView,
    IngressoDetailView,
    ListaInscritosView,
    InscricoesAdminListView,
    exportar_inscritos_evento_csv,
    exportar_inscricoes_csv,
    DashboardView,
)

urlpatterns = [
    path('', EventoListView.as_view(), name='evento-list'),
    path('evento/<int:pk>/inscrever/', InscricaoCreateView.as_view(), name='evento-inscricao'),
    path('ingresso/<int:pk>/', IngressoDetailView.as_view(), name='ingresso-detail'),
    path('novo/', EventoCreateView.as_view(), name='evento-create'),
    path('editar/<int:pk>/', EventoUpdateView.as_view(), name='evento-update'),
    path('<int:pk>/excluir/', EventoDeleteView.as_view(), name='evento-delete'),
    path('login/', LoginView.as_view(template_name='eventos/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='evento-list'), name='logout'),
    path('evento/<int:pk>/inscritos/', ListaInscritosView.as_view(), name='evento-inscritos'),
    path('inscricoes/', InscricoesAdminListView.as_view(), name='inscricoes-admin'),
    path('evento/<int:pk>/inscritos/exportar/', exportar_inscritos_evento_csv, name='evento-inscritos-exportar'),
    path('inscricoes/exportar/', exportar_inscricoes_csv, name='inscricoes-exportar'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
