from django.db import models

# Create your models here.

class Perro(models.Model):
    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    edad = models.IntegerField()
    tamaño = models.CharField(max_length=50)
    peso = models.FloatField()
    estado_salud = models.CharField(max_length=100)
    vacunado = models.BooleanField(default=False)
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('reservado', 'Reservado'),
        ('adoptado', 'Adoptado'),
    ]
    estado = models.CharField(max_length=15, choices=ESTADOS, default='disponible')
    temperamento = models.CharField(max_length=100)

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.save()
#Devuelve una descripción resumida del perro
    def mostrar_informacion(self):
        info = f"ID:{self.id} Nombre:{self.nombre} - Raza:{self.raza} - Edad:{self.edad} - Estado:{self.estado}"
        return info

    def __str__(self):
        return f"{self.nombre} ({self.raza}) - Estado: {self.estado}"
class Galgo(Perro):
    def mostrar_informacion(self):
        base = super().mostrar_informacion()
        return base + " // Galgo: tranquilo, elegante y buen corredor."   

class UsuarioAdoptante(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    preferencias_raza = models.CharField(max_length=50, blank=True)
    preferencias_edad = models.PositiveIntegerField(null=True, blank=True)
    preferencias_tamano = models.CharField(max_length=50, blank=True)
    historial_adopciones = models.ManyToManyField(Perro, blank=True)
    @classmethod
    def registrarse(cls, nombre, dni, email, raza_pref=None, edad_pref=None, tamano_pref=None):
        return cls.objects.create(
            nombre=nombre, dni=dni, email=email,
            preferencias_raza=raza_pref or "", preferencias_edad=edad_pref or 0,
            preferencias_tamano=tamano_pref or ""
        )
#Actualiza los datos
    def modificar_datos(self, nombre=None, email=None, preferencias_raza=None,
                       preferencias_edad=None, preferencias_tamano=None):
        if nombre: self.nombre = nombre
        if email: self.email = email
        if preferencias_raza: self.preferencias_raza = preferencias_raza
        if preferencias_edad is not None: self.preferencias_edad = preferencias_edad
        if preferencias_tamano: self.preferencias_tamano = preferencias_tamano
        self.save()
    def ver_historial(self):
        return self.historial_adopciones.all()

    def __str__(self):
        return f"{self.nombre} (DNI: {self.dni})"