# Conversational Agent.py
# A conversational "zoologist" simulation modelled loosely
# after Professor Tanimoto's implementation of J. Weizenbaum's ELIZA and Steve Irwin.
# This Python program explains data structures and algorithms in Steve's mannerisms.
# This version of the program runs under Python 3.x.

# Arvindram Krishnamoorthy
# (C) 2017.

from re import *   # Loads the regular expression module.
from random import randint

cache = ""
memCounter = 0

def introduce(): 
  return """Crikey Mate! Ma name's Ieve Sterwin; I was created by Arvindram Krishnamoorthy.
          You can contact him at karvi90@uw.edu but for now: 
          Which data structure or algorithm do ya wanna know about?"""

def respond(theInput):
  global cache
  global memCounter
  toRemember = ['map', 'maps', 'tree', 'trees', 'hash', 'hashes', 'set', 'sets', 'quicksort', 'greedy', 'iPhone']
  if match('bye', theInput):
      return 'Hooroo!'
  wordlist = split(' ',remove_punctuation(theInput))
  # undo any initial capitalization:
  for i in range(len(wordlist) - 1):
    wordlist[i] = wordlist[i].lower()
  intersection = list(set(wordlist) & set(toRemember))    
  if len(intersection) != 0:
    cache = intersection[0]
  memCounter = memCounter + 1 
  return respondHelper(theInput, wordlist)

def respondHelper(the_input, wordlist):
  # return str((memCounter))
  # return cache
  global cache
  global memCounter
  if (memCounter == 7 and cache != ''): 
    toReturn = "Before that mate, earlier, ya asked about " + cache + ", and ole Ieve's explanation might have been a bit bodgy. Ya reckon ya've grasped it?"
    cache = ""
    memCounter = 0
    return toReturn
  else:
      if wordlist[0]=='':
          global emptyResCount
          emptyResCount += 1
          return puntCustom(emptyResCount, EMPTYRES)
      if ('iphone' in wordlist):
          global iPhoneCount
          iPhoneCount += 1
          return puntCustom(iPhoneCount, IPHONE)
      if ('stock' in wordlist):
          return "Algorithmic tradin's ripper, mate! Stocks feature heavily in 'em. But back ta learnin'."
      if ('code' in wordlist):
          return "Codin's hard yakka, ya know -- but ya gotta start somewhere. Why don't we go over how ya'd implement a map?"
      if ('genius' in wordlist):
          return "Ya're fully sick if ya can bang out an advanced version o'these algorithms!"
      if ('design' in wordlist):
          return "My design is true blue, mate! Fair Dinkum. I'll teach ya all the structures ya need to pass your interviews."
      if ('map' in wordlist) or ('maps' in wordlist):
          return puntRandom(MAPS)
      if ('tree' in wordlist) or ('trees' in wordlist):
          return "Storin' hierarchies, mate? Piece a piss, trees'll come in handy."
      if (('hash' in wordlist) or ('hashes' in wordlist) and ('table' in wordlist)):
          return "Now deese are bewdy: O(1) lookups!"
      if 'quicksort' in wordlist:
          return "Divide-and-conquer and she'll be apples mate. Those're the guidelines ta code 'er."
      if 'greedy' in wordlist:
          global greedyCount
          greedyCount += 1
          return puntRandom(GREEDY)
      if ('big' in wordlist) and ('o' in wordlist):
          return "Strewth, ya gotta know about how long a method takes ta run and how much space it takes up!."
      if ('binary' in wordlist) and ('search' in wordlist):
          return "Ya'll be a little ripper if ya can eliminate half the input each time each go."    
      if ('set' in wordlist) or ('sets' in wordlist):
          return "This Sheila's the platybus' bill! Ya won't find any duplicates usin' these."
      if wordlist[0:3] == ['i', "don't", 'understand']:
          return "It's real simple, mate. Let me start from the top.'"
      return punt()

def agentName():
  return "Ieve"

def stringify(wordlist):
#    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)

punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")    

def remove_punctuation(text):
#    'Returns a string without any punctuation.'
    return sub(punctuation_pattern,'', text)

def wpred(w):
#    'Returns True if w is one of the question words.'
    return (w in ['when','why','where','how'])

def dpred(w):
#    'Returns True if w is an auxiliary verb.'
    return (w in ['do','can','should','would'])

punt_count = 1
emptyResCount = 1
iPhoneCount = 1

PUNTS = ['Ace!',
         'Crikey? Crikey means gee whizz, wow!',
         "Yeah, ain't that runtime a beaut?!",
         "Bogosort's a bloody mess, I'll tell ya 'hwat.",
         'Gimme a fair go?.',
         'I think your kangaroos loose in the top paddock.',
         "Remember: if ya don't optimize your algorithms, you're in for a dog's breakfast."]
         
EMPTYRES = ["Mate, I dunno what ta do if ya don't speak up!",
            "Ya havin' a chunder?",
            'Rock off then, you pong.'
            'Gonna do a Harold!']

IPHONE = ["I'm a simple bloke, I dunno about no iPhone.",
          'Av a go then, ya mug!',
          "Holey Doley, I'm gobsmacked. But let's get back ta trees, ya hear?"]

MAPS = ["Here's some good oil: if ya need two things saddled up together like a joey an her mama, use a map!",
            "Some seppos call maps 'dictionaries'.",
            'All the tall poppies can use maps to cache things.',
            'If ya really wanna up yourself, graduate from maps to AVL trees.']

GREEDY = ["Ya should be stoked to use greedy algorithms, whenever ya've ta make heaps'a optimis.",
            "Ya're quite the show pony, ain't cha?"]

def puntRandom(theList):
#    'Returns one from a list of default responses.'
    return theList[randint(0,(len(theList) - 1))]

def puntCustom(customPuntCount, theList):
#    'Returns one from a list of default responses.'
    customPuntCount += 1
    return theList[customPuntCount % len(theList)]

def punt():
#    'Returns one from a list of default responses.'
    global punt_count
    punt_count += 1
    return PUNTS[punt_count % len(PUNTS)]

