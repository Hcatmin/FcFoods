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

# Vista que permite mostrar la pagina principal (home) del sitio web
# Cuando se intenta acceder a home/ se ejecuta esta vista
def home(request): 
    advices = get_template("home.html")
    ad_response = advices.render()
    return HttpResponse(ad_response)

# Vista que permite mostrar el perfil de un usuario
# Cuando se intenta acceder a profile/ se ejecuta esta vista
def perfil(request):
    advices = get_template("perfil.html")
    ad_response = advices.render()
    return HttpResponse(ad_response)   

# Vista que permite mostrar la página de registro de un usuario
# Cuando se intenta acceder a register/ se ejecuta esta vista
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

# Vista que permite mostrar la página de ingreso de un usuario
# Cuando se intenta acceder a login/ se ejecuta esta vista
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

# Vista que permite mostrar la página de la lista de reseñas
# Cuando se intenta acceder a reviews/ se ejecuta esta vista
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
        return render(request, "lista_de_reviews.html", {"form_tarea": form_crear_reseña, "reviews_list": reviews})

# Vista que permite mostrar la página dedicada a buscar y mostrar información de las tiendas
# Cuando se intenta acceder a stores/ se ejecuta esta vista
# TODO: Add this demo to mapa.html
def stores(request): 
    advices = get_template("stores.html")
    queryset = Puesto_de_comida.objects.all()
    context = {"list": queryset}
    ad_response = advices.render(context)

    return HttpResponse(ad_response)

# Vista que permite mostrar la información de un puesto de comida
# Cuando se presiona el botón "Mostrar puesto de comida", en la página stores/
def search_store(request):
    queryset = Puesto_de_comida.objects.all() # TODO: Se esta haciendo de nuevo la misma query
    if request.method == "POST":
        puesto = request.GET["local"]
        local = Puesto_de_comida.objects.get(id=puesto)
        form_crear_reseña = CrearReseñaForm(request.POST)
        if form_crear_reseña.is_valid():
            cleaned_data = form_crear_reseña.cleaned_data
            Evaluacion.objects.create(**cleaned_data, usuario=request.user, local_comida=local)
        return render(request, "stores.html", {"list": queryset})
    if request.GET["local"]:
        puesto = request.GET["local"]
        local = Puesto_de_comida.objects.get(id=puesto)
        reviews = Evaluacion.objects.filter(local_comida = local)
        form_crear_reseña = CrearReseñaForm()
        return render(request, "show_store.html", {
            "local": local, "form_tarea": form_crear_reseña, "list": queryset, "reviews_list": reviews
            })
    else:
        message = "Debes seleccionar un campo"
        return HttpResponse(message)

# Vista que permite mostrar la página que solo tiene un botón para crear reseñas
# Cuando se intenta acceder a crear_reseña/ se ejecuta esta vista
# Esta vista no tiene funcionalidad para el producto final, solo esta creada para el desarrollo
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
