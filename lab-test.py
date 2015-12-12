def codes(string):
   '''prints the ASCII character for every character in given string'''
   #ASC = [print(ord(x)) for x in string]
   
codes('cat') # 99 97 116

def codesLoop(string):
   '''prints the ASCII character for every character in given string'''
   for asciiChar in string:
        print(ord(asciiChar))
        
# codesLoop('cat') # 99 97 116
# print(len(None))

# from pprint import pprint
# s = "A man a plan a canal Panama"
# print (s[::-1])
# x = 4
# pprint(x, indent = 2)

def multlists(listA, listB):
    '''takes two lists and returns a list of all elements seuqentially
    combined into 2-tuple pairs
    '''
    output = []
    # crude way
    # for first in listA:
    #     for second in listB:
    #         output.append((first, second))
    output = [(first, second) for first in listA for second in listB]
    return output
            

# test
# expect: [(1, 'a'), (1, 'b'), (1, 'c'), (2, 'a'), (2, 'b'), (2, 'c')]
print (multlists([1], ['a','b','c','d']))

output = [if not(sevenFactor % 7): sevenFactor for sevenFactor 
in range(1,100)]
print(output)