use std::collections::VecDeque;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input").unwrap();
    let reader = BufReader::new(file);

    let mut stacks: Vec<VecDeque<char>> = Vec::new();
    let mut finished_building_stacks = false;

    for line in reader.lines() {
        if !finished_building_stacks {
            //build stacks
            let mut whitespace = 0;
            let mut curr = 0;
            for c in line.unwrap().chars() {
                match c {
                    ' ' => {
                        whitespace += 1;
                        if whitespace == 4 {
                            curr += 1;
                            whitespace = 0;
                        }
                    }
                    letter if letter.is_alphabetic() => {
                        while curr >= stacks.len() {
                            stacks.push(VecDeque::new());
                        }
                        stacks[curr].push_front(letter);
                        curr += 1;
                        whitespace = 0;
                    }
                    num if num.is_numeric() => finished_building_stacks = true,
                    _ => (),
                }
            }
        } else {
            //start moves
            let instructions = line.as_ref().unwrap().split(" ").collect::<Vec<_>>();
            if instructions[0] == "move" {
                let from = instructions[3].parse::<usize>().unwrap() - 1;
                let to = instructions[5].parse::<usize>().unwrap() - 1;
                let mut curr_moving: VecDeque<char> = VecDeque::new();
                for _ in 0..instructions[1].parse().unwrap() {
                    let popped = stacks[from].pop_back().unwrap();
                    // stacks[to].push_back(popped); //part 1 only
                    curr_moving.push_front(popped);
                }
                for c in curr_moving.into_iter() {
                    //part 2
                    stacks[to].push_back(c);
                }
            }
        }
    }

    for stack in stacks.iter() {
        println!("{}", stack[stack.len() - 1])
    }
}
