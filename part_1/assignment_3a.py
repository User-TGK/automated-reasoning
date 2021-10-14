from os import dup
from typing import Final
from z3 import *

NR_OF_PERSONS: Final = 10
NR_OF_HOUSES: Final = 2
NR_OF_ROUNDS: Final = 2

MAX_PERSONS_PER_HOUSE_PER_ROUND: Final = 5

# p1,..,p10 (the persons)
# pi + pi+1 are a couple for i = 1,3,5,7,9

# pi

# If we know if player i is in house j in round k, we can
# determine satisfiability of the constrains

# player_in_house_in_round = [
# [Bool("pihj"), Bool("pihj"), Bool("pihj") ....]  # round 1
# [Bool("pihj"), Bool("pihj"), Bool("pihj") ....]  # round 2
# [Bool("pihj"), Bool("pihj"), Bool("pihj") ....]  # round 3
# [Bool("pihj"), Bool("pihj"), Bool("pihj") ....]  # round 4
# [Bool("pihj"), Bool("pihj"), Bool("pihj") ....]  # round 5
# ]

person_in_house_in_round = [
    [
        [
            Bool(f"r{k+1}h{j+1}p{i+1}")
            for i in range(NR_OF_PERSONS)
        ]
        for j in range(NR_OF_HOUSES)
    ]
    for k in range(NR_OF_ROUNDS)]


s = Solver()

# print(person_in_house_in_round)

for i in range(NR_OF_ROUNDS):
    for j in range(NR_OF_HOUSES):
        persons_in_house = [If(person_in_house_in_round[i][j][k], 1, 0)
                            for k in range(NR_OF_PERSONS)]

        s.add(Sum(persons_in_house) <= MAX_PERSONS_PER_HOUSE_PER_ROUND)

    for k in range(NR_OF_PERSONS):
        occurres_in_house = []
        for j in range(NR_OF_HOUSES):
            occurres_in_house.append(person_in_house_in_round[i][j][k])

        s.add(Sum([If(occurres_in_house[l], 1, 0)
              for l in range(NR_OF_HOUSES)]) == 1)

print(s.check())
print(s.model())
# # print(s)
