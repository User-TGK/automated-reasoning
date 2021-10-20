from os import dup
from typing import Final
from z3 import *

import math

NR_OF_PERSONS: Final = 10
NR_OF_HOUSES: Final = 5
NR_OF_ROUNDS: Final = 5

# A house within a round is either empty or contains exactly five persons
PERSONS_PER_HOUSE_PER_ROUND: Final = 5

# In total, each house should host two rounds
ROUNDS_PER_HOUSE: Final = 2

# The maximum amount of times each player i, j may encounter each other
MAX_ENCOUNTERS: Final = 4

# The minimum amount of times each player i, j must encounter each other
MIN_ENCOUNTERS: Final = 1

# A three-dimensional array, containing NR_OF_ROUNDS × NR_OF_HOUSES × NR_OF_PERSONS
# boolean variables
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

# Returns a tuple with the indices of the persons that own house i


def owners_of_house(i):
    return (i*2, i*2 + 1)

# Returns the index of the person that is the partner of person i


def partner_of_person(i):
    if i % 2 == 0:
        return i + 1
    else:
        return i - 1

# Converts an array of booleans to an array of integers, where 1 represents a 'True' value
# and 0 represents a 'False' value


def bool_to_int_array(xs):
    return [If(xs[i], 1, 0) for i in range(len(xs))]


# Helper array containing whether a house is used within a round
house_used_in_round = []

# Helper array containing whether a person i and j meet each other in a round
persons_encounter_per_round = []

person_is_guest_in_house = []

for i in range(NR_OF_ROUNDS):
    for j in range(NR_OF_HOUSES):
        persons_in_house = bool_to_int_array(person_in_house_in_round[i][j])

        house_used_in_round.append([])
        house_used_in_round[j].append(
            Sum(persons_in_house) == PERSONS_PER_HOUSE_PER_ROUND)

        # Persons in house j is either full or empty in round i
        s.add(Or(Sum(persons_in_house) == PERSONS_PER_HOUSE_PER_ROUND,
                 Sum(persons_in_house) == 0))

        # If there is a dinner hosted at house j, then the owners must be there
        # (Sum(persons_in_house) == 5) ↔ (owner_i ∧ owner_j)
        (owner_i, owner_j) = owners_of_house(j)
        s.add((Sum(persons_in_house) == PERSONS_PER_HOUSE_PER_ROUND) ==
              And(person_in_house_in_round[i][j][owner_i], person_in_house_in_round[i][j][owner_j]))

        # (C): Couples never meet outside their own house
        for k in range(NR_OF_PERSONS):
            s.add(Implies(
                And(person_in_house_in_round[i][j]
                    [k], k != owner_i, k != owner_j),
                Not(person_in_house_in_round[i][j][partner_of_person(k)])
        ))

    for k in range(NR_OF_PERSONS):
        occurres_in_house = []
        for j in range(NR_OF_HOUSES):
            occurres_in_house.append(person_in_house_in_round[i][j][k])

        # Person k is in exactly one house in round k
        s.add(Sum(bool_to_int_array(occurres_in_house)) == 1)


for j in range(NR_OF_HOUSES):
    s.add(Sum(bool_to_int_array(house_used_in_round[j])) == ROUNDS_PER_HOUSE)

for i in range(NR_OF_PERSONS):
    for j in range(NR_OF_PERSONS):
        # Unique, non-self combinations
        if i >= j:
            continue

        meet_per_round = []

        for k in range(NR_OF_ROUNDS):
            encounter_in_house = []
            for l in range(NR_OF_HOUSES):
                encounter_in_house.append(
                    And(person_in_house_in_round[k][l][i], person_in_house_in_round[k][l][j]))

            meet_per_round.append(Or(*encounter_in_house))

        persons_encounter_per_round.append(meet_per_round)

for i in range(len(persons_encounter_per_round)):
    # s.add(Sum(bool_to_int_array(
    #     persons_encounter_per_round[i])) <= MAX_ENCOUNTERS)


    # # (A): Every two people among the 10 participants meet each other at least once
    # s.add(Sum(bool_to_int_array(
    #     persons_encounter_per_round[i])) >= MIN_ENCOUNTERS)

    # (B): Every two people among the 10 participants meet each other at most 3 times
     s.add(Sum(bool_to_int_array(
        persons_encounter_per_round[i])) <= 3)


for i in range(NR_OF_PERSONS):
    person_is_guest_in_house.append([])

    for j in range(NR_OF_HOUSES):
        person_is_guest_in_house[i].append([])

        for k in range(NR_OF_ROUNDS):
            person_is_guest_in_house[i][j].append(
                person_in_house_in_round[k][j][i])

# (D): Guests are distinct
for i in range(NR_OF_PERSONS):
    for j in range(NR_OF_HOUSES):
        (owner_i, owner_j) = owners_of_house(j)
        if i != owner_i and i != owner_j:
            s.add(Sum(bool_to_int_array(person_is_guest_in_house[i][j])) <= 1)


# print(s.sexpr())
# print(s.check())

s.check()
m = s.model()


for i in range(NR_OF_PERSONS):
    for j in range(NR_OF_PERSONS):
        if i == j:
            continue
        meets = []
        for k in range(NR_OF_ROUNDS):
            for l in range(NR_OF_HOUSES):
                if m[person_in_house_in_round[k][l][i]] and m[person_in_house_in_round[k][l][j]]:
                    meets.append(k+1)

        print(f"Person {i+1} meets person {j+1} in rounds {meets}")
        

for d in m.decls():
    print(f"{d.name()}= {m[d]}")


# for i in range(NR_OF_PERSONS):
#     for j in range(NR_OF_HOUSES):
#         total = 0
#         for k in range(NR_OF_ROUNDS):
#             if m[person_in_house_in_round[k][j][i]]:
#                 total += 1
#         print(f"Person {i} is in house {j}: {total}")
