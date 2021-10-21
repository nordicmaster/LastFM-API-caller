import django
import os
import matplotlib.pyplot as plt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello.settings")
django.setup()

from firstapp.models import StatsArtist

fig, ax = plt.subplots()  # Create a figure containing a single axes.
x_axis = []
y_axis = []
filtered_artists = []
for p in StatsArtist.objects.all():
    #if p.listeners > 100000:
    #    filtered_artists.append(p)
    filtered_artists.append(p)
for p in filtered_artists:
    x_axis.append(p.listeners)
    y_axis.append(p.scrobbles)
sc = ax.scatter(x_axis, y_axis)  # Plot some data on the axes.
for p in filtered_artists:
    p_ratio = float(p.scrobbles)/float(p.listeners)
    ax.annotate(p.artist + '(' + str(round(p_ratio, 2)) + ')', (p.listeners, p.scrobbles))
plt.xlabel("listeners")
plt.ylabel("scrobbles")

# annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot.set_visible(False)
#
# def update_annot(ind):
#
#     pos = sc.get_offsets()[ind["ind"][0]]
#     annot.xy = pos
#     text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))),
#                            " ".join([names[n] for n in ind["ind"]]))
#     annot.set_text(text)
#     annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
#     annot.get_bbox_patch().set_alpha(0.4)
#
#
# def hover(event):
#     vis = annot.get_visible()
#     if event.inaxes == ax:
#         cont, ind = sc.contains(event)
#         if cont:
#             update_annot(ind)
#             annot.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot.set_visible(False)
#                 fig.canvas.draw_idle()
#
# fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()
