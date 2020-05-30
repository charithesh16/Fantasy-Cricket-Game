from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from players.models import Players,Matches,User_team,MatchPerformance,User
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import JsonResponse 

# Create your views here

points =100
def dashboard(request):
	captain_id = request.POST["captain"]
	print(captain_id)
	match_id = Matches.objects.get(matchid = request.session['match'])
	print("Dashboard instance",match_id)
	for i in request.session['selected_players']:
		player_id = Players.objects.get(pid = i)
		user_team = User_team(user_id = User.objects.get(user_id=4) ,matchid = match_id,captain = Players.objects.get(pid=captain_id),pid=player_id,stars=0)
		user_team.save()
	batsmen=[]
	bowler=[]
	all_rounder=[]
	wicket_keeper=[]
	for i in request.session['selected_players']:
		d={}
		player = Players.objects.get(pid=int(i))
		if player.category == 'bat':
			d['name']=player.name
			batsmen.append(d)
		elif player.category == 'bowl':
			d['name']=player.name
			bowler.append(d)
		elif player.category == 'all rounder':
			d['name']=player.name
			all_rounder.append(d)
		else:
			d['name']=player.name
			wicket_keeper.append(d)
	return render(request,'dashboard.html',{'batsmen':batsmen,'bowler':bowler,'all_rounder':all_rounder,'wicket_keeper':wicket_keeper})

def select_team(request):
	global points
	points =100
	matches = Matches.objects.filter(status='upcoming')
	return render(request,'team.html',{'matches':matches,'error':False})

def players_list(request,match_id=None):
	global points
	# if request.method=="POST":
	request.session['match'] = int(match_id)
	match = request.session['match']
	# print(match)
	# query = reduce(operator.or_,(Q(country=cn,category='bat') for cn in [country1,country2]))
	country1=Matches.objects.filter(matchid=match)[0].coun1 
	country2 = Matches.objects.filter(matchid=match)[0].coun2
	request.session['batsmen'] = list(Players.objects.filter(country__in=[country1,country2],category='bat').values())
	request.session['all_rounder'] = list(Players.objects.filter(country__in=[country1,country2],category='all rounder').values())
	request.session['bowler'] = list(Players.objects.filter(country__in=[country1,country2],category='bowl').values())
	request.session['wicket_keeper']= list(Players.objects.filter(country__in=[country1,country2],category__startswith='wicket').values())
	# print(request.session['batsmen'])
	return  render(request,'players.html',{'points':points,'batsmen':request.session['batsmen'],'bowler':request.session['bowler'],'all_rounder':request.session['all_rounder'],'wicket_keeper':request.session['wicket_keeper']})
	# return render(request,'players.html',{'points':points})

def user_team(request):
	global points
	request.session['selected_batsmen']=request.POST.getlist("batsmen")
	request.session['selected_bowler'] = request.POST.getlist("bowler")
	request.session['selected_all_rounder'] = request.POST.getlist("all_rounder")
	request.session['selected_wicket_keeper']= request.POST.getlist("wicket_keeper")
	min_batsmen=4
	min_bowlers=3
	min_wk=1
	min_all=1
	all_players=11
	total_points=100
	selected_points=0
	error_msg=[]
	print(request.session['selected_bowler'])
	request.session['selected_players'] = request.session['selected_batsmen'] + request.session['selected_bowler'] + request.session['selected_all_rounder'] + request.session['selected_wicket_keeper']
	for i in request.session['selected_batsmen']:
		selected_points+=Players.objects.filter(pid=int(i))[0].points
	for i in request.session['selected_bowler']:
		selected_points+=Players.objects.filter(pid=int(i))[0].points
	for i in request.session['selected_all_rounder']:
		selected_points+=Players.objects.filter(pid=int(i))[0].points
	for i in request.session['selected_wicket_keeper']:
		selected_points+=Players.objects.filter(pid=int(i))[0].points
	all_selected=len(request.session['selected_batsmen'])+len(request.session['selected_bowler'])+len(request.session['selected_wicket_keeper'])+len(request.session['selected_all_rounder'])
	if len(request.session['selected_batsmen'])<min_batsmen:
		error_msg.append("Select minimum 4 batsmen")
	if len(request.session['selected_bowler']) < min_bowlers:
		error_msg.append("Select minimum 3 bowlers")
	if len(request.session['selected_wicket_keeper']) < min_wk:
		error_msg.append("Select minimum 1 wicket keeper")
	if len(request.session['selected_all_rounder']) < min_all:
		error_msg.append("Select minimum 1 all rounder")
	if all_selected != all_players:
		error_msg.append("Select 11 players")
	if selected_points>total_points:
		error_msg.append("Select players with points less than 100")
	if error_msg != []:
		points = 100
		return  render(request,'players.html',{'points':points,'error_msg':error_msg,'error':True,'batsmen':request.session['batsmen'],'bowler':request.session['bowler'],'all_rounder':request.session['all_rounder'],'wicket_keeper':request.session['wicket_keeper']})
	selected_batsmen = []
	selected_bowler = []
	selected_all_rounder = []
	selected_wicket_keeper = []
	for i in request.session['selected_batsmen']:
		selected_batsmen.append(Players.objects.filter(pid=int(i))[0])
	for i in request.session['selected_bowler']:
		selected_bowler.append(Players.objects.filter(pid=int(i))[0])
	for i in request.session['selected_wicket_keeper']:
		selected_wicket_keeper.append(Players.objects.filter(pid=int(i))[0])
	for i in request.session['selected_all_rounder']:
		selected_all_rounder.append(Players.objects.filter(pid=int(i))[0])
	# print("selected_batsmen",selected_batsmen)
	return render(request,'user_team.html',{'batsmen':selected_batsmen,'bowler':selected_bowler,'all_rounder':selected_all_rounder,'wicket_keeper':selected_wicket_keeper})

@csrf_exempt
def get_points(request):
	p_id = request.POST["id"]
	global points
	# print("pid",p_id)
	# print("points",points)
	p_points = Players.objects.filter(pid=p_id)
	if(int(request.POST["checked"])):
		new_points = int(points) - int(p_points[0].points)
		points = new_points
	else:
		new_points = int(points) + int(p_points[0].points)
		points = new_points

	return HttpResponse(new_points)

def home(request):
	return render(request,'home.html')

def userPointCalculation(i):
	print("id",i)
	print("In userPoint")
	match_id = Matches.objects.get(matchid=int(i))
	print("match instance",match_id)
	match_performances = MatchPerformance.objects.filter(matchid=match_id)
	obj = User_team.objects.filter(matchid=match_id).values('user_id').distinct()
	print(obj)
	for u in obj:
		user_selected_players = User_team.objects.filter(user_id=u['user_id'],matchid=match_id)
		print("user_selected_players",user_selected_players)
		print("match_performances",len(match_performances))
		s = 0
		for w in user_selected_players:
			for m in match_performances:
				if(m.pid == w.pid):
					if(m.pid.pid==w.captain.pid):
						s += (m.runs + m.catches*20 + m.wickets*20)*2
					else:
						s += m.runs + m.catches*20 + m.wickets*20
		print("S",s)
		for w in user_selected_players:
			w.stars = s
			w.save()


# 1. India vs Australia leaderboard
def matchlist(request):
	matches = Matches.objects.filter(status="completed")
	return render(request,'matchlist.html',{'matches':matches})

def lb(request,i=None):
	userPointCalculation(i)
	userTeamObj = User_team.objects.filter(matchid=Matches.objects.get(matchid=int(i))).order_by('-stars').values('stars','user_id').distinct()
	print(userTeamObj)
	# user_names =[]
	for w in userTeamObj:
		user = User.objects.get(user_id=w['user_id'])
		w['name']=user.user_name
	return render(request,"leaderboard.html",{'userTeamList':userTeamObj})


def completed_matches(request):
	completed_matches = Matches.objects.filter(status="completed")
	return render(request,'completed_matches.html',{'completed_matches':completed_matches})

def players_performances(request,id=None):
	match = Matches.objects.get(matchid=id)
	user = User.objects.get(user_id=1)
	players = User_team.objects.filter(user_id=user,matchid=match)
	captain_id=None
	performances = []
	for i in players:
		d={}
		player=MatchPerformance.objects.get(matchid=match,pid=i.pid)
		s = 0
		
		d['runs']=player.runs
		d['catches']=player.catches
		d['wickets']=player.wickets
		d['name']=player.pid.name
		if i.pid.pid == i.captain.pid:
			captain_id=i.captain.pid
			s = (player.runs + player.catches*20 + player.wickets*20)*2
		else:
			s = (player.runs + player.catches*20 + player.wickets*20)

		d['id']=i.pid.pid
		d['score']=s
		performances.append(d)
	print(captain_id)
	performances=sorted(performances, key = lambda i: i['score'],reverse=True) 
	return render(request,'performances.html',{'performances':performances,'captain':captain_id})


def profile(request):
	user = User.objects.get(user_id = 1)
	name=user.user_name
	played_matches = User_team.objects.filter(user_id =user).values('matchid').distinct()
	print(played_matches)
	matches=[]
	for i in played_matches:
		d={}
		obj = User_team.objects.filter(user_id = user,matchid=Matches.objects.get(matchid=i['matchid']))[0]
		d['coun1']=obj.matchid.coun1
		d['coun2']=obj.matchid.coun2
		d['stars']=obj.stars
		matches.append(d)

	return render(request,'profile.html',{'matches':matches,'name':name})

