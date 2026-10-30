"""The safety stock check of Appendix G (app:cal:safety): the load sweep with every SKU's safety
stock sized at the most popular rank instead of its starting rank. Run from the code copy of the
step 12 queue with PYTHONPATH=src and --workers 1, since spawned workers would not see the patch."""
import runpy
import sys

from slap_mapd_coupling.training import spec as spec_module


def top_rank_starting_stock(sku_ids, demand, sizing):
    quantiles = spec_module.period_demand_quantiles(
        len(sku_ids),
        0.0 if demand is None else demand.skew,
        sizing.arrival_rate,
        sizing.epoch_length,
        sizing.service_level,
        sizing.lines_per_order,
        sizing.units_per_line,
    )
    return {sku_id: sizing.refill_units + quantiles[0] for sku_id in sku_ids}


spec_module.refill_starting_stock = top_rank_starting_stock
sys.argv = ["load_sweep.py", *sys.argv[1:]]
runpy.run_path("scripts/sweep/load_sweep.py", run_name="__main__")
