# imports
from espnff import League

# constants 
WINS = 0
LOSSES = 1
TIES = 2

# league info
league_id = 650880
year = 2017
league = League(league_id, year)

# TODO -> either (1) find which weeks have been completed, or (2) make this a command line argument
numWeeks = 4


def getMax(spr, teams) :
	maxWins = 0
	maxTeam = ''
	for team in teams :
		if spr[team][WINS] > maxWins :
			maxWins = spr[team][WINS]
			maxTeam = team
	return maxTeam

# SPR - Santoro Power Rankings
spr = {}

# Calculate the Santoro Power Rankings
for team in league.teams :
	spr[team.team_name] = [0, 0, 0]

	for compare in league.teams :
		if team.team_name != compare.team_name :
			for i in range(0, numWeeks):
				if team.scores[i] > compare.scores[i] :
					spr[team.team_name][WINS] += 1
				elif team.scores[i] < compare.scores[i] :
					spr[team.team_name][LOSSES] += 1
				else :
					spr[team.team_name][TIES] += 1

# sort the teams
teams = list(spr.keys());
rankedTeams = []
while len(teams) > 0 :
	maxTeam = getMax(spr, teams)
	rankedTeams.append(maxTeam)
	teams.remove(maxTeam)

# print out the data
print('SANTORO POWER RANKINGS THROUGH WEEK ' + str(numWeeks))
for i in range(0, len(rankedTeams)) :
	teamRank = spr[rankedTeams[i]]
	toPrint = str(i+1) + '. ' + rankedTeams[i]
	while len(toPrint) < 35 :
		toPrint += '.'
	toPrint += ' ' + str(teamRank[0]) + '-' + str(teamRank[1]) + '-' + str(teamRank[2])
	print(toPrint)




