import sys, statistics
from pathlib import Path
T = Path.home()/"Documents/thesis/thesis-progress/scripts"
sys.path[:0] = [str(T), str(T/"images")]
import appendix_results as ar
from scipy.stats import t
for m in (8,16,32,64):
    d = ar.token_passing_rows(m)
    if "fixed" not in d: print(m, "none"); continue
    fx = {r["seed"]: r for r in d["fixed"]}
    out=[f"{m}: fixed {statistics.fmean(r['mean_order_completion'] for r in fx.values()):.1f} n={len(fx)} keep {sum(r['keeps_up'] for r in fx.values())}"]
    for rule in ("demand","congestion"):
        rs = {r["seed"]: r for r in d.get(rule,[])}
        g=[100*(fx[s]["mean_order_completion"]-rs[s]["mean_order_completion"])/fx[s]["mean_order_completion"] for s in rs if s in fx]
        mu=statistics.fmean(g); h=t.ppf(.975,len(g)-1)*statistics.stdev(g)/len(g)**.5
        out.append(f"{rule} {mu:.1f} [{mu-h:.1f}, {mu+h:.1f}] faster {sum(x>0 for x in g)}/{len(g)} keep {sum(r['keeps_up'] for r in rs.values())}")
    print("  ".join(out))
