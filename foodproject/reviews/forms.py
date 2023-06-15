from django import forms
from reviews.models import Puesto_de_comida, User, Evaluacion

class NewUserForm(forms.Form):
   
   email = forms.EmailField(required=True)


class CrearReseñaForm(forms.ModelForm):
   CHOICES = [(5, '☆'), (4, '☆'), (3, '☆'), (2, '☆'), (1, '☆')]
   calificacion_comida = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
   calificacion_precio = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
   calificacion_presentacion = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
   comentario = forms.CharField(widget=forms.Textarea(attrs={'rows':'4'}), required=False) # <textarea> en vez de <input>

   class Meta:
      model = Evaluacion
      fields = ["calificacion_comida", "calificacion_precio", "calificacion_presentacion", "comentario"]

class SearchForm(forms.Form):
   busqueda = forms.CharField(required=True)


class ComentarioReseña(forms.ModelForm):
   class Meta:
      model = Comentario
      fields = ['comentario', 'es_util']

      widgets = {
         'comentario' : forms.Textarea(attrs={'rows' : 3}), #estilo del campo de texto
         'es_util' : forms.CheckboxInput()
      }


