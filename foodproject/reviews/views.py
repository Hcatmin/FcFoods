# from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template

def home(request): 
    advices = get_template("home.html")
    ad_response = advices.render()

    return HttpResponse(ad_response)
    