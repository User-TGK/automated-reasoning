from z3 import *
from typing import Final

s = Solver()

# Capacity limitations
MAX_TRUCK_CAPACITY: Final = 250
INITIAL_PACKAGES_IN_VILLAGES: Final = 80

MAX_VILLAGE_A_CAPACITY: Final = 110
MAX_VILLAGE_B_CAPACITY: Final = 160
MAX_VILLAGE_C_CAPACITY: Final = 110
MAX_VILLAGE_D_CAPACITY: Final = 160

# Positions the truck may be in
LOCATION_S: Final = 0

VILLAGE_A: Final = 1
VILLAGE_B: Final = 2
VILLAGE_C: Final = 3
VILLAGE_D: Final = 4

LOCATIONS: Final = [LOCATION_S, VILLAGE_A, VILLAGE_B, VILLAGE_C, VILLAGE_D]
VILLAGES: Final = [VILLAGE_A, VILLAGE_B, VILLAGE_C, VILLAGE_D]

# Edges for each vertex
TRAVEL_TIMES: Final = [
    [-1, 15, -1, 15, -1],
    [15, -1, 17, 12, -1],
    [-1, 17, -1, 10, 20],
    [15, 12, 10, -1, 20],
    [-1, -1, 20, 20, -1],
]

# Arrays with variables for capacities and truck positions
truck_position = [Int('Tp0')]
truck_stock = [Int('St0')]

village_a_stock = [Int('Sa0')]
village_b_stock = [Int('Sb0')]
village_c_stock = [Int('Sc0')]
village_d_stock = [Int('Sd0')]

# Initialization
s.add(truck_position[0] == LOCATION_S)
s.add(truck_stock[0] == MAX_TRUCK_CAPACITY)

s.add(village_a_stock[0] == INITIAL_PACKAGES_IN_VILLAGES)
s.add(village_b_stock[0] == INITIAL_PACKAGES_IN_VILLAGES)
s.add(village_c_stock[0] == INITIAL_PACKAGES_IN_VILLAGES)
s.add(village_d_stock[0] == INITIAL_PACKAGES_IN_VILLAGES)


def previous_stock(village, current_iteration):
    if village == VILLAGE_A:
        return village_a_stock[current_iteration - 1]
    elif village == VILLAGE_B:
        return village_b_stock[current_iteration - 1]
    elif village == VILLAGE_C:
        return village_c_stock[current_iteration - 1]
    elif village == VILLAGE_D:
        return village_d_stock[current_iteration - 1]

    print(f'Unknown village {village}')

# Recursion
i = 0

while True:
    i += 1

    if i == 33:
        break

    next_truck_position = Int(f'Tp{i}')
    next_truck_stock = Int(f'St{i}')

    next_village_a_stock = Int(f'Sa{i}')
    next_village_b_stock = Int(f'Sb{i}')
    next_village_c_stock = Int(f'Sc{i}')
    next_village_d_stock = Int(f'Sd{i}')

    s.add(And(
        next_truck_stock >= 0,
        next_village_a_stock >= 0,
        next_village_b_stock >= 0,
        next_village_c_stock >= 0,
        next_village_d_stock >= 0,
    ))

    truck_stock.append(next_truck_stock)

    village_a_stock.append(next_village_a_stock)
    village_b_stock.append(next_village_b_stock)
    village_c_stock.append(next_village_c_stock)
    village_d_stock.append(next_village_d_stock)

    for location in LOCATIONS:
        next_location_choices = []
        
        for next_location, cost in enumerate(TRAVEL_TIMES[location]):
            # No route
            if cost == -1:
                continue

            next_location_consequences = []
            next_location_consequences.append(next_truck_position == next_location)

            if not next_location == VILLAGE_A:
                next_location_consequences.append(next_village_a_stock == previous_stock(VILLAGE_A, i) - cost)
            else:
                next_location_consequences.append(previous_stock(VILLAGE_A, i) - cost >= 0)
                next_location_consequences.append(next_village_a_stock <= MAX_VILLAGE_A_CAPACITY)
                next_location_consequences.append(next_village_a_stock <= previous_stock(VILLAGE_A, i) - cost + truck_stock[i - 1])
                next_location_consequences.append(next_truck_stock == truck_stock[i - 1] - (next_village_a_stock - previous_stock(VILLAGE_A, i) + cost))

            if not next_location == VILLAGE_B:
                next_location_consequences.append(next_village_b_stock == previous_stock(VILLAGE_B, i) - cost)
            else:
                next_location_consequences.append(previous_stock(VILLAGE_B, i) - cost >= 0)
                next_location_consequences.append(next_village_b_stock <= MAX_VILLAGE_B_CAPACITY)
                next_location_consequences.append(next_village_b_stock <= previous_stock(VILLAGE_B, i) - cost + truck_stock[i - 1])
                next_location_consequences.append(next_truck_stock == truck_stock[i - 1] - (next_village_b_stock - previous_stock(VILLAGE_B, i) + cost))

            if not next_location == VILLAGE_C:
                next_location_consequences.append(next_village_c_stock == previous_stock(VILLAGE_C, i) - cost)
            else:
                next_location_consequences.append(previous_stock(VILLAGE_C, i) - cost >= 0)
                next_location_consequences.append(next_village_c_stock <= MAX_VILLAGE_C_CAPACITY)
                next_location_consequences.append(next_village_c_stock <= previous_stock(VILLAGE_C, i) - cost + truck_stock[i - 1])
                next_location_consequences.append(next_truck_stock == truck_stock[i - 1] - (next_village_c_stock - previous_stock(VILLAGE_C, i) + cost))

            if not next_location == VILLAGE_D:
                next_location_consequences.append(next_village_d_stock == previous_stock(VILLAGE_D, i) - cost)
            else:
                next_location_consequences.append(previous_stock(VILLAGE_D, i) - cost >= 0)
                next_location_consequences.append(next_village_d_stock <= MAX_VILLAGE_D_CAPACITY)
                next_location_consequences.append(next_village_d_stock <= previous_stock(VILLAGE_D, i) - cost + truck_stock[i - 1])
                next_location_consequences.append(next_truck_stock == truck_stock[i - 1] - (next_village_d_stock - previous_stock(VILLAGE_D, i) + cost))

            if next_location == LOCATION_S:
                next_location_consequences.append(next_truck_stock == 250)

            next_location_choices.append(And(*next_location_consequences))

        s.add(Implies(truck_position[i - 1] == location, Or(*next_location_choices)))

    truck_position.append(next_truck_position)

print(f'{s.check()}')
# print(f'{s.model()}')
# print(f'{s}')
