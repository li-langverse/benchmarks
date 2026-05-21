# li-httpd master plan — implementation progress log

Auto-appended by `./scripts/httpd-masterplan-step.sh <step-id> <note>` after each milestone.

Plan: `lic/docs/superpowers/plans/2026-05-16-li-httpd-plan.md`

## Step: step-0-baseline — 2026-05-21T09:48:16Z

Baseline before M1 completion push.

```bash
# full suite (fast flags optional: SKIP_BUILD=1 if lic built)
LIC_ROOT=/workspace/lic SKIP_BUILD=${SKIP_BUILD:-1} SKIP_TIER0=${SKIP_TIER0:-1} \
  BENCH_RUNS=${BENCH_RUNS:-1} HTTP_BENCH_RUNS=${HTTP_BENCH_RUNS:-2} \
  /workspace/scripts/run-full-benchmark-suite.sh
```

==> tier 1+2 — micro + physics (runs=1)
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
simd_dot cpp wall_time=0.0580s (median of 1)
simd_dot rust wall_time=0.0563s (median of 1)
simd_dot julia wall_time=0.0512s (median of 1)
simd_dot li wall_time=0.0007s (median of 1)
ok simd_dot
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
matmul_naive cpp wall_time=0.0026s (median of 1)
matmul_naive rust wall_time=0.0034s (median of 1)
matmul_naive julia wall_time=0.0035s (median of 1)
matmul_naive li wall_time=0.0035s (median of 1)
ok matmul_naive
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
matmul_blocked cpp wall_time=0.0101s (median of 1)
matmul_blocked rust wall_time=0.0100s (median of 1)
matmul_blocked julia wall_time=0.0102s (median of 1)
matmul_blocked li wall_time=0.0105s (median of 1)
ok matmul_blocked
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
reduce_sum cpp wall_time=0.3151s (median of 1)
reduce_sum rust wall_time=0.3056s (median of 1)
reduce_sum julia wall_time=0.2981s (median of 1)
reduce_sum li wall_time=0.3001s (median of 1)
ok reduce_sum
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
horner_pure_li cpp wall_time=0.0011s (median of 1)
horner_pure_li rust wall_time=0.0009s (median of 1)
horner_pure_li julia wall_time=0.0010s (median of 1)
horner_pure_li li wall_time=0.0009s (median of 1)
ok horner_pure_li
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
md_lennard_jones cpp wall_time=2.5971s (median of 1)
md_lennard_jones rust wall_time=2.5885s (median of 1)
md_lennard_jones julia wall_time=2.5909s (median of 1)
md_lennard_jones li wall_time=0.0030s (median of 1)
ok md_lennard_jones
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
three_body cpp wall_time=0.2435s (median of 1)
three_body rust wall_time=0.2437s (median of 1)
three_body julia wall_time=0.2436s (median of 1)
three_body li wall_time=0.2435s (median of 1)
ok three_body
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
nbody_gravity cpp wall_time=1.1879s (median of 1)
nbody_gravity rust wall_time=1.1693s (median of 1)
nbody_gravity julia wall_time=1.1698s (median of 1)
nbody_gravity li wall_time=1.1703s (median of 1)
ok nbody_gravity
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
harmonic_oscillator_chain cpp wall_time=0.1120s (median of 1)
harmonic_oscillator_chain rust wall_time=0.0886s (median of 1)
harmonic_oscillator_chain julia wall_time=0.0884s (median of 1)
harmonic_oscillator_chain li wall_time=0.0829s (median of 1)
ok harmonic_oscillator_chain
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
wave_equation_1d cpp wall_time=1.6576s (median of 1)
wave_equation_1d rust wall_time=1.6568s (median of 1)
wave_equation_1d julia wall_time=1.7976s (median of 1)
wave_equation_1d li wall_time=1.6583s (median of 1)
ok wave_equation_1d
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
heat_equation_2d cpp wall_time=0.1341s (median of 1)
heat_equation_2d rust wall_time=0.1385s (median of 1)
heat_equation_2d julia wall_time=0.1334s (median of 1)
heat_equation_2d li wall_time=0.1305s (median of 1)
ok heat_equation_2d
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
double_pendulum cpp wall_time=0.3176s (median of 1)
double_pendulum rust wall_time=0.3178s (median of 1)
double_pendulum julia wall_time=0.3197s (median of 1)
double_pendulum li wall_time=0.3177s (median of 1)
ok double_pendulum
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
advection_diffusion_2d cpp wall_time=0.1129s (median of 1)
advection_diffusion_2d rust wall_time=0.1249s (median of 1)
advection_diffusion_2d julia wall_time=0.1127s (median of 1)
advection_diffusion_2d li wall_time=0.1115s (median of 1)
ok advection_diffusion_2d
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
wave_equation_2d cpp wall_time=0.2745s (median of 1)
wave_equation_2d rust wall_time=0.2720s (median of 1)
wave_equation_2d julia wall_time=0.2775s (median of 1)
wave_equation_2d li wall_time=0.2787s (median of 1)
ok wave_equation_2d
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
sph_dam_break_2d cpp wall_time=0.8394s (median of 1)
sph_dam_break_2d rust wall_time=0.8377s (median of 1)
sph_dam_break_2d julia wall_time=0.8391s (median of 1)
sph_dam_break_2d li wall_time=0.8401s (median of 1)
ok sph_dam_break_2d
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip rigid_body_stack: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/rigid_body_stack/li/main.li', '-o', '/workspace/lic/build/bench/rigid_body_stack/rigid_body_stack_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:5: error [lic.error]: expected ':'
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected ')'
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected '='
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected indented block
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected top-level declaration
WARN skip three_body_pure: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li', '-o', '/workspace/lic/build/bench/three_body_pure/three_body_pure_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip wind_field_bc: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/wind_field_bc/li/main.li', '-o', '/workspace/lic/build/bench/wind_field_bc/wind_field_bc_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip combustion_passive: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/combustion_passive/li/main.li', '-o', '/workspace/lic/build/bench/combustion_passive/combustion_passive_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip orbit_two_body: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/orbit_two_body/li/main.li', '-o', '/workspace/lic/build/bench/orbit_two_body/orbit_two_body_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip fdtd_waveguide_2d: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/fdtd_waveguide_2d/li/main.li', '-o', '/workspace/lic/build/bench/fdtd_waveguide_2d/fdtd_waveguide_2d_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip schrodinger_1d_barrier: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/schrodinger_1d_barrier/li/main.li', '-o', '/workspace/lic/build/bench/schrodinger_1d_barrier/schrodinger_1d_barrier_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip euler_fluid_2d: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/euler_fluid_2d/li/main.li', '-o', '/workspace/lic/build/bench/euler_fluid_2d/euler_fluid_2d_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip cloth_swing: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/cloth_swing/li/main.li', '-o', '/workspace/lic/build/bench/cloth_swing/cloth_swing_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip ragdoll_chain: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/ragdoll_chain/li/main.li', '-o', '/workspace/lic/build/bench/ragdoll_chain/ragdoll_chain_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
tier12: 10 skipped: rigid_body_stack, three_body_pure, wind_field_bc, combustion_passive, orbit_two_body, fdtd_waveguide_2d, schrodinger_1d_barrier, euler_fluid_2d, cloth_swing, ragdoll_chain
updated /workspace/lic/benchmarks/results/latest.csv
==> tier 3 — ecosystem (compile, security, async)
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
lic_build_async lic build wall_time=0.0021s
lic_build_effects_net lic build wall_time=0.0019s
lic_build_effects_async lic build wall_time=0.0018s
lic_build_alloc lic build wall_time=0.0019s
lic_check_contracts lic build wall_time=0.0021s
async_await_chain li wall_time=0.0008s
security_security_corpus wall_time=0.1337s
security_security_cve_patterns wall_time=0.0222s
security_security_webserver_registry wall_time=0.0202s
updated /workspace/lic/benchmarks/results/latest.csv (+6 ecosystem rows)
==> tier 5 — HTTP multi-oracle (nginx, apache, lighttpd, node, bun, li)
bench_http: wrote 26 row(s) -> /workspace/vendor/lis-tier5/results/latest.csv
run-tier5-http-bench: ok (profile=nightly, oracles=nginx,apache,lighttpd,node,bun,li)
==> tier 5 — supplemental proxy_loopback (li_epoll + li c_epoll vs nginx)
2026/05/21 09:53:57 [notice] 47736#47736: signal process started
2026/05/21 09:54:38 [notice] 47780#47780: signal process started
2026/05/21 09:55:42 [notice] 47850#47850: signal process started
static_small li=94906 nginx=80460
keepalive_pipelining li=140104 nginx=119589
proxy_loopback li=115690 li_c=133315 nginx=75161
tier5-http-bench: wrote 7 rows -> /workspace/lic/benchmarks/results/http_tier5.csv
==> tier 5 — HTTP exploits (TIER5_EXPLOIT_PROFILE=pr)
exploit_http: 36 row(s) -> /workspace/vendor/lis-tier5/results/exploit_report.csv (0 fail)
run-tier5-http-exploits: ok (pr, langs=nginx,apache,li, csv=/workspace/vendor/lis-tier5/results/exploit_report.csv)
merged tier5 (latest.csv + extra) into /workspace/lic/benchmarks/results/latest.csv
==> ingest + summary.json
ingest-csv-smoke: skip (lic lacks std/io + std/csv — PH-IO-4)
build-summary-li: skip (lic lacks std/summary — PH-IO-7)
wrote /workspace/data/latest/summary.json (31 rows, 31 charts)
recorded 2026-05-21T095602Z.json (18 deltas vs previous)
regression check failed: matmul_naive
==> benchmark status report
=== Benchmark failures report ===
Dashboard: https://li-langverse.github.io/benchmarks/
generated_at: 2026-05-21T09:56:02.839055+00:00

RED (1):
  matmul_naive                 tier=1    1.346×  lic  PH=PH-5b,PH-7e

YELLOW (1):
  static_large                 tier=5    1.028×  lis  PH=PH-H

GREEN near threshold (>1.0× cpp, 5):
  matmul_blocked               tier=1    1.040×  lic  PH=PH-5b
  wave_equation_2d             tier=2    1.015×  lic  PH=PH-5b
  sph_dam_break_2d             tier=2    1.001×  lic  PH=PH-5b
  wave_equation_1d             tier=2    1.000×  lic  PH=PH-5b
  double_pendulum              tier=2    1.000×  lic  PH=PH-5b

UNKNOWN / no data (9):
  tier0_stability              tier=0  lic
  cloth_swing                  tier=2  lic
  combustion_passive           tier=2  lic
  euler_fluid_2d               tier=2  lic
  rigid_body_stack             tier=2  lic
  wind_field_bc                tier=2  lic
  lip_smoke                    tier=3  lip
  lit_smoke                    tier=3  lit
  tier5_http_exploits          tier=5  lis

Since last snapshot (18 deltas):
  {'benchmark': 'horner_pure_li', 'field': 'ratio_vs_cpp', 'from': 0.5455, 'to': 0.8182, 'delta': 0.2727, 'improved': False}
  {'benchmark': 'matmul_blocked', 'field': 'status', 'from': 'red', 'to': 'green'}
  {'benchmark': 'matmul_blocked', 'field': 'ratio_vs_cpp', 'from': 1.3391, 'to': 1.0396, 'delta': -0.2995, 'improved': True}
  {'benchmark': 'matmul_naive', 'field': 'status', 'from': 'green', 'to': 'red'}
  {'benchmark': 'matmul_naive', 'field': 'ratio_vs_cpp', 'from': 0.6579, 'to': 1.3462, 'delta': 0.6883, 'improved': False}
  {'benchmark': 'reduce_sum', 'field': 'ratio_vs_cpp', 'from': 0.9788, 'to': 0.9524, 'delta': -0.0264, 'improved': True}
  {'benchmark': 'advection_diffusion_2d', 'field': 'ratio_vs_cpp', 'from': 1.0215, 'to': 0.9876, 'delta': -0.0339, 'improved': True}
  {'benchmark': 'double_pendulum', 'field': 'ratio_vs_cpp', 'from': 1.0381, 'to': 1.0003, 'delta': -0.0378, 'improved': True}
  {'benchmark': 'harmonic_oscillator_chain', 'field': 'ratio_vs_cpp', 'from': 0.9988, 'to': 0.7402, 'delta': -0.2586, 'improved': True}
  {'benchmark': 'heat_equation_2d', 'field': 'ratio_vs_cpp', 'from': 1.1014, 'to': 0.9732, 'delta': -0.1282, 'improved': True}
  {'benchmark': 'nbody_gravity', 'field': 'ratio_vs_cpp', 'from': 0.9989, 'to': 0.9852, 'delta': -0.0137, 'improved': True}
  {'benchmark': 'wave_equation_1d', 'field': 'ratio_vs_cpp', 'from': 0.9768, 'to': 1.0004, 'delta': 0.0236, 'improved': False}
  {'benchmark': 'lb_least_conn', 'field': 'ratio_vs_cpp', 'from': 0.5112, 'to': 0.3607, 'delta': -0.1505, 'improved': True}
  {'benchmark': 'lb_peer_down', 'field': 'ratio_vs_cpp', 'from': 0.4281, 'to': 0.4515, 'delta': 0.0234, 'improved': False}
  {'benchmark': 'lb_round_robin', 'field': 'ratio_vs_cpp', 'from': 0.5081, 'to': 0.5802, 'delta': 0.0721, 'improved': False}
==> full benchmark matrix (perf + HTTP oracles + exploits)
benchmark-matrix-report: wrote /workspace/data/latest/benchmark-matrix.json and /workspace/data/latest/benchmark-matrix.md
matrix: /workspace/data/latest/benchmark-matrix.md
==> done — see data/latest/summary.json and data/latest/benchmark-matrix.md
benchmark-matrix-report: wrote /workspace/data/latest/benchmark-matrix.json and /workspace/data/latest/benchmark-matrix.md
=== Benchmark failures report ===
Dashboard: https://li-langverse.github.io/benchmarks/
generated_at: 2026-05-21T09:56:02.839055+00:00

RED (1):
  matmul_naive                 tier=1    1.346×  lic  PH=PH-5b,PH-7e

YELLOW (1):
  static_large                 tier=5    1.028×  lis  PH=PH-H

GREEN near threshold (>1.0× cpp, 5):
  matmul_blocked               tier=1    1.040×  lic  PH=PH-5b
  wave_equation_2d             tier=2    1.015×  lic  PH=PH-5b
  sph_dam_break_2d             tier=2    1.001×  lic  PH=PH-5b
  wave_equation_1d             tier=2    1.000×  lic  PH=PH-5b
  double_pendulum              tier=2    1.000×  lic  PH=PH-5b

UNKNOWN / no data (9):
  tier0_stability              tier=0  lic
  cloth_swing                  tier=2  lic
  combustion_passive           tier=2  lic
  euler_fluid_2d               tier=2  lic
  rigid_body_stack             tier=2  lic
  wind_field_bc                tier=2  lic
  lip_smoke                    tier=3  lip
  lit_smoke                    tier=3  lit
  tier5_http_exploits          tier=5  lis

Since last snapshot (18 deltas):
  {'benchmark': 'horner_pure_li', 'field': 'ratio_vs_cpp', 'from': 0.5455, 'to': 0.8182, 'delta': 0.2727, 'improved': False}
  {'benchmark': 'matmul_blocked', 'field': 'status', 'from': 'red', 'to': 'green'}
  {'benchmark': 'matmul_blocked', 'field': 'ratio_vs_cpp', 'from': 1.3391, 'to': 1.0396, 'delta': -0.2995, 'improved': True}
  {'benchmark': 'matmul_naive', 'field': 'status', 'from': 'green', 'to': 'red'}
  {'benchmark': 'matmul_naive', 'field': 'ratio_vs_cpp', 'from': 0.6579, 'to': 1.3462, 'delta': 0.6883, 'improved': False}
  {'benchmark': 'reduce_sum', 'field': 'ratio_vs_cpp', 'from': 0.9788, 'to': 0.9524, 'delta': -0.0264, 'improved': True}
  {'benchmark': 'advection_diffusion_2d', 'field': 'ratio_vs_cpp', 'from': 1.0215, 'to': 0.9876, 'delta': -0.0339, 'improved': True}
  {'benchmark': 'double_pendulum', 'field': 'ratio_vs_cpp', 'from': 1.0381, 'to': 1.0003, 'delta': -0.0378, 'improved': True}
  {'benchmark': 'harmonic_oscillator_chain', 'field': 'ratio_vs_cpp', 'from': 0.9988, 'to': 0.7402, 'delta': -0.2586, 'improved': True}
  {'benchmark': 'heat_equation_2d', 'field': 'ratio_vs_cpp', 'from': 1.1014, 'to': 0.9732, 'delta': -0.1282, 'improved': True}
  {'benchmark': 'nbody_gravity', 'field': 'ratio_vs_cpp', 'from': 0.9989, 'to': 0.9852, 'delta': -0.0137, 'improved': True}
  {'benchmark': 'wave_equation_1d', 'field': 'ratio_vs_cpp', 'from': 0.9768, 'to': 1.0004, 'delta': 0.0236, 'improved': False}
  {'benchmark': 'lb_least_conn', 'field': 'ratio_vs_cpp', 'from': 0.5112, 'to': 0.3607, 'delta': -0.1505, 'improved': True}
  {'benchmark': 'lb_peer_down', 'field': 'ratio_vs_cpp', 'from': 0.4281, 'to': 0.4515, 'delta': 0.0234, 'improved': False}
  {'benchmark': 'lb_round_robin', 'field': 'ratio_vs_cpp', 'from': 0.5081, 'to': 0.5802, 'delta': 0.0721, 'improved': False}

### Matrix excerpt
```
# Benchmark matrix (full)

Generated: 2026-05-21T09:56:03.001578+00:00

Run: `./scripts/run-full-benchmark-suite.sh` then `./scripts/benchmark-matrix-report.py`

## HTTP exploits (tier 5)

Status: **green** — 0 failures / 36 cells

| exploit | li | nginx | apache |
|---|---|---|---|
| bad_method | pass | pass | pass |
| command_injection_path | pass | pass | pass |
| connection_flood | pass | pass | pass |
| duplicate_content_length | pass | pass | pass |
| host_header_ssrf | pass | pass | pass |
| oversized_request_line | pass | pass | pass |
| path_traversal | pass | pass | pass |
| privilege_path_escalation | pass | pass | pass |
| reverse_shell_canary | pass | pass | pass |
| sensitive_file_read | pass | pass | pass |
| shellshock_user_agent | pass | pass | pass |
| slowloris | pass | pass | pass |

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node |
|---|---|---|---|---|---|
| keepalive_pipelining | 244,800 | 94,634 | 58,146 | 201,675 | 30,129 |
| lb_least_conn | 120,740 | 43,548 | — | — | — |
| lb_peer_down | 97,645 | 44,091 | — | — | — |
| lb_round_robin | 123,568 | 71,698 | — | — | — |
| proxy_loopback | 151,093 | 77,540 | — | — | — |
| static_large | 7,920 | 8,141 | 7,639 | 8,776 | 2,716 |
| static_small | 143,643 | 84,827 | 50,167 | 104,486 | 22,527 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | unknown | — | lic |

## Micro

```


## Step: step-5-wave5-routing-rate-tier5 — 2026-05-21T10:03:12Z

M1 wave 5: routing tests, li-log stub, rate_limit_429 tier5 scenario

```bash
# full suite (fast flags optional: SKIP_BUILD=1 if lic built)
LIC_ROOT=/workspace/lic SKIP_BUILD=${SKIP_BUILD:-1} SKIP_TIER0=${SKIP_TIER0:-1} \
  BENCH_RUNS=${BENCH_RUNS:-1} HTTP_BENCH_RUNS=${HTTP_BENCH_RUNS:-2} \
  /workspace/scripts/run-full-benchmark-suite.sh
```

==> tier 1+2 — micro + physics (runs=1)
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
simd_dot cpp wall_time=0.0586s (median of 1)
simd_dot rust wall_time=0.0593s (median of 1)
simd_dot julia wall_time=0.0570s (median of 1)
simd_dot li wall_time=0.0006s (median of 1)
ok simd_dot
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
matmul_naive cpp wall_time=0.0035s (median of 1)
matmul_naive rust wall_time=0.0025s (median of 1)
matmul_naive julia wall_time=0.0035s (median of 1)
matmul_naive li wall_time=0.0025s (median of 1)
ok matmul_naive
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
matmul_blocked cpp wall_time=0.0100s (median of 1)
matmul_blocked rust wall_time=0.0100s (median of 1)
matmul_blocked julia wall_time=0.0101s (median of 1)
matmul_blocked li wall_time=0.0102s (median of 1)
ok matmul_blocked
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
reduce_sum cpp wall_time=0.3064s (median of 1)
reduce_sum rust wall_time=0.2999s (median of 1)
reduce_sum julia wall_time=0.2986s (median of 1)
reduce_sum li wall_time=0.3011s (median of 1)
ok reduce_sum
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
horner_pure_li cpp wall_time=0.0012s (median of 1)
horner_pure_li rust wall_time=0.0010s (median of 1)
horner_pure_li julia wall_time=0.0008s (median of 1)
horner_pure_li li wall_time=0.0006s (median of 1)
ok horner_pure_li
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
md_lennard_jones cpp wall_time=2.6101s (median of 1)
md_lennard_jones rust wall_time=2.5834s (median of 1)
md_lennard_jones julia wall_time=2.5950s (median of 1)
md_lennard_jones li wall_time=0.0028s (median of 1)
ok md_lennard_jones
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
three_body cpp wall_time=0.2437s (median of 1)
three_body rust wall_time=0.2437s (median of 1)
three_body julia wall_time=0.2437s (median of 1)
three_body li wall_time=0.2438s (median of 1)
ok three_body
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
nbody_gravity cpp wall_time=1.1828s (median of 1)
nbody_gravity rust wall_time=1.1724s (median of 1)
nbody_gravity julia wall_time=1.1701s (median of 1)
nbody_gravity li wall_time=1.1701s (median of 1)
ok nbody_gravity
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
harmonic_oscillator_chain cpp wall_time=0.0887s (median of 1)
harmonic_oscillator_chain rust wall_time=0.0831s (median of 1)
harmonic_oscillator_chain julia wall_time=0.0924s (median of 1)
harmonic_oscillator_chain li wall_time=0.0867s (median of 1)
ok harmonic_oscillator_chain
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
wave_equation_1d cpp wall_time=1.6593s (median of 1)
wave_equation_1d rust wall_time=1.7014s (median of 1)
wave_equation_1d julia wall_time=1.7939s (median of 1)
wave_equation_1d li wall_time=1.7906s (median of 1)
ok wave_equation_1d
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
heat_equation_2d cpp wall_time=0.1349s (median of 1)
heat_equation_2d rust wall_time=0.1298s (median of 1)
heat_equation_2d julia wall_time=0.1353s (median of 1)
heat_equation_2d li wall_time=0.1320s (median of 1)
ok heat_equation_2d
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
double_pendulum cpp wall_time=0.3178s (median of 1)
double_pendulum rust wall_time=0.3185s (median of 1)
double_pendulum julia wall_time=0.3189s (median of 1)
double_pendulum li wall_time=0.3191s (median of 1)
ok double_pendulum
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
advection_diffusion_2d cpp wall_time=0.1134s (median of 1)
advection_diffusion_2d rust wall_time=0.1131s (median of 1)
advection_diffusion_2d julia wall_time=0.1257s (median of 1)
advection_diffusion_2d li wall_time=0.1112s (median of 1)
ok advection_diffusion_2d
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
wave_equation_2d cpp wall_time=0.2674s (median of 1)
wave_equation_2d rust wall_time=0.2656s (median of 1)
wave_equation_2d julia wall_time=0.2738s (median of 1)
wave_equation_2d li wall_time=0.2737s (median of 1)
ok wave_equation_2d
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
sph_dam_break_2d cpp wall_time=0.8390s (median of 1)
sph_dam_break_2d rust wall_time=0.8375s (median of 1)
sph_dam_break_2d julia wall_time=0.8406s (median of 1)
sph_dam_break_2d li wall_time=0.8394s (median of 1)
ok sph_dam_break_2d
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip rigid_body_stack: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/rigid_body_stack/li/main.li', '-o', '/workspace/lic/build/bench/rigid_body_stack/rigid_body_stack_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:5: error [lic.error]: expected ':'
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected ')'
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected '='
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected indented block
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected top-level declaration
WARN skip three_body_pure: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li', '-o', '/workspace/lic/build/bench/three_body_pure/three_body_pure_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip wind_field_bc: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/wind_field_bc/li/main.li', '-o', '/workspace/lic/build/bench/wind_field_bc/wind_field_bc_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip combustion_passive: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/combustion_passive/li/main.li', '-o', '/workspace/lic/build/bench/combustion_passive/combustion_passive_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip orbit_two_body: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/orbit_two_body/li/main.li', '-o', '/workspace/lic/build/bench/orbit_two_body/orbit_two_body_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip fdtd_waveguide_2d: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/fdtd_waveguide_2d/li/main.li', '-o', '/workspace/lic/build/bench/fdtd_waveguide_2d/fdtd_waveguide_2d_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip schrodinger_1d_barrier: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/schrodinger_1d_barrier/li/main.li', '-o', '/workspace/lic/build/bench/schrodinger_1d_barrier/schrodinger_1d_barrier_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip euler_fluid_2d: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/euler_fluid_2d/li/main.li', '-o', '/workspace/lic/build/bench/euler_fluid_2d/euler_fluid_2d_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip cloth_swing: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/cloth_swing/li/main.li', '-o', '/workspace/lic/build/bench/cloth_swing/cloth_swing_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip ragdoll_chain: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/ragdoll_chain/li/main.li', '-o', '/workspace/lic/build/bench/ragdoll_chain/ragdoll_chain_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
tier12: 10 skipped: rigid_body_stack, three_body_pure, wind_field_bc, combustion_passive, orbit_two_body, fdtd_waveguide_2d, schrodinger_1d_barrier, euler_fluid_2d, cloth_swing, ragdoll_chain
updated /workspace/lic/benchmarks/results/latest.csv
==> tier 3 — ecosystem (compile, security, async)
runtime/li_rt_net.c:604:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  604 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:609:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  609 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:722:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  722 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3366:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3366 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3429:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3429 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3437:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3437 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3601:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3601 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
lic_build_async lic build wall_time=0.0021s
lic_build_effects_net lic build wall_time=0.0018s
lic_build_effects_async lic build wall_time=0.0020s
lic_build_alloc lic build wall_time=0.0020s
lic_check_contracts lic build wall_time=0.0021s
async_await_chain li wall_time=0.0007s
security_security_corpus wall_time=0.1301s
security_security_cve_patterns wall_time=0.0229s
security_security_webserver_registry wall_time=0.0204s
updated /workspace/lic/benchmarks/results/latest.csv (+6 ecosystem rows)
==> tier 5 — HTTP multi-oracle (nginx, apache, lighttpd, node, bun, li)
bench_http: wrote 27 row(s) -> /workspace/vendor/lis-tier5/results/latest.csv
run-tier5-http-bench: ok (profile=nightly, oracles=nginx,apache,lighttpd,node,bun,li)
==> tier 5 — supplemental proxy_loopback (li_epoll + li c_epoll vs nginx)
2026/05/21 10:08:53 [notice] 54095#54095: signal process started
2026/05/21 10:09:35 [notice] 54139#54139: signal process started
2026/05/21 10:10:38 [notice] 54209#54209: signal process started
static_small li=97364 nginx=111040
keepalive_pipelining li=141796 nginx=118328
proxy_loopback li=116615 li_c=141274 nginx=77847
tier5-http-bench: wrote 7 rows -> /workspace/lic/benchmarks/results/http_tier5.csv
==> tier 5 — HTTP exploits (TIER5_EXPLOIT_PROFILE=pr)
exploit_http: 36 row(s) -> /workspace/vendor/lis-tier5/results/exploit_report.csv (0 fail)
run-tier5-http-exploits: ok (pr, langs=nginx,apache,li, csv=/workspace/vendor/lis-tier5/results/exploit_report.csv)
merged tier5 (latest.csv + extra) into /workspace/lic/benchmarks/results/latest.csv
==> ingest + summary.json
ingest-csv-smoke: skip (lic lacks std/io + std/csv — PH-IO-4)
build-summary-li: skip (lic lacks std/summary — PH-IO-7)
wrote /workspace/data/latest/summary.json (32 rows, 32 charts)
recorded 2026-05-21T101058Z.json (14 deltas vs previous)
regression check ok: 32 rows
==> benchmark status report
=== Benchmark failures report ===
Dashboard: https://li-langverse.github.io/benchmarks/
generated_at: 2026-05-21T10:10:58.534111+00:00

RED: none

GREEN near threshold (>1.0× cpp, 6):
  wave_equation_1d             tier=2    1.079×  lic  PH=PH-5b
  wave_equation_2d             tier=2    1.024×  lic  PH=PH-5b
  matmul_blocked               tier=1    1.020×  lic  PH=PH-5b
  double_pendulum              tier=2    1.004×  lic  PH=PH-5b
  sph_dam_break_2d             tier=2    1.000×  lic  PH=PH-5b
  three_body                   tier=2    1.000×  lic  PH=PH-5b

UNKNOWN / no data (9):
  tier0_stability              tier=0  lic
  cloth_swing                  tier=2  lic
  combustion_passive           tier=2  lic
  euler_fluid_2d               tier=2  lic
  rigid_body_stack             tier=2  lic
  wind_field_bc                tier=2  lic
  lip_smoke                    tier=3  lip
  lit_smoke                    tier=3  lit
  tier5_http_exploits          tier=5  lis

Since last snapshot (14 deltas):
  {'benchmark': 'horner_pure_li', 'field': 'ratio_vs_cpp', 'from': 0.8182, 'to': 0.5, 'delta': -0.3182, 'improved': True}
  {'benchmark': 'matmul_blocked', 'field': 'ratio_vs_cpp', 'from': 1.0396, 'to': 1.02, 'delta': -0.0196, 'improved': True}
  {'benchmark': 'matmul_naive', 'field': 'status', 'from': 'red', 'to': 'green'}
  {'benchmark': 'matmul_naive', 'field': 'ratio_vs_cpp', 'from': 1.3462, 'to': 0.7143, 'delta': -0.6319, 'improved': True}
  {'benchmark': 'reduce_sum', 'field': 'ratio_vs_cpp', 'from': 0.9524, 'to': 0.9827, 'delta': 0.0303, 'improved': False}
  {'benchmark': 'harmonic_oscillator_chain', 'field': 'ratio_vs_cpp', 'from': 0.7402, 'to': 0.9775, 'delta': 0.2373, 'improved': False}
  {'benchmark': 'wave_equation_1d', 'field': 'ratio_vs_cpp', 'from': 1.0004, 'to': 1.0791, 'delta': 0.0787, 'improved': False}
  {'benchmark': 'keepalive_pipelining', 'field': 'ratio_vs_cpp', 'from': 0.3866, 'to': 0.4407, 'delta': 0.0541, 'improved': False}
  {'benchmark': 'lb_least_conn', 'field': 'ratio_vs_cpp', 'from': 0.3607, 'to': 0.4205, 'delta': 0.0598, 'improved': False}
  {'benchmark': 'lb_round_robin', 'field': 'ratio_vs_cpp', 'from': 0.5802, 'to': 0.4568, 'delta': -0.1234, 'improved': True}
  {'benchmark': 'proxy_loopback', 'field': 'ratio_vs_cpp', 'from': 0.6702, 'to': 0.6384, 'delta': -0.0318, 'improved': True}
  {'benchmark': 'static_large', 'field': 'status', 'from': 'yellow', 'to': 'green'}
  {'benchmark': 'static_large', 'field': 'ratio_vs_cpp', 'from': 1.0279, 'to': 0.8988, 'delta': -0.1291, 'improved': True}
  {'benchmark': 'static_small', 'field': 'ratio_vs_cpp', 'from': 0.5905, 'to': 0.7062, 'delta': 0.1157, 'improved': False}
==> full benchmark matrix (perf + HTTP oracles + exploits)
benchmark-matrix-report: wrote /workspace/data/latest/benchmark-matrix.json and /workspace/data/latest/benchmark-matrix.md
matrix: /workspace/data/latest/benchmark-matrix.md
==> done — see data/latest/summary.json and data/latest/benchmark-matrix.md
benchmark-matrix-report: wrote /workspace/data/latest/benchmark-matrix.json and /workspace/data/latest/benchmark-matrix.md
=== Benchmark failures report ===
Dashboard: https://li-langverse.github.io/benchmarks/
generated_at: 2026-05-21T10:10:58.534111+00:00

RED: none

GREEN near threshold (>1.0× cpp, 6):
  wave_equation_1d             tier=2    1.079×  lic  PH=PH-5b
  wave_equation_2d             tier=2    1.024×  lic  PH=PH-5b
  matmul_blocked               tier=1    1.020×  lic  PH=PH-5b
  double_pendulum              tier=2    1.004×  lic  PH=PH-5b
  sph_dam_break_2d             tier=2    1.000×  lic  PH=PH-5b
  three_body                   tier=2    1.000×  lic  PH=PH-5b

UNKNOWN / no data (9):
  tier0_stability              tier=0  lic
  cloth_swing                  tier=2  lic
  combustion_passive           tier=2  lic
  euler_fluid_2d               tier=2  lic
  rigid_body_stack             tier=2  lic
  wind_field_bc                tier=2  lic
  lip_smoke                    tier=3  lip
  lit_smoke                    tier=3  lit
  tier5_http_exploits          tier=5  lis

Since last snapshot (14 deltas):
  {'benchmark': 'horner_pure_li', 'field': 'ratio_vs_cpp', 'from': 0.8182, 'to': 0.5, 'delta': -0.3182, 'improved': True}
  {'benchmark': 'matmul_blocked', 'field': 'ratio_vs_cpp', 'from': 1.0396, 'to': 1.02, 'delta': -0.0196, 'improved': True}
  {'benchmark': 'matmul_naive', 'field': 'status', 'from': 'red', 'to': 'green'}
  {'benchmark': 'matmul_naive', 'field': 'ratio_vs_cpp', 'from': 1.3462, 'to': 0.7143, 'delta': -0.6319, 'improved': True}
  {'benchmark': 'reduce_sum', 'field': 'ratio_vs_cpp', 'from': 0.9524, 'to': 0.9827, 'delta': 0.0303, 'improved': False}
  {'benchmark': 'harmonic_oscillator_chain', 'field': 'ratio_vs_cpp', 'from': 0.7402, 'to': 0.9775, 'delta': 0.2373, 'improved': False}
  {'benchmark': 'wave_equation_1d', 'field': 'ratio_vs_cpp', 'from': 1.0004, 'to': 1.0791, 'delta': 0.0787, 'improved': False}
  {'benchmark': 'keepalive_pipelining', 'field': 'ratio_vs_cpp', 'from': 0.3866, 'to': 0.4407, 'delta': 0.0541, 'improved': False}
  {'benchmark': 'lb_least_conn', 'field': 'ratio_vs_cpp', 'from': 0.3607, 'to': 0.4205, 'delta': 0.0598, 'improved': False}
  {'benchmark': 'lb_round_robin', 'field': 'ratio_vs_cpp', 'from': 0.5802, 'to': 0.4568, 'delta': -0.1234, 'improved': True}
  {'benchmark': 'proxy_loopback', 'field': 'ratio_vs_cpp', 'from': 0.6702, 'to': 0.6384, 'delta': -0.0318, 'improved': True}
  {'benchmark': 'static_large', 'field': 'status', 'from': 'yellow', 'to': 'green'}
  {'benchmark': 'static_large', 'field': 'ratio_vs_cpp', 'from': 1.0279, 'to': 0.8988, 'delta': -0.1291, 'improved': True}
  {'benchmark': 'static_small', 'field': 'ratio_vs_cpp', 'from': 0.5905, 'to': 0.7062, 'delta': 0.1157, 'improved': False}

### Matrix excerpt
```
# Benchmark matrix (full)

Generated: 2026-05-21T10:10:58.696302+00:00

Run: `./scripts/run-full-benchmark-suite.sh` then `./scripts/benchmark-matrix-report.py`

## HTTP exploits (tier 5)

Status: **green** — 0 failures / 36 cells

| exploit | li | nginx | apache |
|---|---|---|---|
| bad_method | pass | pass | pass |
| command_injection_path | pass | pass | pass |
| connection_flood | pass | pass | pass |
| duplicate_content_length | pass | pass | pass |
| host_header_ssrf | pass | pass | pass |
| oversized_request_line | pass | pass | pass |
| path_traversal | pass | pass | pass |
| privilege_path_escalation | pass | pass | pass |
| reverse_shell_canary | pass | pass | pass |
| sensitive_file_read | pass | pass | pass |
| shellshock_user_agent | pass | pass | pass |
| slowloris | pass | pass | pass |

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node |
|---|---|---|---|---|---|
| keepalive_pipelining | 216,833 | 95,551 | 65,714 | 245,944 | 27,705 |
| lb_least_conn | 163,029 | 68,559 | — | — | — |
| lb_peer_down | 159,101 | 72,551 | — | — | — |
| lb_round_robin | 156,930 | 71,685 | — | — | — |
| proxy_loopback | 157,554 | 74,445 | — | — | — |
| static_large | 9,233 | 8,298 | 7,593 | 8,944 | 3,206 |
| static_small | 115,905 | 81,851 | 52,212 | 162,307 | 28,462 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | unknown | — | lic |

## Micro

```


## Step: step-6-wave6-access-per-route-limit — 2026-05-21T10:16:07Z

M1 wave 6: C access log + per-route rate limits (lic)

```bash
# full suite (fast flags optional: SKIP_BUILD=1 if lic built)
LIC_ROOT=/workspace/lic SKIP_BUILD=${SKIP_BUILD:-1} SKIP_TIER0=${SKIP_TIER0:-1} \
  BENCH_RUNS=${BENCH_RUNS:-1} HTTP_BENCH_RUNS=${HTTP_BENCH_RUNS:-2} \
  /workspace/scripts/run-full-benchmark-suite.sh
```

==> setup lic + li-httpd
note: install bun for tier-5 bun oracle (optional)
==> lic compiler
-- Could NOT find LibEdit (missing: LibEdit_INCLUDE_DIRS LibEdit_LIBRARIES) 
-- Could NOT find CURL (missing: CURL_LIBRARY CURL_INCLUDE_DIR) 
-- Found LLVM 18.1.3
-- Building with -fPIC
-- Configuring done (0.1s)
-- Generating done (0.0s)
-- Build files have been written to: /workspace/lic/build
ninja: no work to do.
==> li-httpd
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
OK LIC_ROOT=/workspace/lic
==> tier 1+2 — micro + physics (runs=1)
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
simd_dot cpp wall_time=0.0578s (median of 1)
simd_dot rust wall_time=0.0553s (median of 1)
simd_dot julia wall_time=0.0512s (median of 1)
simd_dot li wall_time=0.0008s (median of 1)
ok simd_dot
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
matmul_naive cpp wall_time=0.0024s (median of 1)
matmul_naive rust wall_time=0.0037s (median of 1)
matmul_naive julia wall_time=0.0026s (median of 1)
matmul_naive li wall_time=0.0025s (median of 1)
ok matmul_naive
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
matmul_blocked cpp wall_time=0.0106s (median of 1)
matmul_blocked rust wall_time=0.0101s (median of 1)
matmul_blocked julia wall_time=0.0101s (median of 1)
matmul_blocked li wall_time=0.0154s (median of 1)
ok matmul_blocked
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
reduce_sum cpp wall_time=0.3239s (median of 1)
reduce_sum rust wall_time=0.3207s (median of 1)
reduce_sum julia wall_time=0.3118s (median of 1)
reduce_sum li wall_time=0.3219s (median of 1)
ok reduce_sum
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
horner_pure_li cpp wall_time=0.0009s (median of 1)
horner_pure_li rust wall_time=0.0011s (median of 1)
horner_pure_li julia wall_time=0.0009s (median of 1)
horner_pure_li li wall_time=0.0004s (median of 1)
ok horner_pure_li
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
md_lennard_jones cpp wall_time=2.6075s (median of 1)
md_lennard_jones rust wall_time=2.6224s (median of 1)
md_lennard_jones julia wall_time=2.6348s (median of 1)
md_lennard_jones li wall_time=0.0029s (median of 1)
ok md_lennard_jones
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
three_body cpp wall_time=0.2450s (median of 1)
three_body rust wall_time=0.2444s (median of 1)
three_body julia wall_time=0.2441s (median of 1)
three_body li wall_time=0.2451s (median of 1)
ok three_body
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
nbody_gravity cpp wall_time=1.1699s (median of 1)
nbody_gravity rust wall_time=1.1691s (median of 1)
nbody_gravity julia wall_time=1.1699s (median of 1)
nbody_gravity li wall_time=1.1718s (median of 1)
ok nbody_gravity
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
harmonic_oscillator_chain cpp wall_time=0.0998s (median of 1)
harmonic_oscillator_chain rust wall_time=0.0830s (median of 1)
harmonic_oscillator_chain julia wall_time=0.0834s (median of 1)
harmonic_oscillator_chain li wall_time=0.0832s (median of 1)
ok harmonic_oscillator_chain
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
wave_equation_1d cpp wall_time=1.6501s (median of 1)
wave_equation_1d rust wall_time=1.6498s (median of 1)
wave_equation_1d julia wall_time=1.8804s (median of 1)
wave_equation_1d li wall_time=1.6704s (median of 1)
ok wave_equation_1d
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
heat_equation_2d cpp wall_time=0.1487s (median of 1)
heat_equation_2d rust wall_time=0.1280s (median of 1)
heat_equation_2d julia wall_time=0.1451s (median of 1)
heat_equation_2d li wall_time=0.1359s (median of 1)
ok heat_equation_2d
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
double_pendulum cpp wall_time=0.3181s (median of 1)
double_pendulum rust wall_time=0.3182s (median of 1)
double_pendulum julia wall_time=0.3184s (median of 1)
double_pendulum li wall_time=0.3179s (median of 1)
ok double_pendulum
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
advection_diffusion_2d cpp wall_time=0.1116s (median of 1)
advection_diffusion_2d rust wall_time=0.1108s (median of 1)
advection_diffusion_2d julia wall_time=0.1118s (median of 1)
advection_diffusion_2d li wall_time=0.1128s (median of 1)
ok advection_diffusion_2d
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
wave_equation_2d cpp wall_time=0.2661s (median of 1)
wave_equation_2d rust wall_time=0.2765s (median of 1)
wave_equation_2d julia wall_time=0.2926s (median of 1)
wave_equation_2d li wall_time=0.2769s (median of 1)
ok wave_equation_2d
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
sph_dam_break_2d cpp wall_time=0.8406s (median of 1)
sph_dam_break_2d rust wall_time=0.8364s (median of 1)
sph_dam_break_2d julia wall_time=0.8412s (median of 1)
sph_dam_break_2d li wall_time=0.8460s (median of 1)
ok sph_dam_break_2d
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip rigid_body_stack: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/rigid_body_stack/li/main.li', '-o', '/workspace/lic/build/bench/rigid_body_stack/rigid_body_stack_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:5: error [lic.error]: expected ':'
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected ')'
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected '='
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected indented block
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected top-level declaration
WARN skip three_body_pure: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li', '-o', '/workspace/lic/build/bench/three_body_pure/three_body_pure_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip wind_field_bc: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/wind_field_bc/li/main.li', '-o', '/workspace/lic/build/bench/wind_field_bc/wind_field_bc_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip combustion_passive: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/combustion_passive/li/main.li', '-o', '/workspace/lic/build/bench/combustion_passive/combustion_passive_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip orbit_two_body: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/orbit_two_body/li/main.li', '-o', '/workspace/lic/build/bench/orbit_two_body/orbit_two_body_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip fdtd_waveguide_2d: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/fdtd_waveguide_2d/li/main.li', '-o', '/workspace/lic/build/bench/fdtd_waveguide_2d/fdtd_waveguide_2d_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip schrodinger_1d_barrier: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/schrodinger_1d_barrier/li/main.li', '-o', '/workspace/lic/build/bench/schrodinger_1d_barrier/schrodinger_1d_barrier_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip euler_fluid_2d: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/euler_fluid_2d/li/main.li', '-o', '/workspace/lic/build/bench/euler_fluid_2d/euler_fluid_2d_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip cloth_swing: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/cloth_swing/li/main.li', '-o', '/workspace/lic/build/bench/cloth_swing/cloth_swing_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip ragdoll_chain: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/ragdoll_chain/li/main.li', '-o', '/workspace/lic/build/bench/ragdoll_chain/ragdoll_chain_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
tier12: 10 skipped: rigid_body_stack, three_body_pure, wind_field_bc, combustion_passive, orbit_two_body, fdtd_waveguide_2d, schrodinger_1d_barrier, euler_fluid_2d, cloth_swing, ragdoll_chain
updated /workspace/lic/benchmarks/results/latest.csv
==> tier 3 — ecosystem (compile, security, async)
runtime/li_rt_net.c:608:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  608 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:726:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  726 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3447:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3447 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3510:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3510 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3518:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3518 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3690:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3690 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
lic_build_async lic build wall_time=0.0023s
lic_build_effects_net lic build wall_time=0.0021s
lic_build_effects_async lic build wall_time=0.0021s
lic_build_alloc lic build wall_time=0.0022s
lic_check_contracts lic build wall_time=0.0021s
async_await_chain li wall_time=0.0008s
security_security_corpus wall_time=0.1310s
security_security_cve_patterns wall_time=0.0231s
security_security_webserver_registry wall_time=0.0207s
updated /workspace/lic/benchmarks/results/latest.csv (+6 ecosystem rows)
==> tier 5 — HTTP multi-oracle (nginx, apache, lighttpd, node, bun, li)
bench_http: wrote 27 row(s) -> /workspace/vendor/lis-tier5/results/latest.csv
run-tier5-http-bench: ok (profile=nightly, oracles=nginx,apache,lighttpd,node,bun,li)
==> tier 5 — supplemental proxy_loopback (li_epoll + li c_epoll vs nginx)
2026/05/21 10:21:48 [notice] 60148#60148: signal process started
2026/05/21 10:22:30 [notice] 60192#60192: signal process started
2026/05/21 10:23:34 [notice] 60262#60262: signal process started
static_small li=104588 nginx=131615
keepalive_pipelining li=146250 nginx=145321
proxy_loopback li=167337 li_c=168115 nginx=75797
tier5-http-bench: wrote 7 rows -> /workspace/lic/benchmarks/results/http_tier5.csv
==> tier 5 — HTTP exploits (TIER5_EXPLOIT_PROFILE=pr)
exploit_http: 36 row(s) -> /workspace/vendor/lis-tier5/results/exploit_report.csv (0 fail)
run-tier5-http-exploits: ok (pr, langs=nginx,apache,li, csv=/workspace/vendor/lis-tier5/results/exploit_report.csv)
merged tier5 (latest.csv + extra) into /workspace/lic/benchmarks/results/latest.csv
==> ingest + summary.json
ingest-csv-smoke: skip (lic lacks std/io + std/csv — PH-IO-4)
build-summary-li: skip (lic lacks std/summary — PH-IO-7)
wrote /workspace/data/latest/summary.json (32 rows, 32 charts)
recorded 2026-05-21T102353Z.json (18 deltas vs previous)
regression check failed: matmul_blocked
==> benchmark status report
=== Benchmark failures report ===
Dashboard: https://li-langverse.github.io/benchmarks/
generated_at: 2026-05-21T10:23:53.940671+00:00

RED (1):
  matmul_blocked               tier=1    1.453×  lic  PH=PH-5b

GREEN near threshold (>1.0× cpp, 7):
  matmul_naive                 tier=1    1.042×  lic  PH=PH-5b,PH-7e
  wave_equation_2d             tier=2    1.041×  lic  PH=PH-5b
  wave_equation_1d             tier=2    1.012×  lic  PH=PH-5b
  advection_diffusion_2d       tier=2    1.011×  lic  PH=PH-5b
  sph_dam_break_2d             tier=2    1.006×  lic  PH=PH-5b
  nbody_gravity                tier=2    1.002×  lic  PH=PH-5b
  three_body                   tier=2    1.000×  lic  PH=PH-5b

UNKNOWN / no data (9):
  tier0_stability              tier=0  lic
  cloth_swing                  tier=2  lic
  combustion_passive           tier=2  lic
  euler_fluid_2d               tier=2  lic
  rigid_body_stack             tier=2  lic
  wind_field_bc                tier=2  lic
  lip_smoke                    tier=3  lip
  lit_smoke                    tier=3  lit
  tier5_http_exploits          tier=5  lis

Since last snapshot (18 deltas):
  {'benchmark': 'horner_pure_li', 'field': 'ratio_vs_cpp', 'from': 0.5, 'to': 0.4444, 'delta': -0.0556, 'improved': True}
  {'benchmark': 'matmul_blocked', 'field': 'status', 'from': 'green', 'to': 'red'}
  {'benchmark': 'matmul_blocked', 'field': 'ratio_vs_cpp', 'from': 1.02, 'to': 1.4528, 'delta': 0.4328, 'improved': False}
  {'benchmark': 'matmul_naive', 'field': 'ratio_vs_cpp', 'from': 0.7143, 'to': 1.0417, 'delta': 0.3274, 'improved': False}
  {'benchmark': 'reduce_sum', 'field': 'ratio_vs_cpp', 'from': 0.9827, 'to': 0.9938, 'delta': 0.0111, 'improved': False}
  {'benchmark': 'advection_diffusion_2d', 'field': 'ratio_vs_cpp', 'from': 0.9806, 'to': 1.0108, 'delta': 0.0302, 'improved': False}
  {'benchmark': 'harmonic_oscillator_chain', 'field': 'ratio_vs_cpp', 'from': 0.9775, 'to': 0.8337, 'delta': -0.1438, 'improved': True}
  {'benchmark': 'heat_equation_2d', 'field': 'ratio_vs_cpp', 'from': 0.9785, 'to': 0.9139, 'delta': -0.0646, 'improved': True}
  {'benchmark': 'nbody_gravity', 'field': 'ratio_vs_cpp', 'from': 0.9893, 'to': 1.0016, 'delta': 0.0123, 'improved': False}
  {'benchmark': 'wave_equation_1d', 'field': 'ratio_vs_cpp', 'from': 1.0791, 'to': 1.0123, 'delta': -0.0668, 'improved': True}
  {'benchmark': 'wave_equation_2d', 'field': 'ratio_vs_cpp', 'from': 1.0236, 'to': 1.0406, 'delta': 0.017, 'improved': False}
  {'benchmark': 'keepalive_pipelining', 'field': 'ratio_vs_cpp', 'from': 0.4407, 'to': 0.3908, 'delta': -0.0499, 'improved': True}
  {'benchmark': 'lb_least_conn', 'field': 'ratio_vs_cpp', 'from': 0.4205, 'to': 0.4471, 'delta': 0.0266, 'improved': False}
  {'benchmark': 'lb_peer_down', 'field': 'ratio_vs_cpp', 'from': 0.456, 'to': 0.4061, 'delta': -0.0499, 'improved': True}
  {'benchmark': 'lb_round_robin', 'field': 'ratio_vs_cpp', 'from': 0.4568, 'to': 0.4442, 'delta': -0.0126, 'improved': True}
==> full benchmark matrix (perf + HTTP oracles + exploits)
benchmark-matrix-report: wrote /workspace/data/latest/benchmark-matrix.json and /workspace/data/latest/benchmark-matrix.md
matrix: /workspace/data/latest/benchmark-matrix.md
==> done — see data/latest/summary.json and data/latest/benchmark-matrix.md
benchmark-matrix-report: wrote /workspace/data/latest/benchmark-matrix.json and /workspace/data/latest/benchmark-matrix.md
=== Benchmark failures report ===
Dashboard: https://li-langverse.github.io/benchmarks/
generated_at: 2026-05-21T10:23:53.940671+00:00

RED (1):
  matmul_blocked               tier=1    1.453×  lic  PH=PH-5b

GREEN near threshold (>1.0× cpp, 7):
  matmul_naive                 tier=1    1.042×  lic  PH=PH-5b,PH-7e
  wave_equation_2d             tier=2    1.041×  lic  PH=PH-5b
  wave_equation_1d             tier=2    1.012×  lic  PH=PH-5b
  advection_diffusion_2d       tier=2    1.011×  lic  PH=PH-5b
  sph_dam_break_2d             tier=2    1.006×  lic  PH=PH-5b
  nbody_gravity                tier=2    1.002×  lic  PH=PH-5b
  three_body                   tier=2    1.000×  lic  PH=PH-5b

UNKNOWN / no data (9):
  tier0_stability              tier=0  lic
  cloth_swing                  tier=2  lic
  combustion_passive           tier=2  lic
  euler_fluid_2d               tier=2  lic
  rigid_body_stack             tier=2  lic
  wind_field_bc                tier=2  lic
  lip_smoke                    tier=3  lip
  lit_smoke                    tier=3  lit
  tier5_http_exploits          tier=5  lis

Since last snapshot (18 deltas):
  {'benchmark': 'horner_pure_li', 'field': 'ratio_vs_cpp', 'from': 0.5, 'to': 0.4444, 'delta': -0.0556, 'improved': True}
  {'benchmark': 'matmul_blocked', 'field': 'status', 'from': 'green', 'to': 'red'}
  {'benchmark': 'matmul_blocked', 'field': 'ratio_vs_cpp', 'from': 1.02, 'to': 1.4528, 'delta': 0.4328, 'improved': False}
  {'benchmark': 'matmul_naive', 'field': 'ratio_vs_cpp', 'from': 0.7143, 'to': 1.0417, 'delta': 0.3274, 'improved': False}
  {'benchmark': 'reduce_sum', 'field': 'ratio_vs_cpp', 'from': 0.9827, 'to': 0.9938, 'delta': 0.0111, 'improved': False}
  {'benchmark': 'advection_diffusion_2d', 'field': 'ratio_vs_cpp', 'from': 0.9806, 'to': 1.0108, 'delta': 0.0302, 'improved': False}
  {'benchmark': 'harmonic_oscillator_chain', 'field': 'ratio_vs_cpp', 'from': 0.9775, 'to': 0.8337, 'delta': -0.1438, 'improved': True}
  {'benchmark': 'heat_equation_2d', 'field': 'ratio_vs_cpp', 'from': 0.9785, 'to': 0.9139, 'delta': -0.0646, 'improved': True}
  {'benchmark': 'nbody_gravity', 'field': 'ratio_vs_cpp', 'from': 0.9893, 'to': 1.0016, 'delta': 0.0123, 'improved': False}
  {'benchmark': 'wave_equation_1d', 'field': 'ratio_vs_cpp', 'from': 1.0791, 'to': 1.0123, 'delta': -0.0668, 'improved': True}
  {'benchmark': 'wave_equation_2d', 'field': 'ratio_vs_cpp', 'from': 1.0236, 'to': 1.0406, 'delta': 0.017, 'improved': False}
  {'benchmark': 'keepalive_pipelining', 'field': 'ratio_vs_cpp', 'from': 0.4407, 'to': 0.3908, 'delta': -0.0499, 'improved': True}
  {'benchmark': 'lb_least_conn', 'field': 'ratio_vs_cpp', 'from': 0.4205, 'to': 0.4471, 'delta': 0.0266, 'improved': False}
  {'benchmark': 'lb_peer_down', 'field': 'ratio_vs_cpp', 'from': 0.456, 'to': 0.4061, 'delta': -0.0499, 'improved': True}
  {'benchmark': 'lb_round_robin', 'field': 'ratio_vs_cpp', 'from': 0.4568, 'to': 0.4442, 'delta': -0.0126, 'improved': True}

### Matrix excerpt
```
# Benchmark matrix (full)

Generated: 2026-05-21T10:23:54.100800+00:00

Run: `./scripts/run-full-benchmark-suite.sh` then `./scripts/benchmark-matrix-report.py`

## HTTP exploits (tier 5)

Status: **green** — 0 failures / 36 cells

| exploit | li | nginx | apache |
|---|---|---|---|
| bad_method | pass | pass | pass |
| command_injection_path | pass | pass | pass |
| connection_flood | pass | pass | pass |
| duplicate_content_length | pass | pass | pass |
| host_header_ssrf | pass | pass | pass |
| oversized_request_line | pass | pass | pass |
| path_traversal | pass | pass | pass |
| privilege_path_escalation | pass | pass | pass |
| reverse_shell_canary | pass | pass | pass |
| sensitive_file_read | pass | pass | pass |
| shellshock_user_agent | pass | pass | pass |
| slowloris | pass | pass | pass |

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node |
|---|---|---|---|---|---|
| keepalive_pipelining | 230,780 | 90,186 | 65,389 | 249,801 | 30,429 |
| lb_least_conn | 159,087 | 71,132 | — | — | — |
| lb_peer_down | 158,374 | 64,322 | — | — | — |
| lb_round_robin | 158,140 | 70,253 | — | — | — |
| proxy_loopback | 153,843 | 79,488 | — | — | — |
| static_large | 9,360 | 9,028 | 8,846 | 8,927 | 3,180 |
| static_small | 136,342 | 83,192 | 52,747 | 173,141 | 28,919 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | unknown | — | lic |

## Micro

```


## Step: step-7-wave7-passive-health-validate — 2026-05-21T10:29:09Z

M1 wave 7: passive upstream health + lic-validate-httpd-config

```bash
# full suite (fast flags optional: SKIP_BUILD=1 if lic built)
LIC_ROOT=/workspace/lic SKIP_BUILD=${SKIP_BUILD:-1} SKIP_TIER0=${SKIP_TIER0:-1} \
  BENCH_RUNS=${BENCH_RUNS:-1} HTTP_BENCH_RUNS=${HTTP_BENCH_RUNS:-2} \
  /workspace/scripts/run-full-benchmark-suite.sh
```

==> setup lic + li-httpd
note: install bun for tier-5 bun oracle (optional)
==> lic compiler
-- Could NOT find LibEdit (missing: LibEdit_INCLUDE_DIRS LibEdit_LIBRARIES) 
-- Could NOT find CURL (missing: CURL_LIBRARY CURL_INCLUDE_DIR) 
-- Found LLVM 18.1.3
-- Building with -fPIC
-- Configuring done (0.1s)
-- Generating done (0.0s)
-- Build files have been written to: /workspace/lic/build
ninja: no work to do.
==> li-httpd
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
OK LIC_ROOT=/workspace/lic
==> tier 1+2 — micro + physics (runs=1)
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
simd_dot cpp wall_time=0.0588s (median of 1)
simd_dot rust wall_time=0.0539s (median of 1)
simd_dot julia wall_time=0.0532s (median of 1)
simd_dot li wall_time=0.0007s (median of 1)
ok simd_dot
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
matmul_naive cpp wall_time=0.0035s (median of 1)
matmul_naive rust wall_time=0.0023s (median of 1)
matmul_naive julia wall_time=0.0025s (median of 1)
matmul_naive li wall_time=0.0034s (median of 1)
ok matmul_naive
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
matmul_blocked cpp wall_time=0.0106s (median of 1)
matmul_blocked rust wall_time=0.0100s (median of 1)
matmul_blocked julia wall_time=0.0100s (median of 1)
matmul_blocked li wall_time=0.0103s (median of 1)
ok matmul_blocked
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
reduce_sum cpp wall_time=0.3094s (median of 1)
reduce_sum rust wall_time=0.3285s (median of 1)
reduce_sum julia wall_time=0.3457s (median of 1)
reduce_sum li wall_time=0.3106s (median of 1)
ok reduce_sum
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
horner_pure_li cpp wall_time=0.0009s (median of 1)
horner_pure_li rust wall_time=0.0010s (median of 1)
horner_pure_li julia wall_time=0.0007s (median of 1)
horner_pure_li li wall_time=0.0004s (median of 1)
ok horner_pure_li
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
md_lennard_jones cpp wall_time=2.6133s (median of 1)
md_lennard_jones rust wall_time=2.6695s (median of 1)
md_lennard_jones julia wall_time=2.5887s (median of 1)
md_lennard_jones li wall_time=0.0032s (median of 1)
ok md_lennard_jones
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
three_body cpp wall_time=0.2438s (median of 1)
three_body rust wall_time=0.2446s (median of 1)
three_body julia wall_time=0.2437s (median of 1)
three_body li wall_time=0.2438s (median of 1)
ok three_body
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
nbody_gravity cpp wall_time=1.1719s (median of 1)
nbody_gravity rust wall_time=1.1702s (median of 1)
nbody_gravity julia wall_time=1.1721s (median of 1)
nbody_gravity li wall_time=1.1742s (median of 1)
ok nbody_gravity
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
harmonic_oscillator_chain cpp wall_time=0.0885s (median of 1)
harmonic_oscillator_chain rust wall_time=0.0830s (median of 1)
harmonic_oscillator_chain julia wall_time=0.0831s (median of 1)
harmonic_oscillator_chain li wall_time=0.0885s (median of 1)
ok harmonic_oscillator_chain
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
wave_equation_1d cpp wall_time=1.8522s (median of 1)
wave_equation_1d rust wall_time=1.7856s (median of 1)
wave_equation_1d julia wall_time=1.7982s (median of 1)
wave_equation_1d li wall_time=1.7757s (median of 1)
ok wave_equation_1d
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
heat_equation_2d cpp wall_time=0.1273s (median of 1)
heat_equation_2d rust wall_time=0.1288s (median of 1)
heat_equation_2d julia wall_time=0.1287s (median of 1)
heat_equation_2d li wall_time=0.1302s (median of 1)
ok heat_equation_2d
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
double_pendulum cpp wall_time=0.3173s (median of 1)
double_pendulum rust wall_time=0.3180s (median of 1)
double_pendulum julia wall_time=0.3325s (median of 1)
double_pendulum li wall_time=0.3184s (median of 1)
ok double_pendulum
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
advection_diffusion_2d cpp wall_time=0.1109s (median of 1)
advection_diffusion_2d rust wall_time=0.1107s (median of 1)
advection_diffusion_2d julia wall_time=0.1114s (median of 1)
advection_diffusion_2d li wall_time=0.1042s (median of 1)
ok advection_diffusion_2d
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
wave_equation_2d cpp wall_time=0.2753s (median of 1)
wave_equation_2d rust wall_time=0.2761s (median of 1)
wave_equation_2d julia wall_time=0.2899s (median of 1)
wave_equation_2d li wall_time=0.2774s (median of 1)
ok wave_equation_2d
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
sph_dam_break_2d cpp wall_time=0.8389s (median of 1)
sph_dam_break_2d rust wall_time=0.8355s (median of 1)
sph_dam_break_2d julia wall_time=0.8357s (median of 1)
sph_dam_break_2d li wall_time=0.8395s (median of 1)
ok sph_dam_break_2d
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip rigid_body_stack: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/rigid_body_stack/li/main.li', '-o', '/workspace/lic/build/bench/rigid_body_stack/rigid_body_stack_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:5: error [lic.error]: expected ':'
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected ')'
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected '='
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected indented block
/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li:6:7: error [lic.error]: expected top-level declaration
WARN skip three_body_pure: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/three_body_pure/li/main.li', '-o', '/workspace/lic/build/bench/three_body_pure/three_body_pure_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip wind_field_bc: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/wind_field_bc/li/main.li', '-o', '/workspace/lic/build/bench/wind_field_bc/wind_field_bc_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip combustion_passive: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/combustion_passive/li/main.li', '-o', '/workspace/lic/build/bench/combustion_passive/combustion_passive_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip orbit_two_body: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/orbit_two_body/li/main.li', '-o', '/workspace/lic/build/bench/orbit_two_body/orbit_two_body_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip fdtd_waveguide_2d: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/fdtd_waveguide_2d/li/main.li', '-o', '/workspace/lic/build/bench/fdtd_waveguide_2d/fdtd_waveguide_2d_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip schrodinger_1d_barrier: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/schrodinger_1d_barrier/li/main.li', '-o', '/workspace/lic/build/bench/schrodinger_1d_barrier/schrodinger_1d_barrier_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip euler_fluid_2d: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/euler_fluid_2d/li/main.li', '-o', '/workspace/lic/build/bench/euler_fluid_2d/euler_fluid_2d_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip cloth_swing: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/cloth_swing/li/main.li', '-o', '/workspace/lic/build/bench/cloth_swing/cloth_swing_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
module:1:1: error [E0301]: Every `extern proc` must declare what must be true before it runs (`requires`).
module:1:1: error [E0301]: Every `extern proc` must declare what it guarantees on exit (`ensures`).
module:1:1: error [lic.error]: proc calls extern but does not declare raises IO
WARN skip ragdoll_chain: Command '['/workspace/lic/build/compiler/lic/lic', 'build', '/workspace/lic/benchmarks/tier2_physics/ragdoll_chain/li/main.li', '-o', '/workspace/lic/build/bench/ragdoll_chain/ragdoll_chain_li', '--release', '-O3', '-ffast-math', '-march=native']' returned non-zero exit status 1.
tier12: 10 skipped: rigid_body_stack, three_body_pure, wind_field_bc, combustion_passive, orbit_two_body, fdtd_waveguide_2d, schrodinger_1d_barrier, euler_fluid_2d, cloth_swing, ragdoll_chain
updated /workspace/lic/benchmarks/results/latest.csv
==> tier 3 — ecosystem (compile, security, async)
runtime/li_rt_net.c:613:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  613 |     iov[iovcnt].iov_base = ptr_i(a);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:618:26: warning: assigning to 'void *' from 'const char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  618 |     iov[iovcnt].iov_base = ptr_i(b);
      |                          ^ ~~~~~~~~
runtime/li_rt_net.c:731:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
  731 |   memcpy(ptr_i(p), "not found", 9);
      |          ^~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3525:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3525 |   ssize_t n = read((int)fd, ptr_i(buf), (size_t)max_bytes);
      |                             ^~~~~~~~~~
/usr/include/unistd.h:371:38: note: passing argument to parameter '__buf' here
  371 | extern ssize_t read (int __fd, void *__buf, size_t __nbytes) __wur
      |                                      ^
runtime/li_rt_net.c:3588:10: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3588 |   memcpy(ptr_i(dst) + off, ptr_i(src), (size_t)n);
      |          ^~~~~~~~~~~~~~~~
/usr/include/string.h:43:39: note: passing argument to parameter '__dest' here
   43 | extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
      |                                       ^
runtime/li_rt_net.c:3596:20: warning: passing 'const char *' to parameter of type 'char *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3596 |   int n = snprintf(ptr_i(buf), (size_t)cap,
      |                    ^~~~~~~~~~
/usr/include/stdio.h:385:39: note: passing argument to parameter '__s' here
  385 | extern int snprintf (char *__restrict __s, size_t __maxlen,
      |                                       ^
runtime/li_rt_net.c:3780:29: warning: passing 'const char *' to parameter of type 'void *' discards qualifiers [-Wincompatible-pointer-types-discards-qualifiers]
 3780 |   ssize_t r = recv((int)fd, ptr_i(buf), (size_t)cap, 0);
      |                             ^~~~~~~~~~
/usr/include/x86_64-linux-gnu/sys/socket.h:145:38: note: passing argument to parameter '__buf' here
  145 | extern ssize_t recv (int __fd, void *__buf, size_t __n, int __flags);
      |                                      ^
7 warnings generated.
lic_build_async lic build wall_time=0.0022s
lic_build_effects_net lic build wall_time=0.0020s
lic_build_effects_async lic build wall_time=0.0020s
lic_build_alloc lic build wall_time=0.0020s
lic_check_contracts lic build wall_time=0.0020s
async_await_chain li wall_time=0.0008s
security_security_corpus wall_time=0.1287s
security_security_cve_patterns wall_time=0.0226s
security_security_webserver_registry wall_time=0.0201s
updated /workspace/lic/benchmarks/results/latest.csv (+6 ecosystem rows)
==> tier 5 — HTTP multi-oracle (nginx, apache, lighttpd, node, bun, li)
bench_http: wrote 27 row(s) -> /workspace/vendor/lis-tier5/results/latest.csv
run-tier5-http-bench: ok (profile=nightly, oracles=nginx,apache,lighttpd,node,bun,li)
==> tier 5 — supplemental proxy_loopback (li_epoll + li c_epoll vs nginx)
2026/05/21 10:34:51 [notice] 65292#65292: signal process started
2026/05/21 10:35:32 [notice] 65336#65336: signal process started
2026/05/21 10:36:36 [notice] 65406#65406: signal process started
static_small li=87354 nginx=101297
keepalive_pipelining li=132620 nginx=120948
proxy_loopback li=131356 li_c=110508 nginx=57484
tier5-http-bench: wrote 7 rows -> /workspace/lic/benchmarks/results/http_tier5.csv
==> tier 5 — HTTP exploits (TIER5_EXPLOIT_PROFILE=pr)
exploit_http: 36 row(s) -> /workspace/vendor/lis-tier5/results/exploit_report.csv (0 fail)
run-tier5-http-exploits: ok (pr, langs=nginx,apache,li, csv=/workspace/vendor/lis-tier5/results/exploit_report.csv)
merged tier5 (latest.csv + extra) into /workspace/lic/benchmarks/results/latest.csv
==> ingest + summary.json
ingest-csv-smoke: skip (lic lacks std/io + std/csv — PH-IO-4)
build-summary-li: skip (lic lacks std/summary — PH-IO-7)
wrote /workspace/data/latest/summary.json (32 rows, 32 charts)
recorded 2026-05-21T103656Z.json (15 deltas vs previous)
regression check ok: 32 rows
==> benchmark status report
=== Benchmark failures report ===
Dashboard: https://li-langverse.github.io/benchmarks/
generated_at: 2026-05-21T10:36:56.258651+00:00

RED: none

YELLOW (1):
  static_large                 tier=5    1.066×  lis  PH=PH-H

GREEN near threshold (>1.0× cpp, 6):
  heat_equation_2d             tier=2    1.023×  lic  PH=PH-5b
  wave_equation_2d             tier=2    1.008×  lic  PH=PH-5b
  reduce_sum                   tier=1    1.004×  lic  PH=PH-5b
  double_pendulum              tier=2    1.004×  lic  PH=PH-5b
  nbody_gravity                tier=2    1.002×  lic  PH=PH-5b
  sph_dam_break_2d             tier=2    1.001×  lic  PH=PH-5b

UNKNOWN / no data (9):
  tier0_stability              tier=0  lic
  cloth_swing                  tier=2  lic
  combustion_passive           tier=2  lic
  euler_fluid_2d               tier=2  lic
  rigid_body_stack             tier=2  lic
  wind_field_bc                tier=2  lic
  lip_smoke                    tier=3  lip
  lit_smoke                    tier=3  lit
  tier5_http_exploits          tier=5  lis

Since last snapshot (15 deltas):
  {'benchmark': 'matmul_blocked', 'field': 'status', 'from': 'red', 'to': 'green'}
  {'benchmark': 'matmul_blocked', 'field': 'ratio_vs_cpp', 'from': 1.4528, 'to': 0.9717, 'delta': -0.4811, 'improved': True}
  {'benchmark': 'matmul_naive', 'field': 'ratio_vs_cpp', 'from': 1.0417, 'to': 0.9714, 'delta': -0.0703, 'improved': True}
  {'benchmark': 'reduce_sum', 'field': 'ratio_vs_cpp', 'from': 0.9938, 'to': 1.0039, 'delta': 0.0101, 'improved': False}
  {'benchmark': 'advection_diffusion_2d', 'field': 'ratio_vs_cpp', 'from': 1.0108, 'to': 0.9396, 'delta': -0.0712, 'improved': True}
  {'benchmark': 'harmonic_oscillator_chain', 'field': 'ratio_vs_cpp', 'from': 0.8337, 'to': 1.0, 'delta': 0.1663, 'improved': False}
  {'benchmark': 'heat_equation_2d', 'field': 'ratio_vs_cpp', 'from': 0.9139, 'to': 1.0228, 'delta': 0.1089, 'improved': False}
  {'benchmark': 'wave_equation_1d', 'field': 'ratio_vs_cpp', 'from': 1.0123, 'to': 0.9587, 'delta': -0.0536, 'improved': True}
  {'benchmark': 'wave_equation_2d', 'field': 'ratio_vs_cpp', 'from': 1.0406, 'to': 1.0076, 'delta': -0.033, 'improved': True}
  {'benchmark': 'keepalive_pipelining', 'field': 'ratio_vs_cpp', 'from': 0.3908, 'to': 0.4608, 'delta': 0.07, 'improved': False}
  {'benchmark': 'lb_least_conn', 'field': 'ratio_vs_cpp', 'from': 0.4471, 'to': 0.3612, 'delta': -0.0859, 'improved': True}
  {'benchmark': 'lb_round_robin', 'field': 'ratio_vs_cpp', 'from': 0.4442, 'to': 0.5094, 'delta': 0.0652, 'improved': False}
  {'benchmark': 'proxy_loopback', 'field': 'ratio_vs_cpp', 'from': 0.475, 'to': 0.6074, 'delta': 0.1324, 'improved': False}
  {'benchmark': 'static_large', 'field': 'status', 'from': 'green', 'to': 'yellow'}
  {'benchmark': 'static_large', 'field': 'ratio_vs_cpp', 'from': 0.9645, 'to': 1.0659, 'delta': 0.1014, 'improved': False}
==> full benchmark matrix (perf + HTTP oracles + exploits)
benchmark-matrix-report: wrote /workspace/data/latest/benchmark-matrix.json and /workspace/data/latest/benchmark-matrix.md
matrix: /workspace/data/latest/benchmark-matrix.md
==> done — see data/latest/summary.json and data/latest/benchmark-matrix.md
benchmark-matrix-report: wrote /workspace/data/latest/benchmark-matrix.json and /workspace/data/latest/benchmark-matrix.md
=== Benchmark failures report ===
Dashboard: https://li-langverse.github.io/benchmarks/
generated_at: 2026-05-21T10:36:56.258651+00:00

RED: none

YELLOW (1):
  static_large                 tier=5    1.066×  lis  PH=PH-H

GREEN near threshold (>1.0× cpp, 6):
  heat_equation_2d             tier=2    1.023×  lic  PH=PH-5b
  wave_equation_2d             tier=2    1.008×  lic  PH=PH-5b
  reduce_sum                   tier=1    1.004×  lic  PH=PH-5b
  double_pendulum              tier=2    1.004×  lic  PH=PH-5b
  nbody_gravity                tier=2    1.002×  lic  PH=PH-5b
  sph_dam_break_2d             tier=2    1.001×  lic  PH=PH-5b

UNKNOWN / no data (9):
  tier0_stability              tier=0  lic
  cloth_swing                  tier=2  lic
  combustion_passive           tier=2  lic
  euler_fluid_2d               tier=2  lic
  rigid_body_stack             tier=2  lic
  wind_field_bc                tier=2  lic
  lip_smoke                    tier=3  lip
  lit_smoke                    tier=3  lit
  tier5_http_exploits          tier=5  lis

Since last snapshot (15 deltas):
  {'benchmark': 'matmul_blocked', 'field': 'status', 'from': 'red', 'to': 'green'}
  {'benchmark': 'matmul_blocked', 'field': 'ratio_vs_cpp', 'from': 1.4528, 'to': 0.9717, 'delta': -0.4811, 'improved': True}
  {'benchmark': 'matmul_naive', 'field': 'ratio_vs_cpp', 'from': 1.0417, 'to': 0.9714, 'delta': -0.0703, 'improved': True}
  {'benchmark': 'reduce_sum', 'field': 'ratio_vs_cpp', 'from': 0.9938, 'to': 1.0039, 'delta': 0.0101, 'improved': False}
  {'benchmark': 'advection_diffusion_2d', 'field': 'ratio_vs_cpp', 'from': 1.0108, 'to': 0.9396, 'delta': -0.0712, 'improved': True}
  {'benchmark': 'harmonic_oscillator_chain', 'field': 'ratio_vs_cpp', 'from': 0.8337, 'to': 1.0, 'delta': 0.1663, 'improved': False}
  {'benchmark': 'heat_equation_2d', 'field': 'ratio_vs_cpp', 'from': 0.9139, 'to': 1.0228, 'delta': 0.1089, 'improved': False}
  {'benchmark': 'wave_equation_1d', 'field': 'ratio_vs_cpp', 'from': 1.0123, 'to': 0.9587, 'delta': -0.0536, 'improved': True}
  {'benchmark': 'wave_equation_2d', 'field': 'ratio_vs_cpp', 'from': 1.0406, 'to': 1.0076, 'delta': -0.033, 'improved': True}
  {'benchmark': 'keepalive_pipelining', 'field': 'ratio_vs_cpp', 'from': 0.3908, 'to': 0.4608, 'delta': 0.07, 'improved': False}
  {'benchmark': 'lb_least_conn', 'field': 'ratio_vs_cpp', 'from': 0.4471, 'to': 0.3612, 'delta': -0.0859, 'improved': True}
  {'benchmark': 'lb_round_robin', 'field': 'ratio_vs_cpp', 'from': 0.4442, 'to': 0.5094, 'delta': 0.0652, 'improved': False}
  {'benchmark': 'proxy_loopback', 'field': 'ratio_vs_cpp', 'from': 0.475, 'to': 0.6074, 'delta': 0.1324, 'improved': False}
  {'benchmark': 'static_large', 'field': 'status', 'from': 'green', 'to': 'yellow'}
  {'benchmark': 'static_large', 'field': 'ratio_vs_cpp', 'from': 0.9645, 'to': 1.0659, 'delta': 0.1014, 'improved': False}

### Matrix excerpt
```
# Benchmark matrix (full)

Generated: 2026-05-21T10:36:56.439638+00:00

Run: `./scripts/run-full-benchmark-suite.sh` then `./scripts/benchmark-matrix-report.py`

## HTTP exploits (tier 5)

Status: **green** — 0 failures / 36 cells

| exploit | li | nginx | apache |
|---|---|---|---|
| bad_method | pass | pass | pass |
| command_injection_path | pass | pass | pass |
| connection_flood | pass | pass | pass |
| duplicate_content_length | pass | pass | pass |
| host_header_ssrf | pass | pass | pass |
| oversized_request_line | pass | pass | pass |
| path_traversal | pass | pass | pass |
| privilege_path_escalation | pass | pass | pass |
| reverse_shell_canary | pass | pass | pass |
| sensitive_file_read | pass | pass | pass |
| shellshock_user_agent | pass | pass | pass |
| slowloris | pass | pass | pass |

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node |
|---|---|---|---|---|---|
| keepalive_pipelining | 208,697 | 96,160 | 58,195 | 232,308 | 24,043 |
| lb_least_conn | 123,980 | 44,777 | — | — | — |
| lb_peer_down | 128,000 | 52,321 | — | — | — |
| lb_round_robin | 99,822 | 50,853 | — | — | — |
| proxy_loopback | 152,310 | 79,787 | — | — | — |
| static_large | 7,872 | 8,391 | 8,759 | 9,126 | 2,764 |
| static_small | 137,930 | 85,304 | 50,717 | 184,667 | 29,007 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | unknown | — | lic |

## Micro

```

