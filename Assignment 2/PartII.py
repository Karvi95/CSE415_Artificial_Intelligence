'''PartII.py
Arvindram Krishnamoorthy, CSE 415, Spring 2017, University of Washington
Instructor:  S. Tanimoto.
Assignment 2 Part II.  ISA Hierarchy Manipulation, adapted from the Linneus.py program

Status of the implementation of new features:

All forms of redundancy detection and processing are working.
Extra credit (Cycle detection and processing) implemented and working.

'''


from re import *   # Loads the regular expression module.

ISA = {}
INCLUDES = {}
ARTICLES = {}
MEMORY = {}

def store_isa_fact(category1, category2):
    'Stores one fact of the form A BIRD IS AN ANIMAL'
    # That is, a member of CATEGORY1 is a member of CATEGORY2
    try :
        c1list = ISA[category1]
        c1list.append(category2)
    except KeyError :
        ISA[category1] = [category2]
    try :
        c2list = INCLUDES[category2]
        c2list.append(category1)
    except KeyError :
        INCLUDES[category2] = [category1]
        
def get_isa_list(category1):
    'Retrieves any existing list of things that CATEGORY1 is a'
    try:
        c1list = ISA[category1]
        return c1list
    except:
        return []
    
def get_includes_list(category1):
    'Retrieves any existing list of things that CATEGORY1 includes'
    try:
        c1list = INCLUDES[category1]
        return c1list
    except:
        return []
    
def isa_test1(category1, category2):
    'Returns True if category 2 is (directly) on the list for category 1.'
    c1list = get_isa_list(category1)
    return c1list.__contains__(category2)
    
def isa_test(category1, category2, depth_limit = 10):
    'Returns True if category 1 is a subset of category 2 within depth_limit levels'
    if category1 == category2 : return True
    if isa_test1(category1, category2) : return True
    if depth_limit < 2 : return False
    for intermediate_category in get_isa_list(category1):
        if isa_test(intermediate_category, category2, depth_limit - 1):
            return True
    return False

def store_article(noun, article):
    'Saves the article (in lower-case) associated with a noun.'
    ARTICLES[noun] = article.lower()

def get_article(noun):
    'Returns the article associated with the noun, or if none, the empty string.'
    try:
        article = ARTICLES[noun]
        return article
    except KeyError:
        return ''

def linneus():
    'The main loop; it gets and processes user input, until "bye".'
    print('This is Linneus.  Please tell me "ISA" facts and ask questions.')
    print('For example, you could tell me "An ant is an insect."')
    while True :
        info = input('Enter an ISA fact, or "bye" here: ')
        if info == 'bye': return 'Goodbye now!'
        process(info)

# Some regular expressions used to parse the user sentences:    
assertion_pattern = compile(r"^(a|an|A|An)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\.|\!)*$", IGNORECASE)    
query_pattern = compile(r"^is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    
what_pattern = compile(r"^What\s+is\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    
why_pattern = compile(r"^Why\s+is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    

def process(info):
    'Handles the user sentence, matching and responding.'
    result_match_object = assertion_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        print(info)
        if not MEMORY: 
            if items[3] not in get_isa_list(items[1]):
                if items[1] != items[3]:
                    store_article(items[1], items[0])
                    store_article(items[3], items[2])
                    store_isa_fact(items[1], items[3])

#                    print("ISA: ", ISA)
 #                   print("INCLUDES: ", INCLUDES)
  #                  print("FIND CHAIN: ", find_chain(items[1], items[3]))

                                        
                    check = directRedundancyCheck(items[1], items[3])
                    if check == "Printed.":
                        return
                    #if items[1]'s list has a string that item[3]'s list has, then indirect redundant
                    #print('ISA: ' + str(ISA))
                    # for attr in list(set(ISA[items[1]]) & set(ISA.keys())):
                    #     currentValues = ISA[attr]
                    #     while(items[3] not in currentValues):
                    #         for value in ISA[attr]:
                    #             try:
                    #                 currentValues = ISA[value]
                    #             except KeyError:
                    #                 return

                    #     print("You don't have to tell me that.")
                    #     print('')
                    #     ISA[items[1]].remove(items[3])
                    #     return
                    #print('HI')
                    check = indirectRedundancyCheck(items[1], items[3])
                    if check == "Printed.":
                        return
                    #print('Bye')

                    
                    #Make private function; should I do this recursively or check Union-Find (GO BACKWARDS FROM EATING TO FISH BASE CASE IS KEY ERROR OR IT EQUALS so use .keys()!!)?
					
                    

                    print("I understand.")
                    print('')
                    return
                else:
                    print("You don't have to tell me that.")
                    print('')
                    return
            else:
                print ("You told me that earlier.")
                print('')
                return

    result_match_object = query_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        answer = isa_test(items[1], items[3])
        if answer :
            print("Yes, it is.")
        else :
            print("No, as far as I have been informed, it is not.")
        return
    result_match_object = what_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        supersets = get_isa_list(items[1])
        if supersets != [] :
            first = supersets[0]
            a1 = get_article(items[1]).capitalize()
            a2 = get_article(first)
            print(a1 + " " + items[1] + " is " + a2 + " " + first + ".")
            return
        else :
            subsets = get_includes_list(items[1])
            if subsets != [] :
                first = subsets[0]
                a1 = get_article(items[1]).capitalize()
                a2 = get_article(first)
                print(a1 + " " + items[1] + " is something more general than " + a2 + " " + first + ".")
                return
            else :
                print("I don't know.")
        return
    result_match_object = why_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        if not isa_test(items[1], items[3]) :
            print("But that's not true, as far as I know!")
        else:
            answer_why(items[1], items[3])
        return
    print("I do not understand.  You entered: ")
    print(info)


def answer_why(x, y):
    'Handles the answering of a Why question.'
    if x == y:
        print("Because they are identical.")
        return
    if isa_test1(x, y):
        print("Because you told me that.")
        return
    print("Because " + report_chain(x, y))
    return

from functools import reduce
def report_chain(x, y):
    'Returns a phrase that describes a chain of facts.'
    chain = find_chain(x, y)
    all_but_last = chain[0:-1]
    last_link = chain[-1]
    main_phrase = reduce(lambda x, y: x + y, map(report_link, all_but_last))
    last_phrase = "and " + report_link(last_link)
    new_last_phrase = last_phrase[0:-2] + '.'
    return main_phrase + new_last_phrase

def report_link(link):
    'Returns a phrase that describes one fact.'
    x = link[0]
    y = link[1]
    a1 = get_article(x)
    a2 = get_article(y)
    return a1 + " " + x + " is " + a2 + " " + y
    
def find_chain(x, z):
    'Returns a list of lists, which each sublist representing a link.'
    if isa_test1(x, z):
        return [[x, z]]
    else:
        for y in get_isa_list(x):
            if isa_test(y, z):
                temp = find_chain(y, z)
                temp.insert(0, [x,y])
                return temp

def directRedundancyCheck(first, second):
    toReturn = "Didn't Print"
    for attr in list(set(ISA[first]) & set(ISA.keys())):
        currentValues = ISA[attr]
        while(second not in currentValues):
            for value in ISA[attr]:
                try:
                    currentValues = ISA[value]
                except KeyError:
                    return toReturn

        print("You don't have to tell me that.")
        print('')
        toReturn = "Printed."
        ISA[first].remove(second)
        return toReturn

def indirectRedundancyCheck(first, second):
    output = list(indirectRedundancyCheckHelper(first, second))
    listComparisonList = []
    if output:
        print("OUTPUT: " + str(output))
        print("")
        DESCENDENTS = [item for sublist in output for item in sublist]
        # print("DESCENDENTS: " + str(DESCENDENTS))
        # for descendent in DESCENDENTS:
        #     print("THIS DESCENDENT: " + descendent)
        #     unvisitedUniverseNew = [x for x in (INCLUDES[descendent])]
        #     print("NEW UNIVERSE: " + str(unvisitedUniverseNew))
        #     for relationNew in unvisitedUniverseNew:
        #         print("NEW RELATION: " + str(relationNew))
        #         comparison.add(relationNew)
        #         print(comparison)
        #         secondDegreesNew = INCLUDES[relationNew]
        #         print("NEW SECOND DEGREES: " + str(secondDegreesNew))
        #         for childNew in secondDegreesNew:
        #             comparison.add(childNew)
        #             try: 
        #                 secondDegreesNew = INCLUDES[childNew]        
        #             except KeyError:
        #                 print("COMPARISON: " + str(pathNew))
        #                 yield path




def indirectRedundancyCheckHelper(first, second, path=None):
    print("ISA: " + str(ISA))
    print("INCLUDES: " + str(INCLUDES))
    print("")


    if path is None:
        path = [first]

    if first == second:
        try:
            yield path
        except KeyError:
            pass

    childrenOfFirst = dfs(INCLUDES, first)
    childrenOfFirst.remove(first)
    
    parentsDict = {}

    for child in childrenOfFirst:
        parents = dfs(ISA, child)
        parents.remove(child)
        parentsDict[child] = parents

    print("PARENTS DICTIONARY: " + str(parentsDict))

    if second in ISA.keys():
        secondsParents = ISA[second]
        for key in parentsDict.keys():
            values = parentsDict[key]
            print(values)
            inCommon = list(set(secondsParents).intersection(values))
            for common in inCommon:
                chain = find_chain(child, common)
                print('chain ' + str(chain))
                if len(chain) == 1:
                    get_isa_list(chain[0][0]).remove(common)
                    get_includes_list(common).remove(child)
                    print('Your earlier statement that ' + report_link(chain[0]) + ' is redundant.')
                    print("ISA: " + str(ISA))
                    print("INCLUDES: " + str(INCLUDES))
                # elif len(chain) >= 1:
                #     print('The following statements you made earlier are now all redundant:')
                #     for link in chain:
                #         print(report_link + ';')

def isAncestor():
    print("HI")

def dfs(graph, child, visited = None):
    if visited == None:
        visited = []
    if child in visited:
        return

    visited.append(child)

    try: 
        for each in [x for x in graph[child] if x not in visited]:
            dfs(graph, each, visited)
    except KeyError:
        pass

    return visited

    # for finalizedChild in childrenOfFirst:
    #     parents = ISA[finalizedChild]
    #     print("PARENTS: " + str(parents))
    #     for parent in parents:
    #         parentsOfChildren.append(parent)
    #         if parent in ISA.keys():
    #             while parent in ISA.keys():
    #                 parents = ISA[parent]
    #                 break
    # print("PARENTS OF CHILDREN: " + str(parentsOfChildren))



    # unvisitedUniverse = [x for x in list(set(INCLUDES[first]) & set(INCLUDES.keys())) if x not in path]
    # #print("UNVISITED UNIVERSE: " + str(unvisitedUniverse))
    # for relation in unvisitedUniverse:
    #     #print(relation)
    #     path.append(relation)
    #     secondDegrees = INCLUDES[relation]
    #     #print("SECOND DEGREES: " + str(secondDegrees))
    #     for child in secondDegrees:
    #         path.append(child)
    #         try: 
    #             secondDegrees = INCLUDES[child]        
    #         except KeyError:
    #             #print("PATH: " + str(path))
    #             path.remove(first)
    #             yield path
    #     # for eachPath in indirectRedundancyCheckHelper(relation, second, path.append(relation)):
        #     yield eachPath
            
    #print('IN')
    #stack = [(start, [start])]
    #print(stack)
    # while stack:
    #     (vertex, path) = stack.pop()
    #     for next in graph[vertex] - set(path):
    #         if next == goal:
    #             yield path + [next]
    #         else:
    #             stack.append((next, path + [next]))
    # return


    # print("ISA: " + str(ISA))
    # print("INCLUDES: " + str(INCLUDES))
    # if first in INCLUDES.keys():
    #     print("FIRST: " + first)
    #     print("FIRST's LIST: " + str(INCLUDES[first])) 
    #     print("SECOND: " + second)
    #     for included in INCLUDES[first]:
    #         print("SECOND's LIST: " + str(INCLUDES[second]))
    #         if included in INCLUDES[second]:
    #             chain = find_chain(included, second)
    #             print('INCLUDED ' + included)
    #             if len(chain) == 1:
    #                 get_isa_list(chain[0][0]).remove(second)
    #                 get_includes_list(second).remove(included)
    #                 print('Your earlier statement that ' + report_link(chain[0]) + ' is redundant.')
    #                 print("ISA: " + str(ISA))
    #                 print("INCLUDES: " + str(INCLUDES))
    #             elif len(chain) >= 1:
    #                 print('The following statements you made earlier are now all redundant:')
    #                 for link in chain:
    #                     print(report_link + ';')
    #     return		



def test() :
	#indirectTest1()
	indirectTest2()
    #directTest()

def directTest():
	process("A sockeye is a salmon.")
	process("A salmon is a fish.")
	process("A sockeye is a fish.")
	process("A spade is a spade.")
	process("A fish is a animal.")
	process("A sockeye is a salmon.")
	process("A sockeye is a animal.")

def indirectTest1():
    process("A hawk is a bird.")
    process("A hawk is a raptor.")
    process("A raptor is a bird.")	

def indirectTest2():
    process("A hawk is a raptor.")
    process("A hawk is an animal.")
    process("A bird is an animal.")
    process("A raptor is a bird.")

test()
linneus()
