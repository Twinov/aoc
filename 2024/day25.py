def solve(lines, example=True):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    keys, locks = [], []

    curr_key_or_lock, currently_building_key = [], True

    def flush_curr_key_or_lock():
        nonlocal curr_key_or_lock, currently_building_key
        if currently_building_key:
            keys.append(curr_key_or_lock)
        else:
            locks.append(curr_key_or_lock)

        curr_key_or_lock = []

    for line in lines:
        if not line:
            flush_curr_key_or_lock()

        elif not curr_key_or_lock:
            currently_building_key = '.' in line
            curr_key_or_lock = [0] * len(line)
        
        else:
            for i, c in enumerate(line):
                curr_key_or_lock[i] += 1 if c == '#' else 0
    
    flush_curr_key_or_lock()
    
    AVAILABLE_SPACE = 6 # in my implementation keys have one extra than what the example was counting
    for lock in locks:
        for key in keys:
            if all(key[i] + lock[i] <= AVAILABLE_SPACE for i in range(len(lock))):
                p1 += 1

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input, example=False)