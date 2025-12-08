import heapq
from math import prod

class UnionFind:
    def __init__(self):
        self.parents = {}
    
    def union(self, n1, n2):
        p1, p2 = self.find(n1), self.find(n2)
        if p1 == p2:
            return False

        self.parents[p2] = p1
        return True
    
    def find(self, n):
        if n not in self.parents:
            self.parents[n] = n
        
        curr = n
        while self.parents[curr] != curr:
            self.parents[curr] = self.parents[self.parents[curr]]
            curr = self.parents[curr]
        return curr

def get_dist(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2

    return ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)**0.5

def solve(lines):
    lines = [line.strip() for line in lines]
    silver, gold = 0, 0

    points, edges = [], []
    for line in lines:
        x, y, z = map(int, line.split(','))
        points.append((x, y, z))
    
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            p1, p2 = points[i], points[j]

            edges.append((get_dist(p1, p2), p1, p2))

    edges_heap = [e for e in edges]
    heapq.heapify(edges_heap)            
    uf = UnionFind()
    connected_components = len(points)
    iter_count = 0
    EDGES_TO_CONNECT_SILVER = 1000 if len(lines) != 20 else 10
    while connected_components != 1:
        iter_count += 1
        dist, p1, p2 = heapq.heappop(edges_heap)
        if uf.union(p1, p2):
            connected_components -= 1

        if iter_count == EDGES_TO_CONNECT_SILVER:
            circuits = {}
            for p in uf.parents:
                parent = uf.find(p)
                if parent not in circuits:
                    circuits[parent] = 0
                circuits[parent] += 1
    
                circuit_sizes = [v for v in circuits.values()]
                circuit_sizes.sort(reverse=True)

                silver = prod(circuit_sizes[:3])

    gold = p1[0] * p2[0]
    print('part 1:', silver)
    print('part 2:', gold)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)