from collections import defaultdict

def solve(lines, example=True):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    def get_canonical_edge(computer1, computer2):
        return tuple(sorted([computer1, computer2]))

    edges = set()
    computer_connections = defaultdict(list)
    for line in lines:
        computer1, computer2 = line.split('-')
        edges.add(get_canonical_edge(computer1, computer2))
        computer_connections[computer1].append(computer2)
        computer_connections[computer2].append(computer1)
    
    size_3_cliques = set()
    for origin_computer, out_edges in computer_connections.items():
        for connected_computer in out_edges:
            for second_level_connected_computer in computer_connections[connected_computer]:
                if get_canonical_edge(origin_computer, second_level_connected_computer) in edges:
                    size_3_cliques.add(tuple(sorted((origin_computer, connected_computer, second_level_connected_computer))))

    seen_cliques = set()
    largest_clique = set()
    for origin_computer, out_edges in computer_connections.items():
        queue = [[origin_computer, [origin_computer]]]

        while queue:
            curr_computer, curr_network = queue.pop()

            if len(curr_network) > len(largest_clique):
                largest_clique = set(curr_network)

            curr_network = set(curr_network)
            for connected_computer in computer_connections[curr_computer]:
                if connected_computer in curr_network:
                    continue
                if not all(get_canonical_edge(connected_computer, network_computer) in edges for network_computer in curr_network):
                    continue
                
                next_network = [network_computer for network_computer in curr_network]
                next_network.append(connected_computer)
                if ','.join(sorted(next_network)) in seen_cliques:
                    continue
                    
                seen_cliques.add(','.join(sorted(next_network)))
                queue.append([connected_computer, next_network])

    for clique in size_3_cliques:
        if any(computer_name[0] == 't' for computer_name in clique):
            p1 += 1

    p2 = ','.join(sorted(largest_clique))

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input, example=False)