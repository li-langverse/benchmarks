use std::env;

extern "C" {
    fn li_wind_field_kernel();
    fn li_wind_field_checksum() -> f64;
}

fn main() {
    unsafe {
        li_wind_field_kernel();
        let checksum = li_wind_field_checksum();
        let args: Vec<String> = env::args().collect();
        if args.len() > 1 && args[1] == "--verify" {
            println!("{:.17}", checksum);
        }
    }
}
