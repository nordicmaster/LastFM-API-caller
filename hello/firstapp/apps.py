from django.apps import AppConfig
import requests


class FirstappConfig(AppConfig):
    name = 'firstapp'


res = ''
similar_res = ''


def getLastFmInfo(name):
    url = 'https://ws.audioscrobbler.com/2.0/'
    myobj = {'method': 'artist.getinfo',
             'artist': name,
             'api_key': '57ee3318536b23ee81d6b27e36997cde',
             'format': 'json'}
    x = requests.get(url, myobj)
    xInfo = x.json()
    global res
    if 'error' in xInfo:
        res = res + xInfo["message"] + "<br>"
        return res
    listeners = xInfo["artist"]["stats"]["listeners"]
    totalscrobbles = xInfo["artist"]["stats"]["playcount"]
    res = res + "<span class=\"fixwidth\">" + name + "</span> has <span class=\"fixwidth2\">"
    res = res + listeners + "</span> listeners and <span class=\"fixwidth3\">"
    res = res + totalscrobbles + "</span> scrobbles. Ratio=" + str(float(totalscrobbles) / float(listeners)) + "<br>"
    return res


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
