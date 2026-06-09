# Native 2D wave equation (leapfrog) — matches common/wave2d_core.c oracle.
using Printf

const NX = 128
const NY = 128
const STEPS = 25_000
const C = 1.0
const DX = 0.01
const DT = 0.004
const R2 = (C * DT / DX) * (C * DT / DX)

function li_wave_2d_kernel()::Float64
    u0 = Matrix{Float64}(undef, NX, NY)
    u1 = Matrix{Float64}(undef, NX, NY)
    u2 = Matrix{Float64}(undef, NX, NY)
    cx = 0.5 * (NX - 1) * DX
    cy = 0.5 * (NY - 1) * DX
    width = 0.12
    @inbounds for i in 1:NX
        x = (i - 1) * DX
        for j in 1:NY
            y = (j - 1) * DX
            dx = (x - cx) / width
            dy = (y - cy) / width
            pulse = exp(-(dx * dx + dy * dy))
            u1[i, j] = pulse
            u0[i, j] = pulse
            u2[i, j] = pulse
        end
    end
    @inbounds for _ in 1:STEPS
        for i in 2:(NX - 1)
            for j in 2:(NY - 1)
                u2[i, j] = 2.0 * u1[i, j] - u0[i, j] +
                    R2 * (
                        u1[i + 1, j] - 2.0 * u1[i, j] + u1[i - 1, j] +
                        u1[i, j + 1] - 2.0 * u1[i, j] + u1[i, j - 1]
                    )
            end
        end
        for i in 1:NX
            u2[i, 1] = 0.0
            u2[i, NY] = 0.0
            u0[i, 1] = 0.0
            u0[i, NY] = 0.0
            u1[i, 1] = 0.0
            u1[i, NY] = 0.0
        end
        for j in 1:NY
            u2[1, j] = 0.0
            u2[NX, j] = 0.0
            u0[1, j] = 0.0
            u0[NX, j] = 0.0
            u1[1, j] = 0.0
            u1[NX, j] = 0.0
        end
        u0 .= u1
        u1 .= u2
    end
    energy = 0.0
    @inbounds for i in 2:(NX - 1)
        for j in 2:(NY - 1)
            v = (u1[i, j] - u0[i, j]) / DT
            ux = (u1[i + 1, j] - u1[i - 1, j]) / (2.0 * DX)
            uy = (u1[i, j + 1] - u1[i, j - 1]) / (2.0 * DX)
            energy += 0.5 * (v * v + C * C * (ux * ux + uy * uy))
        end
    end
    return energy
end

function main()
    checksum = li_wave_2d_kernel()
    if "--verify" in ARGS
        @printf("%.17g\n", checksum)
    end
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
