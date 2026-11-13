import json, sys, statistics as st
for path in sys.argv[1:]:
    rows = [json.loads(l) for l in open(path) if l.strip()]
    by = {}
    for r in rows:
        by.setdefault((r["variant"], r["changes"]), {})[r["seed"]] = r
    base = by.get(("demand", ""), {})
    print(f"\n=== {path.split('/')[-1]}  ({len(rows)} runs)")
    print(f"{'setup':<26}{'seeds':>6}{'blocked':>9}{'less blocked':>14}{'tasks':>7}{'more tasks':>12}{'service':>9}{'keeps up':>10}")
    for key, name in ((("demand", ""), "today"), (("shelfblock", ""), "signal in storage"),
                      (("demand", "pickb"), "signal in pick choice"), (("shelfblock", "pickb"), "both")):
        runs = by.get(key, {})
        seeds = sorted(set(runs) & set(base))
        if not seeds:
            continue
        f = lambda x: 0.0 if x is None else x
        lb = sum(f(runs[s]["mean_blocked_time"]) < f(base[s]["mean_blocked_time"]) for s in seeds)
        mt = sum(runs[s]["num_completed_tasks"] >= base[s]["num_completed_tasks"] for s in seeds)
        print(f"{name:<26}{len(seeds):>6}{st.mean(f(runs[s]['mean_blocked_time']) for s in seeds):>9.1f}"
              f"{(str(lb)+'/'+str(len(seeds))) if key!=('demand','') else '':>14}"
              f"{st.mean(runs[s]['num_completed_tasks'] for s in seeds):>7.0f}"
              f"{(str(mt)+'/'+str(len(seeds))) if key!=('demand','') else '':>12}"
              f"{st.mean(f(runs[s]['mean_service_time']) for s in seeds):>9.0f}"
              f"{sum(bool(runs[s]['keeps_up']) for s in seeds):>7}/{len(seeds)}")
