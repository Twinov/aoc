import heapq

def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    for line in lines:
        prev, line_jolts = 0, 0
        batteries_heap = []
        for i, c in enumerate(line):
            # p1
            if prev * 10 + int(c) > line_jolts:
                line_jolts = prev * 10 + int(c)
                prev = max(prev, int(c))
            
            # p2
            while (
                len(line) - i + len(batteries_heap) > 12 and 
                batteries_heap and 
                int(c) > batteries_heap[0][0]
            ):
                heapq.heappop(batteries_heap)
            heapq.heappush(batteries_heap, (int(c), i))

            if len(batteries_heap) > 12:
                heapq.heappop(batteries_heap)
            
        p1 += line_jolts
        p2 += int(''.join(str(n[0]) for n in sorted(batteries_heap, key=lambda x: x[1])))

        

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)