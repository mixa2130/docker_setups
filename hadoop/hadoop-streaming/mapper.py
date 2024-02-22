import sys
import random

for line in sys.stdin:
    id_el = line.strip()

    print(id_el, str(random.randint(0, 7777)), sep='\t')

