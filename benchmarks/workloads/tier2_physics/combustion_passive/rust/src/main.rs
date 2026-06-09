//! Passive combustion — fuel burn + temperature rise (matches common/combust_core.c oracle).

use std::env;

const N: usize = 32;
const STEPS: usize = 500;
const DT: f64 = 0.02;
const BURN: f64 = 0.1;

fn li_combustion_passive_kernel() -> f64 {
    let mut fuel = [1.0_f64; N];
    let mut temp = [300.0_f64; N];
    for _ in 0..STEPS {
        for i in 0..N {
            let mut burned = BURN * DT * fuel[i];
            if burned > fuel[i] {
                burned = fuel[i];
            }
            fuel[i] -= burned;
            temp[i] += burned * 100.0;
        }
    }
    temp[0]
}

fn main() {
    let checksum = li_combustion_passive_kernel();
    let args: Vec<String> = env::args().collect();
    if args.len() > 1 && args[1] == "--verify" {
        println!("{:.17}", checksum);
    }
}
