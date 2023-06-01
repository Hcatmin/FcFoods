from django.db import models
#from django.contrib.auth.models import User

# Create your models here.

from django.contrib.auth.models import AbstractUser

# Modelo que representa a los usuarios
# Posee de atributos: username, mail, pronombre, y contraseña
class User(AbstractUser):
  pronombres = [('La','La'),('El','El'), ('Le','Le'),('Otro','Otro')]
  pronombre = models.CharField(max_length=5,choices=pronombres)

# Modelo que representa los puestos de comida que se instalan fuera de 850
# Posee de atributos: el nombre, el dueño, y la foto del local
class Puesto_de_comida(models.Model):
    nombre = models.CharField(max_length=200)
    dueño = models.CharField(max_length=200)
    FotoLocal = models.ImageField(upload_to='Fotos_locales/', null=True, blank=True)

    def __str__(self):
        return self.nombre

# Modelo que representa las reseñas de los puestos de comida
# Posee de atributos: el usuario que creo la reseña, el puesto de comida, un comentario, y 
#                     calficaciones de la comida, el precio, y la presentación.
class Evaluacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    local_comida = models.ForeignKey(Puesto_de_comida, related_name='evaluaciones', on_delete=models.CASCADE)
    comentario = models.TextField(blank=True)
    calificacion_comida = models.IntegerField()
    calificacion_precio = models.IntegerField()
    calificacion_presentacion = models.IntegerField()

    def __str__(self):
        return "f'{self.usuario.username} evaluo {self.local_comida.comida.nombre}'"


#Modelo que representa la calificación que se le da a una reseña    
#Atributos : la evaluación que está siendo calificada y comentada
#            el usuario calificante, que es quien califica la reseña
#            la calificación otorgada a la reseña
#            comentario opcional a la reseña
class Calificacion(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, related_name='calificaciones', on_delete=models.CASCADE)
    calificante = models.ForeignKey(User, on_delete=models.CASCADE)
    calificacion = models.IntegerField()
    comentario = models.TextField(blank=True)

    def __str__(self):
      return "f'{self.calificante.username} calificó la evaluación de {self.evaluacion.usuario.username}'"