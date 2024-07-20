from django.urls import path
from . import views

    # ------------------ #
    #    páginas web     #
    # ------------------ #

urlpatterns = [
    path('', views.buscar_invocador, name='buscar_invocador'),
    #path('plot/', views.plot, name='plot'),
]
