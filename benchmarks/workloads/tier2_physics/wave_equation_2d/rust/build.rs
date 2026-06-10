fn main() {
    cc::Build::new()
        .file("../common/wave2d_core.c")
        .compile("wave_equation_2d_core");
}
