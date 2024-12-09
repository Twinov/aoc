def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    class FileBlockNode:
        def __init__(self, interval_left, interval_right, block_num, next_block=None):
            self.interval_left = interval_left
            self.interval_right = interval_right
            self.block_num = block_num
            self.next_block = next_block

        def get_block_size(self):
            return self.interval_right - self.interval_left + 1

        def calculate_checksum(self):
            checksum = 0
            file_block_node_curr = self.next_block
            for disk_position in range(total_disk_space):
                if disk_position > file_block_node_curr.interval_right:
                    file_block_node_curr = file_block_node_curr.next_block
                
                if not file_block_node_curr:
                    break
            
                if file_block_node_curr.block_num != -1:
                    checksum += disk_position * file_block_node_curr.block_num
            
            return checksum
    
        def print_disk(self, total_disk_space):
            gold_disk = []
            file_block_node_curr = self.next_block
            for disk_position in range(total_disk_space):
                if disk_position > file_block_node_curr.interval_right:
                    file_block_node_curr = file_block_node_curr.next_block
                
                if not file_block_node_curr:
                    gold_disk.append('.')
                    continue
            
                if file_block_node_curr.block_num != -1:
                    gold_disk.append(str(file_block_node_curr.block_num))
                else:
                    gold_disk.append('.')

            print('golden disk:', ''.join(gold_disk))
        
        def print_block_nodes(self):
            file_block_node_curr = self.next_block
            while file_block_node_curr != None:
                print('block num', file_block_node_curr.block_num, '(', file_block_node_curr.interval_left, ',', file_block_node_curr.interval_right, ') size', file_block_node_curr.get_block_size())
                file_block_node_curr = file_block_node_curr.next_block
    
    disk_map = lines[0]
    silver_file_blocks = []
    gold_file_block_head = FileBlockNode(-1, -1, -1, -1)
    file_block_node_curr = gold_file_block_head
    block_num = 0
    total_disk_space = 0
    block_sizes = {}
    for i in range(len(disk_map)):
        block_size = int(disk_map[i])
        if block_size == 0:
            continue

        total_disk_space += block_size
        disk_interval = [total_disk_space - block_size, total_disk_space]

        if i % 2 == 0:
            silver_file_blocks.append([disk_interval, block_num, block_size])
            file_block_node_curr.next_block = FileBlockNode(disk_interval[0], disk_interval[1] - 1, block_num)
            block_sizes[block_num] = block_size
            block_num += 1
        else:
            file_block_node_curr.next_block = FileBlockNode(disk_interval[0], disk_interval[1] - 1, -1)
        
        file_block_node_curr = file_block_node_curr.next_block
    
    
    # silver
    l, r = 0, len(silver_file_blocks) - 1
    disk = []
    for disk_position in range(total_disk_space):
        file_at_disk_pos = '.'
        if silver_file_blocks[l][0][0] <= disk_position <= silver_file_blocks[l][0][1]:
            if silver_file_blocks[l][2]:
                file_at_disk_pos = silver_file_blocks[l][1]
                p1 += disk_position * silver_file_blocks[l][1]
                silver_file_blocks[l][2] -= 1
                if not silver_file_blocks[l][2]:
                    l += 1

        else:
            if silver_file_blocks[r][2]:
                file_at_disk_pos = silver_file_blocks[r][1]
                p1 += disk_position * silver_file_blocks[r][1]
                silver_file_blocks[r][2] -= 1
                if not silver_file_blocks[r][2]:
                    r -= 1

        disk.append(str(file_at_disk_pos))

    # gold
    for moving_block_num in range(block_num - 1, -1, -1):
        file_block_node_curr = gold_file_block_head.next_block
        while file_block_node_curr != None:
            if file_block_node_curr.block_num == moving_block_num:
                break

            if file_block_node_curr.block_num == -1 and block_sizes[moving_block_num] <= file_block_node_curr.get_block_size():
                file_block_node_curr.block_num = moving_block_num
                if file_block_node_curr.get_block_size() > block_sizes[moving_block_num]:
                    
                    # insert new blank block
                    file_block_node_curr.next_block = FileBlockNode(file_block_node_curr.interval_left + file_block_node_curr.get_block_size() + 1, file_block_node_curr.interval_right, -1, file_block_node_curr.next_block)

                    file_block_node_curr.interval_right = file_block_node_curr.interval_left + block_sizes[moving_block_num] - 1
                    file_block_node_curr.next_block.interval_left = file_block_node_curr.interval_right + 1

                # clear old block
                file_block_node_to_clear = file_block_node_curr.next_block
                while file_block_node_to_clear.block_num != moving_block_num:
                    file_block_node_to_clear = file_block_node_to_clear.next_block
                file_block_node_to_clear.block_num = -1

                # compact blank blocks
                file_block_node_curr = gold_file_block_head
                while file_block_node_curr.next_block != None:
                    if file_block_node_curr.block_num == file_block_node_curr.next_block.block_num:
                        file_block_node_curr.interval_right = file_block_node_curr.next_block.interval_right
                        file_block_node_curr.next_block = file_block_node_curr.next_block.next_block
                    else:
                        file_block_node_curr = file_block_node_curr.next_block

                break
            
            file_block_node_curr = file_block_node_curr.next_block
        
    p2 = gold_file_block_head.calculate_checksum()

    print('silver disk:', ''.join(disk))
    gold_file_block_head.print_disk(total_disk_space)

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)