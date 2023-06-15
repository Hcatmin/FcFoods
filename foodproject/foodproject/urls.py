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
from django.conf import settings
from django.conf.urls.static import static
from reviews.views import home, perfil, register_user, login_request, lista_de_reviews, \
                          Crear_reseña, search_store, buscador, grid_stores, editar_reseña, \
                          borrar_reseña, cerrar_sesion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('profile/', perfil, name="profile"),
    path('register', register_user, name='register_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tiendas/', grid_stores, name='tiendas'),
    path('login/', login_request, name="login"),
    path('reviews/', lista_de_reviews),
    path('crear_reseña', Crear_reseña),
    path('search_store/', search_store),
    path('buscar/', buscador),
    path('profile/edit/<int:id>/', editar_reseña, name="edit_review"),
    path('profile/delete/<int:id>/', borrar_reseña, name="delete_review"),
    path('logout/', cerrar_sesion, name= "logout")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
