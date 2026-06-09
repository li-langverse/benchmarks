//! 1D wave equation (leapfrog) — matches common/wave_core.c oracle.

const N: usize = 8192;
const STEPS: usize = 400_000;
const C: f64 = 1.0;
const DX: f64 = 0.01;
const DT: f64 = 0.004;
const R: f64 = C * DT / DX;
const R2: f64 = R * R;

fn li_wave_1d_kernel() -> f64 {
    let mut u0 = [0.0_f64; N];
    let mut u1 = [0.0_f64; N];
    let mut u2 = [0.0_f64; N];

    let center = 0.5 * (N - 1) as f64 * DX;
    let width = 0.15;
    for i in 0..N {
        let x = i as f64 * DX;
        let d = (x - center) / width;
        let val = (-d * d).exp();
        u1[i] = val;
        u0[i] = val;
        u2[i] = val;
    }
    u0[0] = 0.0;
    u0[N - 1] = 0.0;
    u1[0] = 0.0;
    u1[N - 1] = 0.0;

    for _ in 0..STEPS {
        for i in 1..N - 1 {
            u2[i] = 2.0 * u1[i] - u0[i] + R2 * (u1[i + 1] - 2.0 * u1[i] + u1[i - 1]);
        }
        u2[0] = 0.0;
        u2[N - 1] = 0.0;
        u0.copy_from_slice(&u1);
        u1.copy_from_slice(&u2);
    }

    let mut energy = 0.0;
    for i in 1..N - 1 {
        let v = (u1[i] - u0[i]) / DT;
        let du = (u1[i + 1] - u1[i - 1]) / (2.0 * DX);
        energy += 0.5 * (v * v + C * C * du * du);
    }
    energy
}

fn main() {
    let checksum = li_wave_1d_kernel();
    let args: Vec<String> = std::env::args().collect();
    if args.len() > 1 && args[1] == "--verify" {
        println!("{:.17}", checksum);
    }
}
