// 1D upwind wind-field BC smoke — matches common/wind_core.c oracle (in-place updates).
use std::env;

const N: usize = 64;
const STEPS: usize = 1000;
const DT: f64 = 0.01;

fn li_wind_field_kernel() -> f64 {
    let mut u = [1.0_f64; N];
    for _ in 0..STEPS {
        for i in 1..N - 1 {
            u[i] = u[i] - DT * (u[i] - u[i - 1]);
        }
    }
    u[N / 2]
}

fn main() {
    let checksum = li_wind_field_kernel();
    let args: Vec<String> = env::args().collect();
    if args.len() > 1 && args[1] == "--verify" {
        println!("{:.17}", checksum);
    }
}
