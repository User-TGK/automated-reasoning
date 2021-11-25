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

M: Final = [1, 5, 9, 13]

FILE_NAME: Final = 'ex01.smv'

smv_file = open(FILE_NAME, 'w')

smv_file.write('\nMODULE main\n')
smv_file.write('VAR\n')

smv_file.write(f'channels : array 1 ..{NR_OF_CHANNELS} of 0..{NR_OF_NODES};\n')
smv_file.write(f'sources : array 1 ..{NR_OF_CHANNELS} of 1..{NR_OF_NODES};\n')
smv_file.write(f'targets : array 1 ..{NR_OF_CHANNELS} of 1..{NR_OF_NODES};\n')
smv_file.write(f'routes : array 1..{NR_OF_NODES} of array 1..{NR_OF_NODES} of 0..{NR_OF_CHANNELS};\n');
smv_file.write(f'D : boolean;\n')

smv_file.write('ASSIGN\n')

for i in range (1, NR_OF_CHANNELS + 1):
    smv_file.write(f'init(channels[{i}]) := 0;\n')

for i in range(0, NR_OF_CHANNELS):
    smv_file.write(f'init(sources[{i+1}]) := {SOURCES[i]};\n')
    smv_file.write(f'init(targets[{i+1}]) := {TARGETS[i]};\n')

for i in range(0, NR_OF_NODES):
    for j in range(0, NR_OF_NODES):
        smv_file.write(f'init(routes[{i+1}][{j+1}]) := {ROUTES[i][j]};\n')

smv_file.write(f'init(D) := FALSE;\n')

smv_file.write('TRANS\n')

delim = '|'
deadlock_check = '!('

P = ''

for i in range (0, NR_OF_CHANNELS):
    channel_index = i + 1

    P += f'next(channels[{channel_index}]) = channels[{channel_index}] & '

P = P[:-2]

for i in range (0, NR_OF_CHANNELS):
    if i > 0:
        smv_file.write(f'{delim}\n')

    channel_index = i + 1
    receive_check = f'channels[{channel_index}] = targets[{channel_index}]'
    process_check = f'channels[{channel_index}] != 0 & channels[{channel_index}] != targets[{channel_index}] & channels[routes[targets[{channel_index}]][channels[{channel_index}]]] = 0'

    # Receive step
    smv_file.write(f'case {receive_check} : next(channels[{channel_index}]) = 0;\n')
     # Process step
    smv_file.write(f'{process_check} : next(channels[routes[targets[{channel_index}]][channels[{channel_index}]]]) = channels[{channel_index}] & next(channels[{channel_index}]) = 0;\n')
    smv_file.write(f'TRUE : {P}; esac\n')

    deadlock_check += f'({receive_check}) | ({process_check}) |'
# Send step
for m_prime in M:
    for m in M:
        if m_prime != m:
            smv_file.write(f'{delim}\n')
            smv_file.write(f'case channels[routes[{m_prime}][{m}]] = 0 : next(channels[routes[{m_prime}][{m}]]) = {m};\n')
            smv_file.write(f'TRUE : {P}; esac\n')

            deadlock_check += f'channels[routes[{m_prime}][{m}]] = 0 | '

deadlock_check = deadlock_check[:-2]
deadlock_check += ')'

smv_file.write(f'{delim}\n')
smv_file.write(f'case {deadlock_check} : next(D) = TRUE;\n')
smv_file.write(f'TRUE : next(D) = D & {P}; esac;\n')

smv_file.write(f'CTLSPEC !EF(D)')
