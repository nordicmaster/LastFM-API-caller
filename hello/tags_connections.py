import django
import os
import matplotlib.pyplot as plt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello.settings")
django.setup()

from firstapp.models import StatsArtist
from firstapp.apps import get_top_tags


def tag_count_function(c1: int, c2: int) -> int:
    return c1 + c2


fig, ax = plt.subplots()
x_axis = []
y_axis = []

filtered_artists = []
all_tags = []
tags_dict = {}

for p in StatsArtist.objects.all():
    if p.listeners > 10:
        filtered_artists.append(p)
art_count = len(filtered_artists)
i = 0
for p in filtered_artists:
    print(f'{i} of {art_count}')
    tags = get_top_tags(p.artist)
    for t1 in tags:
        if t1.name not in all_tags:
            all_tags.append(t1.name)
        for t2 in tags:
            if t1.name != t2.name:
                if (t1.name, t2.name) in tags_dict:
                    tags_dict[(t1.name, t2.name)] += tag_count_function(t1.count, t2.count)
                    tags_dict[(t2.name, t1.name)] += tag_count_function(t1.count, t2.count)
                else:
                    tags_dict[(t1.name, t2.name)] = tag_count_function(t1.count, t2.count)
                    tags_dict[(t2.name, t1.name)] = tag_count_function(t1.count, t2.count)
    i += 1
for tag in all_tags:
    tags_related = []
    for tdict1, tdict2 in tags_dict.keys():
        if tag == tdict1:
            tags_related.append(tdict2 + "(" + str(tags_dict[tdict1, tdict2]) + ")")
    print(f'{tag} -- is related to {", ".join(tags_related)}')
#plt.show()
