from functools import cache

def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    tags = lines[0].split(',')
    bad_ids = set()

    @cache
    def check_id(num, repeat_len):
        num = str(num)
        if len(num) % repeat_len != 0:
            return False
        
        pattern = num[:len(num) // repeat_len]
        return all(num[i:i+len(pattern)] == pattern for i in range(0, len(num), len(num) // repeat_len))
        

    for tag in tags:
        id1, id2 = tag.split('-')
        for n in range(int(id1), int(id2) + 1):
            for i in range(2, len(str(n)) + 1):
                if n not in bad_ids and check_id(n, i):
                    bad_ids.add(n)
                    if i == 2:
                        p1 += n
                    p2 += n

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)