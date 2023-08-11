#! /usr/bin/env python3

import socket
import struct
import sys

for line in sys.stdin:
    fields = line.split()
    fields[0] = str(struct.unpack("!I", socket.inet_aton(fields[0]))[0])
    print('\t'.join(fields))
