from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicio, name='pagina_inicio'),  # Página de inicio
    path('buscar/', views.buscar_invocador, name='buscar_invocador'),
    path('plot/', views.cr, name='plot')
]
