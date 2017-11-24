# imports
from espnff import League
from enum import Enum

# constants 
WINS = 0
LOSSES = 1
TIES = 2

# league info
league_id = 650880
year = 2017
league = League(league_id, year)

# TODO -> either (1) find which weeks have been completed, or (2) make this a command line argument
numWeeks = 11


class Team:
	scores = []
	record = []
	rank = []

	def __init__(self, name, scores) :
		self.name = name
		self.scores = scores
		self.record = []
		self.rank = []
		for i in range(0, len(self.scores)) :
			self.record.append([0,0,0])
			self.rank.append(0)

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
teams = setRank(teams)
teams = sortByRank(teams, numWeeks)

print('NDL POWER RANKINGS THROUGH WEEK ' + str(numWeeks))
for t in teams :
	name = t.name
	record = t.record[numWeeks-1]
	rank = str(t.rank[numWeeks-1])
	toPrint = rank + '. ' + name + ' ->'
	toPrint += ' ' + str(record[WINS]) + '-' + str(record[LOSSES]) + '-' + str(record[TIES])
	print(toPrint)


# # sort the teams
# teams = list(spr.keys());
# rankedTeams = []
# while len(teams) > 0 :
# 	maxTeam = getMax(spr, teams)
# 	rankedTeams.append(maxTeam)
# 	teams.remove(maxTeam)

# # print out the data
# print('NDL POWER RANKINGS THROUGH WEEK ' + str(numWeeks))
# for i in range(0, len(rankedTeams)) :
# 	teamRank = spr[rankedTeams[i]]
# 	toPrint = str(i+1) + '. ' + rankedTeams[i] + ' ->'
# 	toPrint += ' ' + str(teamRank[0]) + '-' + str(teamRank[1]) + '-' + str(teamRank[2])
# 	print(toPrint)




