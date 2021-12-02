from typing import Final
import string

NR_OF_VILLAGES = 4
# VILLAGES = ['A', 'B', 'C', 'D']
VILLAGES = list(string.ascii_uppercase)[:NR_OF_VILLAGES]
CAPACITY_VILLAGES = [110, 160, 110, 160]
CAPACITY_TRUCK = 250
NR_OF_STORED_PACKAGES = 80

# travel time units from node X to Y, represented by TRAVEL_TIME[X][Y]
# S = 0, A = 1, B = 2, C = 3, D = 4
# a negative value means that there is no direct path between two certain villages
# a 0 value means that the source and target village are equivallent
TRAVEL_TIME =   [
                    [0, 15, -1, 15, -1],
                    [15, 0, 17, 12, -1],
                    [-1, 17, 0, 10, 20],
                    [15, 12, 10, 0, 20],
                    [-1, -1, 20, 20, 0]
                ]


FILE_NAME: Final = 'ex02.smv'

smv_file = open(FILE_NAME, 'w')

smv_file.write('\nMODULE main\n')
smv_file.write('VAR\n')

for i in range(0, NR_OF_VILLAGES):
    smv_file.write(f'S{VILLAGES[i]} : 0..{CAPACITY_VILLAGES[i]};\n')

smv_file.write(f'ST : 0..{CAPACITY_TRUCK};\n')

for i in range(0, NR_OF_VILLAGES):
    smv_file.write(f'C{VILLAGES[i]} : 0..{CAPACITY_VILLAGES[i]};\n')

smv_file.write(f'CT : 0..{CAPACITY_TRUCK};\n')
smv_file.write(f'currentVillage : 0..{NR_OF_VILLAGES};\n')

smv_file.write('ASSIGN\n')

for i in range(0, NR_OF_VILLAGES):
    smv_file.write(f'init(C{VILLAGES[i]}) := {CAPACITY_VILLAGES[i]}\n')
smv_file.write(f'init(CT) := {CAPACITY_TRUCK}\n')

for i in range(0, NR_OF_VILLAGES):
    smv_file.write(f'init(S{VILLAGES[i]}) := {NR_OF_STORED_PACKAGES}\n')
smv_file.write(f'init(ST) := {CAPACITY_TRUCK}\n')
smv_file.write(f'init(currentVillage) := 0;\n')

smv_file.write('TRANS\n')
delim = '|'

TRUE_CASE = '     TRUE : '
temp = 'C'

for x in range (0, 2):
    for i in range(0, NR_OF_VILLAGES):
        TRUE_CASE += f'next({temp}{VILLAGES[i]}) = {temp}{VILLAGES[i]} & '
    TRUE_CASE += f'next({temp}T) = {temp}T'

    if (temp == 'C'):
        TRUE_CASE += ' & '
    temp = 'S'

TRUE_CASE += ' & next(currentVillage) = currentVillage; esac'

SOURCES_ROADS = [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4]
TARGETS_ROADS = [1, 3, 0, 3, 2, 1, 3, 4, 0, 1, 2, 4, 2, 3]

for z in range(0, len(SOURCES_ROADS)):
    if (z > 0):
        smv_file.write(f'|\n')
    
    ALL_VILLAGE_CONDITION = ''
    ALL_VILLAGE_NEXT_BRANCH = ''
    TRUCK_NEXT__BRANCH = ''
    if (TARGETS_ROADS[z] == 0):
        TRUCK_NEXT__BRANCH = f'next(ST) = CT'
    else :
        TRUCK_NEXT__BRANCH = f'next(ST) = ST - {TRAVEL_TIME[SOURCES_ROADS[z]][TARGETS_ROADS[z]]} - (C{VILLAGES[TARGETS_ROADS[z] -1]} - S{VILLAGES[TARGETS_ROADS[z] -1]})'

    for x in range(0, NR_OF_VILLAGES):
        ALL_VILLAGE_CONDITION += f'S{VILLAGES[x]} - {TRAVEL_TIME[SOURCES_ROADS[z]][TARGETS_ROADS[z]]} >= 0 & '
        if ((x == (TARGETS_ROADS[z] - 1)) & (TARGETS_ROADS[z] > 0)):
            # TO-DO: take into account that the truck could contain less packages than
            # what is required to be able to fill the storage up till its capacity 
            ALL_VILLAGE_NEXT_BRANCH += f'next(S{VILLAGES[x]}) = C{VILLAGES[x]} & '
        else:
            ALL_VILLAGE_NEXT_BRANCH += f'next(S{VILLAGES[x]}) = S{VILLAGES[x]} - {TRAVEL_TIME[SOURCES_ROADS[z]][TARGETS_ROADS[z]]} & '

    ALL_VILLAGE_CONDITION = ALL_VILLAGE_CONDITION[:-2] 
    ALL_VILLAGE_NEXT_BRANCH = ALL_VILLAGE_NEXT_BRANCH[:-3]

    smv_file.write(f'case currentVillage = {SOURCES_ROADS[z]} & {ALL_VILLAGE_CONDITION}: next(currentVillage) = {TARGETS_ROADS[z]} & {TRUCK_NEXT__BRANCH} & {ALL_VILLAGE_NEXT_BRANCH};\n')
    smv_file.write(f'{TRUE_CASE}\n')