import sys
import collections

aggregator = dict()
aggregator_counter = collections.defaultdict(int)
prev_len = None


def make_output():
    global aggregator
    global aggregator_counter

    for wr_key in aggregator.keys():
        print('\t'.join(
            [wr_key,
             str(aggregator_counter[wr_key]),
             str(len(aggregator[wr_key]))]
        ))

        # Clear sub-dictionary
        aggregator[wr_key].clear()

    # Clear main dictionaries
    aggregator.clear()
    aggregator_counter.clear()


for line in sys.stdin:
    sm, word, cnt = line.split()
    sorted_word: str = ''.join(sorted(word.strip()))
    cnt: int = int(cnt)
    sm: int = int(sm)

    if prev_len is None:
        prev_len = sm

    if prev_len != sm:
        make_output()
        prev_len = sm

    if aggregator.get(sorted_word) is None:
        aggregator[sorted_word] = collections.defaultdict(int)

    aggregator[sorted_word][word] += cnt
    aggregator_counter[sorted_word] += cnt

# Last partition
make_output()
