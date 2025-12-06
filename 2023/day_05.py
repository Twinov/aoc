def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = float('inf'), float('inf')

    seeds = [int(n) for n in lines[0].split(' ')[1:]]
    seed_ranges = []
    for s in range(0, len(seeds), 2):
        seed_ranges.append([seeds[s], seeds[s] + seeds[s+1] - 1])

    offsets = []
    for line in lines[2:]:
        if not line: continue

        if line[-1] == ':':
            offsets.append([])
        else:
            dst, src, range_len = map(int, line.split(' '))
            # offsets will be (src_range_start, src_range_end, dst_range_start)
            offsets[-1].append((src, src + range_len - 1, dst))

    for group in offsets:
        group.sort(key=lambda x: x[0])

    def get_mapped_value(group, val):
        l, r = 0, len(group) - 1
        while l <= r:
            m = l + (r - l) // 2
            if group[m][0] <= val <= group[m][1]:
                return group[m][2] + val - group[m][0]
            
            if group[m][0] < val:
                l = m + 1
            else:
                r = m - 1

        return val
    
    for seed in seeds:
        curr_val = seed
        for group in offsets:
            curr_val = get_mapped_value(group, curr_val)
        p1 = min(p1, curr_val)

    def get_mapped_ranges(group, mapping):
        overlaps = []
        for off_start, off_end, dst_start in group:
            if off_start <= mapping[1] and mapping[0] <= off_end:
                overlaps.append([max(off_start, mapping[0]), min(off_end, mapping[1])])
                overlaps[-1].append(overlaps[-1][0] - off_start)
                overlaps[-1].append(dst_start)

        mapped_ranges = []
        current_pos = mapping[0]

        for s, e, shift, start in overlaps:
            if current_pos < s:
                mapped_ranges.append([current_pos, s - 1])
            mapped_ranges.append([start + shift, start + shift + (e - s)])
            current_pos = e + 1

        if current_pos <= mapping[1]:
            mapped_ranges.append([current_pos, mapping[1]])
        ranges_sum = sum(m[1] - m[0] + 1 for m in mapped_ranges)
        return mapped_ranges
            
    for seed_range in seed_ranges:
        mappings = [seed_range]
        for group in offsets:
            next_mappings = []
            for mapping in mappings:
                next_mappings.extend(get_mapped_ranges(group, mapping))
            mappings = next_mappings

        p2 = min(p2, *[m[0] for m in mappings])

    print('part 1:', p1)
    print('part 2:', p2)


example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)
