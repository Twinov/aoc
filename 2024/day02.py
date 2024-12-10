input_file = open('input.txt', 'r')

safe_lines = 0
safe_lines_with_removal = 0
for line in input_file:
    if len(line) > 2:
        nums = line.split(' ')
        nums = [int(n) for n in nums]
        if all(1 <= nums[i] - nums[i-1] <= 3 for i in range(1, len(nums))) or all(1 <= nums[i-1] - nums[i] <= 3 for i in range(1, len(nums))):
            safe_lines += 1
            safe_lines_with_removal += 1
        else:
            for i in range(len(nums)):
                nums_with_removal = nums[0:i] + nums[i+1:]
                if all(1 <= nums_with_removal[i] - nums_with_removal[i-1] <= 3 for i in range(1, len(nums) - 1)) or all(1 <= nums_with_removal[i-1] - nums_with_removal[i] <= 3 for i in range(1, len(nums) - 1)):
                    safe_lines_with_removal += 1
                    break

print('part 1:', safe_lines)
print('part 2:', safe_lines_with_removal)
