fn main() {
    cc::Build::new()
        .file("../common/combust_core.c")
        .compile("combustion_passive_core");
}
