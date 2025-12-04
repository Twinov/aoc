def solve(lines):
    lines = [list(line.strip()) for line in lines]
    p1, p2 = 0, 0
    
    iter_num, continue_removing = 0, True
    while continue_removing:
        iter_num, continue_removing = iter_num + 1, False
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j] not in ('X', '@'):
                    continue

                dirs = [(-1, -1), (-1, 0), (0, -1), (-1, 1), (1, -1), (1, 0), (0, 1), (1, 1)]
                adj_boxes = 0
                for di, dj in dirs:
                    if 0 <= i + di < len(lines) and 0 <= j + dj < len(lines[i]):
                        if lines[i + di][j + dj] in ('X', '@'):
                            adj_boxes += 1

                if adj_boxes < 4:
                    if iter_num == 1:
                        p1 += 1
                    p2 += 1
                    lines[i][j] = 'X'
                    continue_removing = True

        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j] == 'X':
                    lines[i][j] = '.'

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)
