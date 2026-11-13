# Training in the cloud, without n8n

Written 2026-10-30. Replaces the n8n plan in `../run_in_cloud.md`.

The idea is simple. A cloud notebook clones the repo from GitHub, trains one arm, and keeps the
run folder. You download the folder into `~/thesis_runs/training/fleet_<m>/<regime>/` and
evaluate it at home, exactly as a run from `bedtime.bash`. Nothing on the home network has to be
reachable from outside.

- Kaggle: [kaggle.md](kaggle.md). Free. The run folder is kept as the notebook's output.
- Colab: [colab.md](colab.md). One paid month. The run folder is kept on Google Drive.

## What the repo already has

The old plan asked for a manifest, a resume command and an evaluate command. The last two exist.

| need | command |
|---|---|
| train one arm | `slap-mapd train --config ... --output RUN` |
| continue a stopped run | `slap-mapd resume RUN` (same budget, same settings) |
| pick a checkpoint and test it | `slap-mapd evaluate RUN` (validation seeds pick, test seeds report) |
| warehouse tables somewhere else | `SLAP_WAREHOUSE_STORE=/some/dir` (built on first use, or copied) |

A run stopped with Ctrl-C (SIGINT) stops cleanly and loses at most 3 iterations. Both guides use
this. They stop training with `timeout --signal=INT` an hour before the platform would kill the
session, so the run folder is always saved in a state `resume` can continue.

`train` writes `<name>_spec.json` into the run folder. That file is the manifest. It holds every
setting the run used. The guides also write `commit.txt` with the code version.

## Be clear about speed

The cloud machines are not faster than this PC. Training is CPU bound (the env runners), and this
PC has 8 cores. Fleet 8, 504,000 steps, took 2 h here with 6 runners and no GPU (2026-10-24).
Kaggle gives 4 cores, so expect roughly twice that. The gain is more machines at once. The PC
keeps running sweeps while the cloud trains arms.

Whether `--gpu` helps is not known yet. The smoke test below measures it.

## What to do, in order

1. **Push the code the cloud should run.** The cloud only sees GitHub. Today the work is on
   `feat/workstation-sections`, which is not pushed and has 9 changed files that are not
   committed. Commit and push the branch you want trained. Write its name into the notebook.
2. **Smoke test on Kaggle** (about 30 minutes, [kaggle.md](kaggle.md), "Smoke test"). It checks
   that the install works, the warehouses build, a checkpoint appears, `resume` continues the
   run, and a downloaded run evaluates at home. It also times one iteration with and without
   the GPU.
3. **Decide what goes to the cloud.** Good candidates are the training arms that do not need the
   PC: fleet 8 and 16, trained under `fixed` and `demand` storage. One notebook per fleet and regime. Each needs
   the fleet's main load from `thesis-progress/results/E_load/`.
4. **Run them on Kaggle.** CPU sessions do not use the weekly GPU quota. A run longer than 11 h
   continues in a second session.
5. **Bring each run home.** Download it to `~/thesis_runs/training/fleet_<m>/<regime>/`, then do
   what `bedtime.bash` does after training. Write a `done` file, copy the progress file to
   `thesis-progress/results/training/fleet_<m>/decentralised_<regime>/progress.jsonl`, and run
   `slap-mapd evaluate` on it. Note the run in `thesis-progress/RUNS.md`.
6. **Buy the Colab month only when Kaggle works** and you have runs waiting. Use it for what
   Kaggle cannot fit, such as fleet 32 and 64 (more memory, and a GPU if step 2 showed it helps).

## Things to keep in mind

- Keep the run folder at the same path in every session (`/kaggle/working/run`,
  `/content/run`). Ray restores most reliably from the path the run started at.
- `resume` keeps the number of env runners the run started with. Resume a Kaggle run on Kaggle
  or at home, not on a smaller machine.
- No secrets are needed in the notebooks, because the repo is public. If you use the Kaggle
  command line at home, its token stays in `~/.kaggle/kaggle.json` and never goes in a notebook
  or a chat.
- Checkpoints are about 8 MB each at fleet 8 and 35 MB at fleet 32 (old model). Kaggle keeps up to
  20 GB of output and Drive's free space is 15 GB, so space is not an issue.
- Platform limits change. The numbers in these guides (12 h sessions, 4 cores, 20 GB) are as of
  late 2026. Check the notebook's settings panel if something behaves differently.
