from collections import defaultdict, deque

def solve(lines):
    p1, p2 = 0, 0

    in_degrees, out_edges = {}, defaultdict(list)
    pages_set = set()
    starting_pages = []

    for line in lines:
        line = line.strip()
        if '|' in line:
            pg1, pg2 = line.split('|')
            if pg1 not in out_edges[pg2]:
                out_edges[pg1].append(pg2)
                in_degrees[pg2] = in_degrees.get(pg2, 0) + 1

                pages_set.add(pg1)
                pages_set.add(pg2)

        elif not line:
            # set up base frontier
            for page in pages_set:
                if page not in in_degrees:
                    starting_pages.append(page)

        else:
            available_pages = set([page for page in starting_pages])
            sorted_pages = [page for page in starting_pages] # topological sort for this particular manual
            needed_pages = line.split(',')
            curr_in_degrees = {}
            for k, v in in_degrees.items():
                curr_in_degrees[k] = v

            for page in pages_set:
                if page not in needed_pages and page not in available_pages:
                    available_pages.add(page)
                    sorted_pages.append(page)

            queue = deque(available_pages)
            while queue:
                curr_page = queue.popleft()

                for next_page in out_edges[curr_page]:
                    curr_in_degrees[next_page] -= 1
                    if not curr_in_degrees[next_page]:
                        if next_page not in available_pages:
                            available_pages.add(next_page)
                            queue.append(next_page)
                            sorted_pages.append(next_page)
            
            def is_page_sorted(needed_pages, sorted_pages):
                sorted_pages_idx, needed_pages_idx = 0, 0
                while sorted_pages_idx < len(sorted_pages) and needed_pages_idx < len(needed_pages):
                    while sorted_pages_idx < len(sorted_pages) and sorted_pages[sorted_pages_idx] != needed_pages[needed_pages_idx]:
                        sorted_pages_idx += 1
                    
                    needed_pages_idx, sorted_pages_idx = needed_pages_idx + 1, sorted_pages_idx + 1
                
                return needed_pages_idx == len(needed_pages)
            
            if is_page_sorted(needed_pages, sorted_pages):
                # part 1, just check if sorted
                middle_page = needed_pages[len(needed_pages) // 2]
                p1 += int(middle_page)
            else:
                # part 2, get the correct ordering from the topological sort
                needed_pages_sorted = []
                sorted_pages_idx = 0
                needed_pages = set(needed_pages)
                while sorted_pages_idx < len(sorted_pages):
                    if sorted_pages[sorted_pages_idx] in needed_pages:
                        needed_pages_sorted.append(sorted_pages[sorted_pages_idx])
                    
                    sorted_pages_idx += 1
                
                middle_page = needed_pages_sorted[len(needed_pages_sorted) // 2]
                p2 += int(middle_page)

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)