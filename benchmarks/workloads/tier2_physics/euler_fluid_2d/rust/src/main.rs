// 1D upwind advection smoke — matches common/euler_fluid_core.c oracle.
use std::env;

const N: usize = 64;
const STEPS: usize = 2000;
const DT: f64 = 0.001;
const DX: f64 = 0.05;
const C: f64 = 0.5;

fn li_euler_fluid_2d_kernel() -> f64 {
    let mut u = [0.0_f64; N];
    let mut un = [0.0_f64; N];
    for i in 0..N {
        u[i] = 0.5 + 0.5 * (0.2 * i as f64).sin();
        un[i] = u[i];
    }
    for _ in 0..STEPS {
        for i in 1..N - 1 {
            un[i] = u[i] - C * DT / DX * (u[i] - u[i - 1]);
        }
        u.copy_from_slice(&un);
    }
    u[N / 2]
}

fn main() {
    let checksum = li_euler_fluid_2d_kernel();
    let args: Vec<String> = env::args().collect();
    if args.len() > 1 && args[1] == "--verify" {
        println!("{:.17}", checksum);
    }
}
