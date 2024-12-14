from collections import defaultdict

def solve(lines, example=True):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    ROW_MAX, COL_MAX = 7, 11
    if not example:
        ROW_MAX, COL_MAX = 103, 101

    class Robot:
        def __init__(self, line):
            p, v = line.split(' ')
            p, v = p.split('=')[1], v.split('=')[1]
            p, v = p.split(','), v.split(',')
            self.r, self.c = int(p[1]), int(p[0])
            self.vr, self.vc = int(v[1]), int(v[0])
        
        def __str__(self):
            return f'pos ({self.r}, {self.c}) velocity ({self.vr}, {self.vc})'

        def move(self):
            self.r += self.vr
            self.c += self.vc

            self.r %= ROW_MAX
            self.c %= COL_MAX

    def get_grid_state(robots):
        positions = defaultdict(int)
        for robot in robots:
            positions[(robot.r, robot.c)] += 1
        
        grid = [['.'] * COL_MAX for _ in range(ROW_MAX)]
        for r in range(ROW_MAX):
            for c in range(COL_MAX):
                if (r, c) in positions:
                    grid[r][c] = str(positions[(r, c)])
        
        return grid

    def get_quadrants_score(robots):
        quadrants = [0] * 4
        for robot in robots:
            if robot.r < ROW_MAX // 2 and robot.c < COL_MAX // 2:
                quadrants[0] += 1
            elif robot.r < ROW_MAX // 2 and robot.c > COL_MAX // 2:
                quadrants[1] += 1
            elif robot.r > ROW_MAX // 2 and robot.c < COL_MAX // 2:
                quadrants[2] += 1
            elif robot.r > ROW_MAX // 2 and robot.c > COL_MAX // 2:
                quadrants[3] += 1

        tot_score = 1
        for quad_score in quadrants:
            tot_score *= quad_score
        return tot_score
    
    robots = []
    for line in lines:
        robots.append(Robot(line))

    seen_states = set()
    for i in range(1, 0xDEADBEEF):
        state_hash = []
        for robot in robots:
            robot.move()
            state_hash.append(str(robot))
        
        if i == 100:
            p1 = get_quadrants_score(robots)
            if example:
                break
        
        state_hash = ''.join(state_hash)
        if state_hash in seen_states and not example:
            print('Cycle detected at iteration', i)
            break
        seen_states.add(''.join(state_hash))

        for row in get_grid_state(robots):
            # Christmas tree state can be detected by a line of 30 ones in a row
            ones_in_a_row = 0
            for c in range(1, len(row)):
                if row[c] == row[c-1] == '1':
                    ones_in_a_row += 1
                
                    if ones_in_a_row == 30 and p2 == 0:
                        p2 = i

                        for row in get_grid_state(robots):
                            print(''.join(row))
                        print('Found Christmas tree at iteration', i)
        

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input, example=False)