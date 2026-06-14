# tier_crypto — primitive microbenchmarks

Cross-implementation **validity** (Li vs hashlib/OpenSSL/cryptography) plus **throughput** rows for Li microbenches and OpenSSL `speed`.

## Run

```bash
export LIC_ROOT=/path/to/lic
./benchmarks/workloads/tier_crypto/run_tier_crypto.sh --profile ci
# or
python3 benchmarks/harness/bench_crypto.py --profile baseline
```

Profiles:

| Profile | Validity | Timing runs | OpenSSL speed |
|---------|----------|-------------|---------------|
| `ci` | yes | 3 | 1s |
| `baseline` | yes | adaptive | 3s |

Output: `benchmarks/workloads/tier_crypto/results/tier_crypto.csv`

Floors: `baseline.csv` (`min_ops_per_sec` per primitive/lang; CI uses 25% slack).

Li bench sources live in `lic/packages/li-crypto/li-tests/bench/` and `lic/packages/li-pqc/li-tests/bench/`.
