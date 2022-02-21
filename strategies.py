import random

class Player(object):
    """A class for a player in the game.""" 
    
    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        self.score = 0
        self.history = []
        self.name = 'Player'

    def getHistory(self):
        return self.history

    def getName(self):
        return self.name
    
    def setScore(self, self_move, opp_move):
        self.history.append(opp_move)
        T=3
        R=2
        P=1 
        S=0
        newScore = 0
        if (self_move == 1 and opp_move == 1): newScore = R
        elif (self_move == 1 and opp_move == 0): newScore = S # loser
        elif (self_move == 0 and opp_move == 1): newScore = T # winner
        else: newScore = P
        self.score += newScore
        return newScore
    
    def play(self):
        # To be overrided in the next classes
        return None

class Nice_guy(Player):
    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        Player.__init__(self)
        self.name = 'nice guy'
        
    def play(self):
        return 1


class Bad_guy(Player):
    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        Player.__init__(self)
        self.name = 'bad guy'
    
    def play(self):
        return 0
    
#       """A player starts by cooperating and then repeat the last movement of the opponent."""


class Tit_for_tat(Player):
    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        Player.__init__(self)
        self.name = 'tit for tat'
    
    def play(self):
        if(len(self.history) == 0):
            return 1
        else:
            return self.history[-1]


class TitFor2Tats(Player):
    """A player starts by cooperating and then defects only after two defects by opponent."""

    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        Player.__init__(self)
        self.name = 'tit for 2 tats'
    
    def play(self):
        if self.history[-2:] == [0, 0]:
            return 0
        else:
            return 1

class SuspiciousTitForTat(Player):
    """A player start with defect then imitates the opponent's previous move thereafter. """
    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        Player.__init__(self)
        self.name = 'suspicious Tit For Tat'

    def play(self):
        if (len(self.history) == 0):
            return 0
        else:
            return self.history[-1]

class Main_bad(Player):
    """randomly defect k\% of the times and cooperate 100-k%, k>50"""
    def __init__(self,K):
        Player.__init__(self)
        self.name = 'main bad'
        self.K = K/10

    def play(self):
        number = random.randint(1,10)
        if number >= self.K:
            return 1
        else:
            return 0

class Main_nice(Player):
    """randomly defect k\% of the times and cooperate 100-k%, k<50"""
    def __init__(self,K):
        Player.__init__(self)
        self.name = 'main nice'
        self.K = K/10

    def play(self):
        number = random.randint(1,10)
        if number >= self.K:
            return 1
        else:
            return 0

class Grudger(Player):
    """A player starts by cooperating however will defect if
    at any point the opponent has defected."""
    def __init__(self):
        Player.__init__(self)
        self.name = 'grudger'

    def play(self):
        if len(self.history)==0:
            return 1
        else:
            if 0 in self.history:
                return 0
            else:
                return 1  

class GoByMajority(Player):
    """A player examines the history of the opponent:
    if the opponent has more defections than cooperations then the player defects."""
    def __init__(self):
        Player.__init__(self)
        self.name = 'go by majority'
    def play(self):
        if sum([s == 0 for s in self.history]) > sum([s == 1 for s in self.history]):
            return 0
        return 1
