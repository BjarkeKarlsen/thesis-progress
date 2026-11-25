import statistics, sys
from pathlib import Path
from slap_mapd_coupling.training.spec import load_spec, seed_spec, build_instance
from slap_mapd_coupling.training.env import _movable
from slap_mapd_coupling.environment.observation import local_subgraph
for m in (8,16,32,64):
    spec = load_spec(Path(f"configs/fleet_{m}/decentralised.yaml"))
    sizes, nv, nmov, shares = [], [], [], []
    for seed in range(200000, 200005):
        g = build_instance(seed_spec(spec, seed)).graph
        mov = sorted(_movable(g))
        w = [len(local_subgraph(g, v, spec.experiment.observation_depth)) for v in mov]
        sizes.append(statistics.fmean(w)); nv.append(len(g.vertices)); nmov.append(len(mov)); shares.append(statistics.fmean(w)/len(g.vertices))
    print(m, "depth", spec.experiment.observation_depth, "|V|", nv, "movable", nmov, f"window {statistics.fmean(sizes):.1f} share {100*statistics.fmean(shares):.1f}%")
