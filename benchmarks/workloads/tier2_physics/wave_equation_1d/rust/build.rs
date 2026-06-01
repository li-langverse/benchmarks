fn main() {
    cc::Build::new().file("../common/wave_core.c").compile("wave_equation_1d_core");
}
