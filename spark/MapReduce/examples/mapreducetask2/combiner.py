import sys
import collections

aggregator = collections.defaultdict(int)

for line in sys.stdin:
    _, word, cnt = line.split()
    cnt: int = int(cnt)
    word = word.strip()

    aggregator[word] += cnt

for key in aggregator.keys():
    print(len(key), key, aggregator[key], sep='\t')
