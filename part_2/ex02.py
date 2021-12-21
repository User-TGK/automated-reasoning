from z3 import *
from typing import Final

from part_1.assignment_3b import bool_to_int_array

s = Solver()
NR_OF_ITTERATIONS = 100
NR_OF_VILLAGES = 4
SA, SB, SC, SD, ST = 80
CA, CC = 110
CB, CD = 160
CT = 250
currentVillage = 0
max_foodbpackages_to_deliver = 0
NR_OF_ROADS = 7
truck_is_driving = False
ROAD_INDEX_MAPPING = [
    [0,1],  # "SA" = 0
    [0,3],  # "SC" = 1
    [1,0],  # "AS" = 2
    [1,2],  # "AB" = 3
    [1,3],  # "AC" = 4
    [2,1],  # "BA" = 5
    [2,3],  # "BC" = 6
    [2,4],  # "BD" = 7
    [3,0],  # "CS" = 8
    [3,1],  # "CA" = 9
    [3,2],  # "CB" = 10
    [3,4],  # "CD" = 11
    [4,2],  # "DB" = 12
    [4,3]   # "DC" = 13
]
road_variables = [Bool(f"R{ROAD_INDEX_MAPPING[i][0]}{ROAD_INDEX_MAPPING[i][1]}") for i in ROAD_INDEX_MAPPING]
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

def bool_to_int_array(xs):
    return [If(xs[i], 1, 0) for i in range(len(xs))]

def get_index_of_current_road(int_array):
    return int_array.index(1)

for i in range(0, NR_OF_ITTERATIONS):
    truck_on_road = bool_to_int_array(road_variables)
    # add constraint: if truck is driving currently, the sum of all booleanvariables should be equal to 1
    #                 else: the sum of all boolean variables should be equal to 0
    s.add(If(truck_is_driving, Sum(truck_on_road) == 1, Sum(truck_on_road) == 0))

    # s.add(If(truck_is_driving, And(If(get_index_of_current_road(truck_on_road) == 0, ST -= TRAVEL_TIME[ROAD_INDEX_MAPPING[0][0]][ROAD_INDEX_MAPPING[0][1]]), ST -= 1)))





for i in range(0,NR_OF_ITTERATIONS):
    # TO-DO: how to decide how many foodpackages will be delivered!! 
    if currentVillage == 1:
        max_foodbpackages_to_deliver = CA
    elif currentVillage == 2:
        max_foodbpackages_to_deliver = CB
    elif currentVillage == 3:
        max_foodbpackages_to_deliver = CC
    elif currentVillage == 4:
        max_foodbpackages_to_deliver = CD

    deliveredFoodpackages = ST

    s.add(If(currentVillage == 0, 
            ST = CT, 
            ST = ST - 1))
    s.add(If(currentVillage == 1, 
            And(SA = SA + deliveredFoodpackages, 
                ST = ST - deliveredFoodpackages), 
            SA = SA - 1))
    s.add(If(currentVillage == 2, 
            And(SB = SB + deliveredFoodpackages, 
                ST = ST - deliveredFoodpackages), 
            SB = SB - 1))
    s.add(If(currentVillage == 3, 
            And(SC = SC + deliveredFoodpackages, 
                ST = ST - deliveredFoodpackages), 
            SC = SC - 1))
    s.add(If(currentVillage == 4, 
            And(SD = SD + deliveredFoodpackages, 
                ST = ST - deliveredFoodpackages), 
            SD = SD - 1))

# the number of stored food packages is not allowed to be smaller than 1
s.add(And(SA < 1, SB < 1, SC < 1, SD < 1))