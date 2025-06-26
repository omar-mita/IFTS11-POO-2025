from django.shortcuts import render
from .models import Perro
# Create your views here.from .models import Perro

def lista_perros(request):
    perros = Perro.objects.all()
    return render(request, 'adopcion/lista_perros.html', {'perros': perros})