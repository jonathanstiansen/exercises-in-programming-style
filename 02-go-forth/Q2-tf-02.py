#!/usr/bin/env python
import sys, re, operator, string

#
# The all-important data stack
#
stack = []

#
# The heap. Maps names to data (i.e. variables)
#
heap = {}

#
# The new "words" (procedures) of our program
#
def read_file():
    """
    Takes a path to a file on the stack and places the entire
    contents of the file back on the stack.
    """
    f = open(stack.pop())
    # Push the result onto the stack
    stack.append([f.read()])
    ##print 'Read file' + str(stack)
    f.close()

def filter_chars():
    """
    Takes data on the stack and places back a copy with all 
    nonalphanumeric chars replaced by white space. 
    """
    # This is not in style. RE is too high-level, but using it
    # for doing this fast and short. Push the pattern onto stack
    stack.append(re.compile('[\W_]+'))
    # Push the result onto the stack
    ##print "before filter" + str(stack)
    stack.append([stack.pop().sub(' ', stack.pop()[0]).lower()])
    ##print "after filter" + str(stack)
def scan():
    """
    Takes a string on the stack and scans for words, placing
    the list of words back on the stack
    """
    # Again, split() is too high-level for this style, but using
    # it for doing this fast and short. Left as exercise.
    stack.extend(stack.pop()[0].split())

def remove_stop_words():
    """ 
    Takes a list of words on the stack and removes stop words.
    """
    f = open('../stop_words.txt')
    stack.append(f.read().split(','))
    f.close()
    # add single-letter words
    stack[-1].extend(list(string.ascii_lowercase))
    heap['stop_words'] = stack.pop()
    # Again, this is too high-level for this style, but using it
    # for doing this fast and short. Left as exercise.
    heap['words'] = []
    while len(stack) > 0:
        if stack[-1] in heap['stop_words']:
            stack.pop() # pop it and drop it
        else:
            heap['words'].append(stack.pop()) # pop it, store it
    stack.extend(heap['words']) # Load the words onto the stack
    del heap['stop_words']; del heap['words'] # Not needed 
    
    # If I was creating this, my first thought is if we don't have pointers -
    # then how do we accumulate more than one word, 
    # its far to hard for us to keep a dictionary of these, and if we can't 
    # iterate throught the stack, thta might be an issue. 
    # My guess is that we can in fact iterate through the heap and thats its purpose...
def frequencies():
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence.
    """
    heap['word_freqs'] = {}
    heap['tmpFreq'] = 0
    # A little flavour of the real Forth style here...
    while len(stack) > 0:
        # ... but the following line is not in style, because the 
        # naive implementation would be too slow
        stack.append(heap['word_freqs'].keys())
        ##print heap['word_freqs']
        exists_in_alpha()
        #print stack[0:2]
        # if stack.pop() < stack[-1]:# stack[-1] > 0
        # Increment the frequency, postfix style: f 1 +
        stack.append(1) # push 1
        stack.append(stack.pop() + stack.pop()) # add
        heap['word_freqs'][stack.pop()] = stack.pop()  
        
    # Push the result onto the stack
    #print "the heap is " +str(heap['word_freqs'])
    stack.append(heap['word_freqs'])
    del heap['tmpFreq'] # don't need this anymore
    del heap['word_freqs'] # We don't need this variable anymore

# Pre condition, stack[-1] is word_freq keys, stack[-2] is current word
# Post condition, stack[-1] is freq of curr word (0 if !exists), stack[-2] is current word 
# This increases the complexity from n to n^3 of this operation
def exists_in_alpha():
    #print 'pre whole stack' + str(stack)
    #print 'pre' + str(stack[-3:-1])
    for word in stack[-1]:
        stack.append(word)
        if stack[-1] == stack[-3]:
            heap['tmpFreq'] = heap['word_freqs'][stack.pop()] # set frequency
            stack.pop() # get rid of keys
            stack.append(heap['tmpFreq'])
            break
        else:
            stack.pop() # get word off, go next
            # stack state here is same as pre-condition
    # 2 cases, either it's a number or its the keys
    if type(stack[-1]) is not int:
        #print 'Its not an int, its a ' + str(type(stack[-1]))
        str(stack.pop()) # pops off the keys
        stack.append(0) # tmp freq = 0
    #print 'post' + str(stack[-3:-1])

def sort():
    # Not in style, left as exercise
    stack.extend(sorted(stack.pop().iteritems(), key=operator.itemgetter(1)))

# The main function
#
stack.append(sys.argv[1])
read_file(); filter_chars(); scan(); remove_stop_words()
frequencies(); sort()

stack.append(0)
# Check stack length against 1, because after we process
# the last word there will be one item left
while stack[-1] < 25 and len(stack) > 1:
    heap['i'] = stack.pop()
    (w, f) = stack.pop(); print w, ' - ', f
    stack.append(heap['i']); stack.append(1)
    stack.append(stack.pop() + stack.pop())

