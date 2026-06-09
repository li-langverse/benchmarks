fn main() {
    cc::Build::new()
        .file("../common/sph_dam_core.c")
        .flag("-O3")
        .flag("-ffast-math")
        .flag("-march=native")
        .compile("sph_dam_break_2d_core");
}
