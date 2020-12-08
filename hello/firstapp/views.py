from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ArtistForm
from .apps import *


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
        return render(request, "similar.html", {"form": userform, "message": "Similarity Check By Last.fm"})


def by_user(request):
    return render(request, "my_stats.html", {"artists": getLastWeekList("nordicmaster65")})


def by_user_top(request):
    return render(request, "my_stats.html", {"artists": getTopArtists("nordicmaster65")})


def about(request):
    return HttpResponse("<h2>About</h2><p>This is simple LastFm API caller. Check it to compare various artists rating.</p>")


def contact(request):
    res = str(request.scheme) + " " + str(request.method) + " " + str(request.path)
    return HttpResponse("<h2>Контакты</h2><p>" + res + "</p>")


def deleteAll(request):
    delete_all_artists()
    return redirect(index)

