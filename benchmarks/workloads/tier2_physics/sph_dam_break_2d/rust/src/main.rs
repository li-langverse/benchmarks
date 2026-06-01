use std::env;

extern "C" {
    fn li_sph_dam_2d_kernel();
    fn li_sph_dam_2d_checksum() -> f64;
}

fn main() {
    unsafe {
        li_sph_dam_2d_kernel();
        let checksum = li_sph_dam_2d_checksum();
        let args: Vec<String> = env::args().collect();
        if args.len() > 1 && args[1] == "--verify" {
            println!("{:.17}", checksum);
        }
    }
}
