use std::env;

extern "C" {
    fn li_schrodinger_1d_barrier_kernel();
    fn li_schrodinger_1d_barrier_checksum() -> f64;
}

fn main() {
    unsafe {
        li_schrodinger_1d_barrier_kernel();
        let checksum = li_schrodinger_1d_barrier_checksum();
        let args: Vec<String> = env::args().collect();
        if args.len() > 1 && args[1] == "--verify" {
            println!("{:.17}", checksum);
        }
    }
}
