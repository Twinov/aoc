use std::fmt;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input").unwrap();
    let reader = BufReader::new(file);

    let mut monkeys = Vec::new();

    //parse
    for (i, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        let mut split_line = line.split(" ");

        split_line.next();
        split_line.next();
        match i % 7 {
            0 => monkeys.push(Monkey::new()),
            1 => {
                for _ in 0..2 {
                    split_line.next();
                }

                for val in split_line {
                    let mut curr = val;
                    if val.chars().nth(val.len() - 1).unwrap() == ',' {
                        curr = &val[0..val.len() - 1];
                    }
                    monkeys[i / 7].items.push(curr.parse().unwrap())
                }
            }
            2 => {
                for _ in 0..4 {
                    split_line.next();
                }

                monkeys[i / 7].operation_op = split_line.next().unwrap().chars().nth(0).unwrap();
                monkeys[i / 7].operation_2nd_value = split_line.next().unwrap().to_owned();
            }
            3 => {
                for _ in 0..3 {
                    split_line.next();
                }

                monkeys[i / 7].test_divisible = split_line.next().unwrap().parse().unwrap();
            }
            4 => {
                for _ in 0..7 {
                    split_line.next();
                }
                monkeys[i / 7].test_true = split_line.next().unwrap().parse().unwrap();
            }
            5 => {
                for _ in 0..7 {
                    split_line.next();
                }
                monkeys[i / 7].test_false = split_line.next().unwrap().parse().unwrap();
            }
            _ => (),
        }
    }

    //lcm
    let mut divisibles = Vec::new();
    for i in 0..monkeys.len() {
        divisibles.push(monkeys[i].test_divisible)
    }
    let divisibles_lcm = lcm_list(divisibles);

    //monke business
    //for _ in 0..20 {
    for _ in 0..10000 {
        for i in 0..monkeys.len() {
            for j in 0..monkeys[i].items.len() {
                monkeys[i].tot_inspected += 1;
                let mut worry_level = monkeys[i].items[j];
                match monkeys[i].operation_op {
                    '+' => worry_level += monkeys[i].operation_2nd_value.parse::<i64>().unwrap(),
                    '*' => match monkeys[i].operation_2nd_value.as_str() {
                        "old" => worry_level = worry_level * worry_level,
                        _ => worry_level *= monkeys[i].operation_2nd_value.parse::<i64>().unwrap(),
                    },
                    _ => panic!(),
                }
                //worry_level /= 3;
                worry_level %= divisibles_lcm;
                let throw_to_monkey;
                if worry_level % monkeys[i].test_divisible == 0 {
                    throw_to_monkey = monkeys[i].test_true
                } else {
                    throw_to_monkey = monkeys[i].test_false
                }
                monkeys[throw_to_monkey].items.push(worry_level);
            }
            monkeys[i].items.clear();
        }
    }
    let mut inspected_totals = Vec::new();
    for i in 0..monkeys.len() {
        println!("{}", monkeys[i]);
        inspected_totals.push(monkeys[i].tot_inspected);
    }
    inspected_totals.sort();
    inspected_totals.reverse();
    println!("{}", inspected_totals[0] * inspected_totals[1]);
}

fn gcd(a: &mut i64, b: &mut i64) -> i64 {
    while *b != 0 {
        (*a, *b) = (*b, *a % *b)
    }
    *a
}

fn lcm(a: i64, b: i64) -> i64 {
    a * b / gcd(&mut a.clone(), &mut b.clone())
}

fn lcm_list(nums: Vec<i64>) -> i64 {
    let mut running_lcm = 1;
    for n in nums {
        running_lcm = lcm(running_lcm, n)
    }
    running_lcm
}
struct Monkey {
    items: Vec<i64>,
    operation_op: char,
    operation_2nd_value: String,
    test_divisible: i64,
    test_true: usize,
    test_false: usize,
    tot_inspected: i64,
}
impl Monkey {
    fn new() -> Monkey {
        Monkey {
            items: Vec::new(),
            operation_op: '+',
            operation_2nd_value: "old".to_owned(),
            test_divisible: 1,
            test_true: 0,
            test_false: 0,
            tot_inspected: 0,
        }
    }
}
impl fmt::Display for Monkey {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "items: {:?}, operation_op: {}, operation_2nd_value: {}, test_divisible: {}, test_true {}, test_false: {}, tot_inspected: {}",
            self.items, self.operation_op, self.operation_2nd_value, self.test_divisible, self.test_true, self.test_false, self.tot_inspected
        )
    }
}
