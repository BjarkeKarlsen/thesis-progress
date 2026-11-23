import sys
from collections import defaultdict
from slap_mapd_coupling.training.spec import load_spec, instance_params
from slap_mapd_coupling.instances.generator import generate_instance
from slap_mapd_coupling.environment.zones import zones_by_aisle, zone_of
for cfg in sys.argv[1:]:
    from pathlib import Path; spec = load_spec(Path(cfg))
    split = 0; total = 0; zones_per=[]
    for seed in range(20):
        p = instance_params(spec).model_copy(update={"seed": seed})
        inst = generate_instance(p)
        g = inst.graph
        zones = zones_by_aisle(g, inst.aisle_index, spec.arm.num_zones)
        zo = zone_of(zones)
        nb = {}
        for (a,b) in [(e.source,e.target) for e in g.edges] if hasattr(g,'edges') else []:
            pass
        sec = defaultdict(list)
        for v, vx in g.vertices.items():
            if vx.section is not None:
                # leaf: zone of its single neighbour's aisle
                sec[vx.section].append(inst.aisle_index[v])
        aisles = sorted(set(inst.aisle_index[v] for v in zo))
        # map aisle->zone
        a2z = {}
        for v,z in zo.items(): a2z[inst.aisle_index[v]] = z
        for s, al in sec.items():
            zs = {a2z.get(a, None) for a in al}
            total += 1; split += len(zs) > 1
        if seed == 42 % 20: pass
    print(cfg, "zones", spec.arm.num_zones, "aisles", len(aisles), "sections/seed", len(sec), "sections spanning >1 zone:", split, "of", total)
