use std::env;

extern "C" {
    fn li_fdtd_waveguide_kernel();
    fn li_fdtd_waveguide_checksum() -> f64;
}

fn main() {
    unsafe {
        li_fdtd_waveguide_kernel();
        let checksum = li_fdtd_waveguide_checksum();
        let args: Vec<String> = env::args().collect();
        if args.len() > 1 && args[1] == "--verify" {
            println!("{:.17}", checksum);
        }
    }
}
