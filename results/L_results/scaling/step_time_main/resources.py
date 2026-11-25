"""Resource measures for the step time test (author 2026-11-24): GPU, RAM and CPU beside the time
per step. A thread samples once a second: the process's RAM (resident, with its children), its CPU
seconds, the PC's load, and from nvidia-smi the GPU's busy share, its memory in use, this
process's own GPU memory and the other programs on the GPU. `summary` reduces the samples of
the timed window to the fields of a row.

Used in-process by timing_probe.py (the step counter reads the episode log) and around a command
by measure_cmd.py (no step counter, the whole run is the window)."""
import os
import platform
import resource
import subprocess
import threading
import time

import psutil


def _smi(query, apps=False):
    kind = "--query-compute-apps" if apps else "--query-gpu"
    try:
        out = subprocess.run(["nvidia-smi", f"{kind}={query}", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=5).stdout
    except Exception:  # noqa: BLE001
        return []
    return [[c.strip() for c in line.split(",")] for line in out.splitlines() if line.strip()]


def hardware():
    cpu = next((l.split(":", 1)[1].strip() for l in open("/proc/cpuinfo") if l.startswith("model name")), platform.processor())
    gpu = _smi("name")
    return dict(machine_cpu=cpu, machine_cores=os.cpu_count(),
                machine_ram_gb=round(psutil.virtual_memory().total / 2**30, 1),
                machine_gpu=gpu[0][0] if gpu else None)


class Sampler:
    def __init__(self, step=lambda: None, pid=None, every=0.5, mark=None):
        """mark: a step count; one extra sample is taken as soon as the episode reaches it (the
        start of the timed window), so CPU per step has an exact start even in a short window."""
        self.proc = psutil.Process(pid or os.getpid())
        self.step, self.every, self.mark, self.samples = step, every, mark, []
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _tree(self):
        procs = [self.proc]
        try:
            procs += self.proc.children(recursive=True)
        except psutil.Error:
            pass
        return procs

    def sample(self):
        rss = cpu = 0.0
        pids = set()
        for p in self._tree():
            try:
                rss += p.memory_info().rss
                t = p.cpu_times()
                cpu += t.user + t.system
                pids.add(str(p.pid))
            except psutil.Error:
                pass
        gpu = _smi("utilization.gpu,memory.used")
        own_gpu, others = 0.0, set()
        for pid, name, used in _smi("pid,process_name,used_memory", apps=True):
            if pid in pids:
                own_gpu += float(used)
            else:
                others.add(os.path.basename(name.replace("\\", "/"))[:40])
        self.samples.append(dict(
            t=time.monotonic(), step=self.step(), rss=rss, cpu=cpu, load=os.getloadavg()[0],
            gpu_util=float(gpu[0][0]) if gpu else None, gpu_used=float(gpu[0][1]) if gpu else None,
            gpu_own=own_gpu if gpu else None, others=sorted(others)))

    def _run(self):
        last = time.monotonic()
        while not self._stop.wait(0.01 if self.mark is not None else self.every):
            if self.mark is not None and (self.step() or 0) >= self.mark:
                self.mark = None
                self.sample(); last = time.monotonic()
            elif time.monotonic() - last >= self.every:
                self.sample(); last = time.monotonic()

    def start(self):
        self.sample()
        self._thread.start()
        return self

    def stop(self):
        self._stop.set()
        self._thread.join()
        self.sample()


def summary(samples, from_step=None):
    """Fields over the window (samples at or after from_step; all samples when None)."""
    w = [s for s in samples if from_step is None or (s["step"] or 0) >= from_step] or samples[-1:]
    a, b = w[0], w[-1]
    wall, cpu = b["t"] - a["t"], b["cpu"] - a["cpu"]
    steps = (b["step"] - a["step"]) if from_step is not None else None
    mean = lambda k: (sum(s[k] for s in w if s[k] is not None) / max(1, sum(s[k] is not None for s in w)))
    gb = 2**30
    return dict(
        res_samples=len(w),
        res_ram_start_gb=a["rss"] / gb, res_ram_end_gb=b["rss"] / gb,
        res_ram_peak_window_gb=max(s["rss"] for s in w) / gb,
        res_ram_peak_run_gb=max(s["rss"] for s in samples) / gb,
        res_cpu_seconds_per_step=cpu / steps if steps else None,
        res_cpu_cores_used=cpu / wall if wall > 0 else None,
        res_gpu_busy_mean_pct=mean("gpu_util") if w[0]["gpu_util"] is not None else None,
        res_gpu_own_peak_mb=max((s["gpu_own"] or 0) for s in w) if w[0]["gpu_own"] is not None else None,
        res_gpu_card_used_peak_mb=max((s["gpu_used"] or 0) for s in w) if w[0]["gpu_used"] is not None else None,
        res_pc_load_mean=mean("load"),
        res_other_gpu_programs=sorted({n for s in w for n in s["others"]}),
        res_process_maxrss_gb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20,
    )
