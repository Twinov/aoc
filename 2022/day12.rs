use std::collections::{HashMap, VecDeque};
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input").unwrap();
    let reader = BufReader::new(file);

    let mut map = Vec::new();
    let mut cached_steps = HashMap::new();

    let mut start = (0, 0);
    let mut end = (0, 0);
    let end_max = 26;

    for (i, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        map.push(Vec::new());
        for (j, c) in line.chars().enumerate() {
            if c == 'S' {
                map[i].push(1);
                start = (i, j);
            } else if c == 'E' {
                map[i].push(end_max);
                //cached_steps.insert((i, j), 0);
                end = (i, j);
            } else {
                map[i].push(c as i32 - 'a' as i32 + 1);
            }
        }
    }

    //bfs with queue of (state, cost)
    let mut bfs_queue = VecDeque::new();
    let starting_cost = 0;
    bfs_queue.push_back((end, starting_cost));
    while bfs_queue.len() > 0 {
        let (curr, curr_cost) = bfs_queue.pop_front().unwrap();
        if cached_steps.contains_key(&curr) {
            continue;
        }

        cached_steps.insert(curr, curr_cost);
        let directions = [(0, 1), (0, -1), (-1, 0), (1, 0)];
        for v in directions {
            let vec_x = curr.0 as i32 + v.0;
            let vec_y = curr.1 as i32 + v.1;
            if vec_x >= 0 && vec_x < map.len() as i32 && vec_y >= 0 && vec_y < map[0].len() as i32 {
                if map[vec_x as usize][vec_y as usize] + 1 >= map[curr.0][curr.1] {
                    bfs_queue.push_back(((vec_x as usize, vec_y as usize), curr_cost + 1));
                }
            }
        }
    }

    let mut lowest_starts = Vec::new();
    for i in 0..map.len() {
        for j in 0..map[i].len() {
            print!("{number:0>2} ", number = map[i][j]);
            if map[i][j] == 1 {
                //'a' or 'S'
                if cached_steps.contains_key(&(i, j)) {
                    lowest_starts.push(cached_steps.get(&(i, j)).unwrap())
                }
            }
        }
        println!("")
    }
    println!("");
    for i in 0..map.len() {
        for j in 0..map[i].len() {
            let to_print;
            match cached_steps.get(&(i, j)) {
                None => to_print = -1,
                Some(i) => to_print = *i,
            }
            print!("{number:>3} ", number = to_print)
        }
        println!("")
    }

    println!("Part 1: {}", cached_steps.get(&start).unwrap());
    println!("Part 2: {}", lowest_starts.iter().min().unwrap());
}
