#---------------------------decentcorrect.py---------------------------
# all code written by Daniel Webber, except code pertaining
# to trie loading and saving, written by Michael Curry

from tkinter import *
from trie import *
from robertperry import *
from generate import *
import pickle

#------------------------------picklename------------------------------

picklename = "trie.pickle"

#----------------------------class BackEnd-----------------------------

class BackEnd():

    def __init__(self, trie):
        self.trie = trie
        self.rp = robertperry(trie)
        self.first = -1 # first index of most recent word considered
        self.last = -1 # last index of most recent word considered
        self.string = "" # string most recently considered
        self.suggestions = None # list of (node, score) pairs OR ((node, node), score) pairs
        self.suggestionsCap = False # whether the user capitalized the string most recently considered
        self.active = False # if False, key bindings are not functional

    def getStringFromCand(self, c):
        try:
            st = c.getWordWithCap()
        except AttributeError:
            # c is a pair of nodes
            st = c[0].getWordWithCap()+" "+c[1].getWordWithCap()
        return st

    def check(self, s):
        l = s.split("\'")
        # remove apostrophes to check lowercase/alphabetism
        if l[-1] == "":
            l = l[:-1]
            # if word ends in apostrophe, remove the trailing empty string
        if len(l) == 0:
            # if nothing remains, don't try to correct
            return False
        for t in l:
            if not t.isalpha() or not t.islower():
                # idiosyncratic capitalization and non-apostrophe punctuation indicate a string to not correct
                return False        
        return True

    def prepare(self, f, l, s):
        cap = False
        leng = len(s)
        t = s.lstrip("\'\"({[#")
        first = f+leng-len(t)
        leng = len(t)
        t = t.rstrip("\'\".,?!)}]:;")
        last = l+len(t)-leng
        st = s[first-f-1:last-f+1]
        if first-f < 1:
            st = s[first-f:last-f+1]
        if st.endswith("\'") and not st.startswith("\'"):
            # if an apostrophe immediately follows but does not immediately proceed the word
            # treat the apostrophe as part of a possessive word
            t = s[first-f:last-f+1]
            last += 1
        if t[0:1].isalpha() and t[0:1].isupper():
            # if the first character is uppercase, lowercase the string and set cap to True
            t = t[0:1].lower()+t[1:]
            cap = True
        if self.check(t):
            return (cap, first, last, t.lower())
        else:
            # if the check fails, return tuple containing None for string
            # to indicate error in calling method
            return (False, f, l, None)

    def correct(self, s):
        t = s.split(" ")[-1] # get the last space-separated string
        self.string = t.split("-")[-1] # get the last hypen-separed string within the above
        self.first = s.rfind(self.string)
        t = t.split("-")[-1] # have t get a copy of self.string
        last = len(s) #last character of the INPUT
        cap, self.first, last, t = self.prepare(self.first, last, t)
        # extract and locate the actual word to be corrected
        
        if t == None:
            # if nothing to correct, return the input
            self.last = last
            return(self.first, last, self.string, False)
        
        if cap:
            self.string = t.capitalize()
        else:
            self.string = t
            
        realCorrection = False
        nodes = self.rp.findCandidates(t)
        # find the best candidate corrections for t
        # if t in the lexicon, the top candidate will be t

        try:
            node = nodes[0][0]
            # node is the first element of the first candidate: either a node or a (node, node) tuple
        except IndexError:
            # no candidates found
            st = t
        else:
            st = self.getStringFromCand(node)
            self.suggestions = nodes[1:]
            self.suggestionsCap = cap
            if st != t:
                # if the top candidate is not the given word, we're making a real correction
                self.active = True
                realCorrection = True
                
        self.last = self.first + len(st)

        if cap and st.islower():
            return (self.first, last, st.capitalize(), realCorrection)
        else:
            return (self.first, last, st, realCorrection)
    
    def reject(self):
        return (self.first, self.last, self.string)

    def learn(self, s):
        cap, f, l, s = self.prepare(-1, -1, s)
        # prepare the word for trie entry as we prepare them for trie comparison
        if s and not cap:
            # don't add words that were capitalized
            self.trie.add(s)

    def takeSuggestion(self, i):
        node = self.suggestions[i][0]
        st = self.getStringFromCand(node)
        if self.suggestionsCap and st.islower():
            return (self.first, self.last, st.capitalize())
        else:
            return (self.first, self.last, st)

#---------------------------begin main script--------------------------

# load the trie from the pickle, unless there's an error: then regenerate it
try:
    pfile = open(picklename, "rb")
    print("restoring pickled trie")
    trie = pickle.load(pfile)
    pfile.close()
except FileNotFoundError:
    print("(re)generating trie")
    trie = genlexicon()
except (KeyError, EOFError):
    print("rotten pickle, regenerating trie")
    trie = genlexicon()

backend = BackEnd(trie)
    
app = Tk()
app.title("DecentCorrect")
app.geometry("1000x80+100+100")

def saveTrie():
    pickle.dump(backend.trie, open(picklename, "wb"))
    app.destroy()
    sys.exit()

app.protocol('WM_DELETE_WINDOW', saveTrie) # on close, save the trie for future use

v = StringVar() # string variable for the top label
v.set("")
v2 = StringVar() # string variable for the bottom label
v2.set("")

e = Entry(app)

def correct():
    backend.suggestions = None # clear the old suggestions list
    v2.set("")
    x = backend.correct(e.get()[0:e.index("insert")])
    # grab the whole text from the entry and send it to correct in the backend
    if x[3]:
        # if a real correction
        v.set("Suggested: "+e.get()[x[0]:x[1]]+" to "+x[2])
    else:
        v.set("")
    e.delete(x[0], x[1])
    e.insert(x[0], x[2])
    if backend.suggestions:
        text = ("Alternatively: ")
        for n in backend.suggestions:
            st = backend.getStringFromCand(n[0])
            if st.islower() and backend.suggestionsCap:
                text = text+st.capitalize()+", "
            else:
                text = text+st+", "
        v2.set(text[:-2])
        backend.active = True # enable keybindings

def reject(event):
    if backend.active:
        r = backend.reject()
        if(r[0] >= 0):
            e.delete(r[0], r[1])
            e.insert(r[0], r[2])
            backend.active = False # disable keybindings
            backend.suggestions = None # clear the old suggestions list
            v.set("") # clear text fields
            v2.set("")

def takeS0(event):
    if backend.active and len(backend.suggestions) > 0:
        r = backend.takeSuggestion(0)
        e.delete(r[0], r[1])
        e.insert(r[0], r[2])
        backend.active = False # disable keybindings
        backend.suggestions = None # clear the old suggestions list
        v.set("") # clear text fields
        v2.set("")

def takeS1(event):
    if backend.active and len(backend.suggestions) > 1:
        r = backend.takeSuggestion(1)
        e.delete(r[0], r[1])
        e.insert(r[0], r[2])
        backend.active = False # disable keybindings
        backend.suggestions = None # clear the old suggestions list
        v.set("") # clear text fields
        v2.set("")

def takeS2(event):
    if backend.active and len(backend.suggestions) > 2:
        r = backend.takeSuggestion(2)
        e.delete(r[0], r[1])
        e.insert(r[0], r[2])
        backend.active = False # disable keybindings
        backend.suggestions = None # clear the old suggestions list
        v.set("") # clear text fields
        v2.set("")
        
state = None

def send(event):
    global state
    before = e.get()[0:e.index("insert")] # the current state of the entry field
    if not state or state != before:
        # if state isn't been set or it's different than the current state
        correct()
        after = e.get()[0:e.index("insert")]
        # the state following the correction
        if before == after:
            # if not a real correction, send
            v.set("Sent: "+before)
            v2.set("")
            e.delete(0, END)
            state = None # clear the state
            for s in before.split():
                # learn all the words in the message
                backend.learn(s)
        else:
            # if it's a real correction, save the current state
            state = before
    else:
        # if the current state is the previous state, send
        v.set("Sent: "+before)
        v2.set("")
        e.delete(0, END)
        state = None # clear the state
        for s in before.split():
            # learn all the words in the message
            backend.learn(s)

def correctShortcut(event):
    correct()

e.bind("<space>", correctShortcut)
e.bind("-", correctShortcut)
e.pack(fill="x")
e.focus_set()

Label(app, textvariable=v, width=1000).pack()
Label(app, textvariable=v2, width=1000).pack()

app.bind("<Return>", send)
app.bind("<Control-z>", reject)
app.bind("<Control-Z>", reject)
app.bind("<Control-j>", takeS0)
app.bind("<Control-J>", takeS0)
app.bind("<Control-k>", takeS1)
app.bind("<Control-K>", takeS1)
app.bind("<Control-l>", takeS2)
app.bind("<Control-L>", takeS2)

app.mainloop()
