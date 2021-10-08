from z3 import *
from typing import Final

import cairo

# We are looking for {rcx1,...,rcx10}, {rcy1,...,rcy10}, {pcx1,pcx2} and {pcy1,pcx2}
# such that the chip design satisfies all constrains.

NR_OF_POWER_COMPONENTS: Final = 2

# Given size of the chip
CHIP_WIDTH: Final = 30
CHIP_HEIGHT: Final = 30

# The minimum distance between the center of two arbitrary power components
MIN_POWER_COMPONENT_DISTANCE: Final = 17

# Given (w, h) size of the 10 regular components
regular_component_sizes = [
    (4, 5), (4, 6), (5, 20), (6, 9), (6, 10),
    (6, 11), (7, 8), (7, 12), (10, 10), (10, 20)
]

# Given (w, h) size of the 2 power components
power_component_sizes = [(4, 3), (4, 3)]

regular_component_widths = []
regular_component_heights = []
regular_component_xs = []
regular_component_ys = []

power_component_widths = []
power_component_heights = []
power_component_xs = []
power_component_ys = []

s = Solver()


def draw_solution(model):
    with cairo.SVGSurface("2.svg", 1000, 1000) as surface:
        context = cairo.Context(surface)
        context.scale(CHIP_WIDTH / 3, CHIP_HEIGHT / 3)
        context.set_line_width(0.03)

        for i in range(CHIP_WIDTH + 1):
            context.move_to(i, 0)
            context.line_to(i, CHIP_WIDTH)
            context.stroke()

        for j in range(CHIP_HEIGHT + 1):
            context.move_to(0, j)
            context.line_to(CHIP_HEIGHT, j)
            context.stroke()

        # draw normal components
        context.set_font_size(2)

        context.set_line_width(0.1)

        for i in range(len(regular_component_sizes)):
            x = model[regular_component_xs[i]].as_long()
            y = model[regular_component_ys[i]].as_long()
            w = model[regular_component_widths[i]].as_long()
            h = model[regular_component_heights[i]].as_long()

            context.rectangle(x, y, w, h)
            context.set_source_rgba(0, 0, 1, 1)
            context.stroke_preserve()
            context.set_source_rgba(0, 0, 1, 0.5)
            context.fill()

            context.set_source_rgba(1, 1, 1, 1)
            context.move_to(x + 0.05, y + 2.0)
            context.show_text(f"C{i+1}")

        # draw power components
        context.set_line_width(0.1)
        for i in range(len(power_component_sizes)):
            x = model[power_component_xs[i]].as_long()
            y = model[power_component_ys[i]].as_long()
            w = model[power_component_widths[i]].as_long()
            h = model[power_component_heights[i]].as_long()

            context.rectangle(x, y, w, h)
            context.set_source_rgba(1, 0, 0, 1)
            context.stroke_preserve()
            context.set_source_rgba(1, 0, 0, 0.5)
            context.fill()

            context.set_source_rgba(1, 1, 1, 1)
            context.move_to(x, y + 2.0)
            context.show_text(f"P{i+1}")


def abs(x):
    return If(x >= 0, x, -x)


# Creates variables for the regular components
for i, _ in enumerate(regular_component_sizes):
    regular_component_widths.append(Int(f"rcw{i+1}"))
    regular_component_heights.append(Int(f"rch{i+1}"))
    regular_component_xs.append(Int(f"rcx{i+1}"))
    regular_component_ys.append(Int(f"rcy{i+1}"))

# Create variables for the power components
for i, _ in enumerate(power_component_sizes):
    power_component_widths.append(Int(f"pcw{i+1}"))
    power_component_heights.append(Int(f"pch{i+1}"))
    power_component_xs.append(Int(f"pcx{i+1}"))
    power_component_ys.append(Int(f"pcy{i+1}"))

# Constrains for the regular components
for i, (w, h) in enumerate(regular_component_sizes):
    rcxi = regular_component_xs[i]
    rcyi = regular_component_ys[i]
    rcwi = regular_component_widths[i]
    rchi = regular_component_heights[i]

    # Constraints for turning components 90 degrees
    s.add(Or(And(rcwi == w, rchi == h),
             And(rcwi == h, rchi == w)))

    # Constraints for the components to be on the chip
    s.add(And(rcxi >= 0, rcyi >= 0, rcxi + rcwi <=
          CHIP_WIDTH, rcyi + rchi <= CHIP_HEIGHT))

    # Constrains for the components to not overlap with other (regular) components
    for j, _ in enumerate(regular_component_sizes):
        if i == j:
            continue

        rcxj = regular_component_xs[j]
        rcyj = regular_component_ys[j]
        rcwj = regular_component_widths[j]
        rchj = regular_component_heights[j]

        s.add(Or(rcxi + rcwi <= rcxj,
                 rcxj + rcwj <= rcxi,
                 rcyi + rchi <= rcyj,
                 rcyj + rchj <= rcyi))

    connected_constraints = []

    for j, _ in enumerate(power_component_sizes):
        pcxj = power_component_xs[j]
        pcyj = power_component_ys[j]
        pcwj = power_component_widths[j]
        pchj = power_component_heights[j]

        # Constrains for the components to not overlap with other (power) components
        s.add(Or(
            rcxi + rcwi <= pcxj,  # RC left from PC
            pcxj + pcwj <= rcxi,  # RC right from PC
            rcyi + rchi <= pcyj,  # RC below PC
            pcyj + pchj <= rcyi   # RC above PC
        ))

        # Case distinction: vertically connected
        connected_constraints.append(
            And(
                Or(
                    rcyi == pcyj + pchj,  # RC above PC
                    pcyj == rcyi + rchi   # PC above RC
                ),
                Or(
                    And(rcxi >= pcxj, rcxi < pcxj + pcwj),
                    And(rcxi < pcxj, rcxi + rcwi > pcxj)
                )
            )
        )
        # Case distinction: horizontally connected
        connected_constraints.append(
            And(
                Or(
                    rcxi == pcxj + pcwj,  # RC right of PC
                    pcxj == rcxi + rcwi   # PC left of RC
                ),
                Or(
                    And(rcyi >= pcyj, rcyi < pcyj + pchj),
                    And(rcyi < pcyj, rcyi + rchi > pcyj)
                )
            )
        )

    s.add(Or(*connected_constraints))

# Constrains for the power components
for i, (w, h) in enumerate(power_component_sizes):
    pcxi = power_component_xs[i]
    pcyi = power_component_ys[i]
    pcwi = power_component_widths[i]
    pchi = power_component_heights[i]

    # Constraints for turning components 90 degrees
    s.add(Or(And(pcwi == w, pchi == h),
             And(pcwi == h, pchi == w)))

    # Constraints for the components to be on the chip
    s.add(And(pcxi >= 0, pcyi >= 0, pcxi + pcwi <=
          CHIP_WIDTH, pcyi + pchi <= CHIP_HEIGHT))

    # Constrains for the components to not overlap with other (power) components
    # and to have the required minimum distance
    for j, _ in enumerate(power_component_sizes):
        # Skip 'ourselves' (we surely overlap with overselves, at least I hope we do)
        if i == j:
            continue

        pcxj = power_component_xs[j]
        pcyj = power_component_ys[j]
        pcwj = power_component_widths[j]
        pchj = power_component_heights[j]

        # No overlap (redundant)
        s.add(Or(pcxi + pcwi <= pcxj,
                 pcxj + pcwj <= pcxi,
                 pcyi + pchi <= pcyj,
                 pcyj + pchj <= pcyi))

        # Minimum distance between centers
        s.add(Or(abs(2 * pcxi + pcwi - (2 * pcxj + pcwj)) >= 2 * MIN_POWER_COMPONENT_DISTANCE,
                 abs((2 * pcyi + pchi) - (2 * pcyj + pchj)) >= 2 * MIN_POWER_COMPONENT_DISTANCE))


# print(s.check())
# print(s.model())
s.check()
print(s.sexpr())

draw_solution(s.model())
