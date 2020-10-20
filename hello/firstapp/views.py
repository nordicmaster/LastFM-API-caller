from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ArtistForm
from .apps import getLastFmInfo
from .apps import getLastFmInfo_similar

def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        # here add json response from lastik
        res = getLastFmInfo(name)
        userform = ArtistForm()
        return render(request, "index.html", {"form": userform, "message": res})
    else:
        data = {"message": "Table Of Content:"}    
        userform = ArtistForm()
        return render(request, "index.html", {"form": userform, "message": "Table Of Content:"})


def similar(request):
    if request.method == "POST":
        name = request.POST.get("name")
        # here add json response from lastik
        res = getLastFmInfo_similar(name)
        userform = ArtistForm()
        return render(request, "similar.html", {"form": userform, "message": res})
    else:
        data = {"message": "Table Of Content:"}
        userform = ArtistForm()
        return render(request, "similar.html", {"form": userform, "message": "Table Of Content:"})


def about(request):
    return HttpResponse("<h2>About</h2><p>This is simple LastFm API caller. Check it to compare various artists rating.</p>")


def contact(request):
    res = str(request.scheme) + " " + str(request.method) + " " + str(request.path)
    return HttpResponse("<h2>Контакты</h2><p>" + res + "</p>")
