from django.urls import path
from . import views

urlpatterns = [
    path('perros/', views.lista_perros, name='lista_perros'),
]
