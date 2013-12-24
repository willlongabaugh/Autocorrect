# generate.py
# generates a trie to hold the lexicon
# code written by Michael Curry

#from __future__ import division
from trie import *
frequency_scale = 23135851162*2
def genlexicon():

    # puts frequency into a dictionary
    fname = "count_1w.txt"
    freqfile = open(fname)
    freq = {}
    for line in iter(freqfile):
        lineoutput = line.split()
        freq[lineoutput[0]] = int(lineoutput[1])
    freqfile.close()

    # collects a list of valid common nouns into a set
    nounname = "12dicts-5.0/agid-4/infl.txt"
    nounfile = open(nounname)
    singlenouns = set([])
    pluralnouns = set([])
    for line in iter(nounfile):
        l = line.split()
        if (l[1] == 'N:') or (l[1] == 'N:?'):
            # add only if lowercase, also add the first plural inflection
            if not l[0].isupper():
                singlenouns.add(l[0].rstrip("!<?~,1"))
                pluralnouns.add(l[2].rstrip("!<?~,1"))
    nounfile.close()

    # all geographic names get counted as nouns
    geoname = "12dicts-5.0/geo.txt"
    geofile = open(geoname)
    for line in iter(geofile):
        singlenouns.add(line.rstrip().lower())
    geofile.close()
            
    t = Trie()
        
        # dictionaries from 12dicts as well as our own additions
    files = ["12dicts-5.0/2of12inf.txt","12dicts-5.0/6of12.txt","12dicts-5.0/geo.txt", "12dicts-5.0/amherst.txt"]
    # filetesthash = {}
    for file in files:
        infile = open(file)
        for line in iter(infile):
            firstcaps = False
            allcaps = False

            # remove newline
            line = line.rstrip()

            # remove 12dicts punctuation tags
            line = line.rstrip(':&#<^=+%')#added %

            # cleans newlines or spaces possibly
            line = line.rstrip()

            # this code for punctuation testing is not as tight or clear as it could be but it should work
            #test for capitalization here?
            if line[0].isupper():
                firstcaps = True
            if line.isupper():
                allcaps = True

            #lowercase
            line = line.lower()

            # throw out all words with spaces or hyphens
            if " " in line or "-" in line:
                continue


            # if we have no apostrophe
            if "'" not in line:
                # but there are other special characters, drop it
                if not line.isalpha():
                    continue

            try:
                count = freq[line]
                #print "Key found for " + line
            except KeyError:
                count = 0 # might want to change to a small constant like 1
                #print "Key not found for " + line

            # add it to the trie, unless it's a two-letter acronym in one of the two main dictionaries
            if not((file == "12dicts-5.0/2of12inf.txt" or file == "12dicts-5.0/6of12.txt") and len(line) == 2 and (firstcaps or allcaps)):
                t.add(line,count/frequency_scale,cap=firstcaps,allcap=allcaps)
                
                # each singular and plural noun gets a possessive, 's unless it ends in s
                if line in singlenouns:
                    t.add(line+"'s",count/frequency_scale,cap=firstcaps,allcap=allcaps)
                if line in pluralnouns:
                    if line[-1] == "s":
                        t.add(line+"'",count/frequency_scale,cap=firstcaps,allcap=allcaps)
                    else:
                        t.add(line+"'s",count/frequency_scale,cap=firstcaps,allcap=allcaps)
                
        infile.close()
                    
                    #lists of names from ssi
    for year in range(1930,2010):
        infile = open("names/yob" + str(year) + ".txt")
        lines = infile.readlines()
        offset=0
        # this searches for the first male name and saves the offset from the beginning
        while lines[offset].split(',')[1] != 'M':
            offset = offset + 1
        for i in range(1,100):
            # the male names are lowered by the offset
            female = lines[i].split(',')[0].lower()
            male = lines[i+offset].split(',')[0].lower()
            # add possessives
            t.add(female,cap=True)
            t.add(female+"'s",cap=True)
            t.add(male,cap=True)
            t.add(male+"'s",cap=True)
        infile.close()
    return t
