"""Runs a command and measures its RAM and CPU with resources.py (Token Passing in the step time
test, author 2026-11-24). The whole run is the window. Usage:
    measure_cmd.py OUT.json -- COMMAND ...
Writes the res_* fields, the machine, the wall seconds and the exit code to OUT.json."""
import json
import subprocess
import sys
import time

import resources

out, cmd = sys.argv[1], sys.argv[sys.argv.index("--") + 1:]
start = time.monotonic()
proc = subprocess.Popen(cmd)
sampler = resources.Sampler(pid=proc.pid).start()
code = proc.wait()
sampler.samples.append(dict(sampler.samples[-1], t=time.monotonic()))  # the end, for the wall time
sampler._stop.set()
row = resources.summary(sampler.samples)
row.pop("res_process_maxrss_gb")
import resource
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
wall = time.monotonic() - start
# the samples miss the CPU of the last second, so the totals come from the finished children
row.update(res_children_maxrss_gb=ru.ru_maxrss / 2**20, res_cpu_seconds_total=ru.ru_utime + ru.ru_stime,
           res_cpu_cores_used=(ru.ru_utime + ru.ru_stime) / wall)
row.update(resources.hardware(), wall_seconds=wall, exit_code=code, command=cmd)
json.dump(row, open(out, "w"), indent=1)
sys.exit(code)
