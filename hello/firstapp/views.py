from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    data = {"message": "Welcome to Python"}
    return render(request, "index.html", context=data)


def about(request):
    return HttpResponse("<h2>About</h2><p>This is simple LastFm API caller. Check it to compare various artists rating.</p>")


def contact(request):
    return HttpResponse("<h2>Контакты</h2>")
