from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import User, Puesto_de_comida, Evaluacion, Comentario
from reviews.forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = ["email", "username", "pronombre"]


# Register your models here.
admin.site.register(Puesto_de_comida)
admin.site.register(Evaluacion)
admin.site.register(Comentario)
admin.site.register(User, CustomUserAdmin)
