# imports
import sys
import getopt
from espnff import League
from enum import Enum
import matplotlib.pyplot as plt
import statistics as stats


# constants 
WINS = 0
LOSSES = 1
TIES = 2
HELP_STRING = '''
For proper use of this script:

analyzeMe.py -y <year> -w <week> -v -h
-v plots visual statistics.
-h shows this message.
'''

# Class definition
class Team:
	scores = []
	record = []
	rank = []
	winDifferential = []
	avgWinDiff = 0
	normAvgWinDiff = 0
	stdDevWinDiff = 0
	normStdDevWinDiff = 0


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

	def setWinDifferential(self, numWeeks) :
		for week in range(0, numWeeks) :
			if week == 0 :
				self.winDifferential[week] = self.record[week][WINS]
			else :
				self.winDifferential[week] = self.record[week][WINS] - self.record[week-1][WINS]

	def setStats(self, numWeeks) :
			gamesPerWeek = (self.record[numWeeks-1][WINS] + self.record[numWeeks-1][LOSSES] + self.record[numWeeks-1][TIES]) / numWeeks
			self.avgWinDiff = stats.mean(self.winDifferential[0:numWeeks])
			self.stdDevWinDiff = stats.stdev(self.winDifferential[0:numWeeks])
			self.normAvgWinDiff = self.avgWinDiff / gamesPerWeek
			self.normStdDevWinDiff = self.stdDevWinDiff / gamesPerWeek

# getNextMax - get the team with the max number of wins for a given week. 
## NOTE: This is only used by setRank and uses the non-existence of a team's rank to ensure
##	an already ranked team isn't re-ranked
def getNextMax(teams, week) :
	# initializaiton
	maxWins = -1
	maxTeam = -1
	
	for i, team in enumerate(teams) :
		if team.record[week][WINS] > maxWins and team.rank[week] == 0 :
			maxWins = team.record[week][WINS]
			maxTeam = i
	return maxTeam

# getTeams - this what's returned from the espnff package and puts it into a local class structure
def getTeams(league) :
	teams = []
	for team in league.teams :
		t = Team(team.team_name, team.scores)
		teams.append(t)
	return teams

# setRecords - set the power ranking records of every team. TODO: more efficient way to do this.
def setRecords(teams, numWeeks) :
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


# setRank - sets the rank of every team. TODO: more efficient way to do this.
def setRank(teams, numWeeks) :
	for week in range(0, numWeeks) :
		prevMaxTeam = ''
		prevMaxWins = -1
		rank = 1
		for team in teams :
			maxTeamIndex = getNextMax(teams, week)
			teams[maxTeamIndex].rank[week] = rank
			rank += 1
	return teams

# sortByRank - all in the name. TODO: more efficient way to do this.
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

# setStats - uses inherent class functions to set team stats
def setStats(teams, numWeeks) :
	for team in teams :
		team.setWinDifferential(numWeeks)
		team.setStats(numWeeks)
	return teams

# plotWinDifferential - its all in the name
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

# saveStats - save stats in CSV file
def saveStats(teams, year, numWeeks) :
	filename = str(year) + '_Stats_Thru_Week_' + str(numWeeks) + '.csv'
	f = open(filename, 'w')

	f.write('Year,Team,Wins,Losses,Ties,WDA,WDSD,NWDA,NWDSD,CM\n')
	for t in teams :
		toWrite = str(year) + ','
		toWrite += t.name + ','
		toWrite += str(t.record[numWeeks-1][WINS]) + ','
		toWrite += str(t.record[numWeeks-1][LOSSES]) + ','
		toWrite += str(t.record[numWeeks-1][TIES]) + ','
		toWrite += str(t.avgWinDiff)[0:4] + ','
		toWrite += str(t.stdDevWinDiff)[0:4] + ','
		toWrite += str(t.normAvgWinDiff)[0:5] + ','
		toWrite += str(t.normStdDevWinDiff)[0:5] + ','
		toWrite += str(t.normAvgWinDiff / t.normStdDevWinDiff)[0:5] + '\n'
		f.write(toWrite)

def runStats(year, numWeeks, visual) :
	# league info - TODO: make this all command line
	league_id = 650880
	league = League(league_id, year)

	# RUN THE SCRIPT
	teams = getTeams(league)
	teams = setRecords(teams, numWeeks)
	teams = setRank(teams, numWeeks)
	teams = sortByRank(teams, numWeeks)
	teams = setStats(teams, numWeeks)

	# PRINT THE RESULTS
	print('NDL POWER RANKINGS THROUGH WEEK ' + str(numWeeks))
	for t in teams :
		name = t.name
		record = t.record[numWeeks-1]
		rank = str(t.rank[numWeeks-1])
		toPrint = rank + '. ' + name + ' ->'
		toPrint += ' ' + str(record[WINS]) + '-' + str(record[LOSSES]) + '-' + str(record[TIES]) + '.'
		toPrint += ' WDA: ' + str(t.avgWinDiff)[0:4] + ', WDSD: ' + str(t.stdDevWinDiff)[0:4] + '.' 
		toPrint += ' CM: ' + str(t.avgWinDiff / t.stdDevWinDiff)[0:4] + '.'
		print(toPrint)

	saveStats(teams, year, numWeeks)

	if visual :
		plotWinDifferential(teams)


def main(argv) :
	year = 0
	numWeeks = 0
	visual = False

	try :
		opts, args = getopt.getopt(argv, "hy:w:v", ["year=","week="])
	except :
			print(HELP_STRING)
			sys.exit(2)

	if len(opts) >= 2: 
		for opt, arg in opts :
			if opt.lower() == '-h' :
				print(HELP_STRING)
				sys.exit()
			elif opt.lower() in ('-y', '--year') :
				try :
					year = int(arg)
				except :
					print('Invalid year!\n')
					print(HELP_STRING)
					sys.exit(2)
			elif opt.lower() in ('-w', '--week') :
				try :
					numWeeks = int(arg)
				except :
					print('Invalid week!\n')
					print(HELP_STRING)
					sys.exit(2)
			elif opt.lower() == '-v' :
				visual = True
	else :
		print(HELP_STRING)

	runStats(year, numWeeks, visual)

if __name__ == "__main__":
   main(sys.argv[1:])





