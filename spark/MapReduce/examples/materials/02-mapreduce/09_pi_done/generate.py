#! /usr/bin/env python

import os
import shutil
import random
import sys

CORE_DIR = 'pi_points'
COUNT_IN_FILE = 100


def prepare_dir():
    shutil.rmtree(CORE_DIR, ignore_errors=True)
    os.makedirs(CORE_DIR)


def generate(amount):
    for i in range(amount):
        if not i % COUNT_IN_FILE:
            fd = open(os.path.join(CORE_DIR, 'part-{}'.format(i / 100)), 'w')
        x = random.random() * 2 - 1
        y = random.random() * 2 - 1
        fd.write("{}\t{}\n".format(x, y))

prepare_dir()
generate(int(sys.argv[1]))
