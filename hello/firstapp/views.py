from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .apps import *


class IndexView:
    def index(request):
        if request.method == "POST":
            name = request.POST.get("name")
            artist = get_lastfm_info(name)
            if isinstance(artist, str):
                return HttpResponse(artist)
            push_or_update(artist)
        return render(request, "index.html",
                      {"form": ArtistForm(), "artists": get_all_artists()})


def index_pagination(request):
    artist_list = get_all_artists()
    paginator = Paginator(artist_list, 100)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "index_pgn.html", {"form": ArtistForm(), "page_obj": page_obj})


def similar(request):
    userform = ArtistForm()
    res = "Similarity Check By Last.fm"
    res2 = "Similarity By My Database"
    if request.method == "POST":
        name = request.POST.get("name")
        res = get_lastfm_info_similar(name)
        res2 = get_db_info_similar(name)
    return render(request, "similar.html", {"form": userform, "message": res, "message_mydb": res2})


def by_user(request):
    artists_result = get_last_week_list("nordicmaster65")
    if isinstance(artists_result, str):
        return render(request, "my_stats.html", {"error_message": artists_result})
    return render(request, "my_stats.html", {"artists": artists_result})


def by_user_top(request):
    if request.method == "POST":
        period = request.POST.get("period")
        username = request.POST.get("username")
        if username == "":
            username = "nordicmaster65"
        return render(request, "my_top_stats.html", {"form": PeriodForm(),
                                                     "form_user": UserNameForm(),
                                                     "artists": get_top_artists(username, period),
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
                                                    "tags": get_top_tags_by_user(username, period),
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
                                                             "artists": get_top_similar_artists(username,
                                                                                                period=period),
                                                             "period_name": period,
                                                             "user_name": username
                                                             })
    return render(request, "my_top_stats_compare.html",
                  {"form": PeriodForm(), "form_user": UserNameForm(), "artists": []})


def about(request):
    return HttpResponse(
        "<h2>About</h2><p>This is simple LastFm API caller. Check it to compare various artists rating.</p>")


def contact(request):
    res = str(request.scheme) + " " + str(request.method) + " " + str(request.path)
    return HttpResponse("<h2>Контакты</h2><p>" + res + "</p>")


def del_artist(request, art_name):
    del_certain_artist(art_name)
    return redirect(IndexView.index)

def delete_all():
    delete_all_artists()
    return redirect(IndexView.index)
