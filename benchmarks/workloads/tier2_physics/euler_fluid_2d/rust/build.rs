fn main() {
    cc::Build::new()
        .file("../common/euler_fluid_core.c")
        .compile("euler_fluid_2d_core");
}
