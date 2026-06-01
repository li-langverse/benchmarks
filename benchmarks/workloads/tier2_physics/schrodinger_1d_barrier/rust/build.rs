fn main() {
    cc::Build::new().file("../common/tdse_core.c").compile("schrodinger_1d_barrier_core");
}
