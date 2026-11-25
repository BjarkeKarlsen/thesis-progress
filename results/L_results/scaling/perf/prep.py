"""Builds the warehouses of the 20 test seeds for every (fleet, arm) of the performance test
before the episodes start, so no two probes build the same store at once and every probe writes
the same manifest (the cap over the 20 seeds). Usage: prep.py WORKERS 'FLEET ARM RUN_DIR' ...
Run from ~/worktrees/scaling-run with PYTHONPATH=src and SLAP_WAREHOUSE_STORE set."""
import sys
from pathlib import Path
from slap_mapd_coupling.training.evaluate_run import load_run_spec
from slap_mapd_coupling.training.scaling_probe import probe_spec, probe_study
from slap_mapd_coupling.training.spec import load_spec

def main():
    workers = int(sys.argv[1])
    seeds = list(range(200000, 200020))
    for job in sys.argv[2:]:
        m, arm, run = job.split()
        cfg = "decentralised" if arm == "decentralised_comm" else arm
        sections = (2 if m == "8" else 3 * int(m) // 16) if arm == "section" else None
        spec = probe_spec(load_run_spec(Path(run)), load_spec(Path(f"configs/fleet_{m}/{cfg}.yaml")),
                          sections, 10000, 5000)
        from slap_mapd_coupling.training.warehouses import WarehousePool
        store = None if spec.warehouse_store is None else Path(spec.warehouse_store).expanduser()
        pool = WarehousePool(spec, store)
        print(m, arm, pool.root, pool.prepare(seeds, workers=workers), flush=True)

if __name__ == "__main__":
    main()
