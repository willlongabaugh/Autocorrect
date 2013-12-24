# Command Line Argument Key:                                                                            #
#                                                                                                       #
# replace:   replace,   word,   # errors,   error type (1-3),   number of words                         #
# error type:   1 = concentrate on neighbors,   2 = non-neighbors,   3 = everything                     #
#                                                                                                       #
# delete:   delete,   word,   # errors,   number of words                                               #
#                                                                                                       #
# add:   add,   word,   # errors,   number of words                                                     #
#-------------------------------------------------------------------------------------------------------#


import timeit
import sys

test = ''

if sys.argv[1] == 'replace':
    test = sys.argv[1]+"('"+sys.argv[2]+"', "+sys.argv[3]+', '+sys.argv[4]+', '+sys.argv[5]+')'
else:
    test = sys.argv[1]+"('"+sys.argv[2]+"', "+sys.argv[3]+', '+sys.argv[4]+')'

print(test)

setup = '''

import random

neighbors = { 'a' : ['q', 'w', 's', 'z'] , 'b' : ['v', 'g', 'h', 'j', 'n'] , 'c' : ['x', 'd', 'f', 'g', 'v'] , 'd' : ['z', 'x', 'c', 'f', 'r', 'e', 's'] , 'e' : ['w', 's', 'd', 'r'] , 'f' : ['x', 'c' 'v', 'g', 't', 'r', 'd'] , 'g' : ['c', 'v', 'b', 'h', 'y', 't', 'f'], 'h' : ['v', 'b', 'n', 'j', 'u', 'y', 'g'] , 'i' : ['u', 'j', 'k', 'o'] , 'j' : ['b', 'n', 'm', 'k', 'i', 'u', 'h'], 'k' : ['n', 'm', 'l', 'o', 'i', 'j'], 'l' : ['m', 'k', 'o', 'p'], 'm' : ['n', 'j', 'k', 'l'] , 'n' : ['b', 'h', 'j', 'k', 'm'] , 'o' : ['i', 'k', 'l', 'p'] , 'p' : ['o', 'l'] , 'q' : ['a', 'w'] , 'r' : ['e', 'd', 'f', 't'] , 's' : ['a', 'z', 'x', 'd', 'e', 'w'], 'z' : ['a', 's', 'd', 'x'], 'y' : ['t', 'g', 'h', 'u'] , 'x' : ['z', 's', 'd', 'f', 'c'] , 'w' : ['q', 'a', 's', 'e'] , 'v' : ['c', 'f', 'g', 'h', 'b'] , 'u' : ['y', 'h', 'j', 'i'] , 't' : ['r', 'f', 'g', 'y'] , "'" : []}

def replace(w, error, nchoice, number):
    
    wlist = []
    print('number: ' + str(number))
    
    if nchoice == 3:
        for z in range(0,number):
            word = w
            ichoices = []
            for x in range(0,error):
                i = random.randint(0,len(w)-1)
                while i in ichoices:
                    i = random.randint(0,len(w)-1)
                ichoices.append(i)
                ci = random.randint(97,122)
                c = chr(ci)
                while c == w[i]:
                    ci = random.randint(97,122)
                    c = chr(ci)
                word = word[:i]+c+word[i+1:]
            wlist.append(word)
    
    elif nchoice == 2:
        for z in range(0, number):
            word = w
            ichoices = []
            for x in range(0, error):
                i = random.randint(0,len(w)-1)
                while i in ichoices:
                    i = random.randint(0,len(w)-1)
                ichoices.append(i)
                ci = random.randint(97,122)
                c = chr(ci)
                while c in neighbors[w[i]]:
                    ci = random.randint(97,122)
                    c = chr(ci)
                word = word[:i]+c+word[i+1:]
            wlist.append(word)
    
    elif nchoice == 1:
        for z in range(0, number):
            word = w
            ichoices = []
            for x in range(0, error):
                i = random.randint(0,len(w)-1)
                while i in ichoices:
                    i = random.randint(0,len(w)-1)
                ichoices.append(i)
                c = random.choice(neighbors[w[i]])
                word = word[:i]+c+word[i+1:]
            wlist.append(word)
    
    return wlist




def add(w, error, number):
    wlist = []
    for z in range(0,number):
        word = w
        for x in range(0, error):
            i = random.randint(0,len(w))
            ci = random.randint(97,122)
            c = chr(ci)
            word = word[:i]+c+word[i:]
        wlist.append(word)
    return wlist




def delete(w, error, number):
    wlist = []
    for z in range(0,number):
        word = w
        for x in range(0, error):
            i = random.randint(0,len(word)-1)
            word = word[:i]+word[i+1:]
        wlist.append(word)
    return wlist


import trie
import algorithm2
import generate

trie = generate.genlexicon()

alg = algorithm2.algorithm(trie)

wlist = %s

''' % test

stmt = '''
for x in wlist:
    alg.findCandidates(x)
'''

x = 1

if sys.argv[1] == 'replace':
    x = int(sys.argv[5])
else:
    x = int(sys.argv[4])

time = timeit.Timer(stmt, setup).timeit(1)
avg = time/x

print()
print('time: ' + str(time) + '   avg time per search: ' + str(avg))






