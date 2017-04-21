# Astar.py, April 2017 
# Based on ItrDFS.py, Ver 0.3, April 11, 2017.

# A* Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowerOfHanoi.py example file for details.
# Examples of Usage:

# python3 AStar.py EightPuzzleWithHeuristics h_manhattan

import sys
from Queue import PriorityQueue

# DO NOT CHANGE THIS SECTION 
if sys.argv==[''] or len(sys.argv)<2:
    import EightPuzzleWithHeuristics as Problem
    heuristics = lambda s: Problem.HEURISTICS['h_manhattan'](s)
    puzzleState = importlib.import_module(sys.argv[3])
else:
    import importlib
    Problem = importlib.import_module(sys.argv[1])
    heuristics = lambda s: Problem.HEURISTICS[sys.argv[2]](s)
    # puzzleState = importlib.import_module(sys.argv[3])

print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}

# DO NOT CHANGE THIS SECTION
def runAStar():
    #initial_state = Problem.CREATE_INITIAL_STATE(keyVal)
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    path, name = AStar(initial_state)
    print(str(COUNT)+" states examined.")
    return path, name

# A star search algorithm
# TODO: finish A star implementation
def AStar(initial_state):
    global COUNT, BACKLINKS
    # TODO: initialze and put first state into 
    # priority queue with respective priority
    # add any auxiliary data structures as needed
    OPEN = PriorityQueue()
    CLOSED = []
    BACKLINKS[initial_state] = -1
    stateTuple = (0, initial_state) 
    OPEN.put(stateTuple)

    stateToCostDict = {}

    while not OPEN.empty():
        S = OPEN.get()
        #print("S is: " + str(type(S)))
        costValue = int(S[0])
        #print("costValue: " + str(type(costValue)))
        S = S[1]
        #print("NOW, S is: " + str(type(S)))
        stateToCostDict[S] = costValue
        #print("COST IN DICTIONARY: " + str(stateToCostDict[S]))
        while S in CLOSED:
            S = OPEN.get()
            #print("Closed S is: " + str(type(S)))
            S = S[1]    
        CLOSED.append(S)
        

        # DO NOT CHANGE THIS SECTION: begining 
        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME
        # DO NOT CHANGE THIS SECTION: end


        # TODO: finish A* implementation
        COUNT += 1
        # if (COUNT % 32)==0:
        #     print(".")
        # if (COUNT % 128)==0:
        #     print("COUNT = "+str(COUNT))
        #     print("len(OPEN)="+str(len(OPEN)))
        #     print("len(CLOSED)="+str(len(CLOSED)))

        for op in Problem.OPERATORS:
            #Optionally uncomment the following when debugging
            #a new problem formulation.
            #print("Trying operator: " + op.name)
            #print("Current S: " + str(S))
            if op.precond(S):
                #print("SATISFIED")
                new_state = op.state_transf(S)
                #print("NEW STATE: " + str(new_state))
                if not new_state in CLOSED:
                    newHeuristic = costValue + heuristics(new_state)
                    if not new_state in stateToCostDict or stateToCostDict[new_state] >  newHeuristic:
                        stateTuple = (newHeuristic, new_state)
                        stateToCostDict[new_state] = newHeuristic
                        OPEN.put(stateTuple)
                        BACKLINKS[new_state] = S

# DO NOT CHANGE
def backtrace(S):
    global BACKLINKS
    path = []
    while not S == -1:
        path.append(S)
        S = BACKLINKS[S]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(s)
    print("\nPath length = "+str(len(path)-1))
    return path    

if __name__=='__main__':
    path, name = runAStar()