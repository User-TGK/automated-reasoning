from typing import Final


# State space is defined as NR_OF_NODES^NR_OF_CHANNELS
NR_OF_CHANNELS: Final = 27
NR_OF_NODES: Final = 17

M: Final = [1, 5, 9, 13];

FILE_NAME: Final = 'ex01.smv'



smv_file = open(FILE_NAME, 'w')

smv_file.write('MODULE rout(n,m)\n')

smv_file.write('VAR\n')
smv_file.write(f'c : 0..{NR_OF_CHANNELS};\n')

smv_file.write('DEFINE routing := [\n')
smv_file.write('    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],\n')
smv_file.write('    [2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],\n')
smv_file.write('    [17, 17, 0, 3, 3, 3, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17],\n')
smv_file.write('    [26, 26, 26, 0, 4, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26],\n')
smv_file.write('    [5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],\n')
smv_file.write('    [6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],\n')
smv_file.write('    [19, 19, 19, 19, 19, 19, 0, 7, 7, 7, 19, 19, 19, 19, 19, 19, 19],\n')
smv_file.write('    [27, 27, 27, 27, 27, 27, 27, 0, 8, 27, 27, 27, 27, 27, 27, 27, 27],\n')
smv_file.write('    [9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9],\n')
smv_file.write('    [10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 10, 10, 10, 10, 10, 10, 10],\n')
smv_file.write('    [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 0, 11, 11, 11, 21, 21, 21],\n')
smv_file.write('    [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 0, 12, 12, 12, 12, 12],\n')
smv_file.write('    [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 0, 13, 13, 13, 13],\n')
smv_file.write('    [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 14, 14, 14],\n')
smv_file.write('    [15, 15, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 0, 15, 23],\n')
smv_file.write('    [16, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 0, 25],\n')
smv_file.write('    [24, 24, 18, 18, 18, 18, 20, 20, 20, 20, 22, 22, 22, 22, 24, 24, 0]\n')
smv_file.write('];\n')

smv_file.write('ASSIGN\n')
smv_file.write('c := routing[n][m];\n')

smv_file.write('\nMODULE target(c)\n')
smv_file.write('VAR\n')
smv_file.write(f'n : 1..{NR_OF_NODES};\n')
smv_file.write('DEFINE targets := [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 17, 3, 17, 7, 17, 11, 17, 15, 2, 6, 10];\n')
smv_file.write('ASSIGN\n')
smv_file.write('n := targets[c];\n')

smv_file.write('\nMODULE main\n')
smv_file.write('VAR\n')

for i in range (1, NR_OF_CHANNELS+1):
    smv_file.write(f'c{i} : 0..{NR_OF_NODES};\n')

smv_file.write(f'm : {{ {", ".join(map(str, M))} }}\n')

smv_file.write('ASSIGN\n')

for i in range (1, NR_OF_CHANNELS+1):
    smv_file.write(f'init(c{i}) := 0;\n')

smv_file.write('TRANS\n')

for i in range (1, NR_OF_CHANNELS+1):
    # TODO: Send step

    # Receive step
    smv_file.write(f'case c{i} = target(c{i}) : next(c{i}) = 0;\n')

    # TODO: Process step
