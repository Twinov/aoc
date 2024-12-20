from collections import defaultdict

def solve(lines, example=True):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    start_pos = end_pos = (0, 0)
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            if lines[r][c] == 'S':
                start_pos = (r, c)
            elif lines[r][c] == 'E':
                end_pos = (r, c)

    # create path
    path = []
    visited = set()
    curr_pos = start_pos
    while curr_pos != end_pos:
        path.append(curr_pos)
        visited.add(curr_pos)

        dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for dr, dc in dirs:
            next_r, next_c = curr_pos[0] + dr, curr_pos[1] + dc
            if 0 <= next_r < len(lines) and 0 <= next_c < len(lines[next_r]) and (next_r, next_c) not in visited and lines[next_r][next_c] != '#':
                curr_pos = (next_r, next_c)
                break
    
    # add on end position
    path.append(curr_pos)
    visited.add(curr_pos)

    def get_cheat_times_saved(cheat_length):
        # iterates over each pair of points (start, end) in the path
        # and checks whether the manhattan distance is <= threshold (cheat length)
        # if it is, then we're able to utilize a cheat to save <manhattan dist> amount of time
        # :)

        def manhattan_distance(start_point, end_point):
            return abs(start_point[0] - end_point[0]) + abs(start_point[1] - end_point[1])
            
        times_saved = defaultdict(int)
        for i in range(len(path)):
            for j in range(i+1, len(path)):
                if manhattan_distance(path[i], path[j]) <= cheat_length:
                    times_saved[j - i - manhattan_distance(path[i], path[j])] += 1
        
        sorted_times_saved = []
        for time_saved, occurrences in times_saved.items():
            sorted_times_saved.append((time_saved, occurrences))

        sorted_times_saved.sort()
        sorted_times_saved.reverse()

        return sorted_times_saved

    CHEAT_LENGTH_SILVER, CHEAT_LENGTH_GOLD = 2, 20
    CHEAT_THRESHOLD_TO_COUNT = 100
    for cheat_time_saved, occurrences in get_cheat_times_saved(CHEAT_LENGTH_SILVER):
        if cheat_time_saved >= CHEAT_THRESHOLD_TO_COUNT:
            p1 += occurrences
    
    for cheat_time_saved, occurrences in get_cheat_times_saved(CHEAT_LENGTH_GOLD):
        if cheat_time_saved >= (CHEAT_THRESHOLD_TO_COUNT if not example else 50):
            p2 += occurrences

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input, example=False)