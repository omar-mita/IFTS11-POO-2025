from .models import Perro, UsuarioAdoptante

class SistemaAdopcion:
    def __init__(self):
        self.perros = list(Perro.objects.all())
        self.usuarios = list(UsuarioAdoptante.objects.all())

    def cargar_perro(self, nombre, raza, edad, tamano, peso, estado_salud="", vacunado=False, temperamento=""):
        nuevo_perro = Perro.objects.create(
            nombre=nombre, raza=raza, edad=edad, tamano=tamano,
            peso=peso, estado_salud=estado_salud, vacunado=vacunado,
            temperamento=temperamento
        )
        self.perros.append(nuevo_perro)
        return nuevo_perro

    def eliminar_perro(self, perro_id):
        Perro.objects.filter(id=perro_id).delete()
        self.perros = [p for p in self.perros if p.id != perro_id]

    def registrar_usuario(self, nombre, dni, email, raza_pref=None, edad_pref=None, tamano_pref=None):
        usuario = UsuarioAdoptante.registrarse(
            nombre, dni, email,
            raza_pref=raza_pref, edad_pref=edad_pref, tamano_pref=tamano_pref
        )
        self.usuarios.append(usuario)
        return usuario

    def postular_perro(self, usuario_id, perro_id):
        try:
            usuario = UsuarioAdoptante.objects.get(id=usuario_id)
            perro = Perro.objects.get(id=perro_id)
        except (UsuarioAdoptante.DoesNotExist, Perro.DoesNotExist):
            return None
        perro.estado = 'reservado'
        perro.save()
        return perro

    def confirmar_adopcion(self, usuario_id, perro_id):
        try:
            usuario = UsuarioAdoptante.objects.get(id=usuario_id)
            perro = Perro.objects.get(id=perro_id)
        except (UsuarioAdoptante.DoesNotExist, Perro.DoesNotExist):
            return None
        perro.estado = 'adoptado'
        perro.save()
        usuario.historial_adopciones.add(perro)
        return perro

    def sugerir_perros(self, usuario_id):
        try:
            usuario = UsuarioAdoptante.objects.get(id=usuario_id)
        except UsuarioAdoptante.DoesNotExist:
            return Perro.objects.none()
        qs = Perro.objects.filter(estado='disponible')
        if usuario.preferencias_raza:
            qs = qs.filter(raza=usuario.preferencias_raza)
        if usuario.preferencias_edad:
            qs = qs.filter(edad__lte=usuario.preferencias_edad)
        if usuario.preferencias_tamano:
            qs = qs.filter(tamano=usuario.preferencias_tamano)
        return qs

    def mostrar_perros_disponibles(self):
        return Perro.objects.filter(estado='disponible')

    def mostrar_perros_por_estado(self, estado):
        return Perro.objects.filter(estado=estado)

    def mostrar_perros_por_usuario(self, usuario_id):
        try:
            usuario = UsuarioAdoptante.objects.get(id=usuario_id)
        except UsuarioAdoptante.DoesNotExist:
            return Perro.objects.none()
        return usuario.historial_adopciones.all()
