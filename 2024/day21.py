def solve(lines, example=True):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    class Keypad:
        def __init__(self):
            self.buttons = {}

    class Button:
        def __init__(self, left=None, right=None, up=None, down=None):
            self.adj_dirs = {}
            if left:
                self.adj_dirs['<'] = left
            if right:
                self.adj_dirs['>']  = right
            if up:
                self.adj_dirs['^']  = up
            if down:
                self.adj_dirs['v']  = down

    KEYPAD_TYPE_NUMPAD = 'numpad'
    KEYPAD_TYPE_CONTROLLER = 'controller'

    keypad_layouts = {}
    keypad_layouts[KEYPAD_TYPE_NUMPAD] = Keypad()
    keypad_layouts[KEYPAD_TYPE_NUMPAD].buttons['A'] = Button(left='0', up='3')
    keypad_layouts[KEYPAD_TYPE_NUMPAD].buttons['0'] = Button(right='A', up='2')
    keypad_layouts[KEYPAD_TYPE_NUMPAD].buttons['1'] = Button(right='2', up='4')
    keypad_layouts[KEYPAD_TYPE_NUMPAD].buttons['2'] = Button(left='1', right='3', up='5', down='0')
    keypad_layouts[KEYPAD_TYPE_NUMPAD].buttons['3'] = Button(left='2', up='6', down='A')
    keypad_layouts[KEYPAD_TYPE_NUMPAD].buttons['4'] = Button(right='5', down='1', up='7')
    keypad_layouts[KEYPAD_TYPE_NUMPAD].buttons['5'] = Button(left='4', right='6', up='8', down='2')
    keypad_layouts[KEYPAD_TYPE_NUMPAD].buttons['6'] = Button(left='5', down='3', up='9')
    keypad_layouts[KEYPAD_TYPE_NUMPAD].buttons['7'] = Button(right='8', down='4')
    keypad_layouts[KEYPAD_TYPE_NUMPAD].buttons['8'] = Button(left='7', right='9', down='5')
    keypad_layouts[KEYPAD_TYPE_NUMPAD].buttons['9'] = Button(left='8', down='6')

    keypad_layouts[KEYPAD_TYPE_CONTROLLER] = Keypad()
    keypad_layouts[KEYPAD_TYPE_CONTROLLER].buttons['A'] = Button(left='^', down='>')
    keypad_layouts[KEYPAD_TYPE_CONTROLLER].buttons['^'] = Button(right='A', down='v')
    keypad_layouts[KEYPAD_TYPE_CONTROLLER].buttons['<'] = Button(right='v')
    keypad_layouts[KEYPAD_TYPE_CONTROLLER].buttons['v'] = Button(left='<', up='^', right='>')
    keypad_layouts[KEYPAD_TYPE_CONTROLLER].buttons['>'] = Button(up='A', left='v')
    
    keypad_cache = {}
    def get_key_path(keypad_layout_id, start, end):
        cache_key = (keypad_layout_id, start, end)
        if cache_key in keypad_cache:
            return keypad_cache[cache_key]
        
        if start == end:
            return []

        buttons_q, visited, depth = [(start, [])], set(), 0
        while buttons_q:
            next_q = []

            while buttons_q:
                curr_button, curr_path = buttons_q.pop()
                
                if curr_button == end:
                    if cache_key not in keypad_cache:
                        keypad_cache[cache_key] = [] 
                    keypad_cache[cache_key].append(''.join(curr_path))
                
                for adj_dir, adj_button in keypad_layouts[keypad_layout_id].buttons[curr_button].adj_dirs.items():
                    next_path = [d for d in curr_path]
                    next_path.append(adj_dir)
                    next_q.append((adj_button, next_path))

            if cache_key in keypad_cache:
                return keypad_cache[cache_key]

            depth += 1
            buttons_q = next_q

    presses_needed_cache = {}
    def get_presses_needed(button_sequence, keypad_layout_id):
        cache_key = (button_sequence, keypad_layout_id)
        if cache_key in presses_needed_cache:
            return presses_needed_cache[cache_key]

        curr_button = 'A'
        button_presses_combos = ['']
        for idx in range(len(button_sequence)):
            next_button = button_sequence[idx]

            prev_combos = [bpc for bpc in button_presses_combos]
            next_bpcs = []
            for new_combo in get_key_path(keypad_layout_id, curr_button, next_button):
                for pc in prev_combos:
                    next_bpcs.append(pc + new_combo + 'A')

            if next_bpcs:
                button_presses_combos = next_bpcs
            else:
                button_presses_combos = [prev_combo + 'A' for prev_combo in prev_combos]

            curr_button = next_button

        presses_needed_cache[cache_key] = button_presses_combos
        return presses_needed_cache[cache_key]
    
    shortest_sequence_cache = {}
    def get_shortest_sequence_level_wise(button_sequence, depth):
        if depth == 0:
            return len(button_sequence)

        cache_key = (button_sequence, depth)
        if cache_key in shortest_sequence_cache:
            return shortest_sequence_cache[cache_key]

        split_sequences, curr_sequence = [], []
        for c in button_sequence:
            curr_sequence.append(c)
            if c == 'A':
                split_sequences.append(''.join(curr_sequence))
                curr_sequence = []

        total_button_presses = 0
        for seq in split_sequences:
            curr_sequence_min = float('inf')
            possible_paths = get_presses_needed(seq, KEYPAD_TYPE_CONTROLLER)
            for path in possible_paths:
                curr_sequence_min = min(curr_sequence_min, get_shortest_sequence_level_wise(path, depth-1))
            total_button_presses += curr_sequence_min
        
        shortest_sequence_cache[cache_key] = total_button_presses
        return shortest_sequence_cache[cache_key]
        
    for code in lines:
        numpad_button_presses_combinations = get_presses_needed(code, KEYPAD_TYPE_NUMPAD)
        
        # part 1, brute force but it prints out the sequence
        robot_button_presses_combinations = set()
        for numpad_combo in numpad_button_presses_combinations:
            for robot_combo in get_presses_needed(numpad_combo, KEYPAD_TYPE_CONTROLLER):
                robot_button_presses_combinations.add((robot_combo, numpad_combo))
        
        my_button_presses_combinations = set()
        min_combo = ('', '', '')
        for robot_combo, numpad_combo in robot_button_presses_combinations:
            for my_combo in get_presses_needed(robot_combo, KEYPAD_TYPE_CONTROLLER):
                if min_combo[0] == '' or len(min_combo[0]) > len(my_combo):
                    min_combo = (my_combo, robot_combo, numpad_combo, code)
                my_button_presses_combinations.add(my_combo)

        # part 2, only get the length
        min_len_25_deep = float('inf')
        for numpad_combo in numpad_button_presses_combinations:
            min_len_25_deep = min(min_len_25_deep, get_shortest_sequence_level_wise(numpad_combo, 25))

        numeric_part_of_code = []
        for char in code:
            if char in '1234567890':
                numeric_part_of_code.append(char)
        numeric_part_of_code = int(''.join(numeric_part_of_code))
        p1 += numeric_part_of_code * len(min_combo[0])
        p2 += numeric_part_of_code * min_len_25_deep

        print(code, len(min_combo[0]), min_combo, min_len_25_deep)
            
    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input, example=False)