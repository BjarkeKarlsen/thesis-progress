"""
Every appendix result figure in one run.

Run:  python thesis-progress/scripts/images/appendix_figures.py [--copy]   (from the workspace root)
Out:  thesis-progress/scripts/Images/app_*.png. With --copy they are also copied into
      thesis/Images/, which the appendices read. Keep the two in sync from this side.

A figure whose run is missing is drawn as a placeholder, so the appendices build before the
results exist. Which run fills which figure and table is in
thesis-progress/decisions/active/appendix_values_overview.md.
"""
import os
import shutil
import sys

from base import OUT
from appendix_load import appendix_load
from appendix_storage import appendix_storage
from appendix_controllers import appendix_controllers
from appendix_training import appendix_training
from appendix_measures import appendix_measures
from appendix_checks import appendix_checks

THESIS_IMAGES = "thesis/Images"

if __name__ == "__main__":
    paths = (appendix_load() + appendix_storage() + appendix_controllers()
             + appendix_training() + appendix_measures() + appendix_checks())
    if "--copy" in sys.argv:
        for path in paths:
            shutil.copy(path, THESIS_IMAGES)
    print(f"wrote {len(paths)} figures to", os.path.abspath(OUT))
