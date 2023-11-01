from django.db import models
from PIL import Image as PILImage
import os


# from django.contrib.auth.models import User


from django.contrib.auth.models import AbstractUser


# Modelo que representa a los usuarios
# Posee de atributos: username: el nombre de usuario
#                     email: el mail del usuario
#                     pronombre: el pronombre del usuario
#                     contraseña: la contraseña del usuario
class User(AbstractUser):
    pronombres = [("La", "La"), ("El", "El"), ("Le", "Le"), ("Otro", "Otro")]
    pronombre = models.CharField(max_length=5, choices=pronombres)


# Modelo que representa los puestos de comida que se instalan fuera de 850
# Posee de atributos: nombre: el nombre del puesto de comida
#                     dueño: el dueño del puesto de comida
#                     FotoLocal: una foto del puesto de comida
class Puesto_de_comida(models.Model):
    nombre = models.CharField(max_length=200)
    dueño = models.CharField(max_length=200, blank=True)
    FotoLocal = models.ImageField(upload_to="Fotos_locales", null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        sizes = [(200, 300), (400, 600), (600, 900)]
        
        img_path = self.FotoLocal.path

        with PILImage.open(img_path) as img:
            for size in sizes:
                img_cropped = self.resize_and_crop(img, size)
                dest_directory = os.path.join('media', 'Fotos_locales', f"{size[0]}x{size[1]}")
                os.makedirs(dest_directory, exist_ok=True)
                img_cropped.save(os.path.join(dest_directory, os.path.basename(img_path)))

    @staticmethod
    def resize_and_crop(img: PILImage.Image, target_size: tuple):
        target_width, target_height = target_size
        img_width, img_height = img.size
        target_aspect = target_width / target_height
        img_aspect = img_width / img_height

        # Si la imagen es más pequeña que el tamaño objetivo, la redimensionamos primero
        if img_width < target_width or img_height < target_height:
            if img_aspect < target_aspect:
                new_width = target_width
                new_height = int(target_width / img_aspect)
            else:
                new_height = target_height
                new_width = int(target_height * img_aspect)
            img = img.resize((new_width, new_height), PILImage.LANCZOS)

        # Luego, recortamos el centro de la imagen
        left = (img.width - target_width) / 2
        top = (img.height - target_height) / 2
        right = (img.width + target_width) / 2
        bottom = (img.height + target_height) / 2

        return img.crop((left, top, right, bottom))


# Modelo que representa las reseñas de los puestos de comida
# Posee de atributos: usuario: el usuario que creo la reseña
#                     local_comida: el puesto de comida del que se está haciendo la reseña
#                     detalle: un texto adicional que se le puede agregar a la reseña
#                     calificacion_comida: un puntaje entre 1 y 5 que se le da a la comida
#                     calificacion_precio: un puntaje entre 1 y 5 que se le da al precio
#                     calificacion_presentacion: un puntaje entre 1 y 5 que se le da a la presentación
#                     likes: cantidad de likes que tiene la reseña
#                     dislikes: cantidad de dislikes que tiene la reseña
#                     fecha: fecha en la que se hizo la reseña
#                     usuario_dio_like: usuarios que dieron like a la reseña
#                     usuario_dio_dislike: usuarios que dieron dislike a la reseña
class Evaluacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    local_comida = models.ForeignKey(
        Puesto_de_comida, related_name="evaluaciones", on_delete=models.CASCADE
    )
    detalle = models.TextField(blank=True)
    calificacion_comida = models.IntegerField()
    calificacion_precio = models.IntegerField()
    calificacion_presentacion = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario_dio_like = models.ManyToManyField(
        User, related_name="like_reviews", blank=True
    )
    usuario_dio_dislike = models.ManyToManyField(
        User, related_name="dislike_reviews", blank=True
    )

    def _str_(self):
        return f"{self.usuario.username} evaluó {self.local_comida.nombre}"

    def dar_like(self, usuario):
        self.usuario_dio_like.add(usuario)
        self.save()

    def dar_dislike(self, usuario):
        self.usuario_dio_dislike.add(usuario)
        self.save()

    def confirmacion_usuario_liked(self, user):
        return self.usuario_dio_like.filter(id=user.id).exists()

    # método para saber si un usuario ha dado dislike a una reseña
    def confirmacion_usuario_disliked(self, user):
        return self.usuario_dio_dislike.filter(id=user.id).exists()

    def cantidad_likes(self):
        return self.usuario_dio_like.count()

    def cantidad_dislikes(self):
        return self.usuario_dio_dislike.count()


# Modelo que representa el comentario que se le da a una reseña
# Atributos : evaluación: la evaluación que está comentada
#            comentarista: el usuario calificante, que es quien califica la reseña
#            comentario: comentario a la reseña
#            es_util: si el comentario es útil o no
#            like_comentario: cantidad de likes que tiene el comentario
#            dislike_comentario: cantidad de dislikes que tiene el comentario
#            fechacomentario: fecha en la que se hizo el comentario
class Comentario(models.Model):
    evaluacion = models.ForeignKey(
        Evaluacion, related_name="calificaciones", on_delete=models.CASCADE
    )
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
