# Firstly we imported all the needed libraries,packages and modules
import sys            # The sys module provides information about constants, functions and methods of the Python interpreter
sys.path.insert(0, '/strategies.py')   
import random         #import random imports the random module, which contains a variety of things to do with random number 
                      #generation
import numpy as np    # we imported NumPy  in order to be able to perform a variety of mathematical operations on arrays
import matplotlib.pyplot as plt    # we imported Matplotlib as it helps to plot graphs
from strategies import Nice_guy, Bad_guy, Main_nice, Main_bad, Grudger, GoByMajority, Tit_for_tat, TitFor2Tats, SuspiciousTitForTat
                                   # we import these functions from our Strategies python file           
    
    
## Iterative Prisoner's Dilemma
# function that takes parameters/arguments
    #P1:First Player
    #P2:Second Player
    #turns:integer that represents number of turns
# return scores: 2D array of scores for both players in each iteration
def IPD(p1, p2, turns=1):
    scores = [[],[]]
    for i in range(0,turns):
        p1_move = p1.play() # 1 for cooperate or 0  for defect
        p2_move = p2.play()
        scores[0].append(p1.setScore(p1_move, p2_move)) # store in p1 history and return p1 score of this play
        scores[1].append(p2.setScore(p2_move, p1_move)) 
    return scores

#setScore function :calculates the score for each player in each iteration based on the movement of players in each iteration
#append:add items to the existing list , it does not return a new list of items but will modify the original list
#by adding the item to the end of the list


#def setScore(self, self_move, opp_move):
        #self.history.append(opp_move)
        #T=3
        #R=2
        #P=1 
        #S=0
        #newScore = 0
        #if (self_move == 1 and opp_move == 1): newScore = R
        #elif (self_move == 1 and opp_move == 0): newScore = S # loser
        #elif (self_move == 0 and opp_move == 1): newScore = T # winner
        #else: newScore = P
        #self.score += newScore
        #return newScore




# function that generates player by startegy name
# name: string represents the name of startegy
# we used lamda when we need a name for  funtion for a short period of time
def strategyGenerator(name):
    strategy = {
        'nice guy': (lambda: Nice_guy()),                    
        'bad guy': (lambda: Bad_guy()),
        'main nice': (lambda: Main_nice(random.randint(1, 49))),
        'main bad': (lambda: Main_bad(random.randint(51, 99) )),
        'grudger': (lambda: Grudger()),
        'go by majority': (lambda: GoByMajority()),
        'tit for tat': (lambda: Tit_for_tat()),
        'tit for 2 tats': (lambda: TitFor2Tats()),
        'suspicious tit for tat': (lambda: SuspiciousTitForTat())
    }
    # check if strategy name exists
    assert(name in strategy)
# if the assert condition is evaluated to be true so continue execution to the next step
    return strategy[name]()   #return a function 


    
# create an array of players
# playersNames: array of array; values of the array must be one of the startegies and the  player who choose 
#this strategy
# for example [['nice guy', 10], ['bad guy', 5]]
# shuffle: takes a sequence like list and organize the order of items , this method changes the original list and does not 
# return a new list
# return array of objects of type Player that 

def createPlayers(playersNames, shuffle=True):
    players = []
    for name, num in playersNames:
     
        for i in range(0,num):
            players.append(strategyGenerator(name))  #Loop on the strategies for each player to check how many players choose 
                                                     # a specific strategy
    
    # shuffle
    if(shuffle): random.shuffle(players)
    return players

# calculate alpha for each strategy according to its score
#alpha = 1 means that all players will change their strategies in each iteration.
#alpha = -1  alpha will be calculated for each strategy according to it's scores.
# calcAlpha args:
    #strategies: object {strategy_name: average_score}
# Function returns: 
    #{strategy_name: strategy_alpha}
def calcAlpha(strategies):
    strategiesName = [] # strategies names
    StrategyScore = []
    alphaDic = {}
    for s in strategies:
        strategiesName.append(s)
        StrategyScore.append(strategies[s])   #strategies => dictionary {strategy name key : avg. score value}.
    maxScore = max(StrategyScore)
    alpha = 1-(np.array(StrategyScore)/maxScore)
    for i in range(0,len(strategiesName)):
        alphaDic[strategiesName[i]]= StrategyScore[i]
    return alphaDic

# mode = 0 => (#players,#turns)
# mode = 1 => (#players,#players)
def MIPD(players, turns=1, mode=1):
    if(mode == 1): 
        scores = np.zeros([len(players),len(players)]) # to return the score of each player againt others
    else: 
        scores = np.zeros([len(players),turns])  # to return the score of player in each turn of play.
    for i in range(0,len(players)):
        for j in range(i+1,len(players)):
            _scores = IPD(players[i],players[j], turns)
            if(mode == 1):
                scores[i][j] = sum(_scores[0])
                scores[j][i] = sum(_scores[1])
            else:
                scores[i] = np.add(scores[i],_scores[0])
                scores[j] = np.add(scores[j],_scores[1])
    return scores 

# players: list of objects of type Player
# turns: int; number of turns of each match between two players
# iters: int; number of iterations
# alpha: float; the probabilty for a player to mutate his strategy
#   set alpha = 1 ;all players will change their startegies in each iteration
#   set alpha = -1 to let alpha be calculated for each strategy according to it's scores
# returns iterPlayers, iterScores, totals
#iterPlayers: 2D array of Player objects:
#       number of rows is the number of iterations
#       number of columns is the number of players
# iterScores: 2D array of float;
#       each row is a set of total scores of each player one iteration
# totals: array of float; number of elements = number of iterations
#       each element is the total score of all players in one iteration
def rMIPD(players, turns=1,iters=1, alpha=0.5):
    iterPlayers = [] # each row is a set of players in one iteration
    iterScores = [] # each row is a set of total scores of each player one iteration
    totals = [] # total scores for all players in each iteration
    # create id for each strategy
    idStrat = {} # { id : name }
    stratId = {} # { name : id }
    for p in players:
        stratId[p.getName()] = 0
    for i, strat in enumerate(stratId.keys()):
        stratId[strat] = i
        idStrat[i] = strat
    # start iterations
    for itr in range(0,iters):
        scores = MIPD(players, turns)
        scores = np.sum(scores,axis=1) # final score for each player
        iterScores.append(scores)
        strats = {} # total score for each strategy
        for i, player in enumerate(players):
            name = player.getName()
            if (name not in strats.keys()): strats[name] = [scores[i]]
            else: strats[name].append(scores[i])
        
         # average score for each strategy
        _totalAvg = 0
        _total = 0
        for strat in strats:
            _total = np.sum(strats[strat])
            avg = np.average(strats[strat])
            strats[strat] = avg # average score for each strategy
            _totalAvg += avg
        totals.append(_total)
        
    return iterPlayers, iterScores, totals