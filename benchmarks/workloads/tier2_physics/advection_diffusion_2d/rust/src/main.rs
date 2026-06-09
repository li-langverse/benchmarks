use std::env;

extern "C" {
    fn li_advdiff_2d_kernel();
    fn li_advdiff_2d_checksum() -> f64;
}

fn main() {
    unsafe {
        li_advdiff_2d_kernel();
        let checksum = li_advdiff_2d_checksum();
        let args: Vec<String> = env::args().collect();
        if args.len() > 1 && args[1] == "--verify" {
            println!("{:.17}", checksum);
        }
    }
}
