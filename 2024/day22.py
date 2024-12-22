from collections import defaultdict

def solve(lines, example=True):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    initial_secret_numbers = [int(line) for line in lines]

    def evolve_number(secret_number):
        secret_number = mix_n_prune(secret_number, secret_number * 64)
        secret_number = mix_n_prune(secret_number, secret_number // 32)
        secret_number = mix_n_prune(secret_number, secret_number * 2048)
        
        return secret_number

    def mix_n_prune(secret_number, mix_num):
        return prune_number(mix_number(secret_number, mix_num))

    def mix_number(secret_number, num):
        return secret_number ^ num
    
    def prune_number(num):
        return num % 16777216

    winnings = defaultdict(int)
    EVOLUTIONS = 2000
    for initial_secret_number in initial_secret_numbers:
        secret_number = initial_secret_number
        price_changes, prev_price = [], secret_number % 10
        used_price_sequences = set()
        for _ in range(EVOLUTIONS):
            secret_number = evolve_number(secret_number)

            curr_price = secret_number % 10
            price_changes.append(curr_price - prev_price)

            if len(price_changes) >= 4:
                last_4_prices = (price_changes[-4], price_changes[-3], price_changes[-2], price_changes[-1])

                if last_4_prices not in used_price_sequences:
                    used_price_sequences.add(last_4_prices)
                    winnings[last_4_prices] += curr_price

            prev_price = curr_price
        
        p1 += secret_number
    
    p2 = max(winnings.values())

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input, example=False)