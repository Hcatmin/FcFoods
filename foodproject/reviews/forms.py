from django import forms
from reviews.models import Puesto_de_comida, User, Evaluacion, Comentario


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "pronombre"]

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "pronombre": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class CrearReseñaForm(forms.ModelForm):
    CHOICES = [(5, "☆"), (4, "☆"), (3, "☆"), (2, "☆"), (1, "☆")]
    calificacion_comida = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
    calificacion_precio = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
    calificacion_presentacion = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=CHOICES
    )
    detalle = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "4"}), required=False
    )  # <textarea> en vez de <input>

    class Meta:
        model = Evaluacion
        fields = [
            "calificacion_comida",
            "calificacion_precio",
            "calificacion_presentacion",
            "detalle",
        ]


class SearchForm(forms.Form):
    busqueda = forms.CharField(required=True)


class ComentarioReseña(forms.ModelForm):
    comentario = forms.CharField(required=True)  # <textarea> en vez de <input>

    class Meta:
        model = Comentario
        fields = ["comentario"]
