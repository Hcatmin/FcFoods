# from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render, redirect
from reviews.models import User
from reviews.models import Puesto_de_comida
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from reviews.forms import NewUserForm, CrearReseñaForm
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages #add this
from reviews.models import Evaluacion
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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Te has logueado como {username}.")
                return redirect("home")
            else:
                messages.error(request,"Usuario o contraseña inválidos.")
        else:
            messages.error(request,"Usuario o contraseña inválidos")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form":form})


def lista_de_reviews(request):

    reviews = Evaluacion.objects.all()  # quering all todos with the object manager
    if request.method == "GET":
        form_crear_reseña = CrearReseñaForm()
        return render(request, "lista_de_reviews.html", {"form_tarea": form_crear_reseña, "reviews_list": reviews})
    if request.method == "POST":
        form_crear_reseña = CrearReseñaForm(request.POST)
        if form_crear_reseña.is_valid():
            cleaned_data = form_crear_reseña.cleaned_data
            Evaluacion.objects.create(**cleaned_data, usuario=request.user)
        return render(request, "crear_reseña.html", {"form_tarea": form_crear_reseña, "reviews_list": reviews})


# TODO: Add this demo to mapa.html
def stores(request): 
    advices = get_template("stores.html")
    queryset = Puesto_de_comida.objects.all()
    context = {"list": queryset}
    ad_response = advices.render(context)

    return HttpResponse(ad_response)

def search_store(request):
    queryset = Puesto_de_comida.objects.all() # TODO: Se esta haciendo de nuevo la misma query
    if request.GET["local"]:
        puesto = request.GET["local"]

        local = Puesto_de_comida.objects.get(id=puesto)
        return render(request, "show_store.html", {"local": local, "list": queryset})
    else:
        message = "Debes seleccionar un campo"
        return HttpResponse(message)

    

def Crear_reseña(request):
    if request.method == "GET":
        form_crear_reseña = CrearReseñaForm()
        return render(request, "crear_reseña.html", {"form_tarea": form_crear_reseña})
    if request.method == "POST":
        form_crear_reseña = CrearReseñaForm(request.POST)
        if form_crear_reseña.is_valid():
            cleaned_data = form_crear_reseña.cleaned_data
            Evaluacion.objects.create(**cleaned_data, usuario=request.user)
        return render(request, "crear_reseña.html", {"form_tarea": form_crear_reseña})
