#!/usr/bin/env python
# My golf score is slightly lower!  
# Best wishes, Peter Norvig

import re, sys, collections as c
stopwords = c.Counter(open('../stop_words.txt').read().split(','))
words = re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower())
counts = c.Counter(words)
print filter(f, counts)
for w, n in counts.most_common(25): print w, '-', n
#map(counts.most_common(25), lambda (c, v): print c, '-', v)
# 346, now 328
# Can I do a dict comprehension with a 'number which is a function? Each time its added to something it adds itself?'
# Map Filter Reduce job? No the issue would be 