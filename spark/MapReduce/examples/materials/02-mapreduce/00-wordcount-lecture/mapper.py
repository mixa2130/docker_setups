
import sys
import re

for line in sys.stdin:
    words = line.strip().split()
    for word in words:
        print("{}\t{}".format(word, 1))
