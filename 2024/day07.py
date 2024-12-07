def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    def backtrack(values, value_idx, test_value, curr_value, part2=False):
        if curr_value > test_value:
            return False

        if value_idx == len(values):
            return test_value == curr_value
        
        return (
            backtrack(values, value_idx + 1, test_value, curr_value * values[value_idx], part2) or 
            backtrack(values, value_idx + 1, test_value, curr_value + values[value_idx], part2) or
            (part2 and backtrack(values, value_idx + 1, test_value, int(str(curr_value) + str(values[value_idx])), part2))
        )


    for line in lines:
        values = line.split(' ')
        test_value = int(values[0][0:len(values[0]) - 1])
        values = [int(value) for value in values[1:]]

        if backtrack(values, 0, test_value, 0):
            p1 += test_value

        if backtrack(values, 0, test_value, 0, part2=True):
            p2 += test_value

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)