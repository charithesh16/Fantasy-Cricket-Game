from django.db import models

# Create your models here.
class User(models.Model):
	user_id = models.IntegerField(primary_key=True)
	user_name = models.CharField(max_length=200)

	def __str__(self):
		return self.user_name

class Matches(models.Model):
	matchid = models.IntegerField(primary_key=True)
	coun1 = models.CharField(max_length=200)
	coun2 = models.CharField(max_length=200)
	status = models.CharField(max_length=200)

	def __str__(self):
		return self.coun1 + ' vs ' + self.coun2

class Players(models.Model):
	pid = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=200)
	category = models.CharField(max_length=200)
	points = models.IntegerField()
	country = models.CharField(max_length=200)

	def __str__ (self):
		return self.name + ' (' + self.country + ')'

class User_team(models.Model):
	user_id = models.ForeignKey(User,on_delete=models.CASCADE)
	matchid = models.ForeignKey(Matches,on_delete=models.CASCADE)
	pid = models.ForeignKey(Players,on_delete=models.CASCADE)
	stars = models.IntegerField(default=0)
	captain = models.ForeignKey(Players,related_name='Players',on_delete=models.CASCADE)
	def __str__(self):
		return self.user_id.user_name + ' plays ' + self.matchid.coun1 +' vs ' + self.matchid.coun2
		
class MatchPerformance(models.Model):
	matchid = models.ForeignKey(Matches,on_delete=models.CASCADE)
	pid = models.ForeignKey(Players,on_delete=models.CASCADE)
	runs = models.IntegerField()
	catches = models.IntegerField()
	wickets = models.IntegerField()

	def __str__(self):
		return self.pid.name + ' in match ' + self.matchid.coun1 + ' vs ' + self.matchid.coun2
