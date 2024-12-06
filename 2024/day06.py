import sys

def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    visited_spaces = set()
    def move(curr_r, curr_c, facing_dir_idx, p2_cache = None, p2_obstacle = None):
        if p2_cache != None:
            nonlocal p2
            cache_key = (curr_r, curr_c, facing_dir_idx)
            if cache_key in p2_cache:
                p2 += 1
                return
            p2_cache.add(cache_key)
        else:
            visited_spaces.add((curr_r, curr_c))

        next_r, next_c = curr_r + directions[facing_dir_idx][0], curr_c + directions[facing_dir_idx][1]
        
        while (0 <= next_r < len(lines) and 0 <= next_c < len(lines[next_r])) and (lines[next_r][next_c] == '#' or (next_r, next_c) == p2_obstacle):
            facing_dir_idx = (facing_dir_idx + 1) % 4
            next_r, next_c = curr_r + directions[facing_dir_idx][0], curr_c + directions[facing_dir_idx][1]
        
        if not (0 <= next_r < len(lines) and 0 <= next_c < len(lines[next_r])):
            return
        
        move(next_r, next_c, facing_dir_idx, p2_cache, p2_obstacle)

    for r in range(len(lines)):
        for c in range(len(lines[r])):
            if lines[r][c] == '^':
                start_pos = (r, c)

    move(start_pos[0], start_pos[1], 0)
    
    # part 1 visualization
    covered_grid = [['.'] * len(lines[0]) for _ in range(len(lines))]
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            if lines[r][c] == '^':
                covered_grid[r][c] = '^'
                p1 += 1
            elif (r, c) in visited_spaces:
                covered_grid[r][c] = 'X'
                p1 += 1
            elif lines[r][c] == '#':
                covered_grid[r][c] = '#'
    
    for line in covered_grid:
        print(''.join(line))


    # part 2 brute force
    for visited_space in visited_spaces:
        move(start_pos[0], start_pos[1], 0, set(), visited_space)

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

sys.setrecursionlimit(50000000)

solve(example_input)
solve(actual_input)