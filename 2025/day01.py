def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    curr = 50    
    for line in lines:
        direction, degree = line[0], int(line[1:])
        movement = degree if direction == 'R' else -degree
        prev = curr
        curr = curr + movement
        clicks_past_zero, curr = divmod(curr, 100)
        if curr == 0:
            p1 += 1
            if direction == 'L':
                p2 += 1

        p2 += abs(clicks_past_zero)
        
        if prev == 0 and clicks_past_zero:
            p2 -= 1
        
    
    if curr == 0:
        p2 += 1

    print('part 1:', p1)
    print('part 2:', p2) # something wrong lol bsearched it

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)