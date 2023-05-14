"""
URL configuration for foodproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from reviews.views import home, perfil, register_user, login_request, lista_de_reviews, Crear_reseña

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name="home"),
    path('profile/', perfil),
    path('register', register_user, name='register_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mapa/', include ('mapa.urls')),
    path('login/', login_request, name="login"),
    path('reviews/', lista_de_reviews),
    path('crear_reseña', Crear_reseña),
]
