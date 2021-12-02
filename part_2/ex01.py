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

M: Final = [5, 11, 14]

FILE_NAME: Final = 'ex01.smv'

smv_file = open(FILE_NAME, 'w')

smv_file.write('\nMODULE main\n')
smv_file.write('VAR\n')

for i in range (1, NR_OF_CHANNELS + 1):
    smv_file.write(f'c{i} : 0 .. {NR_OF_NODES};\n')

smv_file.write('ASSIGN\n')

for i in range (1, NR_OF_CHANNELS + 1):
    smv_file.write(f'init(c{i}) := 0;\n')

smv_file.write('TRANS\n')

deadlock_check = '!('

P = [''] * NR_OF_CHANNELS

for i in range (1, NR_OF_CHANNELS + 1):
    for j in range (1, NR_OF_CHANNELS + 1):
        if i == j:
            continue
        P[i-1] += f'next(c{j}) = c{j} & '

    P[i-1] = P[i - 1][:-2]

for i in range (1, NR_OF_CHANNELS + 1):
    if i > 1:
        smv_file.write(f'|\n')

    channel_used_by_m = False;

    for s in M:
        for t in M:
            if s == t:
                continue

            # OK step
            if i == ROUTES[s - 1][t - 1]:
                channel_used_by_m = True;

                # Send
                smv_file.write(f'case c{i} = 0 : next(c{i}) = {t} & {P[i-1]};\n')
                smv_file.write(f'     TRUE : next(c{i}) = c{i} & {P[i-1]}; esac\n')
                smv_file.write(f'|\n')

    if channel_used_by_m:
        deadlock_check += f'(c{i} = 0) | '

    for n in range(1, NR_OF_NODES):
        target = TARGETS[i-1]
        next_channel = ROUTES[target - 1][n - 1]

        PPT = ''
        for z in range(1, NR_OF_CHANNELS + 1):
            if z == i or z == next_channel:
                continue
            PPT += f'next(c{z}) = c{z} & '
        PPT = PPT[:-2]

        if n > 1:
            smv_file.write(f'|\n')

        # Receive
        if n == target:
            smv_file.write(f'case c{i} = {n} : next(c{i}) = 0 & {P[i-1]};\n')
            smv_file.write(f'     TRUE : next(c{i}) = c{i} & {P[i-1]}; esac\n')

            deadlock_check += f'(c{i} = {n}) | '

            # Exclude messages that should be captured by receive
            continue;

        # Process
        smv_file.write(f'case c{i} = {n} & c{next_channel} = 0 : next(c{i}) = 0 & next(c{next_channel}) = {n} & {PPT};\n')
        smv_file.write(f'     TRUE : next(c{i}) = c{i} & {P[i-1]}; esac\n')

        deadlock_check += f'(c{i} = {n} & c{next_channel} = 0) | '
        
deadlock_check = deadlock_check[:-2]
deadlock_check += ')'

smv_file.write(f'\nCTLSPEC !EF({deadlock_check})')
