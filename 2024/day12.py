from collections import defaultdict

def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    plant_perimeters = defaultdict(int)
    plant_fencings = {}
    plant_areas = defaultdict(int)

    cache = {}
    def dfs(r, c, region_marker):
        if (r, c) in cache:
            return
        cache[(r, c)] = True

        plant_areas[(lines[r][c], region_marker)] += 1

        dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for dr, dc in dirs:
            next_r, next_c = r + dr, c + dc
            if 0 <= next_r < len(lines) and 0 <= next_c < len(lines[next_r]) and lines[next_r][next_c] == lines[r][c]:
                dfs(next_r, next_c, region_marker)
            else:
                plant_perimeters[(lines[r][c], region_marker)] += 1
                plant_fencings[(r, c, region_marker, next_r, next_c)] = True
    
    regions_marked = 0
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            if (r, c) not in cache:
                dfs(r, c, regions_marked)
                regions_marked += 1

    # intuition for discounted fences: there needs to not be a fence above it or to the left of it
    discounted_fences_needed = defaultdict(int)
    for key in plant_fencings.keys():
        row, col, regions_marker, outer_bound_row, outer_bound_col = key
        has_fence_above = (row - 1, col, regions_marker, outer_bound_row - 1, outer_bound_col) in plant_fencings
        has_fence_left = (row, col - 1, regions_marker, outer_bound_row, outer_bound_col - 1) in plant_fencings
        if not has_fence_above and not has_fence_left:
            discounted_fences_needed[(lines[row][col], regions_marker)] += 1

    for key in plant_areas.keys():
        p1 += plant_areas[key] * plant_perimeters[key]
        p2 += plant_areas[key] * discounted_fences_needed[key] 

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)