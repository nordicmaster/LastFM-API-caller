from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    data = {"message": "Table Of Content:"}
    return render(request, "index.html", context=data)


def about(request):
    return HttpResponse("<h2>About</h2><p>This is simple LastFm API caller. Check it to compare various artists rating.</p>")


def contact(request):
    res = str(request.scheme) + " " + str(request.method) + " " + str(request.path)
    return HttpResponse("<h2>Контакты</h2><p>" + res + "</p>")
