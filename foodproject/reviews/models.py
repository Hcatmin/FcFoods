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
    dueño = models.CharField(max_length=200, blank=True)
    FotoLocal = models.ImageField(upload_to='Fotos_locales/', null=True, blank=True)

    def __str__(self):
        return self.nombre

# Modelo que representa las reseñas de los puestos de comida
# Posee de atributos: el usuario que creo la reseña, el puesto de comida, un comentario, y 
#                     calficaciones de la comida, el precio, y la presentación.
#                     también incluye las evaluaciones positivas y negativas dadas a la reseña
class Evaluacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    local_comida = models.ForeignKey(Puesto_de_comida, related_name='evaluaciones', on_delete=models.CASCADE)
    detalle = models.TextField(blank=True)
    calificacion_comida = models.IntegerField()
    calificacion_precio = models.IntegerField()
    calificacion_presentacion = models.IntegerField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default = 0)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario_dio_like = models.ManyToManyField(User, related_name='like_reviews')
    usuario_dio_dislike = models.ManyToManyField(User, related_name='dislike_reviews')
    
    def __str__(self):
        return f"{self.usuario.username} evaluó {self.local_comida.nombre}"
    
    def dar_like(self, usuario):
        self.likes += 1
        self.usuario_dio_like.add(usuario)
        if usuario in self.usuario_dio_dislike.all():
            self.usuario_dio_dislike.remove(usuario)
            self.dislikes -= 1
        self.save()
    
    def quitar_like(self, usuario):
        self.likes -= 1
        self.usuario_dio_like.remove(usuario)
        self.save()
    
    def dar_dislike(self, usuario):
        self.dislikes += 1
        self.usuario_dio_dislike.add(usuario)
        if usuario in self.usuario_dio_like.all():
            self.usuario_dio_like.remove(usuario)
            self.likes -= 1
        self.save()
    
    def quitar_dislike(self, usuario):
        self.dislikes -= 1
        self.usuario_dio_dislike.remove(usuario)
        self.save()

#Modelo que representa el comentario que se le da a una reseña    
#Atributos : la evaluación que está comentada
#            el usuario calificante, que es quien califica la reseña     
#            comentario a la reseña
class Comentario(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, related_name='calificaciones', on_delete=models.CASCADE)
    comentarista = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField(blank=False)
    es_util = models.BooleanField(default=False)
    like_comentario = models.IntegerField(default=0)
    dislike_comentario = models.IntegerField(default=0)
    fechacomentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return f"{self.comentarista.username} comentó la evaluación de {self.evaluacion.usuario.username}"
    
    def valorizar_util(self):
        self.es_util = True
        self.save()

    def valorizar_no_util(self):
        self.es_util = False
        self.save()

    def dar_likeComentario(self):
        self.like_comentario += 1
        self.save()

    def quitar_likeComentario(self):
        self.like_comentario -= 1
        self.save()

    def dar_dislikeComentario(self):
        self.dislike_comentario += 1
        self.save()

    def quitar_dislikeComentario(self):
        self.dislike_comentario -= 1
        self.save()
        