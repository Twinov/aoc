use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input").unwrap();
    let reader = BufReader::new(file);

    let mut dir_stack = Vec::new();
    dir_stack.push(('/'.to_string(), 0));

    let max_dir_size = 100000;
    let mut tot_under_10万 = 0;

    let disk_space = 70000000;
    let needed_space = 30000000;
    let mut popped_dir_and_sizes = Vec::new();

    for line_wrapped in reader.lines() {
        let line = line_wrapped.unwrap();

        if line.starts_with("cd /") {
            for _ in 0..dir_stack.len() {
                pop_and_add_if_under_max(
                    &mut dir_stack,
                    max_dir_size,
                    &mut tot_under_10万,
                    &mut popped_dir_and_sizes,
                )
            }
            dir_stack.push(('/'.to_string(), 0));
        } else if line.starts_with("$ cd ..") {
            pop_and_add_if_under_max(
                &mut dir_stack,
                max_dir_size,
                &mut tot_under_10万,
                &mut popped_dir_and_sizes,
            );
        } else if line.starts_with("$ cd") {
            let dir_name = line.split(" ").collect::<Vec<&str>>()[2];
            dir_stack.push((dir_name.to_owned(), 0));
        } else if line.chars().nth(0).unwrap().is_numeric() {
            //split into [file size] [file name]
            let (file_size, _) = line.split_once(" ").unwrap();

            //add size to all dirs on the stack
            for i in 0..dir_stack.len() {
                dir_stack[i].1 += file_size.parse::<i32>().unwrap()
            }
        }
    }
    //sum dirs that are left
    for _ in 0..dir_stack.len() {
        pop_and_add_if_under_max(
            &mut dir_stack,
            max_dir_size,
            &mut tot_under_10万,
            &mut popped_dir_and_sizes,
        )
    }

    println!("Part 1: {}", tot_under_10万);
    popped_dir_and_sizes.sort();
    println!("{:?}", popped_dir_and_sizes);
    let already_available_space = 26043024; //disk_space - popped_dir_and_sizes.pop().unwrap().1;
    println!(
        "Part 2 already available space: {}",
        already_available_space
    );
    //let mut satisfies_dirs = Vec::new();
    for (space, name) in popped_dir_and_sizes {
        // println!("{} {} {}", name, space, space + already_available_space);
        if space + already_available_space > needed_space {
            println!("{} {}", name, space);
            break;
            //satisfies_dirs.push((space, name));
        }
        //need 3956976
    }
    // satisfies_dirs.sort();
    // for (name, space) in &satisfies_dirs {
    //     println!("{} {}", name, space);
    // }
    // println!("Part 2: {} {}", satisfies_dirs[0].0, satisfies_dirs[0].1);
}

fn pop_and_add_if_under_max(
    dir_stack: &mut Vec<(String, i32)>,
    max_dir_size: i32,
    tot_under_10万: &mut i32,
    popped_dir_and_sizes: &mut Vec<(i32, String)>,
) {
    let (name, popped) = dir_stack.pop().unwrap();
    if popped < max_dir_size {
        *tot_under_10万 += popped;
    }
    println!("{} {}", name, popped);
    popped_dir_and_sizes.push((popped, name));
}
