fn main() {
    cc::Build::new()
        .file("../common/fdtd_core.c")
        .compile("fdtd_waveguide_2d_core");
}
