def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    nums = [int(n) for n in lines[0].split(' ')]

    memo = {}
    # returns the total number of numbers that a given n expands into with <remaining_blinks> blinks left 
    def solve_total_expansion_size_subproblem(n, remaining_blinks):
        if remaining_blinks == 0:
            return 1

        if (n, remaining_blinks) in memo:
            return memo[(n, remaining_blinks)]
        
        subproblem_answer = 0
        str_n = str(n)
        if n == 0:
            subproblem_answer += solve_total_expansion_size_subproblem(1, remaining_blinks - 1)
        elif len(str_n) % 2 == 0:
            left, right = str_n[:len(str_n) // 2], str_n[len(str_n) // 2:]
            subproblem_answer += solve_total_expansion_size_subproblem(int(left), remaining_blinks - 1)
            subproblem_answer += solve_total_expansion_size_subproblem(int(right), remaining_blinks - 1)
        else:
            subproblem_answer += solve_total_expansion_size_subproblem(n * 2024, remaining_blinks - 1)

        memo[(n, remaining_blinks)] = subproblem_answer
        return memo[(n, remaining_blinks)]

    number_of_blinks_silver = 25
    number_of_blinks_gold = 75
    p1 = sum(solve_total_expansion_size_subproblem(n, number_of_blinks_silver) for n in nums)
    p2 = sum(solve_total_expansion_size_subproblem(n, number_of_blinks_gold) for n in nums)

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)