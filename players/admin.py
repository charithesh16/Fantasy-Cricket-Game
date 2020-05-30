from django.contrib import admin

# Register your models here.
from .models import Players,Matches,User_team,MatchPerformance,User
admin.site.register(Players)
admin.site.register(Matches)
admin.site.register(User_team)
admin.site.register(MatchPerformance)
admin.site.register(User)