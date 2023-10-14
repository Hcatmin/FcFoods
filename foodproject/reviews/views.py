# from django.shortcuts import render
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from reviews.models import Puesto_de_comida
from django.contrib.auth.forms import AuthenticationForm
from reviews.forms import CrearReseñaForm, SearchForm, ComentarioReseña, CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from reviews.models import Evaluacion, Comentario
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse, HttpResponse

# Vista que permite mostrar la pagina principal (home) del sitio web
# Cuando se intenta acceder a home/ se ejecuta esta vista
def home(request):
    reviews_date = Evaluacion.objects.order_by("-fecha")[:6]
    # reviews_likes = Evaluacion.objects.order_by('-likes')[:6]
    reviews_likes = Evaluacion.objects.annotate(
        num_likes=Count("usuario_dio_like")
    ).order_by("-num_likes")[:6]

    return render(
        request,
        "home.html",
        {"reviews_date": reviews_date, "reviews_likes": reviews_likes},
    )


# Vista que permite mostrar el perfil de un usuario
# Cuando se intenta acceder a profile/ se ejecuta esta vista
@login_required
def perfil(request):
    reviews_usuario = Evaluacion.objects.filter(usuario_id=request.user)
    comentarios_usuario = Comentario.objects.filter(comentarista=request.user)
    return render(
        request,
        "perfil.html",
        {
            "reviews_usuario": reviews_usuario,
            "comentarios_usuario": comentarios_usuario,
        },
    )


# Vista que permite mostrar la página de registro de un usuario
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registro.html"
    
    def form_valid(self, form):
        response = super().form_valid(form)  # Llama al método original form_valid()
        password = form.cleaned_data.get('password1')
        self.object.set_password(password)  # Establece la contraseña
        self.object.save()  # Guarda el objeto
        return response


# Vista que permite mostrar la página de ingreso de un usuario
# Cuando se intenta acceder a login/ se ejecuta esta vista
def login_request(request: HttpRequest):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        # To clean the messages
        system_messages = messages.get_messages(request)
        for message in system_messages:
            pass
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Te has logueado como {user.username}.")
            return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña inválidos")
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="registration/login.html",
        context={"form": form},
    )


# Vista que permite mostrar la información de un puesto de comida
# Cuando se presiona el botón "Mostrar puesto de comida", en la página stores/
def tiendas_view(request):
    queryset = (
        Puesto_de_comida.objects.all()
    )  # TODO: Se esta haciendo de nuevo la misma query
    form_crear_reseña = CrearReseñaForm()
    form_agregar_comentario = ComentarioReseña()

    if "local" in request.GET:
        puesto = request.GET["local"]
        local = Puesto_de_comida.objects.get(id=puesto)
        if request.method == "GET":
            reviews = (
                Evaluacion.objects.filter(local_comida=local).order_by("-fecha").all()
            )
            return render(
                request,
                "tiendas.html",
                {
                    "local": local,
                    "form_tarea": form_crear_reseña,
                    "form_comentario": form_agregar_comentario,
                    "list": queryset,
                    "reviews_list": reviews,
                },
            )

    if request.method == "POST":
        reviews = Evaluacion.objects.filter(local_comida=local).order_by("-fecha")

        if "like" in request.POST:
            review_id = request.POST.get("like")
            review = get_object_or_404(Evaluacion, id=review_id)
            if review.confirmacion_usuario_liked(request.user):
                review.usuario_dio_like.remove(request.user)
            else:
                review.usuario_dio_like.add(request.user)
                if review.confirmacion_usuario_disliked(request.user):
                    review.usuario_dio_dislike.remove(request.user)

        elif "dislike" in request.POST:
            review_id = request.POST.get("dislike")
            review = get_object_or_404(Evaluacion, id=review_id)
            if review.confirmacion_usuario_disliked(request.user):
                review.usuario_dio_dislike.remove(request.user)
            else:
                review.dar_dislike(request.user)
                if review.confirmacion_usuario_liked(request.user):
                    review.usuario_dio_like.remove(request.user)

        elif "review_form" in request.POST:
            form_crear_reseña = CrearReseñaForm(request.POST)
            if form_crear_reseña.is_valid():
                cleaned_data = form_crear_reseña.cleaned_data
                Evaluacion.objects.create(
                    **cleaned_data, usuario=request.user, local_comida=local
                )

        elif "comment_form" in request.POST:
            form_agregar_comentario = ComentarioReseña(request.POST)
            if form_agregar_comentario.is_valid():
                evaluacion = request.POST["evaluacion"]
                cleaned_data = form_agregar_comentario.cleaned_data
                Comentario.objects.create(
                    **cleaned_data, comentarista=request.user, evaluacion_id=evaluacion
                )

        return render(
            request,
            "tiendas.html",
            {
                "local": local,
                "form_tarea": form_crear_reseña,
                "form_comentario": form_agregar_comentario,
                "list": queryset,
                "reviews_list": reviews,
            },
        )

    return render(request, "tiendas.html", {"list": queryset})

def stores_view(request):
    queryset = Puesto_de_comida.objects.all()
    return render(request, 'stores.html', {'list': queryset})

def display_store(request):
    id_local = request.GET.get('id_local')
    puesto = Puesto_de_comida.objects.get(id=id_local)    
    reviews = Evaluacion.objects.filter(local_comida = puesto).order_by('-fecha').all()
    form_agregar_comentario = ComentarioReseña()
    form_crear_reseña = CrearReseñaForm()

    rendered_data = render_to_string('display_store.html', {'id_local': id_local, 'local': puesto, 'list_reviews': reviews, "form_tarea": form_crear_reseña, "form_comentario": form_agregar_comentario, 'user_is_authenticated': request.user.is_authenticated, 'user': request.user})

    return JsonResponse({'rendered_data': rendered_data})

@csrf_protect
def display_like_and_dislike(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' # verifica si es ajax
    if request.method == 'POST' and is_ajax:
        id_review = request.POST.get('id_review')
        request_type = request.POST.get('type')

        review = get_object_or_404(Evaluacion, id=id_review)
        response = ''
        if request_type == 'like':
            if review.confirmacion_usuario_liked(request.user):
                review.usuario_dio_like.remove(request.user)
                response+= '''
                <button type="submit" class="btn btn-outline-secondary" name="like" value="'''+str(id_review)+'''">
                    <i class="bi bi-hand-thumbs-up"></i>'''+str(review.usuario_dio_like.count())+'''
                </button>'''
            else:
                review.usuario_dio_like.add(request.user)
                if review.confirmacion_usuario_disliked(request.user):
                    review.usuario_dio_dislike.remove(request.user)
                response+= '''
                <button type="submit" class="btn btn-secondary" name="like" value="'''+str(id_review)+'''">
                    <i class="bi bi-hand-thumbs-up"></i>'''+str(review.usuario_dio_like.count())+'''
                </button>'''
            response+= '''
                <button type="submit" class="btn btn-outline-secondary" name="dislike" value="'''+str(id_review)+'''">
                <i class="bi bi-hand-thumbs-down"></i>'''+str(review.usuario_dio_dislike.count())+'''
                </button>'''
        elif request_type == 'dislike':
            if review.confirmacion_usuario_disliked(request.user):
                review.usuario_dio_dislike.remove(request.user)
                response+= '''
                  <button type="submit" class="btn btn-outline-secondary" name="dislike" value="'''+str(id_review)+'''">
                    <i class="bi bi-hand-thumbs-down"></i>'''+str(review.usuario_dio_dislike.count())+'''
                  </button>'''
            else:
                review.dar_dislike(request.user)
                if review.confirmacion_usuario_liked(request.user):
                    review.usuario_dio_like.remove(request.user)
                response+= '''
                <button type="submit" class="btn btn-secondary" name="dislike" value="'''+str(id_review)+'''">
                    <i class="bi bi-hand-thumbs-down"></i>'''+str(review.usuario_dio_dislike.count())+'''
                </button>'''

            response = '''
                <button type="submit" class="btn btn-outline-secondary" name="like" value="'''+str(id_review)+'''">
                <i class="bi bi-hand-thumbs-up"></i>'''+str(review.usuario_dio_like.count())+'''
                </button>''' + response

        return HttpResponse(response)
        
    else:
        return JsonResponse({'error': 'Invalid Request'})

@csrf_protect
def display_comment(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' # verifica si es ajax
    if request.method == 'POST' and is_ajax:
        # user = request.POST.get('user')
        id_local = request.POST.get('id_local')
        id_review = request.POST.get('id_review')
        content_comment = request.POST.get('comentario')
        form_agregar_comentario = ComentarioReseña(request.POST)
        print(request.POST)
        if form_agregar_comentario.is_valid():
            cleaned_data = form_agregar_comentario.cleaned_data
            Comentario.objects.create(**cleaned_data, comentarista=request.user, evaluacion_id = id_review)
            response_data = {"id_review": id_review, "content_comment": content_comment}
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': request.POST})
    else:
        return JsonResponse({'error': 'Invalid Request'})

# Vista que permite mostrar la página para realizar busquedas
# Cuando se presiona el botón "Buscar", en la página buscar/
def buscador(request):
    if request.method == "POST":
        form_busqueda = SearchForm(request.POST)
        if form_busqueda.is_valid():
            cleaned_data = form_busqueda.cleaned_data
            resultados = Evaluacion.objects.filter(
                detalle__icontains=cleaned_data["busqueda"]
            )  # Realiza la búsqueda en el campo deseado
            return render(
                request,
                "resultados.html",
                {"resultados": resultados, "busqueda": cleaned_data["busqueda"]},
            )
        else:
            return render(request, "buscar.html", {"form_busqueda": form_busqueda})
    if request.method == "GET":
        form_busqueda = SearchForm()
        return render(request, "buscar.html", {"form_busqueda": form_busqueda})


# Vista que permite editar las reseñas del usuario
# Cuando se intenta acceder a profile/edit/id se ejecuta esta vista
def editar_reseña(request, id):
    post = get_object_or_404(Evaluacion, id=id)

    if request.method == "GET":
        context = {"form": CrearReseñaForm(instance=post), "id": id}
        return render(request, "editar_reseña.html", context)

    elif request.method == "POST":
        form = CrearReseñaForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Los cambios se han realizado con exito")
            return redirect("profile")
        else:
            messages.error(request, "Los siguientes campos son erróneos: ")
            return render(request, "editar_reseña.html", {"form": form})


# Vista que permite borrar las reseñas del usuario
# Cuando se intenta acceder a profile/delete_review/id se ejecuta esta vista
def borrar_reseña(request, id):
    post = get_object_or_404(Evaluacion, pk=id)
    context = {"post": post}

    if request.method == "GET":
        return render(request, "borrar_reseña.html", context)

    elif request.method == "POST":
        post.delete()
        messages.success(request, "La reseña se ha borrado correctamente")
        return redirect("profile")


# Vista que permite editar los comentarios realizados a reseñas
# Cuando se intenta acceder a profile/edit_comment/id se ejecuta esta vista
def editar_comentario(request, id):
    post = get_object_or_404(Comentario, id=id)

    if request.method == "GET":
        context = {"form": ComentarioReseña(instance=post), "id": id}
        return render(request, "editar_comentario.html", context)

    elif request.method == "POST":
        form = ComentarioReseña(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Los cambios se han realizado con exito")
            return redirect("profile")
        else:
            messages.error(request, "Los siguientes campos son erróneos: ")
            return render(request, "editar_comentario.html", {"form": form})


# Vista que permite borrar los comentarios del usuario
# Cuando se intenta acceder a profile/delete_comment/id se ejecuta esta vista
def borrar_comentario(request, id):
    post = get_object_or_404(Comentario, pk=id)
    context = {"post": post}

    if request.method == "GET":
        return render(request, "borrar_comentario.html", context)

    elif request.method == "POST":
        post.delete()
        messages.success(request, "El comentario se ha borrado correctamente")
        return redirect("profile")


# Vista que permite cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect("login")
