# from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render, redirect
from reviews.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from reviews.forms import NewUserForm
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages #add this
from reviews.models import Puesto_de_comida
from django.views.generic.list import ListView

def home(request): 
    advices = get_template("home.html")
    ad_response = advices.render()

    return HttpResponse(ad_response)

def perfil(request):
    advices = get_template("perfil.html")
    ad_response = advices.render()
    return HttpResponse(ad_response)   

def register_user(request):
    advices = get_template("registro.html")
    ad_response = advices.render()
    return HttpResponse(ad_response)


def register_user(request):
    if request.method == 'GET': #Si estamos cargando la página
        #Mostrar el template
        return render(request, 'registro.html')
    
    elif request.method == 'POST': #Si estamos recibiendo el form de registro
     #Tomar los elementos del formulario que vienen en request.POST
        nombre = request.POST['name']
        contraseña = request.POST['password']
        mail = request.POST['email']

        #Crear el nuevo usuario
        user = User.objects.create_user(username=nombre, password=contraseña, email=mail)

     #Redireccionar la página /tareas
        return HttpResponseRedirect('/home')
    
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('mail')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                print("gola")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form":form})


class lista_de_puestos(ListView):
    # specify the model for list view
    model = Puesto_de_comida