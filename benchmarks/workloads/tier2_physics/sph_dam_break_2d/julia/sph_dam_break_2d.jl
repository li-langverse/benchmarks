# Native 2D dam-break SPH stub — matches common/sph_dam_core.c oracle.
using Printf

const LI_SPH_N = 256
const LI_SPH_STEPS = 8000
const LI_SPH_BOX = 1.0
const LI_SPH_H = 0.08
const LI_SPH_DT = 0.00025
const LI_SPH_G = 9.81
const LI_SPH_K = 500.0

function li_sph_forces!(x::Matrix{Float64}, v::Matrix{Float64}, a::Matrix{Float64})
    @inbounds for i in 1:LI_SPH_N
        a[1, i] = 0.0
        a[2, i] = -LI_SPH_G
    end
    @inbounds for i in 1:LI_SPH_N
        for j in (i + 1):LI_SPH_N
            rx = x[1, j] - x[1, i]
            ry = x[2, j] - x[2, i]
            r2 = rx * rx + ry * ry + 1e-12
            r = sqrt(r2)
            if r >= LI_SPH_H
                continue
            end
            q = 1.0 - r / LI_SPH_H
            f = LI_SPH_K * q * q / r
            fx = f * rx
            fy = f * ry
            a[1, i] -= fx
            a[2, i] -= fy
            a[1, j] += fx
            a[2, j] += fy
        end
    end
    @inbounds for i in 1:LI_SPH_N
        if x[1, i] < 0.0
            x[1, i] = 0.0
            v[1, i] = 0.0
        end
        if x[1, i] > LI_SPH_BOX
            x[1, i] = LI_SPH_BOX
            v[1, i] = 0.0
        end
        if x[2, i] < 0.0
            x[2, i] = 0.0
            v[2, i] = 0.0
        end
        if x[2, i] > LI_SPH_BOX
            x[2, i] = LI_SPH_BOX
            v[2, i] = 0.0
        end
    end
end

function li_sph_dam_2d_kernel()::Float64
    x = zeros(2, LI_SPH_N)
    v = zeros(2, LI_SPH_N)
    a = zeros(2, LI_SPH_N)
    idx = 1
    dx = 0.04
    @inbounds for j in 0:15
        for i in 0:15
            if idx > LI_SPH_N
                break
            end
            x[1, idx] = 0.05 + i * dx
            x[2, idx] = 0.05 + j * dx
            a[2, idx] = -LI_SPH_G
            idx += 1
        end
        if idx > LI_SPH_N
            break
        end
    end
    @inbounds for _ in 1:LI_SPH_STEPS
        li_sph_forces!(x, v, a)
        for i in 1:LI_SPH_N
            v[1, i] += 0.5 * LI_SPH_DT * a[1, i]
            v[2, i] += 0.5 * LI_SPH_DT * a[2, i]
            x[1, i] += LI_SPH_DT * v[1, i]
            x[2, i] += LI_SPH_DT * v[2, i]
        end
        li_sph_forces!(x, v, a)
        for i in 1:LI_SPH_N
            v[1, i] += 0.5 * LI_SPH_DT * a[1, i]
            v[2, i] += 0.5 * LI_SPH_DT * a[2, i]
        end
    end
    acc = 0.0
    @inbounds for i in 1:LI_SPH_N
        acc += x[2, i]
    end
    return acc
end

if abspath(PROGRAM_FILE) == @__FILE__
    checksum = li_sph_dam_2d_kernel()
    println(@sprintf("%.17g", checksum))
end
