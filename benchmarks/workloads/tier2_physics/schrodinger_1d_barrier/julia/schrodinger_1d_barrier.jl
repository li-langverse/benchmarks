# 1D TDSE barrier smoke — matches common/tdse_core.c oracle.
using Printf

const N = 64
const STEPS = 4000
const DT = 0.0001

function li_schrodinger_1d_barrier_kernel()::Float64
    re = Vector{Float64}(undef, N)
    im = Vector{Float64}(undef, N)
    half = N ÷ 2
    @inbounds for i in 1:N
        d = (i - 1 - half) * 0.15
        re[i] = exp(-0.5 * d * d)
        im[i] = 0.0
    end
    @inbounds for _ in 1:STEPS
        for i in 2:(N - 1)
            lap = re[i + 1] - 2.0 * re[i] + re[i - 1]
            re[i] += DT * lap
            im[i] += DT * lap
        end
    end
    n2 = 0.0
    @inbounds for i in 1:N
        n2 += re[i] * re[i] + im[i] * im[i]
    end
    return n2
end

if abspath(PROGRAM_FILE) == @__FILE__
    checksum = li_schrodinger_1d_barrier_kernel()
    println(@sprintf("%.17g", checksum))
end
