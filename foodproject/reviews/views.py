# from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render, redirect, get_object_or_404
from reviews.models import User
from reviews.models import Puesto_de_comida
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from reviews.forms import NewUserForm, CrearReseñaForm, SearchForm, ComentarioReseña
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib import messages #add this
from reviews.models import Evaluacion,Comentario 
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required

# Vista que permite mostrar la pagina principal (home) del sitio web
# Cuando se intenta acceder a home/ se ejecuta esta vista
def home(request):
    return render(request, "home.html")

# Vista que permite mostrar el perfil de un usuario
# Cuando se intenta acceder a profile/ se ejecuta esta vista
@login_required
def perfil(request):
    reviews_usuario = Evaluacion.objects.filter(usuario_id = request.user)
    return render(request, "perfil.html", {"reviews_usuario" : reviews_usuario})

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
        return HttpResponseRedirect('')

# Vista que permite mostrar la página de ingreso de un usuario
# Cuando se intenta acceder a login/ se ejecuta esta vista
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        # To clean the messages
        system_messages = messages.get_messages(request)
        for message in system_messages:
            pass
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Te has logueado como {username}.")
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
# Cuando se intenta acceder a tiendas/ se ejecuta esta vista
def grid_stores(request): 
    queryset = Puesto_de_comida.objects.all()
    return render(request, "tiendas.html", {"list": queryset})

# Vista que permite mostrar la información de un puesto de comida
# Cuando se presiona el botón "Mostrar puesto de comida", en la página stores/
def search_store(request):
    queryset = Puesto_de_comida.objects.all() # TODO: Se esta haciendo de nuevo la misma query
    if request.method == "POST":
        puesto = request.GET["local"]
        local = Puesto_de_comida.objects.get(id=puesto)
        reviews = Evaluacion.objects.filter(local_comida = local)
        form_crear_reseña = CrearReseñaForm(request.POST)
        if form_crear_reseña.is_valid():
            cleaned_data = form_crear_reseña.cleaned_data
            Evaluacion.objects.create(**cleaned_data, usuario=request.user, local_comida=local)
        return render(request, "show_store.html", {
            "local": local, "form_tarea": form_crear_reseña, "list": queryset, "reviews_list": reviews
            })
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

def buscador(request):
    if request.method == 'POST':
        form_busqueda = SearchForm(request.POST)
        resultados = ""
        if form_busqueda.is_valid():
            cleaned_data = form_busqueda.cleaned_data
            resultados = Evaluacion.objects.filter(comentario__icontains=cleaned_data['busqueda'])  # Realiza la búsqueda en el campo deseado
            return render(request, 'resultados.html', {'resultados': resultados})
        else:
            return render(request, 'buscar.html', {"form_busqueda": form_busqueda})
    if request.method == "GET":
        form_busqueda = SearchForm()
        return render(request, "buscar.html", {"form_busqueda": form_busqueda})

# Vista que permite editar las reseñas del usuario
# Cuando se intenta acceder a profile/edit/id se ejecuta esta vista
def editar_reseña(request, id):
    post = get_object_or_404(Evaluacion, id=id)

    if request.method == 'GET':
        context = {'form' : CrearReseñaForm(instance=post), "id": id}
        return render(request, "editar_reseña.html", context)
    
    elif request.method == 'POST':
        form = CrearReseñaForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Los cambios se han realizado con exito")
            return redirect('profile')
        else:
            messages.error(request, "Los siguientes campos son erróneos: ")
            return render(request, "editar_reseña.html", {'form': form})

# Vista que permite borrar las reseñas del usuario
# Cuando se intenta acceder a profile/delete_review/id se ejecuta esta vista
def borrar_reseña(request, id):
    post = get_object_or_404(Evaluacion, pk=id)
    context = {'post': post}    
    
    if request.method == 'GET':
        return render(request, 'borrar_reseña.html', context)
    
    elif request.method == 'POST':
        post.delete()
        messages.success(request, "La reseña se ha borrado correctamente")
        return redirect('profile')

# Vista que permite editar los comentarios realizados a reseñas
# Cuando se intenta acceder a profile/edit_comment/id se ejecuta esta vista
def editar_comentario(request, id):
    post = get_object_or_404(Comentario, id=id)

    if request.method == 'GET':
        context = {'form' : ComentarioReseña(instance=post), "id": id}
        return render(request, "editar_reseña.html", context)
    
    elif request.method == 'POST':
        form = ComentarioReseña(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Los cambios se han realizado con exito")
            return redirect('profile')
        else:
            messages.error(request, "Los siguientes campos son erróneos: ")
            return render(request, "editar_comentario.html", {'form': form})

# Vista que permite cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('login')