from django import forms

class NewUserForm(forms.Form):
   
   email = forms.EmailField(required=True)