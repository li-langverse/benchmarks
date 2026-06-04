//! 1D FDTD waveguide smoke — matches common/fdtd_core.c oracle.

use std::env;

const N: usize = 32;
const STEPS: usize = 2000;
const DT: f64 = 0.001;
const DX: f64 = 0.01;

fn li_fdtd_waveguide_kernel() -> f64 {
    let mut ex = [0.0_f64; N];
    let mut hz = [0.0_f64; N];
    for i in 0..N {
        hz[i] = if i == N / 2 { 1.0 } else { 0.0 };
    }
    let coeff = DT / DX;
    for _ in 0..STEPS {
        for i in 0..N - 1 {
            ex[i] += coeff * (hz[i + 1] - hz[i]);
        }
        for i in 1..N {
            hz[i] += coeff * (ex[i] - ex[i - 1]);
        }
    }
    let mut e = 0.0;
    for i in 0..N {
        e += ex[i] * ex[i] + hz[i] * hz[i];
    }
    e
}

fn main() {
    let checksum = li_fdtd_waveguide_kernel();
    let args: Vec<String> = env::args().collect();
    if args.len() > 1 && args[1] == "--verify" {
        println!("{:.17}", checksum);
    }
}
