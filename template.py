def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)