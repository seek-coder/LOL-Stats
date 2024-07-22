from django.urls import path
from . import views

    # ------------------ #
    #    páginas web     #
    # ------------------ #

urlpatterns = [
    path('', views.buscar_invocador, name='buscar_invocador'),
    path('plot1/', views.plot1, name='plot_image1'),
    path('plot2/', views.plot2, name='plot_image2'),
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros')
]
