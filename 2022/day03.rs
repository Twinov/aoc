use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input").unwrap();
    let reader = BufReader::new(file);

    let mut p1_tot = 0;

    let mut p2_set1 = HashSet::<char>::new();
    let mut p2_set2 = HashSet::<char>::new();
    let mut p2_tot = 0;

    for (i, line) in reader.lines().enumerate() {
        let sack = line.unwrap(); //star 1
        let mut compartments = HashSet::<char>::new();
        let mut found = false;

        for (j, c) in sack.chars().enumerate() {
            if j < sack.len() / 2 {
                compartments.insert(c);
            } else {
                if compartments.contains(&c) && !found {
                    if c.is_uppercase() {
                        p1_tot += c as usize - 'A' as usize + 1;
                        p1_tot += 26;
                    } else {
                        p1_tot += c as usize - 'a' as usize + 1;
                    }
                    found = true;
                }
            }
        }

        for c in sack.chars() {
            //star 2
            match i % 3 {
                0 => drop(p2_set1.insert(c)),
                1 => {
                    if p2_set1.contains(&c) {
                        p2_set2.insert(c);
                    }
                }
                2 => {
                    if p2_set2.contains(&c) {
                        if c.is_uppercase() {
                            p2_tot += c as usize - 'A' as usize + 1;
                            p2_tot += 26;
                        } else {
                            p2_tot += c as usize - 'a' as usize + 1;
                        }
                        p2_set1.clear();
                        p2_set2.clear();
                    }
                }
                _ => panic!(),
            }
        }
    }
    println!("Part 1: {}", p1_tot);
    println!("Part 2: {}", p2_tot);
}
