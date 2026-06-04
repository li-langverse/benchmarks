//! 2D wave equation (leapfrog) — matches common/wave2d_core.c oracle.

use std::env;

const NX: usize = 128;
const NY: usize = 128;
const STEPS: usize = 25_000;
const C: f64 = 1.0;
const DX: f64 = 0.01;
const DT: f64 = 0.004;

type Grid = [[f64; NY]; NX];

fn init(u0: &mut Grid, u1: &mut Grid, u2: &mut Grid) {
    let cx = 0.5 * (NX - 1) as f64 * DX;
    let cy = 0.5 * (NY - 1) as f64 * DX;
    let width = 0.12;
    for i in 0..NX {
        for j in 0..NY {
            let x = i as f64 * DX;
            let y = j as f64 * DX;
            let dx = (x - cx) / width;
            let dy = (y - cy) / width;
            let pulse = (-(dx * dx + dy * dy)).exp();
            u1[i][j] = pulse;
            u0[i][j] = pulse;
            u2[i][j] = pulse;
        }
    }
}

fn energy(u0: &Grid, u1: &Grid) -> f64 {
    let mut e = 0.0;
    for i in 1..NX - 1 {
        for j in 1..NY - 1 {
            let v = (u1[i][j] - u0[i][j]) / DT;
            let ux = (u1[i + 1][j] - u1[i - 1][j]) / (2.0 * DX);
            let uy = (u1[i][j + 1] - u1[i][j - 1]) / (2.0 * DX);
            e += 0.5 * (v * v + C * C * (ux * ux + uy * uy));
        }
    }
    e
}

fn li_wave_2d_kernel() -> f64 {
    let mut u0 = [[0.0; NY]; NX];
    let mut u1 = [[0.0; NY]; NX];
    let mut u2 = [[0.0; NY]; NX];
    init(&mut u0, &mut u1, &mut u2);
    let r2 = (C * DT / DX) * (C * DT / DX);
    for _ in 0..STEPS {
        for i in 1..NX - 1 {
            for j in 1..NY - 1 {
                u2[i][j] = 2.0 * u1[i][j] - u0[i][j]
                    + r2
                        * (u1[i + 1][j] - 2.0 * u1[i][j] + u1[i - 1][j]
                            + u1[i][j + 1] - 2.0 * u1[i][j] + u1[i][j - 1]);
            }
        }
        for i in 0..NX {
            u2[i][0] = 0.0;
            u2[i][NY - 1] = 0.0;
            u0[i][0] = 0.0;
            u0[i][NY - 1] = 0.0;
            u1[i][0] = 0.0;
            u1[i][NY - 1] = 0.0;
        }
        for j in 0..NY {
            u2[0][j] = 0.0;
            u2[NX - 1][j] = 0.0;
            u0[0][j] = 0.0;
            u0[NX - 1][j] = 0.0;
            u1[0][j] = 0.0;
            u1[NX - 1][j] = 0.0;
        }
        for i in 0..NX {
            for j in 0..NY {
                u0[i][j] = u1[i][j];
                u1[i][j] = u2[i][j];
            }
        }
    }
    energy(&u0, &u1)
}

fn main() {
    let checksum = li_wave_2d_kernel();
    let args: Vec<String> = env::args().collect();
    if args.len() > 1 && args[1] == "--verify" {
        println!("{:.17}", checksum);
    }
}
