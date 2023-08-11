import sys
import re

for raw_line in sys.stdin:
    _, text = raw_line.lower().strip().split('\t', 1)
    words = re.split("\W*\s+\W*", text, flags=re.UNICODE)

    for raw_word in words:
        _word = re.sub(r'[^A-Za-z\\s]', '', raw_word.strip())

        if len(_word) >= 3:
            print(len(_word), _word, 1, sep='\t')


