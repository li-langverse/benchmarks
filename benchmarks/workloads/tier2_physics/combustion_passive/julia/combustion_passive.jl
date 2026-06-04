# Passive combustion scalar — matches common/combust_core.c oracle.
using Printf

const N = 32
const STEPS = 500
const DT = 0.02
const BURN = 0.1

function li_combustion_passive_kernel()::Float64
    fuel = ones(Float64, N)
    temp = fill(300.0, N)
    @inbounds for _ in 1:STEPS
        for i in 1:N
            burned = BURN * DT * fuel[i]
            if burned > fuel[i]
                burned = fuel[i]
            end
            fuel[i] -= burned
            temp[i] += burned * 100.0
        end
    end
    return temp[1]
end

if abspath(PROGRAM_FILE) == @__FILE__
    checksum = li_combustion_passive_kernel()
    println(@sprintf("%.17g", checksum))
end
