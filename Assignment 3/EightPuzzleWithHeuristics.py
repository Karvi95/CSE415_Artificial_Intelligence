'''PartII-4.py
Arvindram Krishnamoorthy (karvi90), CSE 415, Spring 2017, University of Washington
A QUIET Solving Tool problem formulation.
QUIET = Quetzal User Intelligence Enhancing Technology.
The XML-like tags used here serve to identify key sections of this 
problem formulation.  

This is the updated version with Heuristics.

CAPITALIZED constructs are generally present in any problem
formulation and therefore need to be spelled exactly the way they are.
Other globals begin with a capital letter but otherwise are lower
case or camel case.
'''

#<IMPORTS>
import math
#</IMPORTS>

#<METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Basic Eight Puzzle"
PROBLEM_VERSION = "1.1"
PROBLEM_AUTHORS = ['A. Krishnamoorthy']
PROBLEM_CREATION_DATE = "14-APR-2017"
PROBLEM_DESC=\
'''This formulation of the Basic Eight Puzzle problem uses generic
Python 3 constructs and has been tested with Python 3.4.
It is designed to work according to the QUIET tools interface, Version 0.2.
'''
#</METADATA>

#<COMMON_CODE>

def can_move(s,From,To):
  '''Tests whether it's legal to move a tile in state s
  from the From place to the To slot.'''
  try:
      xDistance = abs((From % 3) - (To % 3))
      yDistance = abs((From / 3) - (To / 3))
      if s.d[From] == 0 or s.d[To] != 0: 
        return False
      if (xDistance == 1 and yDistance == 0) or (yDistance == 1 and xDistance == 0): 
        return True
      return False # 
  except (Exception) as e:
      print(e)

def move(s,From,To):
  '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the topmost disk
     from the From peg to the To peg.'''
  news = s.__copy__() # start with a deep copy.
  d2 = news.d # grab the new state's dictionary.
  d2[To] = d2[From] # make the move
  d2[From] = 0 # make from the new empty
  return news # return new state

def goal_test(s):
  '''If the first two pegs are empty, then s is a goal state.'''
  return s.d == goalList# all(s.d[i] < s.d[i+1] for i in xrange(len(s.d)-1))

def goal_message(s):
  return "The sequence is in strictly ascending order!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)
  
def h_euclidean(s): 
    euclideanDist = 0
    for i in s.d:
      currIndex = s.d.index(i)
      gIndex = goalList.index(i)
      euclideanDist += math.sqrt((((currIndex / 3) - (gIndex / 3)) ** 2) + (((currIndex % 3) - (gIndex % 3)) ** 2))
    return euclideanDist
  
def h_hamming(s): 
    count = 0
    for i in range(N_pieces):
      if s.d[i] != i:
          count += 1
    return count

def h_manhattan(s):
    manhattanDist = 0
    for i in s.d:
      currIndex = s.d.index(i)
      gIndex = goalList.index(i)
      manhattanDist += abs((currIndex / 3) - (gIndex / 3)) + abs((currIndex % 3) - (gIndex % 3))
    return manhattanDist
  
def h_custom(s):
    return ((h_hamming(s) + h_euclidean(s) + h_manhattan(s)) / 3)
    # customDistance = 0
    # for i in s:
    #   if s[i] != i:  
    #     currIndex = s.index(i)
    #     gIndex = goalList.index(i)
    #     euclidean = sqrt((((currIndex / 3) - (gIndex / 3)) ** 2) + (((currIndex % 3) - (gIndex % 3)) ** 2))
    #     manhattan = abs((currIndex / 3) - (gIndex / 3)) + abs((currIndex % 3) - (gIndex % 3))
    #     aNum = 2
    #     if i != 0
    #       if i == 4:
    #         aNum = 4
    #       elif i % 2 == 0:
    #         aNum = 2
    #       elif i % 2 == 1:
    #         aNum = 3
    #     a = math.ciel(aNum / N_pieces)
    #     customDistance += abs(((euclidean * a) + (manhattan * (1 - a))))
    # return math.floor((math.min(  math.max( (N_pieces % h_euclidean(s)), customDistance ) , math.max( (N_pieces % h_hamming(s)), customDistance )  ) + math.max(  math.min( (N_pieces % h_euclidean(s)), customDistance ) , math.min( (N_pieces % h_hamming(s)), customDistance )  )) / 2)


#</COMMON_CODE>

#<COMMON_DATA>
N_pieces = 9
#</COMMON_DATA>

#<STATE>
class State():
  def __init__(self, d):
    self.d = d

  def __str__(self):
    # Produces a brief textual description of a state.
    splitter = "\n"
    for i in range(9):
        splitter += str(self.d[i]) + " "
        if i % 3 == 2:
            splitter += "\n"
    return splitter

  def __eq__(self, s2):
    if not (type(self)==type(s2)): return False
    d1 = self.d; d2 = s2.d
    return d1 == d2

  def __hash__(self):
    return (str(self)).__hash__()

  def __copy__(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State([])
    for i in self.d:
      news.d.append(i)
    return news

  def __lt__(self, rhs):
    return False

  def __gt__(self, rhs):
    return self[0] > rhs[0]

  def __le__(self, rhs):
    return self[0] <= rhs[0]

  def __ge__(self, rhs):
    return self[0] >= rhs[0]
#</STATE>

#<INITIAL_STATE>
p0 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
p1 = [1, 0, 2, 3, 4, 5, 6, 7, 8]
p2 = [3, 1, 2, 4, 0, 5, 6, 7, 8]
p4 = [1, 4, 2, 3, 7, 0, 6, 8, 5]


p10 = [4, 5, 0, 1, 2, 3, 6, 7, 8]
p12 = [3, 1, 2, 6, 8, 7, 5, 4, 0]
p14 = [4, 5, 0, 1, 2, 8, 3, 7, 6]
p16 = [0, 8, 2, 1, 7, 4, 3, 6, 5]

INITIAL_STATE = State(p16)
CREATE_INITIAL_STATE = lambda: INITIAL_STATE
#</INITIAL_STATE>

#<GOAL_STATE>
goalList = list(range(N_pieces))
#</GOAL_STATE>

#<OPERATORS>
puzzleCombinations = [(x, y) for x in goalList for y in goalList if x != y]
OPERATORS = [Operator("Move piece from "+ str(p) + " to " + str(q),
                      lambda s,p1=p,q1=q: can_move(s,p1,q1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,p1=p,q1=q: move(s,p1,q1))
             for (p,q) in puzzleCombinations]
#</OPERATORS>

#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<HEURISTICS>
HEURISTICS = {'h_euclidean': h_euclidean, 'h_hamming': h_hamming, 'h_manhattan': h_manhattan, 'h_custom': h_custom} 
#</HEURISTICS>