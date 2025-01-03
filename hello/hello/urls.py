"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from firstapp import views

urlpatterns = [
    path('', views.IndexView.index, name='home'),
    path('admin', admin.site.urls),
    path('about', views.about),
    path('contact', views.contact),
    path('similar', views.similar, name='similar'),
    path('index_pagination', views.index_pagination, name='index_pagination'),
    path('by_user', views.by_user),
    path('by_user_top', views.by_user_top, name='by_user_top'),
    path('by_user_top_tags', views.by_user_top_tags, name='by_user_top_tags'),
    path('by_user_top_compare', views.by_user_top_compare, name='by_user_top_compare'),
    path('del/<str:art_name>/', views.del_artist, name='del_artist'),
    path('deleteAll', views.delete_all)
]
