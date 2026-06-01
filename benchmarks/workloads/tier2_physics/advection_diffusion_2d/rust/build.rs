fn main() {
    cc::Build::new()
        .file("../common/advdiff_core.c")
        .compile("advection_diffusion_2d_core");
}
