def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    curr = 50    
    for line in lines:
        direction, degree = line[0], int(line[1:])
        for _ in range(degree): #lol
            curr += 1 if direction == 'R' else -1
            curr %= 100
            if curr == 0:
                p2 += 1

        if curr == 0:
            p1 += 1

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)