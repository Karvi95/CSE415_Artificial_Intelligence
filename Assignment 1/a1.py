# HW 1, part a
# Number 1
def four_x_cubed_plus_1(x):
  return (4 * (x * x * x)) + 1


# Number 2
def mystery_code(plaintext, n):
  key = 'abcdefghijklmnopqrstuvwxyz'
  result = ''
  n -= 2

  for l in plaintext: 
    checker = l.lower()
    try:
        i = (key.index(checker) + n) % 26
        encoded = key[i]
        if (l.isupper()):
          encoded = encoded.upper()
        result += encoded
    except ValueError:
        result += l
  return result.swapcase()

# Number 3
# Create a function called "chunks" with two arguments, l and n:
def quintuples(l):
  return list(quintuplesHelper(l))
  
def quintuplesHelper(l):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), 5):
        # Create an index range for l of n items:
        yield l[i:i+5]

#Number 4
def past_tense(list):
  returnList = []
  for item in list:
    if (item.endswith('y') and item[len(item) - 2] not in "aeiouy"):
      returnList.append(item[0:(len(item) - 1)] + 'ied')
    elif (item in ['have', 'be', 'eat', 'go']):
      irregulars = {'have': 'had', 'be':'been', 'eat': 'ate', 'go': 'went'}
      returnList.append(irregulars[item])
    elif ((item[len(item) - 3] not in "aeiouy") and (item[len(item) - 2] in "aeiouy") and (item[len(item) - 1] not in "aeiouyw")):
      repeater = item[len(item) - 1]
      returnList.append(item + repeater + 'ed')
    elif (item[len(item) - 1] == 'e'):
      returnList.append(item + 'd')
    else:
      returnList.append(item + 'ed')
  return returnList
