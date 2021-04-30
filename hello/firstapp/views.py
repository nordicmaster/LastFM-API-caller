from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .apps import *


class IndexView():
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
    userform = ArtistForm()
    if request.method == "POST":
        name = request.POST.get("name")
        res = getLastFmInfo_similar(name)
        return render(request, "similar.html", {"form": userform, "message": res})
    else:
        return render(request, "similar.html", {"form": userform, "message": "Similarity Check By Last.fm"})


def by_user(request):
    return render(request, "my_stats.html", {"artists": getLastWeekList("nordicmaster65")})


def by_user_top(request):
    if request.method == "POST":
        period = request.POST.get("period")
        username = request.POST.get("username")
        if username == "":
            username = "nordicmaster65"
        return render(request, "my_top_stats.html", {"form": PeriodForm(),
                                                     "form_user": UserNameForm(),
                                                     "artists": getTopArtists(username, period),
                                                     "period_name": period,
                                                     "user_name": username
                                                     })
    return render(request, "my_top_stats.html", {"form": PeriodForm(), "form_user": UserNameForm(), "artists": []})


def by_user_top_tags(request):
    if request.method == "POST":
        period = request.POST.get("period")
        username = request.POST.get("username")
        if username == "":
            username = "nordicmaster65"
        return render(request, "my_top_tags.html", {"form": PeriodForm(),
                                                    "form_user": UserNameForm(),
                                                    "tags": getTopTagsByUser(username, period),
                                                    "period_name": period,
                                                    "user_name": username
                                                    })
    return render(request, "my_top_tags.html", {"form": PeriodForm(), "form_user": UserNameForm(), "tags": []})


def by_user_top_compare(request):
    if request.method == "POST":
        period = request.POST.get("period")
        username = request.POST.get("username")
        if username == "":
            username = "nordicmaster65"
        return render(request, "my_top_stats_compare.html", {"form": PeriodForm(),
                                                     "form_user": UserNameForm(),
                                                     "artists": getTopSimilarArtists(username, period=period),
                                                     "period_name": period,
                                                     "user_name": username
                                                     })
    return render(request, "my_top_stats_compare.html", {"form": PeriodForm(), "form_user": UserNameForm(), "artists": []})


def about(request):
    return HttpResponse("<h2>About</h2><p>This is simple LastFm API caller. Check it to compare various artists rating.</p>")


def contact(request):
    res = str(request.scheme) + " " + str(request.method) + " " + str(request.path)
    return HttpResponse("<h2>Контакты</h2><p>" + res + "</p>")


def deleteAll(request):
    delete_all_artists()
    return redirect(IndexView.index)

