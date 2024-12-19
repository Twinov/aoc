from collections import defaultdict

def solve(lines, example=True):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    available_patterns = set(lines[0].split(', '))
    wanted_designs = [design for design in lines[2:]]

    cached_patterns = {}
    def backtrack(design_number, pattern_idx):
        if pattern_idx == len(wanted_designs[design_number]):
            return 1

        cache_key = wanted_designs[design_number][pattern_idx:]
        if cache_key in cached_patterns:
            return cached_patterns[cache_key]
        
        ways_to_make_design = 0
        for pattern in available_patterns:
            if pattern_idx + len(pattern) <= len(wanted_designs[design_number]) and \
                wanted_designs[design_number][pattern_idx:pattern_idx + len(pattern)] == pattern:

                ways_to_make_design += backtrack(design_number, pattern_idx + len(pattern))

        cached_patterns[cache_key] = ways_to_make_design
        return cached_patterns[cache_key]

    for i, wanted_design in enumerate(wanted_designs):
        if (ways_to_make_design := backtrack(i, 0)) > 0:
            p1 += 1
            p2 += ways_to_make_design

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input, example=False)