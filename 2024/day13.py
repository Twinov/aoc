def solve(lines):
    lines = [line.strip() for line in lines]
    p1, p2 = 0, 0

    class ClawMachine:
        def __init__(self, button_a=None, button_b=None, prize=None):
            self.button_a = button_a
            self.button_b = button_b
            self.prize = prize
        
        def __str__(self):
            return f'button_a: {self.button_a} button_b: {self.button_b} prize: {self.prize}'

        def get_least_pushes_cost(self, part2=False):
            ### solved the 
            ### A(x1) + B(x2) = x3
            ### A(y1) + B(y2) = y3
            ### system of equations by hand and got some massive ugly thing
            ### luckily don't have to substitute A back into B :DDD
            ### (did have to relearn how to algebra though)

            x1, x2, x3 = self.button_a[0], self.button_b[0], self.prize[0]
            y1, y2, y3 = self.button_a[1], self.button_b[1], self.prize[1]

            if part2:
                offset = 10000000000000
                x3 += offset
                y3 += offset

            a = ((x3 * y2 - y3 * x2) / (x1 * y2 - y1 * x2))
            b = (y3 - a * y1) / y2
            
            return a * 3 + b if int(a) == a and int(b) == b and (part2 or (a <= 100 and b <= 100)) else -1

    claw_machines = []
    for i, line in enumerate(lines):
        if i % 4 == 0:
            x_offset = int(line.split('+')[1].split(',')[0])
            y_offset = int(line.split('+')[2])
            claw_machines.append(ClawMachine(button_a=(x_offset, y_offset)))
        elif i % 4 == 1:
            x_offset = int(line.split('+')[1].split(',')[0])
            y_offset = int(line.split('+')[2])
            claw_machines[-1].button_b = (x_offset, y_offset)
        elif i % 4 == 2:
            x_offset = int(line.split('=')[1].split(',')[0])
            y_offset = int(line.split('=')[2])
            claw_machines[-1].prize = (x_offset, y_offset)
    
    for machine in claw_machines:
        if (least_pushes := machine.get_least_pushes_cost()) != -1:
            p1 += int(least_pushes)
        
        if (least_pushes := machine.get_least_pushes_cost(part2=True)) != -1:
            p2 += int(least_pushes)

    print('part 1:', p1)
    print('part 2:', p2)

example_input = open('example_input.txt', 'r').readlines()
actual_input = open('input.txt', 'r').readlines()

solve(example_input)
solve(actual_input)