# Training on Kaggle

Updated 2026-11-02 for `main` after #201: the configs in `configs/fleet_<m>/` hold the model the
Token Passing runs settled, at each fleet's main load.

One Kaggle run trains one arm (a controller, a fleet and a regime). It is a script kernel,
`kaggle_kernel/train.py`, pushed and started from the terminal with the Kaggle command line, so
nothing is clicked in the browser. It keeps going with the terminal closed, and Kaggle keeps
everything in `/kaggle/working` as the kernel's output. A run that does not finish in one session
(12 h) continues in the next from that output.

## One-time setup

1. Verify the Kaggle account with a phone number (Settings). Without it a kernel has no internet
   and cannot clone the repo.
2. Install the command line, version 2 or later, which reads the new API tokens:
   `uv tool install --python 3.12 "kaggle>=1.8" --with six` (version 1.7 only reads
   `kaggle.json`, and version 2 misses its `six` dependency).
3. Put your API token in `~/.kaggle/access_token` (Kaggle, Settings, API, Create New Token) and
   `chmod 600 ~/.kaggle/access_token`. Never paste the token into a chat or a commit.
4. `kaggle_kernel/kernel-metadata.json` holds the user name `bjarkekarlsen`.
5. Check it works: `kaggle kernels list --mine`.

## The two files

- `kaggle_kernel/train.py`. Clones `slap-mapd-coupling`, installs it with the same Ray as at
  home (2.57.0), trains one arm with `slap-mapd train`, and stops it cleanly with Ctrl-C after
  `HOURS`, so the run folder is always in a state `slap-mapd resume` can continue. The settings at
  the top are the only part to edit: `CONTROLLER`, `FLEET`, `REGIME` (the storage rule it
  trains under: `fixed`, `demand` or `congestion`), `HOURS`, `BUDGET`, `GPU` and
  `RESUME_FROM`. Everything else, the fleet's main load included, comes from the config
  `configs/fleet_<FLEET>/<CONTROLLER>.yaml`.
- `kaggle_kernel/kernel-metadata.json`. A private script kernel, CPU only, internet on.

## Warehouse tables, built at home

Before training, a run needs the window tables of every seed's warehouse. Built on Kaggle they
take about 20 minutes at fleet 8 and about 1.5 hours at fleet 64, in every session. So they are
built at home once per arm and fleet and uploaded as a private Kaggle dataset:

```bash
PYTHONPATH=slap-mapd-coupling/src ~/.venvs/rl/bin/python \
    thesis-progress/decisions/active/cloud/upload_warehouses.py \
    slap-mapd-coupling/configs/fleet_8/decentralised.yaml
```

It prints the dataset's name, for example `bjarkekarlsen/slap-wh-fleet8-decentralised-f681777fff13`.
Put that name in `"dataset_sources"` of `kaggle_kernel/kernel-metadata.json`, and `train.py`
copies the tables into place before training ("warehouse tables ... files" in the log). The name
holds a fingerprint of everything the tables depend on, the code and the config, but not the
budget or the regime. A set that no longer matches is ignored and the run builds its own, so run
the script again after a change to the model or the configs. Each arm has its own set.

Uploaded so far: fleet 8 decentralised (`f681777fff13`, 200 MB, 2026-11-02).

## Running it

From the workspace root:

```bash
kaggle kernels push -p thesis-progress/decisions/active/cloud/kaggle_kernel
kaggle kernels status bjarkekarlsen/slap-mapd-train      # queued, running, complete or error
```

A push starts a new version of the kernel. Pushing again while a version runs starts another, so
wait for `complete` before the next push of the same kernel. To train two arms at once, copy the
folder and give the copy its own `id` and `title` (for example `slap-mapd-train-section`).

## Bringing it home

```bash
kaggle kernels output bjarkekarlsen/slap-mapd-train -p /tmp/kaggle_out
mkdir -p ~/thesis_runs/training/fleet_8/decentralised/fixed
cp -r /tmp/kaggle_out/run/. ~/thesis_runs/training/fleet_8/decentralised/fixed/
```

## Continuing

A run that hit `HOURS` before its budget ends with "Not finished" in its log.

1. Copy the folder to a new kernel (its own `id`), and in its `kernel-metadata.json` set
   `"kernel_sources": ["bjarkekarlsen/slap-mapd-train"]`, so the first run's output is mounted.
2. Set `RESUME_FROM` to the first run's folder. Kaggle mounts a kernel's output under
   `/kaggle/input/notebooks/<user>/<kernel>/`, not `/kaggle/input/<kernel>/` (2026-11-04), so
   `kaggle_kernel_section_resume/train.py` finds the folder by its `*_spec.json` instead of
   naming the path. Copy that block. The script prints the inputs it finds.
3. Push the new kernel.

Then evaluate it at home. The tables are rebuilt or found in `~/thesis_runs/warehouses`.

```bash
mkdir -p /var/tmp/ray_eval
RAY_TMPDIR=/var/tmp/ray_eval ~/.venvs/rl/bin/python -m slap_mapd_coupling.main evaluate \
    ~/thesis_runs/training/fleet_8/decentralised/fixed
```

Finally copy `decentralised_<regime>_training_progress.jsonl` to
`thesis-progress/results/training/fleet_8/decentralised_<regime>/progress.jsonl`, as
`bedtime.bash` does.

Evaluation at home plays the config's episode, 2000 steps with no warm-up. The Token Passing
runs played 10000 steps with a 5000-step warm-up (Appendix E), so a comparison with Token Passing
needs the evaluation set to match first. Still open (2026-11-02).

## Smoke test

Do this once before any real run. It takes about an hour.

1. Settings: `CONTROLLER = "decentralised"`, `FLEET = 8`, `BUDGET = 60000`, `HOURS = 1`.
   Push. Before training, a run builds the warehouse tables of every seed in `/tmp`. At fleet 8
   (258 warehouses) that took 20 minutes on Kaggle's 4 cores, so 0.4 hours left no time for an
   iteration (2026-11-02, version 1). In an 11-hour run it is about 3 percent.
2. The output should hold `run/` with a `*_spec.json`, at least one `checkpoint_*` folder, and a
   log that ends with "Stopped at ... Continue it with: slap-mapd resume". That proves the clean
   stop. If no checkpoint appears, raise `HOURS` and run it again.
3. Continue it as above with `HOURS = 1`. The log should show it reaching 60,000 steps, and
   `run/done` should exist. That proves resume.
4. Bring it home and run `slap-mapd evaluate` on it. That proves a cloud run works at home.
5. Read the time per iteration in the log (`time_this_iter_s`). Then run steps 1 and 2 once more
   with `"enable_gpu": true` in the metadata and `GPU = True`, and compare. Keep the GPU only if it is clearly
   faster, since it uses the weekly quota.
