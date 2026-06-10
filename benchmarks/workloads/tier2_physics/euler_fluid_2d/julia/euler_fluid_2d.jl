# 1D upwind advection smoke — matches common/euler_fluid_core.c oracle.
using Printf

const N = 64
const STEPS = 2000
const DT = 0.001
const DX = 0.05
const C = 0.5

function li_euler_fluid_2d_kernel()::Float64
    u = Vector{Float64}(undef, N)
    un = Vector{Float64}(undef, N)
    @inbounds for i in 0:(N - 1)
        u[i + 1] = 0.5 + 0.5 * sin(0.2 * i)
        un[i + 1] = u[i + 1]
    end
    @inbounds for _ in 1:STEPS
        for i in 1:(N - 2)
            un[i + 1] = u[i + 1] - C * DT / DX * (u[i + 1] - u[i])
        end
        @inbounds for i in 0:(N - 1)
            u[i + 1] = un[i + 1]
        end
    end
    return u[N ÷ 2 + 1]
end

if abspath(PROGRAM_FILE) == @__FILE__
    checksum = li_euler_fluid_2d_kernel()
    println(@sprintf("%.17g", checksum))
end
