#!/usr/bin/python3

import sys

from typing import Final

# State space is defined as NR_OF_NODES^NR_OF_CHANNELS
NR_OF_CHANNELS: Final = 27
NR_OF_NODES: Final = 17

# SOURCES[0] is the source m of channel 1
SOURCES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 3, 17, 7, 17, 11, 17, 15, 17, 16, 4, 8]

# TARGETS [0] is the target m of channel 1
TARGETS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 17, 3, 17, 7, 17, 11, 17, 15, 2, 6, 10]

# ROUTES[0][1] is the channel you have to take if you want to go from node 1 to node 2
ROUTES = [
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [17, 17, 0, 3, 3, 3, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17],
            [26, 26, 26, 0, 4, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26],
            [5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
            [19, 19, 19, 19, 19, 19, 0, 7, 7, 7, 19, 19, 19, 19, 19, 19, 19],
            [27, 27, 27, 27, 27, 27, 27, 0, 8, 27, 27, 27, 27, 27, 27, 27, 27],
            [9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 10, 10, 10, 10, 10, 10, 10],
            [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 0, 11, 11, 11, 21, 21, 21],
            [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 0, 12, 12, 12, 12, 12],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 0, 13, 13, 13, 13],
            [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 14, 14, 14],
            [15, 15, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 0, 15, 23],
            [16, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 0, 25],
            [24, 24, 18, 18, 18, 18, 20, 20, 20, 20, 22, 22, 22, 22, 24, 24, 0]
        ]

M: Final = [11, 12, 15]

if len(sys.argv) != 3:
    print("Usage: python3 ex01-result-parser.py <result-file> <latex-file>")
    exit(-1)

result_filename = sys.argv[1]
latex_filename = sys.argv[2]

print('before opening')

infile = open(result_filename, 'r')

print('Opened infile')

outfile = open(latex_filename, 'w+')

counter_trace_started = False

state = []

def process_state():
    if len(state) == 1:
        c = state[0][0]
        m = state[0][1]
        outfile.write(f'send({SOURCES[c-1]}, {m})     & : &     C{c} := {m}\\\\ \n')
    if len(state) == 2:
        print(state)

        chan_processed = 0
        target_chan = 0
        m = 0

        if state[0][1] == 0:
            chan_processed = state[0][0]
            m = state[1][1]

            target_chan = state[1][0]
        elif state[1][1] == 0:
            chan_processed = state[1][0]
            m = state[0][1]

            target_chan = state[0][0]
        else:
            print("PROCESS BUT NO CHANNEL IS 0?!")
            exit(-1)

        outfile.write(f'process(C{chan_processed})     & : &    C{target_chan} := {m}; C{chan_processed} := 0\\\\ \n')

for line in infile:
    # print(line)
    if '-> State: 1.2 <-' in line:
        counter_trace_started = True

    if not counter_trace_started:
        continue

    if '->' in line:
        process_state()

        state.clear()
        outfile.write(f'% {line}')
    else:
        line = line.replace('c', '')
        trans = [int(s) for s in line.split() if s.isdigit()]
        if len(trans) != 2:
            print(f"POSSIBLY MALFORMED INPUT {line}")
            exit(-1)

        state.append((trans[0], trans[1]))

process_state()