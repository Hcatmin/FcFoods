from django.shortcuts import render
from django.http import HttpResponse

def mapa(request):
    return render(request, 'mapa.html')

# Create your views here.
