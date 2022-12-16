use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input").unwrap();
    let reader = BufReader::new(file);

    let mut tot = 0;

    let prev = [3, 1, 2];
    let next = [2, 3, 1];

    for line in reader.lines() {
        let line = line.unwrap();

        let first = line.chars().nth(0).unwrap() as usize - 'A' as usize + 1;
        let second = line.chars().nth(2).unwrap() as usize - 'W' as usize;

        // part 1
        // tot += second;
        // match second - first {
        //     1 | -2 => tot += 6,
        //     0 => tot += 3,
        //     _ => (),
        // }

        // part 2
        match second {
            1 => tot += &prev[first - 1],     //lose
            2 => tot += first + 3,            //draw
            3 => tot += &next[first - 1] + 6, //win
            _ => println!("{}", second),
        }
        println!("{} {} {}", first, second, tot);
    }
}
