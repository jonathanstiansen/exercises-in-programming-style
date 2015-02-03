#!/usr/bin/env python
import re, sys, operator

# Mileage may vary. If this crashes, make it lower
RECURSION_LIMIT = 9500
# We add a few more, because, contrary to the name,
# this doesn't just rule recursion: it rules the 
# depth of the call stack
sys.setrecursionlimit(RECURSION_LIMIT+10)

def count(word_list, stopwords, wordfreqs):
    # What to do with an empty list
    if word_list == []:
        return
    # The inductive case, what to do with a list of words
    else:
        # Process the head word
        word = word_list[0]
        if word not in stopwords:
            if word in word_freqs:
                wordfreqs[word] += 1
            else:
                wordfreqs[word] = 1
        # Process the tail 
        count(word_list[1:], stopwords, wordfreqs)

def wf_print(wordfreq):
    if wordfreq == []:
        return
    else:
        (w, c) = wordfreq[0]
        print w, '-', c
        wf_print(wordfreq[1:])
# String -> ListOf Words
# The part that is difficult with this is the 
def stringToWords(f0):
    # String String -> ListOfWords
    def strHelper(f, currS):
        if f is '': return []
        else: 
            firstLetter = f[0]
            if(firstLetter is ',' or firstLetter is ' '): 
                return [currS] + strHelper( f[1:], '')   
            else: 
                return strHelper( f[1:], currS + firstLetter)     
    return strHelper(f0, '')

# String -> ListOf Words
stop_words = set( stringToWords(open('../stop_words.txt').read()) )

words = re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower())
word_freqs = {}
# Theoretically, we would just call count(words, word_freqs)
# Try doing that and see what happens.
for i in range(0, len(words), RECURSION_LIMIT):
    count(words[i:i+RECURSION_LIMIT], stop_words, word_freqs)

wf_print(sorted(word_freqs.iteritems(), key=operator.itemgetter(1), reverse=True)[:25])

