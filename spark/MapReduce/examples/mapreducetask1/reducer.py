import sys
import random
import typing as tp

new_line: tp.List[str] = []
limiter: int = random.randint(1, 5)


def new_iteration():
    global new_line
    global limiter

    new_line = []
    limiter = random.randint(1, 5)


for line in sys.stdin:
    new_id, _ = line.split('\t')

    new_line.append(new_id.strip())
    limiter -= 1

    if limiter == 0:
        print(','.join(new_line))
        new_iteration()

# End of iteration
if new_line:
    print(','.join(new_line))
