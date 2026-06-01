# Native 2D heat equation (explicit Euler) — matches common/heat_core.c oracle.
using Printf

const NX = 128
const NY = 128
const STEPS = 20_000
const ALPHA = 0.25
const DX = 0.01
const DT = 0.0001
const R = ALPHA * DT / (DX * DX)
const PI = 3.141592653589793

function li_heat_2d_kernel()::Float64
    u = Matrix{Float64}(undef, NX, NY)
    v = Matrix{Float64}(undef, NX, NY)
    @inbounds for i in 1:NX
        x = (i - 1) * DX
        for j in 1:NY
            y = (j - 1) * DX
            u[i, j] = sin(PI * x) * sin(PI * y)
        end
    end
    @inbounds for _ in 1:STEPS
        for i in 2:(NX - 1)
            for j in 2:(NY - 1)
                v[i, j] = u[i, j] + R * (
                    u[i + 1, j] + u[i - 1, j] + u[i, j + 1] + u[i, j - 1] -
                    4.0 * u[i, j]
                )
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
    checksum = li_heat_2d_kernel()
    println(@sprintf("%.17g", checksum))
end
