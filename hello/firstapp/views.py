from django.http import HttpResponse
from django.shortcuts import render
from .forms import ArtistForm
from .apps import getLastFmInfo
from .apps import getLastFmInfo_similar
from .apps import pushOrUpdate
from .apps import get_all_artists


def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        artist = getLastFmInfo(name)
        if isinstance(artist, str):
            return HttpResponse(artist)
        pushOrUpdate(artist)
    userform = ArtistForm()
    return render(request, "index.html", {"form": userform, "artists": get_all_artists()})


def similar(request):
    if request.method == "POST":
        name = request.POST.get("name")
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
