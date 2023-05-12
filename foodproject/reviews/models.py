from django.db import models
#from django.contrib.auth.models import User

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  apodo = models.CharField(max_length=30, default='user1')

#modelo de Mapa de comida
class MapaComida(models.Model):
    nombre = models.CharField(max_length=200)
    dueño = models.ForeignKey(User, on_delete= models.CASCADE)
    FotoLocal = models.ImageField(upload_to='Fotos_locales/', null=True, blank=True)

    def __str__(self):
        return self.nombre

#modelo de Evaluaciones
class Evaluacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    local_comida = models.ForeignKey(MapaComida, related_name='evaluaciones', on_delete=models.CASCADE)
    comentario = models.TextField()
    calificacion = models.ImageField()

    def __str__(self):
        return "f'{self.usuario.username} evaluo {self.local_comida.comida.nombre}'"
    

 
    