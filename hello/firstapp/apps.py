from django.apps import AppConfig
import requests


class FirstappConfig(AppConfig):
    name = 'firstapp'


res = ''


def getLastFmInfo(name):
    #if ' ' in name:
    #    name = name.replace(" ", "+")
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
    res = res + totalscrobbles + "</span> scrobbles. Ratio=" + str(float(totalscrobbles) / float(listeners)) + "<br>";
    return res