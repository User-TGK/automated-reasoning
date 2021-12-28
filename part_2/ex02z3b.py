from z3 import *
from typing import Final

s = Solver()

ITERATIONS_ATTEMPT = 14

# Capacity limitations
MAX_TRUCK_CAPACITY: Final = 260
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

lasso_found = [[Bool(f'Found{i}{j}') for j in range(i + 1, ITERATIONS_ATTEMPT)] for i in range(ITERATIONS_ATTEMPT)]

# Initialization
s.add(truck_position[0] == LOCATION_S)
s.add(truck_stock[0] == MAX_TRUCK_CAPACITY)

s.add(village_a_stock[0] == INITIAL_PACKAGES_IN_VILLAGES)
s.add(village_b_stock[0] == INITIAL_PACKAGES_IN_VILLAGES)
s.add(village_c_stock[0] == INITIAL_PACKAGES_IN_VILLAGES)
s.add(village_d_stock[0] == INITIAL_PACKAGES_IN_VILLAGES)

def max_capacity(village):
    if village == VILLAGE_A:
        return MAX_VILLAGE_A_CAPACITY
    elif village == VILLAGE_B:
        return MAX_VILLAGE_B_CAPACITY
    elif village == VILLAGE_C:
        return MAX_VILLAGE_C_CAPACITY
    elif village == VILLAGE_D:
        return MAX_VILLAGE_D_CAPACITY

    print(f'Unknown village {village}') 

def current_stock(village, current_iteration):
    if village == VILLAGE_A:
        return village_a_stock[current_iteration]
    elif village == VILLAGE_B:
        return village_b_stock[current_iteration]
    elif village == VILLAGE_C:
        return village_c_stock[current_iteration]
    elif village == VILLAGE_D:
        return village_d_stock[current_iteration]

    print(f'Unknown village {village}') 

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

def print_solution(model):
    global i

    for s in range(ITERATIONS_ATTEMPT):
        for f in range(s + 1, ITERATIONS_ATTEMPT):
            if is_true(model.eval(lasso_found[s][f - s - 1])):
                print(f'Start from iteration {s} to {f}')

    print('{:<12} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8}'.format(
    'Iteration', 'Position', 'Stock', 
    'A stock', 'B stock', 'C stock', 'D stock'))

    for n in range(i+1):
        truck_p = model[truck_position[n]].as_long()
        truck_s = model[truck_stock[n]].as_long()

        assert(truck_p in LOCATIONS)
        assert(truck_s >= 0 and truck_s <= MAX_TRUCK_CAPACITY)

        village_a_s = model[village_a_stock[n]].as_long()
        village_b_s = model[village_b_stock[n]].as_long()
        village_c_s = model[village_c_stock[n]].as_long()
        village_d_s = model[village_d_stock[n]].as_long()

        assert(village_a_s >= 0 and village_a_s <= MAX_VILLAGE_A_CAPACITY)
        assert(village_b_s >= 0 and village_a_s <= MAX_VILLAGE_B_CAPACITY)
        assert(village_c_s >= 0 and village_a_s <= MAX_VILLAGE_C_CAPACITY)
        assert(village_d_s >= 0 and village_a_s <= MAX_VILLAGE_D_CAPACITY)

        if n > 0:
            last_truck_p = model[truck_position[n - 1]].as_long()
            last_truck_s = model[truck_stock[n - 1]].as_long()

            cost = TRAVEL_TIMES[last_truck_p][truck_p]

            assert(cost != -1)                

            for village in VILLAGES:
                l_stock = model[previous_stock(village, n)].as_long()
                c_stock = model[current_stock(village, n)].as_long()

                if village == truck_p:
                    supplied = last_truck_s - truck_s

                    assert(c_stock == l_stock - cost + supplied)
                else:
                    assert(c_stock == l_stock - cost)

        print('{:<12} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8}'.format(
            n, truck_p, truck_s, village_a_s, village_b_s, village_c_s, village_d_s
        ))

# Recursion
i = 0

while True:
    if i == ITERATIONS_ATTEMPT:
        break

    i += 1

    next_truck_position = Int(f'Tp{i}')
    next_truck_stock = Int(f'St{i}')
    previous_truck_stock = truck_stock[i - 1]

    next_village_a_stock = Int(f'Sa{i}')
    next_village_b_stock = Int(f'Sb{i}')
    next_village_c_stock = Int(f'Sc{i}')
    next_village_d_stock = Int(f'Sd{i}')

    # Never drop below 0, or some village dies
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

    # Determine our current location
    for location in LOCATIONS:
        next_location_choices = []
        
        # Determine the locations to which we can move in the next step
        for next_location, cost in enumerate(TRAVEL_TIMES[location]):
            # No route
            if cost == -1:
                continue

            next_location_consequences = []
            next_location_consequences.append(next_truck_position == next_location)

            # We are now in a village that we can provide some supplies
            if next_location in VILLAGES:
                next_location_consequences.append(previous_stock(next_location, i) - cost >= 0)
                next_location_consequences.append(current_stock(next_location, i) <= max_capacity(next_location))
                next_location_consequences.append(current_stock(next_location, i) <= previous_stock(next_location, i) - cost + previous_truck_stock)
                next_location_consequences.append(next_truck_stock == previous_truck_stock - (current_stock(next_location, i) - previous_stock(next_location, i) + cost))

            # The next location is S, so we can refill the truck to full capacity
            elif next_location == LOCATION_S:
                next_location_consequences.append(next_truck_stock == MAX_TRUCK_CAPACITY)

            # Every other village cusomes the cost
            for village in VILLAGES:
                if village == next_location:
                    continue

                next_location_consequences.append(current_stock(village, i) == previous_stock(village, i) - cost)

            # Add all consequences of moving to this location
            next_location_choices.append(And(*next_location_consequences))

        # If we are in this location, there are a some choices to be made.
        s.add(Implies(truck_position[i - 1] == location, Or(*next_location_choices)))

    truck_position.append(next_truck_position)

contains_lasso = []

for i in range(ITERATIONS_ATTEMPT):
    for j in range(i + 1, ITERATIONS_ATTEMPT):
        not_decreased = []

        not_decreased.append(truck_position[j] == truck_position[i])
        not_decreased.append(truck_stock[j] >= truck_stock[i])
        not_decreased.append(village_a_stock[j] >= village_a_stock[i])
        not_decreased.append(village_b_stock[j] >= village_b_stock[i])
        not_decreased.append(village_c_stock[j] >= village_c_stock[i])
        not_decreased.append(village_d_stock[j] >= village_d_stock[i])

        lasso_found[i][j - i - 1] = And(*not_decreased)

        contains_lasso.append(lasso_found[i][j - i - 1])

s.add(Or(*contains_lasso))

if s.check() == sat:
    print(f'Found lasso after {i} iterations')
    print_solution(s.model())
else:
    print(f'Not satisfiable within {i} iterations')

print('Terminated')
