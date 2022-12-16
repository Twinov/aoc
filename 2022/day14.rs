use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input").unwrap();
    let reader = BufReader::new(file);

    let mut rock_structures = HashSet::new();
    let mut deepest_level = 0;
    let mut sand_steps = 0;

    for line in reader.lines() {
        let line = line.unwrap();
        let coords = parse_line(line);
        rock_structures.insert(coords[0]);
        if coords[0].1 > deepest_level {
            deepest_level = coords[0].1;
        }
        for i in 1..coords.len() {
            if coords[i].0 == coords[i - 1].0 {
                //vertical expand
                for j in 1..=(coords[i].1 - coords[i - 1].1).abs() {
                    if coords[i].1 > coords[i - 1].1 {
                        rock_structures.insert((coords[i].0, coords[i - 1].1 + j));
                        if coords[i - 1].1 + j > deepest_level {
                            deepest_level = coords[i - 1].1 + j;
                        }
                    } else {
                        rock_structures.insert((coords[i].0, coords[i - 1].1 - j));
                        if coords[i - 1].1 - j > deepest_level {
                            deepest_level = coords[i - 1].1 - j;
                        }
                    }
                }
            } else {
                //horizontal expand
                for j in 1..=(coords[i].0 - coords[i - 1].0).abs() {
                    if coords[i].0 > coords[i - 1].0 {
                        rock_structures.insert((coords[i - 1].0 + j, coords[i].1));
                    } else {
                        rock_structures.insert((coords[i - 1].0 - j, coords[i].1));
                    }
                }
            }
        }
    }

    //part 2 just fill in everything (0, deepest_level + 2)..(1000, deepest_level + 2) lol
    for i in 0..1000 {
        rock_structures.insert((i, deepest_level + 2));
    }

    let pour_point = (500, 0);
    let mut keep_pouring = true;
    while keep_pouring {
        sand_steps += 1;

        let mut falling = true;
        let mut current_position = pour_point;

        while falling {
            // part 1
            // if current_position.1 == deepest_level {
            //     //done
            //     falling = false;
            //     keep_pouring = false;
            // } else
            if !rock_structures.contains(&(current_position.0, current_position.1 + 1)) {
                //straight down
                current_position = (current_position.0, current_position.1 + 1);
            } else if !rock_structures.contains(&(current_position.0 - 1, current_position.1 + 1)) {
                //down left
                current_position = (current_position.0 - 1, current_position.1 + 1);
            } else if !rock_structures.contains(&(current_position.0 + 1, current_position.1 + 1)) {
                //down right
                current_position = (current_position.0 + 1, current_position.1 + 1);
            } else {
                //cannot pour
                rock_structures.insert(current_position);
                falling = false;

                //part 2 end
                if current_position == pour_point {
                    keep_pouring = false;
                    sand_steps += 1;
                }
            }
        }
        //println!("{:?}", current_position);
    }

    println!("{:?}", rock_structures);

    println!("Part 1: {}", sand_steps - 1);
}

fn parse_line(line: String) -> Vec<(i32, i32)> {
    let mut coords = Vec::new();
    let split_line = line.split(" ");
    for s in split_line {
        if s != "->" {
            let (x, y) = s.split_once(",").unwrap();
            coords.push((x.parse().unwrap(), y.parse().unwrap()));
        }
    }
    coords
}
