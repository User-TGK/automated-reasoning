from typing import Final

# State space is defined as NR_OF_NODES^NR_OF_CHANNELS
NR_OF_CHANNELS: Final = 4
NR_OF_NODES: Final = 4

# SOURCES[0] is the source m of channel 1
SOURCES = [1, 2, 3, 4]

# TARGETS [0] is the target m of channel 1
TARGETS = [2, 3, 4, 1]

# ROUTES[0][1] is the channel you have to take if you want to go from node 1 to node 2
ROUTES = [
            [0, 1, 1, 1],
            [2, 0, 2, 2],
            [3, 3, 0, 3],
            [4, 4, 4, 0]
        ]

M: Final = [1, 2, 3, 4]

FILE_NAME: Final = 'networkex.smv'

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

for i in range (1, NR_OF_CHANNELS + 1):
    if i > 1:
        smv_file.write(f'|\n')

    if i in M:
        for j in M:
            if j == i:
                continue
            # Send
            smv_file.write(f'case c{i} = 0 : next(c{i}) = {j};\n')
            smv_file.write(f'     TRUE : next(c{i}) = c{i}; esac\n')
            smv_file.write(f'|\n')

        deadlock_check += f'(c{i} = 0) | '

    for n in range(1, NR_OF_NODES):
        target = TARGETS[i-1]
        next_channel = ROUTES[target - 1][n - 1]

        if n > 1:
            smv_file.write(f'|\n')

        # Receive
        smv_file.write(f'case c{i} = {n} & {target} = {n} : next(c{i}) = 0;\n')
        smv_file.write(f'     TRUE : next(c{i}) = c{i}; esac\n')

        deadlock_check += f'(c{i} = {n} & {target} = {n}) | '

        # Exclude messages that should be captured by receive
        if n == target:
            continue
    
        smv_file.write(f'|\n')

        # Process
        smv_file.write(f'case c{i} = {n} & {target} != {n} & c{next_channel} = 0 : next(c{i}) = 0 & next(c{next_channel}) = {n};\n')
        smv_file.write(f'     TRUE : next(c{i}) = c{i}; esac\n')

        deadlock_check += f'(c{i} = {n} & {target} != {n} & c{next_channel} = 0) | '
        
deadlock_check = deadlock_check[:-2]
deadlock_check += ')'

smv_file.write(f'CTLSPEC !EF({deadlock_check})')
