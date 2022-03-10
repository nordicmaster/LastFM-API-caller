import django
import os
import networkx as nx
import matplotlib.pyplot as plt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello.settings")
django.setup()

from firstapp.models import StatsArtist
from firstapp.apps import get_top_tags


def tag_count_function(c1: int, c2: int) -> float:
    return (c1 + c2) / c2 if c2 > 50 else 0


fig, ax = plt.subplots()
x_axis = []
y_axis = []

filtered_artists = []
all_tags = []
tags_dict = {}

for p in StatsArtist.objects.all():
    #if p.listeners > 10:
    if str(p).startswith('a'):
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
                    tags_dict[(t2.name, t1.name)] += tag_count_function(t2.count, t1.count)
                else:
                    tags_dict[(t1.name, t2.name)] = tag_count_function(t1.count, t2.count)
                    tags_dict[(t2.name, t1.name)] = tag_count_function(t2.count, t1.count)
    i += 1
j = 0
all_tags.sort()
G = nx.Graph()
for tag in all_tags:
    j += 1
    tags_related = []
    for tdict1, tdict2 in tags_dict.keys():
        if tag == tdict1:
            tags_related.append(tdict2 + "(" + str(tags_dict[tdict1, tdict2]) + ")")
            if tags_dict[tdict1, tdict2] > 0:
                G.add_edge(tag, tdict2, weight=tags_dict[tdict1, tdict2])
    print(f'{j}. {tag} -- is related to {", ".join(tags_related)}')
edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())
pos1 = nx.kamada_kawai_layout(G)
#pos1 = nx.random_layout(G)
nx.draw(G, pos=pos1, with_labels=True, edgelist=edges, arrowstyle="->", edge_color=weights, edge_cmap=plt.cm.Reds)
plt.show()
