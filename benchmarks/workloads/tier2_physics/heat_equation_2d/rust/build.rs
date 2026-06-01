fn main() {
    cc::Build::new().file("../common/heat_core.c").compile("heat_equation_2d_core");
}
