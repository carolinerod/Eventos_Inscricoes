from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    EventoListView,
    EventoCreateView,
    EventoUpdateView,
    EventoDeleteView,
    InscricaoCreateView,
    IngressoDetailView,
)

urlpatterns = [
    
    path('', EventoListView.as_view(), name='evento-list'),
    path('novo/', EventoCreateView.as_view(), name='evento-create'),
    path('editar/<int:pk>/', EventoUpdateView.as_view(), name='evento-update'),
    path('<int:pk>/excluir/', EventoDeleteView.as_view(), name='evento-delete'),
    path('evento/<int:pk>/inscrever/', InscricaoCreateView.as_view(), name='evento-inscricao'),
    path('login/', LoginView.as_view(template_name='eventos/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='evento-list'), name='logout'),
    path('ingresso/<int:pk>/', IngressoDetailView.as_view(), name='ingresso-detail'),
]
