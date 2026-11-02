"""
The figures of the Storage rule values appendix (G.StorageValues.tex, app:storagecal).

Run:  python thesis-progress/scripts/images/appendix_storage.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/app_storage_period.png   fig:app:storageperiod
      thesis-progress/scripts/Images/app_storage_beta.png     fig:app:storagebeta
      thesis-progress/scripts/Images/app_storage_refill.png   fig:app:storagerefill

Reads the storage columns of the Token Passing parameter sweep
(results/G_storage/fleet_<m>/storage_rule.*/ and arrival.refill_units/, from slap-mapd-coupling's
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


def storage_refill():
    """The refill size Q under demand storage, paired with fixed storage at the same Q
    (app:cal:refill). Q changes fixed storage too, since it sets how much arrives. The sweep ran
    Q = 15, 30 and 60, and the point at Q = 10 is the storage period sweep at Delta = 100."""
    columns = [("arrival.refill_units", "demand", r"refill size $Q$ (units)", 10.0, None)]
    return sweep_figure("app_storage_refill.png", columns, SWEEP,
                        add_default=("storage_rule.epoch_length", 100.0))


def appendix_storage():
    return [storage_period(), storage_beta(), storage_refill()]


if __name__ == "__main__":
    for path in appendix_storage():
        print(path)
