"""yorking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from players.views import profile,players_list,user_team,select_team,dashboard,get_points,home,matchlist,lb,completed_matches,players_performances
urlpatterns = [
    path('',home,name="home"),
    path('profile/',profile,name="profile"),
    path('dashboard/',dashboard,name="dashboard"),
    path('get_points/',get_points,name="get_points"),
    path('team/',select_team,name="select_team"),
    path('user_team/',user_team,name="user_team"),
    path('players/<int:match_id>',players_list,name="players"),
    path('matchlist/',matchlist,name="matchlist"),
    path('leaderboard/<int:i>',lb,name="leaderboard"),
    path('players_dashboard',completed_matches,name="players_dashboard"),
    path('performances/<int:id>',players_performances,name="performances"),
    path('admin/', admin.site.urls),
]
