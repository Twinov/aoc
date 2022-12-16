use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input").unwrap();
    let reader = BufReader::new(file);

    let mut p1_tot = 0;
    let mut p2_tot = 0;

    for line in reader.lines() {
        let assignment = line.as_ref().unwrap().split(",").collect::<Vec<_>>();
        if range_contained(&assignment) {
            p1_tot += 1;
        }
        if range_overlap(&assignment) {
            p2_tot += 1;
        }
    }

    println!("Part 1: {}", p1_tot);
    println!("Part 2: {}", p2_tot);
}

fn range_start_end(range: &str) -> (i32, i32) {
    let r = range.split("-").collect::<Vec<_>>();
    (r[0].parse().unwrap(), r[1].parse().unwrap())
}

fn range_contained(assignment: &[&str]) -> bool {
    let (a1_start, a1_end) = range_start_end(assignment[0]);
    let (a2_start, a2_end) = range_start_end(assignment[1]);
    (a1_start <= a2_start && a1_end >= a2_end) || (a2_start <= a1_start && a2_end >= a1_end)
}

fn range_overlap(assignment: &[&str]) -> bool {
    let (a1_start, a1_end) = range_start_end(assignment[0]);
    let (a2_start, a2_end) = range_start_end(assignment[1]);
    (a1_start <= a2_end && a1_end >= a2_end) || (a2_start <= a1_end && a2_end >= a1_start)
}
