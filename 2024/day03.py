example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

def solve(input_lines):
    p1, p2 = 0, 0

    enabled = True
    for line in input_lines:
        for i in range(len(line)):
            if i >= 4 and line[i-4:i] == 'do()':
                enabled = True
            if i >= 7 and line[i-7:i] == 'don\'t()':
                enabled = False
            if i >= 4 and line[i-4:i] == 'mul(':
                buf1 = []
                j = i
                while line[j] in '1234567890':
                    buf1.append(line[j])
                    j += 1
                if line[j] != ',':
                    continue
                j += 1

                buf2 = []
                while line[j] in '1234567890':
                    buf2.append(line[j])
                    j += 1

                if line[j] != ')':
                    continue
            
                p1 += int(''.join(buf1)) * int(''.join(buf2))
                p2 += int(''.join(buf1)) * int(''.join(buf2)) if enabled else 0
                #print(line[i:j], p1)
    
    print('part 1:', p1)
    print('part 2:', p2)

solve(example_input)
solve(actual_input)
