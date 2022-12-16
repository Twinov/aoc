use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input").unwrap();
    let reader = BufReader::new(file);

    let mut visited = HashSet::new();

    let mut rope = Vec::new();
    for _ in 0..10 {
        rope.push((0, 0));
    }

    for line in reader.lines() {
        let line = line.unwrap();
        let (direction, distance) = line.split_once(" ").unwrap();
        let direction = direction.chars().nth(0).unwrap();
        let distance = distance.parse::<i32>().unwrap();

        let movement;
        match direction {
            'R' => movement = (1, 0),
            'U' => movement = (0, 1),
            'L' => movement = (-1, 0),
            'D' => movement = (0, -1),
            _ => panic!(),
        }

        for _ in 0..distance {
            rope[0] = (rope[0].0 + movement.0, rope[0].1 + movement.1);

            for i in 1..10 {
                rope[i] = move_tail(rope[i - 1], rope[i])
            }

            visited.insert(rope[9]);
        }
    }
    println!("{}", visited.len());
}

fn move_tail(head: (i32, i32), tail: (i32, i32)) -> (i32, i32) {
    let mut new_tail = tail;
    let (dx, dy) = ((head.0 - tail.0).abs(), (head.1 - tail.1).abs());
    if dx <= 1 && dy <= 1 {
        return new_tail;
    }
    if dx >= 1 {
        //horizontal
        if head.0 > tail.0 {
            new_tail.0 += 1
        } else {
            new_tail.0 -= 1
        }
    }
    if dy >= 1 {
        //vertical
        if head.1 > tail.1 {
            new_tail.1 += 1
        } else {
            new_tail.1 -= 1
        }
    }
    return new_tail;
}
