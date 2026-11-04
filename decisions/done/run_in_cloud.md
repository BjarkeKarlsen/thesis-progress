Status 2026-10-30: dropped. Cloud training runs without n8n, see `../active/cloud/`.

I gonna use Kaggle the free i have and then buy access to the Colab for a month to have it running.

Yes — use **n8n as the orchestration and artifact-collection layer**, but do **not** make it the training controller. Each training platform should run your repo, write a structured run manifest, upload checkpoints/metrics to durable storage, and then call an n8n webhook. n8n can then ingest the run, copy artifacts into storage, trigger evaluation, and notify you. n8n supports schedule and webhook triggers, which fits this design. [n8n](https://n8n.io/integrations/webhook/and/isn/)

## Target architecture

```text
Kaggle / Colab / LUMI
        │
        │  train + periodic checkpoints
        ▼
Artifact store: S3-compatible / Google Drive / Nextcloud / MinIO
        │
        │  run_finished webhook + manifest.json
        ▼
n8n on home Linux PC
        │
        ├─ validate manifest and files
        ├─ copy/download checkpoints + metrics
        ├─ enqueue evaluation job
        ├─ run test/validation suite
        └─ notify Slack/Discord/email + update experiment registry
```

Use this separation:

- **Training platform:** runs PPO, writes checkpoints and metrics.
- **Object storage:** durable home for checkpoints, TensorBoard logs, configs, and manifests.
- **n8n:** reacts to completion, moves data, triggers evaluation, tracks status.
- **Evaluation worker:** a separate small machine/job that runs validation and test episodes using saved checkpoints.

Do not have n8n directly execute long RL training. It should orchestrate short, idempotent jobs.

## Common repo additions

Add these to `slap-mapd-coupling` so every platform behaves identically.

### 1. Run manifest

At the end of every training run, write:

```json
{
  "run_id": "decentralised_2026-10-28_1100_a1b2",
  "platform": "kaggle",
  "git_commit": "abc1234",
  "config": "configs/decentralised.yaml",
  "seed": 42,
  "env_steps": 10000000,
  "checkpoint_path": "checkpoints/ppo_final/checkpoint_000500",
  "metrics_path": "results/metrics.parquet",
  "tensorboard_path": "results/tb/",
  "status": "completed",
  "started_at": "2026-10-28T10:00:00Z",
  "finished_at": "2026-10-28T18:12:00Z"
}
```

Also write `manifest.json` after every checkpoint, with `"status": "running"` and the latest checkpoint path. This lets n8n distinguish an interrupted run from a completed one.

### 2. Evaluation command

Add a CLI verb such as:

```bash
slap-mapd evaluate \
  --checkpoint checkpoints/ppo_final/checkpoint_000500 \
  --config configs/decentralised.yaml \
  --split validation \
  --episodes 200 \
  --output results/validation/decentralised_2026-10-28_1100_a1b2.parquet
```

Then a test command:

```bash
slap-mapd evaluate \
  --checkpoint checkpoints/ppo_final/checkpoint_000500 \
  --config configs/decentralised.yaml \
  --split test \
  --episodes 500 \
  --output results/test/decentralised_2026-10-28_1100_a1b2.parquet
```

Keep the **test set locked** until after model selection. Use validation results to choose checkpoints or hyperparameters; use test results only once per final model.

### 3. Artifact layout

Use one directory per run:

```text
runs/
  decentralised_2026-10-28_1100_a1b2/
    manifest.json
    config.yaml
    git_commit.txt
    checkpoints/
      checkpoint_000100/
      checkpoint_000200/
      checkpoint_000500/
    metrics/
      train_metrics.parquet
      tensorboard/
    evaluation/
      validation/
        validation_metrics.parquet
      test/
        test_metrics.parquet
```

This makes n8n processing simple and avoids mixing outputs from different experiments.

## Kaggle guide

Kaggle is the best first production target because it gives you a bounded weekly GPU quota and multi-hour notebook sessions. 

### Notebook setup

Create a Kaggle notebook with GPU enabled, then use a setup cell:

```python
import os, subprocess, sys

REPO = "https://github.com/BjarkeKarlsen/slap-mapd-coupling.git"
RUN_ID = os.environ.get("RUN_ID", "kaggle_smoke")

subprocess.run(["git", "clone", REPO], check=True)
os.chdir("slap-mapd-coupling")
subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
```

Because your repository is public, no GitHub token is needed. If you later make it private, use a Kaggle Secret and install with a token-bearing HTTPS URL rather than embedding the token in the notebook. [kaggle](https://www.kaggle.com/docs/efficient-gpu-usage?ref=hackernoon.ai)

### Training cell

```python
import os, subprocess

RUN_ID = "decentralised_kaggle_001"

subprocess.run([
    "slap-mapd", "train",
    "--config", "configs/decentralised.yaml",
    "--budget-env-steps", "1000000",
    "--checkpoint-dir", f"/kaggle/working/runs/{RUN_ID}/checkpoints",
    "--output-dir", f"/kaggle/working/runs/{RUN_ID}",
], check=True)
```

The exact flags should match your current `train` CLI; the important point is that all outputs go under `/kaggle/working/runs/<run_id>/`.

### Save outputs

Kaggle notebook output is not a durable long-term archive, so upload the run directory to external storage before the session ends:

```python
import os
from google.oauth2 import service_account
from google.cloud import storage

# Preferred: use Kaggle Secrets for the service-account JSON or token.
client = storage.Client.from_service_account_json(
    "/kaggle/input/secrets/slap-mapd-uploader.json"
)
bucket = client.bucket("slap-mapd-runs")

for root, _, files in os.walk(f"/kaggle/working/runs/{RUN_ID}"):
    for name in files:
        local = os.path.join(root, name)
        remote = os.path.relpath(local, "/kaggle/working")
        bucket.blob(remote).upload_from_filename(local)
```

Alternatively, use `rclone` with credentials stored in Kaggle Secrets; it is simpler for large checkpoint directories.

### Trigger n8n

At the end:

```python
import requests, json

webhook = os.environ["N8N_RUN_FINISHED_WEBHOOK"]

requests.post(webhook, json={
    "run_id": RUN_ID,
    "platform": "kaggle",
    "status": "completed",
    "artifact_prefix": f"runs/{RUN_ID}/",
    "manifest_url": f"https://your-storage.example/runs/{RUN_ID}/manifest.json"
}, timeout=30)
```

Store the webhook URL in a Kaggle Secret, never in the notebook.

### Kaggle workflow

1. Run the 5–10 minute smoke test.
2. Confirm checkpoints appear in `/kaggle/working`.
3. Confirm upload to storage works.
4. Confirm n8n receives the webhook.
5. Launch a real run sized to remain below Kaggle’s session and weekly GPU limits. Kaggle documents a 12-hour GPU session limit and displays the weekly accelerator quota in the interface. 
6. On completion, let n8n trigger validation.

## Colab guide

Use Colab for interactive debugging and short runs. Its resources are not guaranteed, and usage limits fluctuate, so always design around interruption. 

### Setup cell

```python
import os, subprocess, sys

!git clone https://github.com/BjarkeKarlsen/slap-mapd-coupling.git
%cd slap-mapd-coupling
!pip install -e .
```

Mount Google Drive for persistent artifacts:

```python
from google.colab import drive
drive.mount("/content/drive")

RUN_ID = "decentralised_colab_001"
RUN_DIR = f"/content/drive/MyDrive/slap-mapd-runs/{RUN_ID}"
os.makedirs(RUN_DIR, exist_ok=True)
```

### Training cell

```python
!slap-mapd train \
  --config configs/decentralised.yaml \
  --budget-env-steps 1000000 \
  --checkpoint-dir "$RUN_DIR/checkpoints" \
  --output-dir "$RUN_DIR"
```

### Resume after disconnect

Colab may disconnect, so make the training command resumable:

```bash
slap-mapd train \
  --config configs/decentralised.yaml \
  --resume "$RUN_DIR/checkpoints/latest" \
  --budget-env-steps 2000000 \
  --checkpoint-dir "$RUN_DIR/checkpoints" \
  --output-dir "$RUN_DIR"
```

Implement `--resume` in the RLlib/Tune layer so it loads the latest checkpoint and continues the experiment rather than restarting.

### Colab-specific rules

- Save directly to Drive, not only `/content`.
- Checkpoint at least every 15–30 minutes.
- Use a small validation job after each major checkpoint.
- Do not rely on a Colab session surviving overnight.
- For paid Colab, remember that even paid runtimes have resource and runtime limits; Pro+ advertises up to 24-hour runtimes subject to available compute units and capacity. 

## LUMI guide

LUMI should be your main platform for thesis-scale experiments. It uses Slurm batch jobs, submitted with `sbatch`; a job script declares resources and the commands to run. [stackoverflow](https://stackoverflow.com/questions/54801199/how-do-i-install-python-package-from-private-github-repo-using-jenkins)

LUMI uses AMD GPUs and ROCm rather than NVIDIA CUDA, and provides PyTorch/Singularity containers; use their provided container/module environment rather than assuming a normal CUDA Docker image will work. [research.google](https://research.google.com/colaboratory/faq.html)

### Repository layout

```text
hpc/
  lumi/
    train.slurm
    evaluate.slurm
    env.sh
    README.md
```

### `env.sh`

```bash
#!/bin/bash
module purge
module load LUMI
module load Local-LAIF lumi-aif-singularity-bindings

export SIF=/appl/local/laifs/containers/lumi-multitorch-latest.sif
export PROJECT_DIR=/project/project_XXXX
export RUN_ROOT=$PROJECT_DIR/slap-mapd-runs
```

LUMI’s AI container guidance shows loading `Local-LAIF` and the Singularity bindings module, then using the provided container from `/appl/local/laifs/containers`. [colab.research.google](https://colab.research.google.com/signup)

### `train.slurm`

```bash
#!/bin/bash -e
#SBATCH --job-name=slap-mapd-train
#SBATCH --account=project_XXXX
#SBATCH --partition=small-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-task=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --output=logs/train_%x_%j.out
#SBATCH --error=logs/train_%x_%j.err

source "$SLURM_SUBMIT_DIR/env.sh"

RUN_ID=${RUN_ID:-decentralised_lumi_$(date +%Y%m%d_%H%M)}
RUN_DIR=$RUN_ROOT/$RUN_ID
mkdir -p "$RUN_DIR"/{checkpoints,metrics,logs}

git rev-parse HEAD > "$RUN_DIR/git_commit.txt"
cp configs/decentralised.yaml "$RUN_DIR/config.yaml"

srun --cpu-bind=none \
  singularity exec \
  --bind "$PROJECT_DIR:/project" \
  --bind "$RUN_DIR:/run_output" \
  "$SIF" \
  bash -lc '
    cd /project/slap-mapd-coupling
    pip install --user -e .
    slap-mapd train \
      --config /run_output/config.yaml \
      --budget-env-steps 10000000 \
      --checkpoint-dir /run_output/checkpoints \
      --output-dir /run_output
  '
```

Adjust the bind paths, container name, partition, account, CPU count, and memory to your actual LUMI project and allocation. LUMI’s examples use `srun` together with `singularity exec` for containerized PyTorch work. [research.google](https://research.google.com/colaboratory/faq.html)

### Submit

```bash
cd hpc/lumi
RUN_ID=decentralised_lumi_001
sbatch --export=RUN_ID=$RUN_ID train.slurm
```

### Evaluate after training

Create `evaluate.slurm`:

```bash
#!/bin/bash -e
#SBATCH --job-name=slap-mapd-eval
#SBATCH --account=project_XXXX
#SBATCH --partition=small-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-task=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00

source "$SLURM_SUBMIT_DIR/env.sh"

RUN_ID=$1
CHECKPOINT=$2
SPLIT=${3:-validation}
EPISODES=${4:-200}

RUN_DIR=$RUN_ROOT/$RUN_ID

srun singularity exec \
  --bind "$PROJECT_DIR:/project" \
  --bind "$RUN_DIR:/run_output" \
  "$SIF" \
  bash -lc "
    cd /project/slap-mapd-coupling
    slap-mapd evaluate \
      --checkpoint $CHECKPOINT \
      --config /run_output/config.yaml \
      --split $SPLIT \
      --episodes $EPISODES \
      --output /run_output/evaluation/$SPLIT/metrics.parquet
  "
```

Submit it after training:

```bash
sbatch evaluate.slurm decentralised_lumi_001 \
  /project/project_XXXX/slap-mapd-runs/decentralised_lumi_001/checkpoints/checkpoint_000500 \
  validation 200
```

## n8n orchestration

Your home n8n server is a good control plane, provided the home PC is reliable enough and you expose only a tightly authenticated webhook.

### Required components

- **n8n** on your Linux PC.
- **Storage backend:** MinIO/S3-compatible storage is ideal; Google Drive, Nextcloud, or Backblaze B2 also work.
- **A small evaluation runner:** either the same Linux PC, a university lab machine, or a cheap cloud VM.
- **Secrets:** store all tokens in n8n credentials, not in workflow JSON or Git.

### Workflow 1: `training-finished`

Trigger: **Webhook**, `POST /webhook/slap-mapd/run-finished`.

Nodes:

1. **Webhook** — receives `run_id`, `platform`, `status`, `artifact_prefix`, `manifest_url`.
2. **IF** — reject if `status != completed`.
3. **HTTP Request** — download `manifest.json`.
4. **Validate manifest** — check required fields, Git commit, checkpoint path, metrics path.
5. **HTTP Request / S3 node / Google Drive node** — download or copy:
   - `manifest.json`
   - `config.yaml`
   - final checkpoint
   - training metrics
   - TensorBoard event files
6. **Write to local archive** — e.g. `/srv/slap-mapd/runs/<run_id>/`.
7. **HTTP Request to evaluation runner** — POST:

```json
{
  "run_id": "decentralised_lumi_001",
  "checkpoint": "/srv/slap-mapd/runs/decentralised_lumi_001/checkpoints/checkpoint_000500",
  "config": "/srv/slap-mapd/runs/decentralised_lumi_001/config.yaml",
  "split": "validation",
  "episodes": 200
}
```

8. **Database/JSON update** — mark run as `awaiting_validation`.
9. **Notify** — Discord/Slack/email: “Training finished; validation queued.”

### Workflow 2: `validation-finished`

Trigger: webhook from the evaluation runner.

Nodes:

1. Validate that the evaluation output exists.
2. Copy validation metrics into the run directory.
3. Compute or fetch summary metrics: success rate, makespan, throughput, congestion, reward, constraint violations.
4. Compare against the reference planner and prior runs.
5. Update run status to `validation_complete`.
6. Optionally trigger test evaluation only for the selected best checkpoint.
7. Notify you with a compact result summary.

### Workflow 3: nightly artifact poller

Use this as a fallback for platforms that cannot reliably call a webhook.

Trigger: **Schedule**, every 15–30 minutes.

Nodes:

1. List new objects in storage under `runs/`.
2. For each run directory, fetch `manifest.json`.
3. If `status == completed` and `n8n_processed != true`, invoke the `training-finished` workflow.
4. Mark the manifest as processed, preferably by writing `n8n_processed.json` back to storage.
5. Alert if a run has been `running` for longer than its expected maximum duration.

This poller is useful because Kaggle and Colab sessions can die before the final webhook fires.

## Evaluation design

After training, do this in two stages.

### Validation loop

Run validation on several checkpoints, not only the final one:

```text
checkpoint_000100 -> validation
checkpoint_000200 -> validation
checkpoint_000300 -> validation
checkpoint_000400 -> validation
checkpoint_000500 -> validation
```

For each checkpoint, use the same:

- Warehouse instances.
- Seeds.
- Agent counts.
- Task-generation regime.
- Storage rule.
- Number of validation episodes.

Select the checkpoint with the best validation performance, considering both objective metrics and robustness across seeds/loads.

### Test loop

Run only the selected checkpoint on the held-out test set:

```bash
slap-mapd evaluate \
  --checkpoint checkpoints/checkpoint_000400 \
  --config configs/decentralised.yaml \
  --split test \
  --episodes 500 \
  --output results/test/final.parquet
```

Report mean and confidence intervals across seeds/episodes. For a thesis, include:

- Pickup-and-delivery throughput.
- Makespan or completion time.
- Travel distance.
- Congestion or conflict-resolution frequency.
- Constraint violations.
- Comparison against prioritised A* / Token Passing.
- Generalization across warehouse sizes, agent counts, and demand levels.

## What I would build first

1. Add `manifest.json`, checkpoint resume, and `slap-mapd evaluate` to the repository.
2. Add a Kaggle notebook that clones, trains, checkpoints, uploads, and webhooks n8n.
3. Add a Colab notebook with Drive persistence and resume.
4. Add LUMI `train.slurm` and `evaluate.slurm` once you have an allocation.
5. Build the n8n `training-finished` workflow and a local/S3 artifact archive.
6. Build the validation workflow.
7. Only after validation works, add the test workflow and final reporting.

This gives you a reproducible pipeline: **train anywhere → persist artifacts → n8n collects → evaluate checkpoints → select best model → run held-out test once.**