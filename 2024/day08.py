from collections import defaultdict

def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    p1_antinode_positions, p2_antinode_positions = set(), set()
    antenna_positions = defaultdict(list)
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            if lines[r][c] != '.':
                antenna_positions[lines[r][c]].append((r, c))
                p2_antinode_positions.add((r, c))

    for freq in antenna_positions.keys():
        for i in range(len(antenna_positions[freq])):
            for j in range(i+1, len(antenna_positions[freq])):
                antenna_1, antenna_2 = antenna_positions[freq][i], antenna_positions[freq][j]
                r_dist, c_dist = antenna_2[0] - antenna_1[0], antenna_2[1] - antenna_1[1]

                # antinode 1 is the negative axis, antinode 2 is the positive axis
                antinode_1, antinode_2 = (antenna_1[0] - r_dist, antenna_1[1] - c_dist), (antenna_2[0] + r_dist, antenna_2[1] + c_dist)

                def test_in_bounds(pos):
                    return 0 <= pos[0] < len(lines) and 0 <= pos[1] < len(lines[0])

                first_antinode_added, second_antinode_added = False, False
                while test_in_bounds(antinode_1):
                    if not first_antinode_added:
                        p1_antinode_positions.add(antinode_1)
                        first_antinode_added = True
                    p2_antinode_positions.add(antinode_1)
                    antinode_1 = (antinode_1[0] - r_dist, antinode_1[1] - c_dist)
                while test_in_bounds(antinode_2):
                    if not second_antinode_added:
                        p1_antinode_positions.add(antinode_2)
                        second_antinode_added = True
                    p2_antinode_positions.add(antinode_2)
                    antinode_2 = (antinode_2[0] + r_dist, antinode_2[1] + c_dist)

    # visualization
    grid = [['.'] * len(lines[0]) for _ in range(len(lines))]
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            if lines[r][c] != '.':
                grid[r][c] = lines[r][c]
            elif (r, c) in p2_antinode_positions:
                grid[r][c] = '#'
    
    for row in grid:
        print(''.join(row))

    p1 = len(p1_antinode_positions)
    p2 = len(p2_antinode_positions)
    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)