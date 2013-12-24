import trie
import itertools

# hard-code close neighbors to letters


class algorithm():
    def __init__(self, trie, w):
        self.trie = trie
        self.w = w
        self.candidates = []
        searchDown(self, self.w, self.trie.root)
        delete(self, self.w, self.trie, error)
   
    
    #------------Method for trying to replace letters----------------------------
    
    def searchDown(self, w, index, node, neighbor, err, error):
        # Figure out how to handle base case
        if x[index] != node.letter:
            err++

        if err < error:
            if neighbor == true:
                for x in w[index].neighbors:
                    if node.children.get(x) != None:
                        searchdown(self, w, index+1, node.children.get(x), err, error)
            else:
                for x in range(26):
                    if x not in w[index].neighbors:
                        if node.children.get(x) != None:
                            searchdown(self, w, index+1, node.children.get(x), err, error)

        else:
            for y in range(index, w.length+1):
                # Print y to debug whether we need to add 1 to the range
                if node.children.get(w[y+1]) != None:
                    node = node.children.get(w[y+1])
                else:
                    break
                if node.end:
                    self.candidates.append((node.word, err))


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
                        
                        
                        
    #------------Method for returning candidate list-------------------------------

    def getCandidates():
        return self.candidates















