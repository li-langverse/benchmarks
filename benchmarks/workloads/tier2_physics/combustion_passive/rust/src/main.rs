use std::env;

extern "C" {
    fn li_combustion_passive_kernel();
    fn li_combustion_passive_checksum() -> f64;
}

fn main() {
    unsafe {
        li_combustion_passive_kernel();
        let checksum = li_combustion_passive_checksum();
        let args: Vec<String> = env::args().collect();
        if args.len() > 1 && args[1] == "--verify" {
            println!("{:.17}", checksum);
        }
    }
}
