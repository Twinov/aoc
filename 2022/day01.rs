use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut elves = Vec::new();
    let mut curr_int = 0;

    if let Ok(lines) = read_lines("./input") {
        for line in lines {
            if let Ok(curr) = line {
                match curr.as_str() {
                    "" => {
                        elves.push(curr_int);
                        curr_int = 0;
                    }
                    _ => curr_int += curr.parse::<i32>().unwrap(),
                }
            }
        }
    }
    elves.sort();
    let mut top3tot = 0;
    for i in 0..3 {
        println!("{}", elves[elves.len() - i - 1]);
        top3tot += elves[elves.len() - i - 1];
    }
    println!("{}", top3tot);
}

// The output is wrapped in a Result to allow matching on errors
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
