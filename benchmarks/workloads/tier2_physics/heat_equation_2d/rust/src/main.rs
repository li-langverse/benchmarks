//! 2D heat equation (explicit Euler) — matches common/heat_core.c oracle.

const NX: usize = 128;
const NY: usize = 128;
const STEPS: usize = 20_000;
const ALPHA: f64 = 0.25;
const DX: f64 = 0.01;
const DT: f64 = 0.0001;

fn li_heat_2d_kernel() -> f64 {
    let mut u = [[0.0_f64; NY]; NX];
    let mut v = [[0.0_f64; NY]; NX];

    let pi = std::f64::consts::PI;
    for i in 0..NX {
        for j in 0..NY {
            let x = i as f64 * DX;
            let y = j as f64 * DX;
            u[i][j] = (pi * x).sin() * (pi * y).sin();
        }
    }

    let r = ALPHA * DT / (DX * DX);
    for _ in 0..STEPS {
        for i in 1..NX - 1 {
            for j in 1..NY - 1 {
                v[i][j] = u[i][j]
                    + r * (u[i + 1][j] + u[i - 1][j] + u[i][j + 1] + u[i][j - 1] - 4.0 * u[i][j]);
            }
        }
        for i in 1..NX - 1 {
            for j in 1..NY - 1 {
                u[i][j] = v[i][j];
            }
        }
    }

    let mut acc = 0.0;
    for i in 0..NX {
        for j in 0..NY {
            acc += u[i][j];
        }
    }
    acc
}

fn main() {
    let checksum = li_heat_2d_kernel();
    let args: Vec<String> = std::env::args().collect();
    if args.len() > 1 && args[1] == "--verify" {
        println!("{:.17}", checksum);
    }
}
