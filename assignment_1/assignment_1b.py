from os import dup
from typing import Final
from z3 import *

# Pallets of nuzzles in truck i is stored in TPNi
# Pallets of prittles in truck i is stored in TPPi
# Pallets of skipples in truck i is stored in TPSi
# Pallets of cottles in truck i is stored in TPCi
# Pallets of dupples in truck i is stored in TPDi

NR_OF_TRUCKS: Final = 8

TRUCK_WEIGHT_CAPACITY: Final = 8000
TRUCK_PALLET_CAPACITY: Final = 8

MAX_COOLING_TRUCKS: Final = 3
MAX_NUZZLE_PALLETS_PER_TRUCK: Final = 1

NUZZLE_PALLET_WEIGHT: Final = 700
PRITTLE_PALLET_WEIGHT: Final = 400
SKIPPLE_PALLET_WEIGHT: Final = 1000
CROTTLE_PALLET_WEIGHT: Final = 2500
DUPPLE_PALLET_WEIGHT: Final = 200

NR_OF_NUZZLE_PALLETS: Final = 4
NR_OF_SKIPPLE_PALLETS: Final = 8
NR_OF_CROTTLE_PALLETS: Final = 10
NR_OF_DUPPLE_PALLETS: Final = 20

# Optimization solver for computing the maximum amount of prittle pallets

optimizer = Optimize()

# Create the variables

nuzzles_in_trucks = [Int(f"TPN{s}") for s in range(NR_OF_TRUCKS)]
prittles_in_trucks = [Int(f"TPP{s}") for s in range(NR_OF_TRUCKS)]
skipples_in_trucks = [Int(f"TPS{s}") for s in range(NR_OF_TRUCKS)]
crottles_in_trucks = [Int(f"TPC{s}") for s in range(NR_OF_TRUCKS)]
dupples_in_trucks = [Int(f"TPD{s}") for s in range(NR_OF_TRUCKS)]

# Add constraints for transporting the required amount of pallets
# ------------------------------------------------
# Σ(TPN0..TPN7) == 4  ^
# Σ(TPN0..TPS7) == 8  ^
# Σ(TPN0..TPC7) == 10 ^
# Σ(TPN0..TPD7) == 20
# ------------------------------------------------
pallet_constraints = And(Sum(nuzzles_in_trucks) == NR_OF_NUZZLE_PALLETS,
                         Sum(skipples_in_trucks) == NR_OF_SKIPPLE_PALLETS,
                         Sum(crottles_in_trucks) == NR_OF_CROTTLE_PALLETS,
                         Sum(dupples_in_trucks) == NR_OF_DUPPLE_PALLETS)

optimizer.add(pallet_constraints)

# Add per pallet constraints

for i in range(NR_OF_TRUCKS):

    # No negative pallets are allowed
    # ------------------------------------------------
    # TPNi >= 0 ^
    # TPPi >= 0 ^
    # TPSi >= 0 ^
    # TPCi >= 0 ^
    # TPDi >= 0
    # ------------------------------------------------
    optimizer.add(nuzzles_in_trucks[i] >= 0)
    optimizer.add(prittles_in_trucks[i] >= 0)
    optimizer.add(skipples_in_trucks[i] >= 0)
    optimizer.add(crottles_in_trucks[i] >= 0)
    optimizer.add(dupples_in_trucks[i] >= 0)

    # No truck weight must exceed TRUCK_WEIGHT_CAPACITY
    # ------------------------------------------------
    # + (* TPNi NUZZLE_PALLET_WEIGHT)
    #   (* TPPi PRITTLE_PALLET_WEIGHT)
    #   (* TPSi SKITTLE_PALLET_WEIGHT)
    #   (* TPCi CROTTLE_PALLET_WEIGHT)
    #   (* TPDi DUPPLE_PALLET_WEIGHT)
    #   <= TRUCK_PALLET_CAPACITY
    # ------------------------------------------------
    weight_constraint = (nuzzles_in_trucks[i] * NUZZLE_PALLET_WEIGHT +
                         prittles_in_trucks[i] * PRITTLE_PALLET_WEIGHT +
                         skipples_in_trucks[i] * SKIPPLE_PALLET_WEIGHT +
                         crottles_in_trucks[i] * CROTTLE_PALLET_WEIGHT +
                         dupples_in_trucks[i] * DUPPLE_PALLET_WEIGHT <=
                         TRUCK_WEIGHT_CAPACITY)
    optimizer.add(weight_constraint)

    # No truck weight must exceed TRUCK_PALLET_CAPACITY
    # ------------------------------------------------
    # + TPNi TPPi TPSi TPCi TPDi <= TRUCK_PALLET_CAPACITY
    # ------------------------------------------------
    pallet_constraint = (nuzzles_in_trucks[i] + prittles_in_trucks[i] + skipples_in_trucks[i] +
                         crottles_in_trucks[i] + dupples_in_trucks[i] <= TRUCK_PALLET_CAPACITY)
    optimizer.add(pallet_constraint)

    # No truck must contain more then MAX_NUZZLE_PALLETS_PER_TRUCK nuzzle pallets
    # ------------------------------------------------
    # TPNi <= MAX_NUZZLE_PALLETS_PER_TRUCK
    # ------------------------------------------------
    nuzzle_constraint = (nuzzles_in_trucks[i] <= MAX_NUZZLE_PALLETS_PER_TRUCK)
    optimizer.add(nuzzle_constraint)

    optimizer.add(Implies(prittles_in_trucks[i] > 0, crottles_in_trucks[i] == 0))
    optimizer.add(Implies(crottles_in_trucks[i] > 0, prittles_in_trucks[i] == 0))

    # Trucks 0..MAX_COOLING_TRUCKS have a cooling facility
    if i >= MAX_COOLING_TRUCKS:
        optimizer.add(skipples_in_trucks[i] == 0)

optimizer.maximize(Sum(prittles_in_trucks))

print(optimizer)
print(optimizer.check())
print(optimizer.model())
