import trie
import itertools

# hard-code close neighbors to letters
neighbors = { 'a' : ['q', 'w', 's', 'z'] , 'b' : ['v', 'g', 'h', 'j', 'n'] , 'c' : ['x', 'd', 'f', 'g', 'v'] , 'd' : ['z', 'x', 'c', 'f', 'r', 'e', 's'] , 'e' : ['w', 's', 'd', 'r'] , 'f' : ['x', 'c' 'v', 'g', 't', 'r', 'd'] , 'g' : ['c', 'v', 'b', 'h', 'y', 't', 'f'], 'h' : ['v', 'b', 'n', 'j', 'u', 'y', 'g'] , 'i' : ['u', 'j', 'k', 'o'] , 'j' : ['b', 'n', 'm', 'k', 'i', 'u', 'h'], 'k' : ['n', 'm', 'l', 'o', 'i', 'j'], 'l' : ['m', 'k', 'o', 'p'], 'm' : ['n', 'j', 'k', 'l'] , 'n' : ['b', 'h', 'j', 'k', 'm'] , 'o' : ['i', 'k', 'l', 'p'] , 'p' : ['o', 'l'] , 'q' : ['a', 'w'] , 'r' : ['e', 'd', 'f', 't'] , 's' : ['a', 'z', 'x', 'd', 'e', 'w'], 'z' : ['a', 's', 'd', 'x'], 'y' : ['t', 'g', 'h', 'u'] , 'x' : ['z', 's', 'd', 'f', 'c'] , 'w' : ['q', 'a', 's', 'e'] , 'v' : ['c', 'f', 'g', 'h', 'b'] , 'u' : ['y', 'h', 'j', 'i'] , 't' : ['r', 'f', 'g', 'y'] }


#delete letter for neighbor before or after, also for letter itself


class algorithm():
    def __init__(self, trie):
        self.trie = trie
        self.candidates = []

        #this method is called when the maximum errors allowed has been reached
    def complete(self, w, index, node, neighbor, err, error, score):
        for y in range(index, len(w)-1): #try to add on all remaining letters
            if node.children.get(w[y+1]) != None:
                node = node.children.get(w[y+1])
            else: #if it is not a valid node
                return
        if node.end: #if it is a valid word
            score = score * (1-node.freq)
            double = False
            for x in self.candidates:
                if x[0] == node.word:
                    double = True
            if not double: #update the sorted list of candidates
                self.candidates.append((node.word, score))
                self.candidates.sort(key = lambda x : x[1])
                if len(self.candidates) > 3:
                    self.candidates.pop()


    #------------Main recursion method
    def searchDown(self, w, index, node, neighbor, err, error, score):

        print(node.getString(), index)

        if err < error:  #if we haven't reached max errors
            if index < len(w): 
                for y in range(97,123): #remember apostrophes
                    x = chr(y)
                    if node.children.get(x) != None: 
                        self.searchDown(w, index, node.children.get(x), neighbor, err+1, error, score+1) # adding a letter

                if index+1 < len(w):
                    if node.children.get(w[index+1]) != None:
                        self.searchDown(w, index+1, node.children.get(w[index+1]), neighbor, err, error, score)  #recurring without errors

                    if neighbor == True:
                        for x in neighbors[w[index+1]]:
                            if node.children.get(x) != None:
                                self.searchDown(w, index+1, node.children.get(x), True, err+1, error,score+1)   #replace with neighbor

                    else:
                        for y in range(97,123): #remember apostrophe
                            x = chr(y)
                            if x not in neighbors[w[index+1]]:
                                if node.children.get(x) != None:
                                    self.searchDown(w, index+1, node.children.get(x), False, err+1, error, score+2) # replacing non neighbor

                    if index+2 == len(w): #if we want to delete a letter at the end
                        if neighbor == True and w[index+2] in neighbors[w[index+1]]:
                            self.searchDown(w, index+2, node, True, err+1, error, score+1) #delete letter at end if neighbor
                        if neighbor == False and w[index+2] not in neighbors[w[index+1]]:
                            self.searchDown(w, index+2, node, False, err+1, error, score+1.5) #delete letter at end if not neighbor
                        return
                    
                    if node.children.get(w[index+2]) != None:
                        if neighbor == True and w[index+2] in neighbors[w[index+1]]:
                            self.searchDown(w, index+2, node.children.get(w[index+2]), True, err+1, error, score+1) #delete letter if neighbor
                        if neighbor == False and w[index+2] not in neighbors[w[index+1]]:
                            self.searchDown(w, index+2, node.children.get(w[index+2]), False, err+1, error, score+1.5) #delete letter

                else:
                    self.complete(w, index, node, neighbor, err, error, score)
            else:
                self.complete(w, index, node, neighbor, err, error, score)
        else:
            self.complete(w, index, node, neighbor, err, error, score)


    #------------header method for main recursion
    def searchDownHead(self, w, node, neighbor, error):

        self.searchDown(w, 0, node.children.get(w[0]), neighbor, 0, error,0) #starting with correct letter
        if neighbor == True:
            for x in neighbors[w[0]]:
                if node.children.get(x) != None:
                    self.searchDown(w, 0, node.children.get(x), True, 1, error,1) #replaced neighboring letter
                    if x == w[1]:
                        self.searchDown(w, 1, node.children.get(w[1]), True, 1, error,1) #delete first letter if neighbor
        else:
            for y in range(97,123):
                x = chr(y)
                if x not in neighbors[w[index]]:
                    if node.children.get(x) != None:
                        self.searchDown(w, 0, node.children.get(x), False, 1, error,2) #replaced non-neighboring letter
                        if x==w[1]:
                            self.searchDown(w, 1, node.children.get(w[1]), False, 1, error,2) #delete first letter if non-neighbor
        for y in range(97,123):
            x = chr(y)
            self.searchDown(w, -1, node.children.get(x), neighbor, 1, error,1) #add letter



    
    def findCandidates(self,w):
        self.candidates = []
        counter = 0
        # while(len(candidates)<3):
        neighbor = True
        if counter%2 == 1:
            neighbor = False
        self.searchDownHead(w, self.trie.header, neighbor, 1+counter/2)
        # counter++
        print('candidates:',self.candidates)
        return self.candidates




    #------------Method for trying to delete letters-------------------------------

    def delete(self, w, trie, error):
        # Get all combinations of k letters in w (in lexicographic sort order) where k = w.length - error
        deletions = list(itertools.combinations(w, len(w)-error)) # might be len(w)-1-error
        
        # Check each combination against trie. If it's there, add to candidates.
        for x in deletions:
            y = ''.join(x)
            if trie.lookup(y):
                self.candidates.append((y, error))

                    
    #------------Method for trying to add letters----------------------------------

    def add(self, w, trie, error):
        # All combinations of indices into w where we want to test adding letters
        addIndex = list(itertools.combinations(range(len(w)+1), error))
        
        # Try every letter in the combinations of indices specified by addIndex. If resulting word is in trie, add to candidates.
        for x in addIndex:
            attempt = w
            for y in x:
                for z in range(97, 123):
                    attempt = attempt[:y] + chr(z) + attempt[y:]
                    if trie.lookup(attempt):
                        self.candidates.append((attempt, error))
                    attempt = w














