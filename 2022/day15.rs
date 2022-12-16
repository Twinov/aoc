use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input").unwrap();
    let reader = BufReader::new(file);

    let mut sensors = Vec::new();
    let mut beacons = HashSet::new();
    let search_max = 4000001;
    let mut covered_area = HashMap::new();

    for line in reader.lines() {
        let line = line.unwrap();
        sensors.push(Sensor::new(parse_line(line.clone())));
        beacons.insert(parse_line(line).1);
    }
    for (s, sensor) in sensors.iter().enumerate() {
        println!("{}/{}: {:?}", s + 1, sensors.len(), sensor);
        for i in 0..search_max {
            let projected_size = project_onto_y_size(*sensor, i);
            let projected_start = project_onto_y_start(*sensor, i);
            // if i % 500000 == 0 {
            //     println!(
            //         "sensor: {:?}, y={}, projected size: {}, projected range: {}..{}",
            //         sensor,
            //         i,
            //         project_onto_y_size(sensor, i),
            //         project_onto_y_start(sensor, i),
            //         projected_size + projected_start
            //     );
            // }
            if !covered_area.contains_key(&i) {
                covered_area.insert(i, Vec::new());
            }
            covered_area
                .get_mut(&i)
                .unwrap()
                .push((projected_start, projected_start + projected_size));
            // covered_area.insert((projected_start + projected_size, i));
            // for j in 0..projected_size {
            //     covered_area.insert((projected_start + j, i));
            // }
        }
    }
    for beacon in beacons.clone() {
        if beacon.0 >= 0 && beacon.1 < search_max {
            if !covered_area.contains_key(&beacon.1) {
                covered_area.insert(beacon.1, Vec::new());
            }
            covered_area
                .get_mut(&beacon.1)
                .unwrap()
                .push((beacon.0, beacon.0 + 1))
        }
    }
    //println!("{:?}", covered_area);

    //merge intervals
    for i in 0..search_max {
        let curr_row = covered_area.get_mut(&i).unwrap();
        curr_row.sort_by_key(|item| item.0);
        //println!("old {:?}", curr_row);
        let mut stack = Vec::new();
        stack.push(curr_row[0]);
        for j in 1..curr_row.len() {
            if stack[stack.len() - 1].0 <= curr_row[j].0
                && curr_row[j].0 <= stack[stack.len() - 1].1
            {
                let max;
                let stack_len = stack.len() - 1;
                if curr_row[j].1 > stack[stack_len].1 {
                    max = curr_row[j].1
                } else {
                    max = stack[stack_len].1;
                }
                stack[stack_len].1 = max
            } else {
                stack.push(curr_row[j]);
            }
        }
        let mut trimmed_stack = Vec::new();
        for s in stack {
            if !(s.0 < 0 && s.1 < 0) && !(s.0 > search_max && s.1 > search_max) {
                trimmed_stack.push(s);
            }
        }
        //println!("new {:?}", stack);
        covered_area.insert(i, trimmed_stack);
    }

    for i in 0..search_max {
        if i % 100000 == 0 {
            println!("starting row: {}", i);
        }
        let curr_row = covered_area.get(&i).unwrap();
        if curr_row.len() != 1 {
            println!("{:?}", curr_row);
            for j in 0..search_max {
                let mut contained = false;
                for (start, end) in curr_row {
                    if j >= *start && j < *end {
                        contained = true;
                        break;
                    }
                }
                if !contained {
                    println!("{:?}", (j, i));
                    println!("Part 2: {}", j * 4000000 + i)
                }
            }
        }
    }
    //brute force lol
    // for i in 0..search_max {
    //     if i % 100000 == 0 {
    //         println!("starting row: {}", i);
    //     }
    //     let curr_row = covered_area.get(&i).unwrap();
    //     for j in 0..search_max {
    //         let mut contained = false;
    //         for (start, end) in curr_row {
    //             if j >= *start && j < *end {
    //                 contained = true;
    //                 break;
    //             }
    //         }
    //         if !contained {
    //             println!("{:?}", (j, i));
    //             println!("Part 2: {}", j * 4000000 + i)
    //         }
    //     }
    // }
    // temp.sort();
    //println!("{:?}", beacons);
    //println!("{}", covered_area.len());
}

fn manhattan_dist(p1: (i32, i32), p2: (i32, i32)) -> i32 {
    let x_dist = (p1.0 - p2.0).abs();
    let y_dist = (p1.1 - p2.1).abs();
    x_dist + y_dist
}

fn project_onto_y_size(sensor: Sensor, y: i32) -> i32 {
    let dist = (sensor.center.1 - y).abs();
    if dist <= sensor.radius {
        return (sensor.radius - dist) * 2 + 1;
    }
    0
}

fn project_onto_y_start(sensor: Sensor, y: i32) -> i32 {
    sensor.center.0 - (sensor.radius - (sensor.center.1 - y).abs())
}

#[derive(Debug, Clone, Copy)]
struct Sensor {
    center: (i32, i32),
    radius: i32,
}
impl Sensor {
    fn new(sensor_beacon_pair: ((i32, i32), (i32, i32))) -> Sensor {
        Sensor {
            center: sensor_beacon_pair.0,
            radius: manhattan_dist(sensor_beacon_pair.0, sensor_beacon_pair.1),
        }
    }
}

fn parse_line(line: String) -> ((i32, i32), (i32, i32)) {
    let mut coords = Vec::new();
    let split_line = line.split(" ");
    let mut prev_x = 0;
    for (i, s) in split_line.enumerate() {
        if s.contains("=") {
            let s_split = s.split_once("=").unwrap();
            let num = s_split
                .1
                .trim_end_matches(",")
                .trim_end_matches(":")
                .parse()
                .unwrap();
            if i % 2 == 0 {
                prev_x = num;
            } else {
                coords.push((prev_x, num))
            }
        }
    }
    (coords[0], coords[1])
}
