def solve(lines):
    lines = [line for line in lines]
    p1, p2 = 0, 0

    columns, ops = [], []
    for line in lines:
        for i, c in enumerate(filter(lambda x: x.strip(), line.split(' '))):
            if line == lines[0]:
                columns.append([int(c)])
            elif line != lines[-1]:
                columns[i].append(int(c))
            else:
                ops.append(c)

    rtl_cols = []
    for j in range(len(lines[0])):
        rtl_cols.append([])
        for i in range(len(lines)):
            if lines[i][j] in '1234567890':
                rtl_cols[-1].append(lines[i][j])
    
    rtl_nums = [[]] 
    for c in rtl_cols:
        if not c:
            rtl_nums.append([])
        else:
            rtl_nums[-1].append(int(''.join(c)))
    rtl_nums.pop()

    def get_sol(columns, ops):
        overall_sol = 0
        for i, col in enumerate(columns):
            op = ops[i]
            sol = 0 if op == '+' else 1
            for c in col:
                if op == '+':
                    sol += c
                else:
                    sol *= c 
            overall_sol += sol
        return overall_sol
    
    p1 = get_sol(columns, ops)
    p2 = get_sol(rtl_nums, ops)

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)
