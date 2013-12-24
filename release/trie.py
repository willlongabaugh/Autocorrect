# Written by Daniel Webber and Michael Curry

class Node():
    def __init__(self, end, parent, children, freq, cap, allcap, word, char):
        #end is boolean, parent is Node, children is dictionary mapping chars to Nodes
        #freq is long, cap is boolean, allcap is boolean word is string, char is string
        self.end = end
        self.parent = parent
        self.children = children
        self.freq = freq
        self.cap = cap
        self.allcap = allcap
        self.word = word
        self.char = char

    def __repr__(self):
        return self.word

    def getWordWithCap(self):
        if self.allcap:
            return self.word.upper()
        elif self.cap:
            return self.word.capitalize()
        else:
            return self.word

    def getString(self):
        s = self.char
        node = self
        while node.parent.char:
            node = node.parent
            s = node.char + s
        return s
            
class Trie():
    def __init__(self):
        self.header = Node(False, None, {}, -1, False, False, None, None)

    #python's replacement for overloaded constructors
    #call like: t = Trie.fromfilename("filename")
    @classmethod
    def fromfilename(cls, f):
        t = cls()
        fin = open(f, "r")
        for line in iter(fin):
            t.add(line)
        return t

    def add(self, s, freq=0, cap=False, allcap=False):
        n = self.header
        for c in list(s):
            if n.children.get(c) == None:
                # if no child corresponding to character c, add the child with default initial values
                n.children[c] = Node(False, n, {}, -1, False, False, None, str(c))
            n = n.children[c] # keep walking down the trie
            
        if not n.end:
            # if not already a word, mark it a word and assign node attributes
            n.end = True
            n.freq = freq
            n.cap = cap
            n.allcap = allcap
            n.word = s

    def lookup(self, s):
        n = self.header
        for c in list(s):
            # walk down the trie for each character
            try:
                n = n.children[c]
            except KeyError:
                #if you ever can't keep walking down, the word isn't there
                return None
        if n.end:
            # if you finish the word, return it if and only if it's a real word
            return n
        else:
            return None

