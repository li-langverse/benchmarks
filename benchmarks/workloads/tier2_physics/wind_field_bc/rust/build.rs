fn main() {
    cc::Build::new()
        .file("../common/wind_core.c")
        .compile("wind_field_bc_core");
}
