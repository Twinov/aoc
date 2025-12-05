def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    ranges, ingredients = [], []

    for line in lines:
        if '-' in line:
            start, end = line.split('-')
            ranges.append([int(start), int(end)])
        elif line:
            ingredients.append(int(line))
    
    ingredients.sort()

    def merge_intervals(intervals):
        intervals.sort(key=lambda x: x[0])
        sorted_intervals = []
        for s, e in intervals:
            if not sorted_intervals or sorted_intervals[-1][1] < s:
                sorted_intervals.append([s, e])
            
            sorted_intervals[-1][1] = max(sorted_intervals[-1][1], e)
        
        return sorted_intervals

    ranges = merge_intervals(ranges)
    
    ranges_ptr, ingredients_ptr = 0, 0
    while ingredients_ptr < len(ingredients):
        while (
            ranges_ptr < len(ranges) and
            ingredients[ingredients_ptr] > ranges[ranges_ptr][1]
        ):
            ranges_ptr += 1

        if (
            ranges_ptr < len(ranges) and
            ranges[ranges_ptr][0] <= ingredients[ingredients_ptr] <= ranges[ranges_ptr][1]
        ):
            p1 += 1
        
        ingredients_ptr += 1

    for s, e in ranges:
        p2 += e - s + 1

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)
