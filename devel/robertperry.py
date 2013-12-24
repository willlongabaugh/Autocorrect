import trie
import itertools

# Co-written by Colin Robert White and Will Perry Longabaugh

# hard-code close neighbors to letters
neighbors = { 'a' : ['a', 'q', 'w', 's', 'z'] , 'b' : ['b', 'v', 'g', 'h', 'j', 'n'] , 'c' : ['c', 'x', 'd', 'f', 'g', 'v'] , 'd' : ['d', 'z', 'x', 'c', 'f', 'r', 'e', 's'] , 'e' : ['e', 'w', 's', 'd', 'r'] , 'f' : ['f', 'x', 'c' 'v', 'g', 't', 'r', 'd'] , 'g' : ['g', 'c', 'v', 'b', 'h', 'y', 't', 'f'], 'h' : ['h', 'v', 'b', 'n', 'j', 'u', 'y', 'g'] , 'i' : ['i', 'u', 'j', 'k', 'o'] , 'j' : ['j', 'b', 'n', 'm', 'k', 'i', 'u', 'h'], 'k' : ['k', 'n', 'm', 'l', 'o', 'i', 'j'], 'l' : ['l', 'm', 'k', 'o', 'p'], 'm' : ['m', 'n', 'j', 'k', 'l'] , 'n' : ['n', 'b', 'h', 'j', 'k', 'm'] , 'o' : ['o', 'i', 'k', 'l', 'p'] , 'p' : ['p', 'o', 'l'] , 'q' : ['q', 'a', 'w'] , 'r' : ['r', 'e', 'd', 'f', 't'] , 's' : ['s', 'a', 'z', 'x', 'd', 'e', 'w'], 'z' : ['z', 'a', 's', 'd', 'x'], 'y' : ['y', 't', 'g', 'h', 'u'] , 'x' : ['x', 'z', 's', 'd', 'f', 'c'] , 'w' : ['w', 'q', 'a', 's', 'e'] , 'v' : ['v', 'c', 'f', 'g', 'h', 'b'] , 'u' : ['u', 'y', 'h', 'j', 'i'] , 't' : ['t', 'r', 'f', 'g', 'y'] , "'" : []}

bottomRow = {'z', 'x', 'c', 'v', 'b', 'n', 'm'}

class robertperry():
    def __init__(self, trie):
        self.trie = trie
        self.candidates = []
        self.size = 4

        # our algorithm starts at the root and recurs for every type of error that can happen, until it reaches the current error cap (1 to 3)

    #----------this method is called when the error cap has been reached
    def complete(self, w, index, node, score):
        for y in range(index, len(w)-1): #tack on all remaining letters, and see if it makes a word
            if node.children.get(w[y+1]) != None:
                node = node.children.get(w[y+1])
            else: #if it is not a valid node, return
                return
        if node.end: #if it is a valid word, calculate the score and see if it's in the top four so far
            score = score * (1-node.freq) #score is based on the type of error (add, replace, delete, transpose etc), and frequency
            double = False
            for x in self.candidates: #check if the word is already in the list of candidates 
                try:
                    if x[0].word == node.word:   #(this is because in a few small cases, the same word can make it here twice)
                        double = True
                except AttributeError:
                    pass

            if not double:   #if the word is not already in the list of candidates
                self.candidates.append((node, score))
                self.candidates.sort(key = lambda x : x[1]) #sort the list of candidates by score
                if len(self.candidates) > self.size:    #make sure candidates only contains the top four words
                    self.candidates.pop()


    #------------Main recursion method
    #a given node in the trie recurs for all errors that can happen
    def searchDown(self, w, index, node, neighbor, err, error, score):
        global searchDownCount
        searchDownCount = searchDownCount + 1 #count the number of times we recur

        if searchDownCount > 15000: #experimentally determined cap that is fast and has good performance
            return


        if err < error:  #if we haven't reached the error cap yet
            if index < len(w): #if we still have enough space left to add a letter at the end
                for y in range(97,123): 
                    x = chr(y)
                    if node.children.get(x) != None:
                        self.searchDown(w, index, node.children.get(x), neighbor, err+1, error, score+1.05) # adding a letter
                x = "'"
                if node.children.get(x) != None:
                    self.searchDown(w, index, node.children.get(x), neighbor, err+1, error, score+.75) # adding apostrophe 

                if index+1 < len(w): #if we have enough space to replace a letter (or recur without errors)
                    if node.children.get(w[index+1]) != None:
                        self.searchDown(w, index+1, node.children.get(w[index+1]), neighbor, err, error, score)  #recurring without errors

                    if neighbor == True:   #recur on errors from neighboring keys first
                        for x in neighbors[w[index+1]]:
                            if node.children.get(x) != None:
                                self.searchDown(w, index+1, node.children.get(x), True, err+1, error,score+1)   #replace with neighbor

                    else:                  #then recur on errors from non-neighbors
                        for y in range(97,123):
                            x = chr(y)
                            if node.children.get(x) != None:
                                self.searchDown(w, index+1, node.children.get(x), False, err+1, error, score+1.15) # replacing non neighbor
                        x = "'"
                        if node.children.get(x) != None:
                            self.searchDown(w, index+1, node.children.get(x), neighbor, err+1, error, score+1.15) # replacing with apostrophe 

                    if index+2 < len(w): #if we have enough space to delete or transpose a letter
                        if node.children.get(w[index+2]) != None:

                            node2 = node.children.get(w[index+2])  #check for transposes
                            if node2.children.get(w[index+1]) != None:
                                self.searchDown(w, index+2, node2.children.get(w[index+1]), True, err+1, error, score+1) #transpose two letters

                            if neighbor == True and w[index+2] in neighbors[w[index+1]]:
                                self.searchDown(w, index+2, node.children.get(w[index+2]), True, err+1, error, score+1.05) #delete letter if neighbor with letter to right
                            else:
                                if neighbor == True and w[index] in neighbors[w[index+1]]:
                                    self.searchDown(w, index+2, node.children.get(w[index+2]), True, err+1, error, score+1.05) #delete letter if neighbor with letter to left
                                else:
                                    if neighbor == False:
                                        self.searchDown(w, index+2, node.children.get(w[index+2]), False, err+1, error, score+1.2) #delete letter

                    
                    if index + error - err + 1 == len(w): #if we have enough space to delete letters at the end of the input
                        neigh = True
                        for x in range(0,error-err):
                            if w[index] not in neighbors[w[index+1+x]]:
                                neigh = False
                        if neigh == True and neighbor == True:
                            self.searchDown(w, index+1+error-err, node, neighbor, error, error, score+1.05*(error-err)) #delete all letters at the end if they're neighbors
                        else:
                            self.searchDown(w, index+1+error-err, node, neighbor, error, error, score+1.2*(error-err)) #delete letters at end if non-neighbors

        else:
            self.complete(w, index, node, score) #once we've reached the max error cap, go to the complete method


    #------------header method for main recursion
    #starts all recursions
    def searchDownHead(self, w, node, neighbor, error):

        self.searchDown(w, 0, node.children.get(w[0]), neighbor, 0, error,0) #recur with the correct first letter
        if neighbor == True:
            for x in neighbors[w[0]]:
                if node.children.get(x) != None:
                    self.searchDown(w, 0, node.children.get(x), True, 1, error,1) #replace first letter with neighboring letter
            for x in neighbors[w[1]]:
                if node.children.get(x) != None:
                    self.searchDown(w, 1, node.children.get(w[1]), True, 1, error,1.05) #delete first letter if neighbor
        else:
            for y in range(97,123):
                x = chr(y)
                if x not in neighbors[w[0]]:
                    if node.children.get(x) != None:
                        self.searchDown(w, 0, node.children.get(x), False, 1, error,1.15) #replace with non-neighboring letter
                        
            for y in range(97,123):
                x = chr(y)
                if x not in neighbors[w[1]]:
                    if node.children.get(x) != None:
                        self.searchDown(w, 1, node.children.get(w[1]), False, 1, error,1.2) #delete first letter if non-neighbor
        for y in range(97,123):
            x = chr(y)
            self.searchDown(w, -1, node.children.get(x), neighbor, 1, error,1.05) #add letter

        if node.children.get(w[1]) != None:
            node2 = node.children.get(w[1])
            if node2.children.get(w[0]) != None:
                self.searchDown(w, 1, node2.children.get(w[0]), neighbor, 1, error, 1) #transposition   0 to 1


    #------------the method that is called from the front end    
    def findCandidates(self,w):
        self.candidates = [] #resets candidate list from previous calls to the algorithm
        global searchDownCount
        searchDownCount = 0
        
        if len(w) == 1: #if the input is one letter, just check if it's next to 'a' or 'i'

            if w[0] in neighbors['a']:
                self.candidates.append((self.trie.header.children.get('a'),0))
            if w[0] in neighbors['i']:
                self.candidates.append((self.trie.header.children.get('i'),0))
            return self.candidates

        for x in range(2,len(w) - 3):  #check to see if the input is two words back to back "elephantpelican"   0 to 2. lenw-1 to -3
            node = self.trie.header
            word = True
            for y in range(0,x+1): #see if first part makes a word
                if node.children.get(w[y]) != None:
                    node = node.children.get(w[y])
                else:
                    word = False
                    break
            if node.end and word:
                node2 = self.trie.header
                for y in range(x+1,len(w)):  #see if second part makes a word
                    if node2.children.get(w[y]) != None:
                        node2 = node2.children.get(w[y])
                    else:
                        word = False
                        break
                if node2.end and word:  #add to the trie
  
                    avgFreq = (node.freq + node2.freq) / 2 #calculate the average of the two frequencies
                    self.candidates.append(((node,node2), 1.05 * (1 - avgFreq))) #add the words to the list of candidates

                    self.candidates.sort(key = lambda x : x[1]) #sort the list of candidates by score
                    if len(self.candidates) > self.size:    #make sure candidates only contains the top four words
                        self.candidates.pop()

        for x in range(2,len(w) - 4):  #input has a bottom row letter in between two words "elephantvpelican" 0 to 2. lenw-2 to -4
            node = self.trie.header
            word = True
            for y in range(0,x+1): #check first part
                if node.children.get(w[y]) != None:
                    node = node.children.get(w[y])
                else:
                    word = False
                    break
            if node.end and word == True and w[x+1] in bottomRow:
                node2 = self.trie.header
                for y in range(x+2,len(w)):  #check second part
                    if node2.children.get(w[y]) != None:
                        node2 = node2.children.get(w[y])
                    else:
                        word = False
                        break
                if node2.end and word == True:
                    print('double word with letter in between')

                    avgFreq = (node.freq + node2.freq) / 2 #calculate the average of the two frequencies       
                    self.candidates.append(((node,node2),(1 - avgFreq)))
                    
                    self.candidates.sort(key = lambda x : x[1]) #sort the list of candidates by score
                    if len(self.candidates) > self.size:    #make sure candidates only contains the top four words
                        self.candidates.pop()

        self.searchDownHead(w, self.trie.header, True, 1) #first find single errors that are neighbors
        if len(self.candidates) < self.size:
            self.searchDownHead(w, self.trie.header, False, 1)  #if we need to continue, look for single errors that aren't neighbors
        if len(self.candidates) < self.size:            
            self.searchDownHead(w, self.trie.header, True, 2) #if we need to continue, look for double errors that are neighbors
        if len(self.candidates) < self.size:
            self.searchDownHead(w, self.trie.header, False, 2) #etc
        if len(self.candidates) < self.size:            
            self.searchDownHead(w, self.trie.header, True, 3)
        if len(self.candidates) < self.size:
            self.searchDownHead(w, self.trie.header, False, 3) #stop after triple errors

        # Ensures that the first word in the candidate list is the word the user entered (if it was a valid word)
        wb = False

        for x in self.candidates:
            if x[0] == self.trie.lookup(w):
                self.candidates.remove(x)
                wb = True

        if wb == True:
            self.candidates.append((self.trie.lookup(w), 0.0))

        if self.trie.lookup(w) and wb == False:
            self.candidates.insert(0, (self.trie.lookup(w), 0.0))

        self.candidates.sort(key = lambda x : x[1])
        
        if len(self.candidates) > self.size:
            self.candidates.pop()        

        # Print candidates and return them
        print(searchDownCount)
        print('candidates:',self.candidates)
        return self.candidates










