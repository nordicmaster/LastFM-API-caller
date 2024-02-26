from django.apps import AppConfig
from .models import StatsArtist
from datetime import date
import requests
import json
import os
import matplotlib.pyplot as plt


#class FirstappConfig(AppConfig):
#    name = 'my_firstapp'
#    verbose_name = "First App"


class MyWeekArtistInfo:
    def __init__(self, name, scr, listn):
        self.artist = name
        self.scrobbles = scr
        self.listeners = listn


class MyComparisonInfo:
    def __init__(self, name, scr, listn, user_listn):
        self.artist = name
        self.scrobbles = scr
        self.listeners = listn
        self.user_listn = user_listn


class MyTagInfo:
    ignore_tags_common = ['rock', 'metal']
    with open(os.path.join(os.path.dirname(__file__), 'static', 'ignore_tags_trash.json')) as f_ignore_tags_trash:
        data = json.load(f_ignore_tags_trash)
        ignore_tags_trash = data

    with open(os.path.join(os.path.dirname(__file__), 'static', 'ignore_tags_countries.json')) as f_ign_tags_countries:
        data = json.load(f_ign_tags_countries)
        ignore_tags_countries = data

    def __init__(self, name: str, count: int):
        self.name = name
        self.count = count

    def __str__(self):
        return self.name + ": " + str(self.count) + "; "


def get_lastfm_info(name):
    """ Gets Artist.GetInfo for specified artist"""
    url = 'https://ws.audioscrobbler.com/2.0/'
    myobj = {'method': 'artist.getinfo',
             'artist': name,
             'api_key': '57ee3318536b23ee81d6b27e36997cde',
             'format': 'json'}
    x = requests.get(url, myobj)
    x_info = x.json()
    if 'error' in x_info:
        return x_info["message"] + "<br>"
    listeners = x_info["artist"]["stats"]["listeners"]
    totalscrobbles = x_info["artist"]["stats"]["playcount"]
    new_artist = StatsArtist(last_seen=date.today(),
                             ratio=float(totalscrobbles) / float(listeners),
                             scrobbles=totalscrobbles,
                             listeners=listeners,
                             artist=name)
    return new_artist


def get_last_week_list(myname):
    """ Gets User.GetWeeklyArtistChart for specified user"""
    url = 'https://ws.audioscrobbler.com/2.0/'
    myobj = {'method': 'user.getWeeklyArtistChart',
             'user': myname,
             'api_key': '57ee3318536b23ee81d6b27e36997cde',
             'format': 'json'}
    try:
        x = requests.get(url, myobj, timeout=1)
    except requests.exceptions.Timeout:
        return "request timeout"
    x_info = x.json()
    if 'error' in x_info:
        return x_info["message"] + "<br>"
    week_artists = x_info["weeklyartistchart"]["artist"]
    result = []
    for art in week_artists:
        lsn = get_lastfm_info(art["name"]).listeners
        artist_in_week_stats = MyWeekArtistInfo(art["name"], art["playcount"], lsn)
        result.append(artist_in_week_stats)
    return result


def get_top_tags_by_user(username, period='overall'):
    """ Gets User.GetTopArtists by period and calculates top tags"""
    url = 'https://ws.audioscrobbler.com/2.0/'
    myobj = {'method': 'user.getTopArtists',
             'period': period,
             'user': username,
             'api_key': '57ee3318536b23ee81d6b27e36997cde',
             'format': 'json'}
    x = requests.get(url, myobj)
    x_info = x.json()
    if 'error' in x_info:
        return x_info["message"] + "<br>"
    top_artists = x_info["topartists"]["artist"]
    result = []
    for art in top_artists:
        tags = get_top_tags(art["name"])
        if type(tags) == str:
            continue
        for tg in tags:
            exist = False
            for i in enumerate(result):
                if i[1].name == tg.name:
                    i[1].count += tg.count * int(art["playcount"])
                    exist = True
                    break
            if not exist:
                result.append(MyTagInfo(tg.name, tg.count * int(art["playcount"])))
    result.sort(key=lambda tag: tag.count, reverse=True)
    all_tagcount = sum(x.count for x in result)
    result = list(map(lambda tag_reduced: MyTagInfo(tag_reduced.name, 100 * tag_reduced.count / all_tagcount), result))
    return result


def get_top_tags(artist):
    """ Gets Artist.GetTopTags for specified artist"""
    url = 'https://ws.audioscrobbler.com/2.0/'
    myobj = {'method': 'artist.gettoptags',
             'artist': artist,
             'api_key': '57ee3318536b23ee81d6b27e36997cde',
             'format': 'json'}
    x = requests.get(url, myobj)
    x_info = x.json()
    if 'error' in x_info:
        return x_info["message"] + "<br>"
    tags = x_info["toptags"]["tag"]
    result = []
    for tag in tags:
        if tag["name"] in MyTagInfo.ignore_tags_trash:
            continue
        if tag["name"] in MyTagInfo.ignore_tags_countries:
            continue
        if tag["count"] > 20:
            result.append(MyTagInfo(tag["name"], tag["count"]))
    return result


def get_lastfm_info_similar(name):
    """ Gets Artist.GetInfo - similar artists for specified artist"""
    url = 'https://ws.audioscrobbler.com/2.0/'
    myobj = {'method': 'artist.getinfo',
             'artist': name,
             'api_key': '57ee3318536b23ee81d6b27e36997cde',
             'format': 'json'}
    x = requests.get(url, myobj)
    x_info = x.json()
    similar_res = ''
    if 'error' in x_info:
        similar_res = similar_res + x_info["message"] + "<br>"
        return similar_res
    artists = x_info["artist"]["similar"]["artist"]
    if bool(artists):
        similar_res = similar_res + "<span class=\"fixwidth\">" + name + "</span> is similar to "
    else:
        similar_res = similar_res + "<span class=\"fixwidth\">" + name + "</span> is unique "
    for art in artists:
        similar_res = similar_res + art["name"] + ", "
    similar_res = similar_res + "<br>"
    return similar_res


def push_or_update(myartist: StatsArtist):
    # print(StatsArtist.objects.filter(artist=myartist.artist))
    if StatsArtist.objects.filter(artist=myartist.artist):
        StatsArtist.objects.filter(artist=myartist.artist).update(listeners=myartist.listeners,
                                                                  scrobbles=myartist.scrobbles,
                                                                  ratio=myartist.ratio, last_seen=myartist.last_seen)
    else:
        myartist.save()
    return


def get_all_artists():
    return StatsArtist.objects.all()


def delete_all_artists():
    StatsArtist.objects.all().delete()
    return

def del_certain_artist(name):
    if StatsArtist.objects.filter(artist=name):
        StatsArtist.objects.filter(artist=name).delete()


def get_library_of_user(username):
    """ Gets scrobbles for specified user"""
    url = 'https://ws.audioscrobbler.com/2.0/'
    myobj = {'method': 'library.getArtists',
             'user': username,
             'limit': 1500,
             'api_key': '57ee3318536b23ee81d6b27e36997cde',
             'format': 'json'}
    x = requests.get(url, myobj)
    x_info = x.json()
    if 'error' in x_info:
        return 0
    return x_info["artists"]["artist"]


def get_scrobbles_of_certain_artist_in_library(library, name):
    if library == 0:
        return 0
    for art in library:
        if art["name"] == name:
            return art["playcount"]
    return 0


def get_top_artists(myname, period='overall'):
    """ Gets User.GetTopArtists for specified user by period"""
    url = 'https://ws.audioscrobbler.com/2.0/'
    myobj = {'method': 'user.getTopArtists',
             'period': period,
             'user': myname,
             'api_key': '57ee3318536b23ee81d6b27e36997cde',
             'format': 'json'}
    x = requests.get(url, myobj)
    x_info = x.json()
    if 'error' in x_info:
        return x_info["message"] + "<br>"
    top_artists = x_info["topartists"]["artist"]
    result = []
    library = get_library_of_user(myname)
    for art in top_artists:
        artist_in_week_stats = MyWeekArtistInfo(art["name"], art["playcount"],
                                                get_scrobbles_of_certain_artist_in_library(library, art["name"]))
        upd_artist = get_lastfm_info(art["name"])
        if not isinstance(upd_artist, str):
            push_or_update(upd_artist)
        result.append(artist_in_week_stats)
    return result


def get_top_similar_artists(other_username, myname='nordicmaster65', period='overall'):
    """ Gets my User.GetTopArtists and other user by period"""
    url = 'https://ws.audioscrobbler.com/2.0/'
    myobj = {'method': 'user.getTopArtists',
             'period': period,
             'user': myname,
             'api_key': '57ee3318536b23ee81d6b27e36997cde',
             'format': 'json'}
    x = requests.get(url, myobj)
    x_info = x.json()
    if 'error' in x_info:
        return x_info["message"] + "<br>"
    top_artists = x_info["topartists"]["artist"]
    result = []
    my_library = get_library_of_user(myname)
    other_library = get_library_of_user(other_username)
    for art in top_artists:
        artist_in_week_stats = MyComparisonInfo(art["name"], art["playcount"],
                                                get_scrobbles_of_certain_artist_in_library(my_library, art["name"]),
                                                get_scrobbles_of_certain_artist_in_library(other_library, art["name"]))
        result.append(artist_in_week_stats)
    return result


def get_db_info_similar(name):
    similar_db_res = "<i>" + name + "</i> is popular as (in database): <br>"
    if StatsArtist.objects.filter(artist=name):
        artist_listeners = list(StatsArtist.objects.filter(artist=name))[0].listeners
        artist_scrobbles = list(StatsArtist.objects.filter(artist=name))[0].scrobbles
        similar_db_arr_names = []
        filtered_artists = []
        filtered_artists.append(StatsArtist.objects.filter(artist=name)[0])
        percent_step = 3
        percent_i = 1
        while (len(similar_db_arr_names) < 5) and (percent_i < 10):
            min_listeners = artist_listeners * (1 - 0.01 * percent_step * percent_i)
            max_listeners = artist_listeners * (1 + 0.01 * percent_step * percent_i)
            min_scrobbles = artist_scrobbles * (1 - 0.01 * percent_step * percent_i)
            max_scrobbles = artist_scrobbles * (1 + 0.01 * percent_step * percent_i)
            for p in StatsArtist.objects.all():
                if p.artist == name:
                    continue
                if p.artist in similar_db_arr_names:
                    continue
                if (p.listeners > min_listeners and p.listeners < max_listeners and
                        p.scrobbles > min_scrobbles and p.scrobbles < max_scrobbles):
                    similar_db_arr_names.append(p.artist)
                    filtered_artists.append(p)
            percent_i += 1
        similar_db_res += ', '.join(similar_db_arr_names) + "<br>"
        similar_db_res += 'with ' + str(artist_listeners) + ' listeners and ' + str(artist_scrobbles) + ' scrobbles<br>'
        # matplotlib
        # todo: run matplotlib in separate thread
        fig, ax = plt.subplots()
        x_axis = []
        y_axis = []
        for p in filtered_artists:
            x_axis.append(p.listeners)
            y_axis.append(p.scrobbles)
        sc = ax.scatter(x_axis, y_axis)
        for p in filtered_artists:
            p_ratio = float(p.scrobbles) / float(p.listeners)
            ax.annotate(p.artist + '(' + str(round(p_ratio, 2)) + ')', (p.listeners, p.scrobbles))
        plt.xlabel("listeners")
        plt.ylabel("scrobbles")
        plt.show()
    else:
        similar_db_res += name + 'is not in database'
    return similar_db_res
