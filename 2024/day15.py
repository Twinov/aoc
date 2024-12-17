def solve(lines, example=True):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    small_box_locations = set()
    large_box_locations_left = set()
    large_box_locations_right = set()
    small_wall_locations = set()
    large_wall_locations = set()
    robot_location_small = (0, 0)
    robot_location_large = (0, 0)
    MAX_R_SMALL, MAX_C_SMALL = 0, 0
    MAX_R_LARGE, MAX_C_LARGE = 0, 0

    def get_grid_score(small_grid=True):
        boxes = small_box_locations if small_grid else large_box_locations_left
        tot_score = 0
        for box in boxes:
            tot_score += 100 * box[0] + box[1]
        
        return tot_score

    def print_grid(small_grid=True):
        max_r = MAX_R_SMALL if small_grid else MAX_R_LARGE
        max_c = MAX_C_SMALL if small_grid else MAX_C_LARGE
        grid = [['.'] * (max_c) for _ in range(max_r)]
        wall_locations = small_wall_locations if small_grid else large_wall_locations
        robot_location = robot_location_small if small_grid else robot_location_large
        for r in range(max_r):
            for c in range(max_c):
                if (r, c) in wall_locations:
                    grid[r][c] = '#'
                elif small_grid and (r, c) in small_box_locations:
                    grid[r][c] = 'O'
                elif not small_grid and (r, c) in large_box_locations_left:
                    grid[r][c] = '['
                elif not small_grid and (r, c) in large_box_locations_right:
                    grid[r][c] = ']'
                elif (r, c) == robot_location:
                    grid[r][c] = '@'
        
        for r in grid:
            print(''.join(r))

    building_map = True
    for r in range(len(lines)):
        if len(lines[r]) == 0:
            building_map = False

            MAX_R_SMALL = max(list(map(lambda box: box[0], small_box_locations)) + list(map(lambda wall: wall[0], small_wall_locations))) + 1
            MAX_C_SMALL = max(list(map(lambda box: box[1], small_box_locations)) + list(map(lambda wall: wall[1], small_wall_locations))) + 1

            MAX_R_LARGE = max(list(map(lambda box: box[0], large_box_locations_right)) + list(map(lambda wall: wall[0], large_wall_locations))) + 1
            MAX_C_LARGE = max(list(map(lambda box: box[1], large_box_locations_right)) + list(map(lambda wall: wall[1], large_wall_locations))) + 1

            print_grid()
            print_grid(small_grid=False)

            continue

        for c in range(len(lines[r])):
            if building_map:
                if lines[r][c] == '#':
                    small_wall_locations.add((r, c))
                    large_wall_locations.add((r, c * 2))
                    large_wall_locations.add((r, c * 2 + 1))
                elif lines[r][c] == 'O':
                    small_box_locations.add((r, c))
                    large_box_locations_left.add((r, c * 2))
                    large_box_locations_right.add((r, c * 2 + 1))
                elif lines[r][c] == '@':
                    robot_location_small = (r, c)
                    robot_location_large = (r, c * 2)

            else:
                direction = (0, 0)
                if lines[r][c] == '^':
                    direction = (-1, 0)
                elif lines[r][c] == 'v':
                    direction = (1, 0)
                elif lines[r][c] == '<':
                    direction = (0, -1)
                elif lines[r][c] == '>':
                    direction = (0, 1)
                
                # part 1, small grid
                moving_stack = []
                small_move_possible = True
                prev_location, next_location = robot_location_small, (robot_location_small[0] + direction[0], robot_location_small[1] + direction[1])
                if next_location in small_wall_locations:
                    small_move_possible = False
                moving_stack.append((prev_location, next_location, 'robot'))
                
                while next_location in small_box_locations:
                    prev_location, next_location = next_location, (next_location[0] + direction[0], next_location[1] + direction[1])
                    moving_stack.append((prev_location, next_location, 'box'))
                
                if next_location in small_wall_locations:
                    small_move_possible = False
                
                if small_move_possible:
                    # move everything in the stack one by one
                    reverse_direction = (direction[0] * -1, direction[1] * -1)
                    while moving_stack:
                        moving_from, moving_to, moving_type = moving_stack.pop()
                        if moving_type == 'box':
                            small_box_locations.remove(moving_from)
                            small_box_locations.add(moving_to)

                        elif moving_type == 'robot':
                            robot_location_small = moving_to

                # part 2, large grid
                moving_stack = []
                large_move_possible = True
                prev_location, next_location = robot_location_large, (robot_location_large[0] + direction[0], robot_location_large[1] + direction[1])
                if next_location in large_wall_locations:
                    large_move_possible = False
                moving_stack.append((prev_location, next_location, 'robot'))

                pushes_stack = [next_location]
                done_pushes = set()
                while pushes_stack and large_move_possible:
                    enqueued_pushes = []

                    while pushes_stack:
                        prev_moving_to = pushes_stack.pop()
                        if not (prev_moving_to in large_box_locations_left or prev_moving_to in large_box_locations_right) or prev_moving_to in done_pushes or not large_move_possible:
                            continue
                        done_pushes.add(prev_moving_to) # lol, there's definitely a better way of doing the visited set

                        curr_moving_to = prev_moving_to[0] + direction[0], prev_moving_to[1] + direction[1]
                        if curr_moving_to in large_wall_locations:
                            large_move_possible = False
                            break

                        enqueued_pushes.append(curr_moving_to)
                        moving_stack.append((prev_moving_to, curr_moving_to, 'box_right' if prev_moving_to in large_box_locations_right else 'box_left'))

                        if lines[r][c] in '^v':
                            # have to enqueue the push on the other side of the box
                            if prev_moving_to in large_box_locations_left:
                                enqueued_pushes.append((prev_moving_to[0], prev_moving_to[1] + 1))
                            else:
                                enqueued_pushes.append((prev_moving_to[0], prev_moving_to[1] - 1))
                    
                    pushes_stack = enqueued_pushes
                
                if not large_move_possible:
                    continue

                while moving_stack:
                    moving_from, moving_to, moving_type = moving_stack.pop()
                    if moving_type == 'box_left':
                        large_box_locations_left.remove(moving_from)
                        large_box_locations_left.add(moving_to)

                    elif moving_type == 'box_right':
                        large_box_locations_right.remove(moving_from)
                        large_box_locations_right.add(moving_to)

                    elif moving_type == 'robot':
                        robot_location_large = moving_to

    print_grid()
    print_grid(small_grid=False)

    p1 = get_grid_score()
    p2 = get_grid_score(small_grid=False)

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input, example=False)