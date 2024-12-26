from collections import defaultdict

def solve(lines, example=True):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    SWAPS = {
        'z27': 'bfq',
        'fjp': 'bng',
        'z18': 'hmt',
        'hkh': 'z31',
    }

    for k, v in list(SWAPS.items()):
        SWAPS[v] = k # reverse map it back

    def set_up_gates(use_swaps=False):
        gates = []
        for line in lines:
            params = line.split(' ')
            if '->' in line:
                if use_swaps and params[-1] in SWAPS:
                    params[-1] = SWAPS[params[-1]]

                gates.append((params[0], params[2], params[1], params[-1]))
            elif ':' in line:
                wire_states[params[0][:-1]] = params[1] == '1'
        
        return gates

    def process_all_gates():
        processing_gates = True
        while processing_gates:
            processing_gates = False
            for input_1, input_2, operator, output in gates:
                if not solve_gate(input_1, input_2, operator, output):
                    processing_gates = True

    def solve_gate(input_1, input_2, operator, output):
        init_output_state = wire_states[output]
        match operator:
            case 'AND':
                wire_states[output] = wire_states[input_1] and wire_states[input_2]
            case 'OR':
                wire_states[output] = wire_states[input_1] or wire_states[input_2]
            case 'XOR':
                wire_states[output] = (wire_states[input_1] and not wire_states[input_2]) or (not wire_states[input_1] and wire_states[input_2])
            case _:
                print('lol?')
        
        return init_output_state == wire_states[output]
    
    def get_xyz():
        binary_numbers = [[0] * 50 for _ in range(3)]
        for wire, is_on in sorted(wire_states.items()):
            if is_on and wire[0] == 'x':
                wire_num = int(wire.split('x')[1])
                binary_numbers[0][wire_num] = 1
            if is_on and wire[0] == 'y':
                wire_num = int(wire.split('y')[1])
                binary_numbers[1][wire_num] = 1
            if is_on and wire[0] == 'z':
                wire_num = int(wire.split('z')[1])
                binary_numbers[2][wire_num] = 1
        
        for binary_number in binary_numbers:
            binary_number.reverse()

        finished_numbers = {}
        for number_label, binary_number in zip(('x', 'y', 'z'), binary_numbers):
            decimal_number = int(''.join(str(b) for b in binary_number), 2)
            print(number_label, ''.join(str(b) for b in binary_number), decimal_number)
            finished_numbers[number_label] = decimal_number
        
        return finished_numbers
    
    # part 1, no swaps
    wire_states = defaultdict(bool)
    gates = set_up_gates()
    process_all_gates()

    p1 = get_xyz()['z']

    # part 2, use swaps
    wire_states = defaultdict(bool)
    gates = set_up_gates(use_swaps=True)
    process_all_gates()
    finished_numbers = get_xyz()

    if not finished_numbers['x'] + finished_numbers['y'] == finished_numbers['z']:
        print(f'not found yet!!!, {finished_numbers['z'] - finished_numbers['x']}')
    else:
        print('got the right answer!!!!!!!!!!!!!!!!!! :) :) :) :) :)')
        p2 = []
        for swapped_gate in SWAPS.keys():
            p2.append(swapped_gate)
        
        p2.sort()
        p2 = ','.join(p2)

    ### all the below are helpers I wrote to get the mismatched gate outputs

    def get_wire_dependencies(label):
        dependencies = []
        for gate in gates:
            if any(label in param for param in gate):
                dependencies.append((gate[3], gate[0], gate[2], gate[1]))

        return dependencies

    def get_wire_source(label):
        for gate in gates:
            if label == gate[3]:
                return (gate[3], gate[0], gate[2], gate[1])

    # first check: all z bits need to be a XOR between prev carry bit and AND of corresponding x/y except z45 (final carry)
    suspicious_gates = []
    for gate in get_wire_dependencies('z'):
        if 'XOR' != gate[2] and gate[0] != 'z45':
            print(gate, 'is a z bit that is not the result of a XOR!!!')
            suspicious_gates.append(gate)
    
    # next check: XORs that aren't from x/y should all go to z
    for gate in get_wire_dependencies('XOR'):
        if 'y' not in gate[1] and 'y' not in gate[3]:
            if 'z' not in gate[0]:
                print(gate, 'is a XOR that isnt from x/y and doesnt go to z!!!')
                suspicious_gates.append(gate)

    # need some deeper checks in the dependency trees to find remaining suspicious gates
    for i in range(45):
        wire_num = i if i >= 10 else f'0{i}'
        print(f'dependency tree for wire z{wire_num}')
        printed = set()
        for gate in sorted(get_wire_dependencies(f'z{wire_num}')):
            print(gate)

            # basically do a dfs to print dependencies a couple deep
            visited = set(gate[0])
            def dfs(curr_wire, depth):
                curr_gate = get_wire_source(curr_wire)
                if depth > 2 or curr_gate == None:
                    return
                
                print(f'{'--' * depth} {curr_gate}')

                # some rules for weird gates after looking at the outputs
                if depth == 1:
                    if curr_gate[2] == 'XOR':
                        if curr_gate[1][0] not in 'xy':
                            print('z XOR dependency isnt from an xy!!!!!', curr_gate)
                            suspicious_gates.append(curr_gate)
                    elif curr_gate[2] == 'OR':
                        if curr_gate[1][0] in 'xy':
                            print('z OR dependency is from an xy!!!!!', curr_gate)
                            suspicious_gates.append(curr_gate)
                    elif curr_gate[1] not in ('y00', 'x00'): # half adder special handling
                        print('z has a non-OR/XOR dependency!!!!!', curr_gate)
                        suspicious_gates.append(curr_gate)

                next_gates = []
                if get_wire_source(curr_gate[1]):
                    next_gates.append(get_wire_source(curr_gate[1]))
                if get_wire_source(curr_gate[3]):
                    next_gates.append(get_wire_source(curr_gate[3]))

                for next_gate in next_gates:
                    next_wires = (next_gate[1], next_gate[3])
                    for next_wire in next_wires:
                        if next_wire not in visited:
                            visited.add(next_wire)
                            dfs(next_wire, depth + 1)
            
            dfs(gate[1], 1)
            dfs(gate[3], 1)
        
        print()
        
    print('suspicious gates count:', len(suspicious_gates), suspicious_gates)
    for gate in suspicious_gates:
        print(f'{gate[1]} {gate[2]} {gate[3]} -> {gate[0]}')
 
    print()

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

#solve(example_input) # no example input that makes sense for part 2 and 90% of the code I wrote
solve(actual_input, example=False)