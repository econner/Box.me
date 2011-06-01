# This file converts stopwords.txt into Python code that creates a 
# set of all the stopwords.
#
# Input: stopwords.txt - a newline-separated list of words
# Output: code.txt - Python code written into this file

f = open('stopwords.txt')
out = open('code.txt', 'w')
out.write('stopwords = set([')
lines = f.readlines()
words=[]
for l in lines:
    if l != '\n':
        words.append('\'' + l[:-1] + '\'')

out.write(','.join(words))
out.write('])\n\n')

f.close()
out.close()