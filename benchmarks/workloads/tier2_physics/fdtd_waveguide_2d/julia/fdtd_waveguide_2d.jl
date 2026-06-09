# 1D Yee FDTD waveguide — matches common/fdtd_core.c oracle.
using Printf

const N = 32
const STEPS = 2000
const DT = 0.001
const DX = 0.01

function li_fdtd_waveguide_kernel()::Float64
    ex = zeros(Float64, N)
    hz = zeros(Float64, N)
    hz[N ÷ 2 + 1] = 1.0
    coeff = DT / DX
    @inbounds for _ in 1:STEPS
        for i in 1:(N - 1)
            ex[i] += coeff * (hz[i + 1] - hz[i])
        end
        for i in 2:N
            hz[i] += coeff * (ex[i] - ex[i - 1])
        end
    end
    e = 0.0
    @inbounds for i in 1:N
        e += ex[i] * ex[i] + hz[i] * hz[i]
    end
    return e
end

if abspath(PROGRAM_FILE) == @__FILE__
    checksum = li_fdtd_waveguide_kernel()
    println(@sprintf("%.17g", checksum))
end
