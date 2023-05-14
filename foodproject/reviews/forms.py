from django import forms
from reviews.models import Puesto_de_comida

class NewUserForm(forms.Form):
   
   email = forms.EmailField(required=True)


class CrearReseñaForm(forms.Form):
   calificacion_comida = forms.IntegerField(max_value=5, min_value=1)
   calificacion_precio = forms.IntegerField(max_value=5, min_value=1)
   calificacion_presentacion = forms.IntegerField(max_value=5, min_value=1)
   comentario = forms.CharField(widget=forms.Textarea()) # <textarea> en vez de <input>
   puesto_de_comida = forms.ModelChoiceField(queryset=Puesto_de_comida.objects.all())



