# Native 1D wave equation (leapfrog) — matches common/wave_core.c oracle.
using Printf

const N = 8192
const STEPS = 400_000
const C = 1.0
const DX = 0.01
const DT = 0.004
const R = C * DT / DX
const R2 = R * R

function li_wave_1d_kernel()::Float64
    u0 = Vector{Float64}(undef, N)
    u1 = Vector{Float64}(undef, N)
    u2 = Vector{Float64}(undef, N)
    center = 0.5 * (N - 1) * DX
    width = 0.15
    @inbounds for i in 1:N
        x = (i - 1) * DX
        d = (x - center) / width
        val = exp(-d * d)
        u1[i] = val
        u0[i] = val
        u2[i] = val
    end
    u0[1] = 0.0
    u0[N] = 0.0
    u1[1] = 0.0
    u1[N] = 0.0

    @inbounds for _ in 1:STEPS
        for i in 2:(N - 1)
            u2[i] = 2.0 * u1[i] - u0[i] + R2 * (u1[i + 1] - 2.0 * u1[i] + u1[i - 1])
        end
        u2[1] = 0.0
        u2[N] = 0.0
        u0 .= u1
        u1 .= u2
    end

    energy = 0.0
    @inbounds for i in 2:(N - 1)
        v = (u1[i] - u0[i]) / DT
        du = (u1[i + 1] - u1[i - 1]) / (2.0 * DX)
        energy += 0.5 * (v * v + C * C * du * du)
    end
    return energy
end

if abspath(PROGRAM_FILE) == @__FILE__
    checksum = li_wave_1d_kernel()
    println(@sprintf("%.17g", checksum))
end
