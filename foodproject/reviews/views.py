# from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from reviews.models import User
from django.http import HttpResponseRedirect


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
        advices = get_template("registro.html")
        ad_response = advices.render()
        return HttpResponse(ad_response)
    
    elif request.method == 'POST': #Si estamos recibiendo el form de registro
     #Tomar los elementos del formulario que vienen en request.POST
        nombre = request.POST['name']
        contraseña = request.POST['password']
        mail = request.POST['email']

        #Crear el nuevo usuario
        user = User.objects.create_user(username=nombre, password=contraseña, email=mail)

     #Redireccionar la página /tareas
        return HttpResponseRedirect('/home')
    
