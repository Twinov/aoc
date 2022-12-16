use std::fmt;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input").unwrap();
    let reader = BufReader::new(file);

    let mut grid: Vec<Vec<Space>> = Vec::new();
    let mut grid_size = 0;

    let mut tot_visible = 0;
    let mut max_scenic = 0;

    for (i, line_wrapped) in reader.lines().enumerate() {
        let line = line_wrapped.unwrap();
        grid.push(Vec::new());
        for (_, c) in line.chars().enumerate() {
            grid_size = line.len();
            grid[i].push(Space::new(c.to_digit(10).unwrap() as i32))
        }
    }

    for i in 0..grid_size {
        for j in 0..grid_size {
            let curr_tree_height = grid[i][j].tree_height;

            let mut max_left = 0;
            let mut continue_scenic_search = true;
            let mut scenic_left = 0;
            for k in (0..j).rev() {
                if grid[i][k].tree_height > max_left {
                    max_left = grid[i][k].tree_height
                }
                if continue_scenic_search && grid[i][k].tree_height >= curr_tree_height {
                    scenic_left += 1;
                    continue_scenic_search = false;
                } else if continue_scenic_search {
                    scenic_left += 1;
                }
            }
            let mut max_right = 0;
            let mut continue_scenic_search = true;
            let mut scenic_right = 0;
            for k in j + 1..grid_size {
                if grid[i][k].tree_height > max_right {
                    max_right = grid[i][k].tree_height
                }
                if continue_scenic_search && grid[i][k].tree_height >= curr_tree_height {
                    scenic_right += 1;
                    continue_scenic_search = false;
                } else if continue_scenic_search {
                    scenic_right += 1;
                }
            }
            let mut max_up = 0;
            let mut continue_scenic_search = true;
            let mut scenic_up = 0;
            for k in (0..i).rev() {
                if grid[k][j].tree_height > max_up {
                    max_up = grid[k][j].tree_height
                }
                if continue_scenic_search && grid[k][j].tree_height >= curr_tree_height {
                    scenic_up += 1;
                    continue_scenic_search = false;
                } else if continue_scenic_search {
                    scenic_up += 1;
                }
            }
            let mut max_down = 0;
            let mut continue_scenic_search = true;
            let mut scenic_down = 0;
            for k in i + 1..grid_size {
                if grid[k][j].tree_height > max_down {
                    max_down = grid[k][j].tree_height
                }
                if continue_scenic_search && grid[k][j].tree_height >= curr_tree_height {
                    scenic_down += 1;
                    continue_scenic_search = false;
                } else if continue_scenic_search {
                    scenic_down += 1;
                }
            }
            let visible = i == 0
                || i == grid_size - 1
                || j == 0
                || j == grid_size - 1
                || curr_tree_height > max_left
                || curr_tree_height > max_right
                || curr_tree_height > max_up
                || curr_tree_height > max_down;
            grid[i][j].visible = visible;
            grid[i][j].scenic_score = scenic_left * scenic_right * scenic_up * scenic_down;
        }
    }

    for i in 0..grid_size {
        for j in 0..grid_size {
            if grid[i][j].visible {
                tot_visible += 1;
            }
            if grid[i][j].scenic_score > max_scenic {
                max_scenic = grid[i][j].scenic_score;
            }
            print!("{}", grid[i][j])
        }
        println!();
    }
    println!("Part 1: {}", tot_visible);
    println!("Part 2: {}", max_scenic);
}

struct Space {
    tree_height: i32,
    visible: bool,
    scenic_score: i32,
}
impl Space {
    fn new(tree_height: i32) -> Space {
        Space {
            tree_height,
            visible: false,
            scenic_score: 0,
        }
    }
}
impl fmt::Display for Space {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut t_or_f = 'F';
        if self.visible {
            t_or_f = 'T'
        }
        write!(f, "{}", t_or_f)
    }
}
