# Native 1D wind-field BC update — matches common/wind_core.c oracle.
using Printf

const N = 64
const STEPS = 1000
const DT = 0.01

function li_wind_field_kernel()::Float64
    u = ones(Float64, N)
    @inbounds for _ in 1:STEPS
        for i in 2:(N - 1)
            u[i] = u[i] - DT * (u[i] - u[i - 1])
        end
    end
    return u[N ÷ 2]
end

if abspath(PROGRAM_FILE) == @__FILE__
    checksum = li_wind_field_kernel()
    println(@sprintf("%.17g", checksum))
end
