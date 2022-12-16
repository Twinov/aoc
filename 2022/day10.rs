use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input").unwrap();
    let reader = BufReader::new(file);

    let mut x_register = 1;
    let mut total_signal_strength = 0;
    let mut tick = 1;
    let mut buffer;

    for line in reader.lines() {
        let line = line.unwrap();
        let mut split_line = line.split(" ");

        let instruction = split_line.next().unwrap();
        let argument = split_line.next();

        match instruction {
            "addx" => {
                buffer = argument.unwrap().parse::<i32>().unwrap();
                for _ in 0..2 {
                    cycle(&mut tick, x_register, &mut total_signal_strength)
                }
                x_register += buffer;
            }
            "noop" => cycle(&mut tick, x_register, &mut total_signal_strength),
            _ => panic!(),
        }
    }
    println!();
    println!("Part 1: {}", total_signal_strength);
}

fn cycle(tick: &mut i32, x_register: i32, total_signal_strength: &mut i32) {
    if (*tick - 20) % 40 == 0 {
        *total_signal_strength += *tick * x_register;
    }

    let pixel = *tick % 40 - 1;
    let drawn_char;
    if pixel == 0 {
        println!();
    }
    if x_register - 1 == pixel || x_register == pixel || x_register + 1 == pixel {
        drawn_char = '#';
    } else {
        drawn_char = '.';
    }
    print!("{}", drawn_char);
    // println!(
    //     "{} {} {} {}",
    //     tick,
    //     pixel,
    //     x_register,
    //     x_register - 1 == pixel || x_register == pixel || x_register + 1 == pixel
    // );

    *tick += 1;
}
