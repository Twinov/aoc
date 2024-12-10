def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    grid = [[0] * len(lines[0]) for _ in range(len(lines))]
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            grid[r][c] = int(lines[r][c])

    reachable_peaks = {} # (set of unique peaks that can be reached from (r, c), # of paths there are to a peak from (r, c))
    def find_peaks(r, c):
        if (r, c) in reachable_peaks:
            return reachable_peaks[(r, c)]

        if grid[r][c] == 9:
            return [[(r, c)], 1]
        
        unique_reachable_peaks, reachable_peak_paths = set(), 0
        dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for dr, dc in dirs:
            next_r, next_c = r + dr, c + dc
            if 0 <= next_r < len(grid) and 0 <= next_c < len(grid[next_r]):
                if grid[next_r][next_c] == grid[r][c] + 1:
                    unique_peaks, paths = find_peaks(next_r, next_c)
                    
                    for peak in unique_peaks:
                        unique_reachable_peaks.add(peak)

                    reachable_peak_paths += paths
        
        reachable_peaks[(r, c)] = (unique_reachable_peaks, reachable_peak_paths)
        return reachable_peaks[(r, c)]
    
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 0:
                unique_peaks, paths = find_peaks(r, c)
                p1 += len(unique_peaks)
                p2 += paths

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)