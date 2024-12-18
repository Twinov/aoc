import heapq

def solve(lines, example=True):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    BYTES_TO_SIMULATE = 12 if example else 1024
    ROW_MAX = COL_MAX = 7 if example else 71

    falling_bytes = [(int(r), int(c)) for c, r in map(lambda x: x.split(','), lines)]
    corrupted_memory = set()
    for i in range(BYTES_TO_SIMULATE):
        corrupted_memory.add(falling_bytes[i])

    def print_grid(corrupted_memory, path):
        grid = [['.'] * COL_MAX for _ in range(ROW_MAX)]
        for r in range(ROW_MAX):
            for c in range(COL_MAX):
                if (r, c) in corrupted_memory:
                    grid[r][c] = '#'
                elif (r, c) in path:
                    grid[r][c] = 'O'
        
        for row in grid:
            print(''.join(row))
        print()

    def find_path(corrupted_memory): 
        q = [(0, (0, 0), [])]
        seen = {}
        seen[(0, 0)] = 0
        path = None
        while q:
            cost, pos, prev_path = heapq.heappop(q)
            curr_path = [space for space in prev_path]
            curr_path.append(pos)
            if seen[pos] > cost:
                continue

            if pos == (ROW_MAX - 1, COL_MAX - 1):
                path = set(curr_path)
                return (cost, path)

            dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
            for dr, dc in dirs:
                next_r, next_c = pos[0] + dr, pos[1] + dc
                next_pos, next_cost = (next_r, next_c), cost + 1
                if 0 <= next_r < ROW_MAX and 0 <= next_c < COL_MAX and not next_pos in corrupted_memory:
                    if next_cost < seen.get(next_pos, float('inf')):
                        seen[next_pos] = next_cost
                        heapq.heappush(q, (next_cost, next_pos, curr_path))
        
        return (-1, set())
    

    # part 1
    p1, path = find_path(corrupted_memory)
    print_grid(corrupted_memory, path)

    # part 2
    for i in range(BYTES_TO_SIMULATE, len(falling_bytes)):
        corrupted_memory.add(falling_bytes[i])
        if falling_bytes[i] in path:
            cost, path = find_path(corrupted_memory)
            print_grid(corrupted_memory, path)

            if not path:
                p2 = f'{falling_bytes[i][1]},{falling_bytes[i][0]}'
                break

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input, example=False)