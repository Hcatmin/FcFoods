from django.contrib import admin

from reviews.models import User, Puesto_de_comida, Evaluacion, Comentario

# Register your models here.
admin.site.register(User)
admin.site.register(Puesto_de_comida)
admin.site.register(Evaluacion)
admin.site.register(Comentario)
