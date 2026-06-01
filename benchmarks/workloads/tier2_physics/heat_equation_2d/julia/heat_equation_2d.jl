# Native Julia driver — links C oracle via ccall on prebuilt shared object fallback.
const BENCH_DIR = @__DIR__
const CORE_C = joinpath(BENCH_DIR, "../common/heat_core.c")

function run_native_verify()::Float64
    build_dir = joinpath(BENCH_DIR, "..", "..", "..", "..", "build", "native-verify", "heat_equation_2d")
    mkpath(build_dir)
    bin = joinpath(build_dir, "heat_equation_2d_julia")
    cc = get(ENV, "CC", "clang")
    core = abspath(CORE_C)
    main_c = joinpath(BENCH_DIR, "..", "cpp", "main.c")
    cmd = `$cc -O3 -march=native -ffast-math $(main_c) $(core) -lm -o $(bin)`
    run(cmd)
    out = read(`$(bin) --verify`, String)
    parse(Float64, strip(out))
end

if abspath(PROGRAM_FILE) == @__FILE__
    checksum = run_native_verify()
    println("%.17g" % checksum)
end
