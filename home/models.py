from django.db import models
from django.shortcuts import render


# Create your models here.
def index(request):
    """A view that displays the index page"""
    return render(request, "index.html")
    