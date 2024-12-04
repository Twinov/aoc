from collections import defaultdict

def solve(lines):
    p1, p2 = 0, 0

    XMAS = 'XMAS'
    p2_as = defaultdict(int)
    def dfs(r, c, search_pos, search_dir, part):
        nonlocal p1, lines
        if search_pos == len(XMAS):
            if part == 1:
                p1 += 1
            else:
                p2_as[(r - search_dir[0], c - search_dir[1])] += 1

            return


        next_r, next_c = r + search_dir[0], c + search_dir[1]
        if 0 <= next_r < len(lines) and 0 <= next_c < len(lines[next_r]):
            if lines[next_r][next_c] == XMAS[search_pos]:
                dfs(next_r, next_c, search_pos + 1, search_dir, part)
    
    search_dirs_cardinal = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    search_dirs_diagonal = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            if lines[r][c] == XMAS[0]:
                for i in range(len(search_dirs_cardinal)):
                    dfs(r, c, 1, search_dirs_cardinal[i], 1)
                for i in range(len(search_dirs_diagonal)):
                    dfs(r, c, 1, search_dirs_diagonal[i], 1)
            if lines[r][c] == XMAS[1]:
                for i in range(len(search_dirs_diagonal)):
                    dfs(r, c, 2, search_dirs_diagonal[i], 2)

    for count in p2_as.values():
        p2 += 1 if count == 2 else 0 

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)