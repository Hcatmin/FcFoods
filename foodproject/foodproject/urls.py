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
from reviews.views import home, perfil, login_request, \
                          buscador, tiendas_view, editar_reseña, \
                          stores_view, display_store, display_comment, display_like_and_dislike, display_review, \
                          borrar_reseña, cerrar_sesion, editar_comentario, borrar_comentario, \
                          SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('profile/', perfil, name="profile"),
    path('register', SignUpView.as_view(), name='register_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tiendas/', tiendas_view, name='tiendas'),
    path('stores/', stores_view, name='stores'),
    path('display_store/', display_store, name='display_store'),
    path('display_comment/', display_comment, name='display_comment'),
    path('display_like_and_dislike/', display_like_and_dislike, name='display_like_and_dislike'),
    path('display_review/', display_review, name='display_review'),
    path('login/', login_request, name="login"),
    path('buscar/', buscador, name="buscador"),
    path('profile/edit_review/<int:id>/', editar_reseña, name="edit_review"),
    path('profile/delete_review/<int:id>/', borrar_reseña, name="delete_review"),
    path('profile/edit_comment/<int:id>/', editar_comentario, name="edit_comment"),
    path('profile/delete_comment/<int:id>/', borrar_comentario, name="delete_comment"),
    path('logout/', cerrar_sesion, name= "logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
