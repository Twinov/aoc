import heapq

def solve(lines, example=True):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    NEXT_DIRS = {
        (-1, 0): (0, 1),
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0)
    }

    walls = set()
    start_tile, end_tile = (0, 0), (0, 0)
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            if lines[r][c] == '#':
                walls.add((r, c))
            elif lines[r][c] == 'S':
                start_tile = (r, c)
            elif lines[r][c] == 'E':
                end_tile = (r, c)

    queue = [(0, start_tile, (0, 1), [])] # (cost, position, facing direction, path)
    tiles_min_cost = {}
    tiles_min_cost[(start_tile, (0, 1))] = 0
    best_cost, best_path_tiles = float('inf'), set()
    while queue:
        curr_cost, curr_pos, curr_dir, prev_path = heapq.heappop(queue)
        if curr_cost > best_cost:
            continue

        curr_path = [tile for tile in prev_path]
        curr_path.append(curr_pos)
        if curr_pos == end_tile:
            best_cost = curr_cost
            
            for tile in curr_path:
                best_path_tiles.add(tile)
            
        # move forwards
        movements = [(curr_cost + 1, (curr_pos[0] + curr_dir[0], curr_pos[1] + curr_dir[1]), curr_dir, curr_path)]

        # turn CW
        cw_dir = NEXT_DIRS[curr_dir]
        movements.append((curr_cost + 1001, (curr_pos[0] + cw_dir[0], curr_pos[1] + cw_dir[1]), cw_dir, curr_path))

        # turn CCW
        reverse_dir = NEXT_DIRS[cw_dir]
        ccw_dir = NEXT_DIRS[reverse_dir]
        movements.append((curr_cost + 1001, (curr_pos[0] + ccw_dir[0], curr_pos[1] + ccw_dir[1]), ccw_dir, curr_path))

        for movement in movements:
            if 0 <= movement[1][0] < len(lines) and 0 <= movement[1][1] < len(lines[0]) and movement[1] not in walls:
                state_key = (movement[1], movement[2])
                if state_key not in tiles_min_cost or movement[0] <= tiles_min_cost[state_key]:
                    heapq.heappush(queue, movement)
                    tiles_min_cost[state_key] = min(tiles_min_cost.get(state_key, float('inf')), movement[0])
    
    p1 = best_cost

    grid = [['.'] * len(lines[0]) for _ in range(len(lines))]
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if (r, c) in walls:
                grid[r][c] = '#'
            elif (r, c) in best_path_tiles:
                grid[r][c] = 'O'
                p2 += 1
        
    for row in grid:
        print(''.join(row))

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input, example=False)