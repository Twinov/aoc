input = open('./input.txt', 'r')

first_list, second_list = [], []
for line in input:
    if len(line) > 2:
        print(line.split('   '))
        num1, num2 = line.split('   ')
        num1 = int(num1)
        num2 = int(num2.split('\\')[0])
        first_list.append(num1)
        second_list.append(num2)

first_list.sort()
second_list.sort()

tot_dist = 0
for n1, n2 in zip(first_list, second_list):
    tot_dist += abs(n2 - n1)

print('part 1:', tot_dist)

frequencies = {}
for num in second_list:
    frequencies[num] = frequencies.get(num, 0) + 1

similarity_score = 0
for num in first_list:
    similarity_score += num * frequencies.get(num, 0)
print('part 2', similarity_score)
