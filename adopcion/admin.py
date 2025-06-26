from django.contrib import admin
from .models import Perro, Galgo, UsuarioAdoptante
#admin@example.com
#pepito2025

# Register your models here.

admin.site.register(Perro)
admin.site.register(Galgo)
admin.site.register(UsuarioAdoptante)