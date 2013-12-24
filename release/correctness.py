# Command line arguments same as measuring.py

import random
import sys
import trie
import robertperry
import generate

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




trie = generate.genlexicon()

alg = robertperry.robertperry(trie)

wlist = []
tword = sys.argv[2]

if sys.argv[1] == 'replace':
    wlist = replace(tword, int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
elif sys.argv[1] == 'add':
    wlist = add(tword, int(sys.argv[3]), int(sys.argv[4]))
elif sys.argv[1] == 'delete':
    wlist = delete(tword, int(sys.argv[3]), int(sys.argv[4]))

autocounter = 0
candcounter = 0
nocounter = 0

for x in wlist:
    cands = alg.findCandidates(x)
    print(x)
    if len(cands) > 0:
        for y in cands:
            if type(y[0]) != tuple:
                if y[0].word == tword:
                    candcounter += 1
        if type(cands[0][0]) != tuple:
            if tword == cands[0][0].word:
                autocounter += 1
    else:
        nocounter += 1

print(tword)

print(str(len(wlist)))

print('times autocorrected to original word: ' + str(autocounter) + '    percentage: ' +str((autocounter/len(wlist))*100)+'%')
print('times candidates contained original word: '  + str(candcounter) + '    percentage: ' +str((candcounter/len(wlist))*100)+'%')
print('times no candidates were found: '  + str(nocounter) + '    percentage: ' +str((nocounter/len(wlist))*100)+'%')





