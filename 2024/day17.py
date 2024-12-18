from collections import deque

def solve(lines, example=True):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    register_a, register_b, register_c = int(lines[0].split(' ')[2]), int(lines[1].split(' ')[2]), int(lines[2].split(' ')[2])

    instructions = [int(num) for num in lines[4].split(' ')[1].split(',')]
    instruction_pointer = 0

    print(instructions)

    def get_combo_op(operand):
        nonlocal register_a, register_b, register_c
        combo_op = operand
        if combo_op == 4:
            combo_op = register_a
        elif combo_op == 5:
            combo_op = register_b
        elif combo_op == 6:
            combo_op = register_c
        elif combo_op == 7:
            print('Found error!', instruction, operand)
        
        return combo_op

    def run_program(print_instructions=True, find_quine_for=None):
        nonlocal register_a, register_b, register_c
        instruction_pointer = 0
        output = []
        while True:
            if instruction_pointer > len(instructions) - 1:
                if print_instructions:
                    print('HALT')
                break

            instruction, operand = instructions[instruction_pointer], instructions[instruction_pointer + 1]

            if instruction == 0:
                if print_instructions:
                    print(f'adv {operand}, register_a: {register_a}, register_b: {register_b}, register_c: {register_c}')

                register_a = register_a // (2**get_combo_op(operand))
            
            elif instruction == 1:
                if print_instructions:
                    print(f'bxl {operand}, register_a: {register_a}, register_b: {register_b}, register_c: {register_c}')
                register_b = register_b ^ operand

            elif instruction == 2:
                if print_instructions:
                    print(f'bst {operand}, register_a: {register_a}, register_b: {register_b}, register_c: {register_c}')
                register_b = get_combo_op(operand) % 8

            elif instruction == 3:
                if print_instructions:
                    print(f'jnz {operand}, register_a: {register_a}, register_b: {register_b}, register_c: {register_c}')
                if register_a != 0:
                    instruction_pointer = operand - 2

            elif instruction == 4:
                if print_instructions:
                    print(f'bxc {operand}, register_a: {register_a}, register_b: {register_b}, register_c: {register_c}')
                register_b = register_b ^ register_c

            elif instruction == 5:
                if print_instructions:
                    print(f'out {operand}, register_a: {register_a}, register_b: {register_b}, register_c: {register_c}')
                output.append(get_combo_op(operand) % 8)

                if find_quine_for and not output[-1] == find_quine_for[len(output) - 1]:
                    break

            elif instruction == 6:
                if print_instructions:
                    print(f'bdv {operand}, register_a: {register_a}, register_b: {register_b}, register_c: {register_c}')
                register_b = register_a // (2**get_combo_op(operand))

            elif instruction == 7:
                if print_instructions:
                    print(f'cdv {operand}, register_a: {register_a}, register_b: {register_b}, register_c: {register_c}')
                register_c = register_a // (2**get_combo_op(operand))

            instruction_pointer += 2

        return output

    p1 = ','.join(str(val) for val in run_program())

    q = deque([(0, len(instructions) - 1)])
    best_quine = float('inf')
    while q:
        register_val, numbers_needed = q.popleft()
        if numbers_needed < 0:
            register_a = register_val
            output = run_program(print_instructions=False)

            if all(ins_1 == ins_2 for ins_1, ins_2 in zip(instructions, output)):
                print('Found quine!', register_val)
                best_quine = min(best_quine, register_val)
            
            continue

        for bits in range(8):
            test_val = (register_val << 3) + bits
            register_a = test_val

            output = run_program(print_instructions=False)

            if output[0] == instructions[numbers_needed] and len(output) == len(instructions[numbers_needed:]):
                q.append((test_val, numbers_needed - 1))

    p2 = best_quine

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input, example=False)