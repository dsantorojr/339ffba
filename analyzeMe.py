# imports
from espnff import League
from enum import Enum
import matplotlib.pyplot as plt
import statistics as stats

# constants 
WINS = 0
LOSSES = 1
TIES = 2

# league info
league_id = 650880
year = 2016
league = League(league_id, year)

# TODO -> either (1) find which weeks have been completed, or (2) make this a command line argument
numWeeks = 13


class Team:
	scores = []
	record = []
	rank = []
	winDifferential = []
	averageWinDiff = 0
	stdDevWinDiff = 0

	def __init__(self, name, scores) :
		self.name = name
		self.scores = scores
		self.record = []
		self.rank = []
		self.winDifferential = []
		for i in range(0, len(self.scores)) :
			self.record.append([0,0,0])
			self.rank.append(0)
			self.winDifferential.append(0)

	def addScore(self, score, week) :
		self.scores.append(score)

def getNextMax(teams, week) :
	maxWins = -1
	maxTeam = -1
	for i, team in enumerate(teams) :
		wins = team.record[week][WINS]
		if wins > maxWins and team.rank[week] == 0 :
			maxWins = team.record[week][WINS]
			maxTeam = i
	return maxTeam

def getTeams(league) :
	teams = []
	for team in league.teams :
		t = Team(team.team_name, team.scores)
		teams.append(t)
	return teams

def setRecords(teams) :
	# pick a team
	for team in teams :
		# get a team to which to compare
		for compare in teams :
			# ensure unique teams are being compared
			if team.name != compare.name :
				# loop through every week
				for i in range(0, numWeeks) :
					# add a win
					if team.scores[i] > compare.scores[i] :
						for j in range(i, numWeeks) :
							team.record[j][WINS] += 1;
					# add a loss
					elif team.scores[i] < compare.scores[i] :
						for j in range(i, numWeeks) :
							team.record[j][LOSSES] += 1;
					# add a tie
					else :
						for j in range(i, numWeeks) :
							team.record[j][TIES] += 1;
	return teams

def setWinDifferential(teams) :
	for week in range(0, numWeeks) :
		for team in teams :
			if week == 0 :
				team.winDifferential[week] = team.record[week][WINS]
			else :
				team.winDifferential[week] = team.record[week][WINS] - team.record[week-1][WINS]
	return teams

def setStats(teams) :
	for team in teams :
		team.averageWinDiff = stats.mean(team.winDifferential[0:numWeeks])
		team.stdDevWinDiff = stats.stdev(team.winDifferential[0:numWeeks])
	return teams

def plotWinDifferential(teams) :
	weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
	plt.figure()
	for team in teams :
		plt.plot(weeks, team.winDifferential, '-^', label = team.name)
	plt.ylabel("Win Differential")
	plt.xlabel("Week")
	plt.title("Win Differential Week By Week")
	plt.legend(loc='upper left', bbox_to_anchor=(1, 1))	
	plt.show()

def setRank(teams) :
	for week in range(0, numWeeks) :
		prevMaxTeam = ''
		prevMaxWins = -1
		rank = 1
		for team in teams :
			maxTeamIndex = getNextMax(teams, week)
			teams[maxTeamIndex].rank[week] = rank
			rank += 1
	return teams

def sortByRank(teams, week) :
	sortedTeams = []
	rank = 1
	while len(teams) > 0 :
		i = 0
		while teams[i].rank[week-1] != rank :
			i += 1
		sortedTeams.append(teams[i])
		teams = teams[:i] + teams[i+1:]
		rank+=1
	return sortedTeams

teams = getTeams(league)
teams = setRecords(teams)
teams = setWinDifferential(teams)
teams = setRank(teams)
teams = sortByRank(teams, numWeeks)
teams = setStats(teams)
#plotWinDifferential(teams)

print('NDL POWER RANKINGS THROUGH WEEK ' + str(numWeeks))
for t in teams :
	name = t.name
	record = t.record[numWeeks-1]
	rank = str(t.rank[numWeeks-1])
	toPrint = rank + '. ' + name + ' ->'
	toPrint += ' ' + str(record[WINS]) + '-' + str(record[LOSSES]) + '-' + str(record[TIES]) + '.'
	toPrint += ' WDA: ' + str(t.averageWinDiff)[0:4] + ', WDSD: ' + str(t.stdDevWinDiff)[0:4] + '.' 
	toPrint += ' CM: ' + str(t.averageWinDiff / t.stdDevWinDiff)[0:4] + '.'
	print(toPrint)





