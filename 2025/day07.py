def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    beam_locations = {}
    for i in range(len(lines)):
        new_beams = {}
        for j in range(len(lines[i])):
            if lines[i][j] == 'S':
                new_beams[j] = 1
            elif lines[i][j] == '^' and j in beam_locations and beam_locations[j] > 0:
                if j-1 not in new_beams:
                    new_beams[j-1] = 0
                new_beams[j-1] += beam_locations[j]
                if j+1 not in new_beams:
                    new_beams[j+1] = 0
                new_beams[j+1] += beam_locations[j]
                beam_locations[j] = 0
                p1 += 1

        for k, v in new_beams.items():
            if k not in beam_locations:
                beam_locations[k] = 0
            beam_locations[k] += v
        
        line_display = []
        for j in range(len(lines[i])):
            if lines[i][j] in ('S', '^'):
                line_display.append(lines[i][j])
            elif j in beam_locations and beam_locations[j] > 0:
                line_display.append(str(beam_locations[j]))
            else:
                line_display.append('.')
        # crude display for debugging
        #print(''.join(line_display))
                
    p2 = sum(v for v in beam_locations.values())
    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)