"""Build the warehouse tables of one config at home and upload them as a private Kaggle dataset.

Run from the workspace root with the venv of slap-mapd-coupling:

    PYTHONPATH=slap-mapd-coupling/src ~/.venvs/rl/bin/python \\
        thesis-progress/decisions/active/cloud/upload_warehouses.py \\
        slap-mapd-coupling/configs/fleet_8/decentralised.yaml [--workers 6]

It computes the store key of the config (training/warehouses.py, pool_key), builds every seed's
tables with `slap-mapd prepare-warehouses` (seeds already stored are skipped), and uploads the
folder as bjarkekarlsen/slap-wh-<key>, a new version if the dataset exists. Then add that name to
"dataset_sources" in kaggle_kernel/kernel-metadata.json, and train.py copies the tables into
place before training. The key covers everything the tables depend on, so a set built for other
code or another config is never used by mistake. The training budget and the regime do not
change it. Needs the Kaggle command line with a token (kaggle.md, one-time setup).
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from slap_mapd_coupling.training.spec import load_spec
from slap_mapd_coupling.training.warehouses import DEFAULT_STORE, STORE_VARIABLE, pool_key

USER = "bjarkekarlsen"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("config")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()

    key = pool_key(load_spec(Path(args.config)))
    store = Path(os.environ.get(STORE_VARIABLE, DEFAULT_STORE)) / key
    subprocess.run([sys.executable, "-m", "slap_mapd_coupling.main", "prepare-warehouses",
                    "--config", args.config, "--workers", str(args.workers)], check=True)
    slug = "slap-wh-" + key.replace("_", "-")
    if len(slug) > 50:
        raise SystemExit(f"{slug} is longer than Kaggle's 50 characters.")
    with tempfile.TemporaryDirectory() as staging:
        for path in store.iterdir():
            shutil.copy(path, staging)
        Path(staging, "pool_key.txt").write_text(key + "\n")
        Path(staging, "dataset-metadata.json").write_text(json.dumps({
            "title": "slap wh " + key.replace("_", " "),
            "id": f"{USER}/{slug}",
            "licenses": [{"name": "CC0-1.0"}],
        }))
        exists = subprocess.run(["kaggle", "datasets", "status", f"{USER}/{slug}"],
                                capture_output=True, text=True).returncode == 0
        if exists:
            cmd = ["kaggle", "datasets", "version", "-p", staging, "-m", f"tables of {key}"]
        else:
            cmd = ["kaggle", "datasets", "create", "-p", staging]
        subprocess.run(cmd, check=True)
    print(f'Uploaded {len(list(store.iterdir()))} files. Add "{USER}/{slug}" to dataset_sources.')


if __name__ == "__main__":
    main()
