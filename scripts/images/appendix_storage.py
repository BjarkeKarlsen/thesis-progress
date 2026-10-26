"""
The figures of the Storage rule values appendix (G.StorageValues.tex, app:storagecal).

Run:  python thesis-progress/scripts/images/appendix_storage.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/app_storage_period.png   fig:app:storageperiod
      thesis-progress/scripts/Images/app_storage_beta.png     fig:app:storagebeta
      thesis-progress/scripts/Images/app_storage_margin.png   fig:app:storagemargin

Reads the storage columns of the Token Passing parameter sweep
(results/G_storage/fleet_<m>/storage_rule.*/, from slap-mapd-coupling's
scripts/sweep/parameter_sweep.bash). A missing run is drawn as a placeholder.
"""
import os

from appendix_data import RESULTS, sweep_figure

SWEEP = os.path.join(RESULTS, "G_storage")


def storage_period():
    """The storage period Delta under demand storage, paired with fixed storage at the same
    Delta (app:cal:period). Keep the value where the gain levels off."""
    columns = [("storage_rule.epoch_length", "demand", r"storage period $\Delta$ (steps)",
                100, None)]
    return sweep_figure("app_storage_period.png", columns, SWEEP)


def storage_beta():
    """The congestion weight beta of the congestion-aware rule, paired with fixed storage at
    the default values, with the crowding as a fourth panel (app:cal:beta). beta = 0 is
    demand storage, the built-in check."""
    columns = [("storage_rule.congestion_weight", "congestion", r"congestion weight $\beta$",
                1.0, ("storage_rule.epoch_length", 100))]
    return sweep_figure("app_storage_beta.png", columns, SWEEP,
                        extra=("mean_crowding", "mean\ncrowding"))


def storage_margin():
    """The stock margin epsilon under demand storage, paired with fixed storage at the same
    margin (app:cal:margin). The margin sets how much stock arrives above the last period's
    orders, so it changes fixed storage too."""
    columns = [("arrival.margin", "demand", r"stock margin $\varepsilon$", 1.0, None)]
    return sweep_figure("app_storage_margin.png", columns, SWEEP)


def appendix_storage():
    return [storage_period(), storage_beta(), storage_margin()]


if __name__ == "__main__":
    for path in appendix_storage():
        print(path)
