# Passive scalar: upwind advection + explicit diffusion — matches common/advdiff_core.c oracle.
using Printf

const NX = 128
const NY = 128
const STEPS = 15_000
const DX = 0.01
const DT = 0.0002
const VX = 0.8
const VY = 0.2
const DIFF = 0.05

function li_advdiff_2d_kernel()::Float64
    u = Matrix{Float64}(undef, NX, NY)
    v = Matrix{Float64}(undef, NX, NY)
    @inbounds for i in 1:NX
        x = (i - 1) * DX
        for j in 1:NY
            y = (j - 1) * DX
            r2 = (x - 0.35)^2 + (y - 0.35)^2
            u[i, j] = exp(-r2 / 0.002)
        end
    end
    r = DIFF * DT / (DX * DX)
    cfx = VX * DT / DX
    cfy = VY * DT / DX
    @inbounds for _ in 1:STEPS
        for i in 2:(NX - 1)
            for j in 2:(NY - 1)
                u_c = u[i, j]
                du_x = cfx > 0.0 ? u_c - u[i - 1, j] : u[i + 1, j] - u_c
                du_y = cfy > 0.0 ? u_c - u[i, j - 1] : u[i, j + 1] - u_c
                lap = u[i + 1, j] + u[i - 1, j] + u[i, j + 1] + u[i, j - 1] - 4.0 * u_c
                v[i, j] = u_c - cfx * du_x - cfy * du_y + r * lap
            end
        end
        for i in 2:(NX - 1)
            for j in 2:(NY - 1)
                u[i, j] = v[i, j]
            end
        end
    end
    acc = 0.0
    @inbounds for i in 1:NX, j in 1:NY
        acc += u[i, j]
    end
    return acc
end

if abspath(PROGRAM_FILE) == @__FILE__
    checksum = li_advdiff_2d_kernel()
    println(@sprintf("%.17g", checksum))
end
