from django.apps import AppConfig
from .models import StatsArtist
from datetime import date
import requests


class FirstappConfig(AppConfig):
    name = 'firstapp'


class MyWeekArtistInfo:
    def __init__(self,name,scr,listn):
        self.artist = name
        self.scrobbles = scr
        self.listeners = listn


similar_res = ''


def getLastFmInfo(name):
    url = 'https://ws.audioscrobbler.com/2.0/'
    myobj = {'method': 'artist.getinfo',
             'artist': name,
             'api_key': '57ee3318536b23ee81d6b27e36997cde',
             'format': 'json'}
    x = requests.get(url, myobj)
    xInfo = x.json()
    if 'error' in xInfo:
        return xInfo["message"] + "<br>"
    listeners = xInfo["artist"]["stats"]["listeners"]
    totalscrobbles = xInfo["artist"]["stats"]["playcount"]
    new_artist = StatsArtist(last_seen=date.today(),
                             ratio=float(totalscrobbles)/float(listeners),
                             scrobbles=totalscrobbles,
                             listeners=listeners,
                             artist=name)
    return new_artist


def getLastWeekList(myname):
    url = 'https://ws.audioscrobbler.com/2.0/'
    myobj = {'method': 'user.getWeeklyArtistChart',
             'user': myname,
             'api_key': '57ee3318536b23ee81d6b27e36997cde',
             'format': 'json'}
    x = requests.get(url, myobj)
    xInfo = x.json()
    if 'error' in xInfo:
        return xInfo["message"] + "<br>"
    week_artists = xInfo["weeklyartistchart"]["artist"]
    result = []
    for art in week_artists:
        #add new item to result array
        # and add there art["name"] and art["playcount"]
        lsn = getLastFmInfo(art["name"]).listeners
        artist_in_week_stats = MyWeekArtistInfo(art["name"],art["playcount"],lsn)
        result.append(artist_in_week_stats)
    return result


def getLastFmInfo_similar(name):
    url = 'https://ws.audioscrobbler.com/2.0/'
    myobj = {'method': 'artist.getinfo',
             'artist': name,
             'api_key': '57ee3318536b23ee81d6b27e36997cde',
             'format': 'json'}
    x = requests.get(url, myobj)
    xInfo = x.json()
    global similar_res
    if 'error' in xInfo:
        similar_res = similar_res + xInfo["message"] + "<br>"
        return similar_res
    artists = xInfo["artist"]["similar"]["artist"]
    if bool(artists):
        similar_res = similar_res + "<span class=\"fixwidth\">" + name + "</span> is similar to "
    else:
        similar_res = similar_res + "<span class=\"fixwidth\">" + name + "</span> is unique "
    for art in artists:
        similar_res = similar_res + art["name"] + ", "
    similar_res = similar_res + "<br>"
    return similar_res


def pushOrUpdate(myartist: StatsArtist):
    print(StatsArtist.objects.filter(artist=myartist.artist))
    if StatsArtist.objects.filter(artist=myartist.artist):
        StatsArtist.objects.filter(artist=myartist.artist).update(listeners=myartist.listeners, scrobbles=myartist.scrobbles,
                                                              ratio=myartist.ratio, last_seen=myartist.last_seen)
    else:
        myartist.save()
    return


def get_all_artists():
    return StatsArtist.objects.all()


def delete_all_artists():
    StatsArtist.objects.all().delete()
    return
