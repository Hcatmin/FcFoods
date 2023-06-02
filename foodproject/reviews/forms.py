from django import forms
from reviews.models import Puesto_de_comida, User

class NewUserForm(forms.Form):
   
   email = forms.EmailField(required=True)


class CrearReseñaForm(forms.Form):
   calificacion_comida = forms.IntegerField(max_value=5, min_value=1)
   calificacion_precio = forms.IntegerField(max_value=5, min_value=1)
   calificacion_presentacion = forms.IntegerField(max_value=5, min_value=1)
   comentario = forms.CharField(widget=forms.Textarea(), required=False) # <textarea> en vez de <input>

class SearchForm(forms.Form):
   busqueda = forms.CharField(required=True)



