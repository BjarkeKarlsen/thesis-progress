# Rules for every L4 agent (read first)

Source of the design: `../L4_design.md`. Repo rules: "Rules for every run" in `../fix_prs_plan.md`.
Where this file and the package plan differ, the package plan wins for its own package. Where this file and
`../fix_prs_plan.md` differ, stop and report.

## Setup

1. Read `../AGENTS.md`, `../CLAUDE.md`, `../slap-mapd-coupling/AGENTS.md`, `../slap-mapd-coupling/CLAUDE.md`, and
   `../L4_design.md` (the package plan names the parts to read).
2. Run `git -C ../thesis pull --no-rebase`. Print the thesis sections the plan names with
   `python3 ../thesis_section.py <label> ...` from the workspace root. The thesis is the source of truth. If the
   plan and the thesis disagree, stop and report.
3. Work in a git worktree off `origin/main`, never in the author's checkout.
   ```
   git -C ../slap-mapd-coupling fetch origin
   git -C ../slap-mapd-coupling worktree add <scratchpad>/<name> -b <branch> origin/main
   ```
   Packages that depend on another branch say which branch to start from instead. Work only inside the
   worktree with `PYTHONPATH=<worktree>/src PYTHONDONTWRITEBYTECODE=1` and the interpreter
   `/home/bjarkek/.venvs/rl/bin/python`. Check that `slap_mapd_coupling.__file__` points inside the worktree.
   Leave the worktree in place and report its path.
4. Line numbers in the plans refer to `origin/main` at 0961081. `origin/main` has since moved to 7bf81d4 (#134),
   which changed only example 04, the trace summary code in `evaluation/trace.py`, `training/callbacks.py` and
   their tests. The simulator, the generator, the trace writer and the golden reference are unaffected. Confirm each
   line number before editing, and report any that moved.

## Hard limits

- Never push, never merge, never run `gh pr create`, never open or edit GitHub issues. The author does these.
- Never edit `thesis/`. Never touch the untracked `thesis-progress/` folder inside `slap-mapd-coupling/`.
- Do not run `pytest`, `black`, `flake8` or `mypy`, not even a partial run. Write the tests, commit, and hand back
  the commands in "Hand back". The author runs them.
- You may run the golden comparison script and your own scratch scripts, since neither is the test suite. Say so
  in the hand back.
- Keep to the package. If the change grows past it (a file not listed, a new design question, a test that
  needs a new fixture module), stop and report.
- A value the thesis marks TBD becomes a config field with no default. Do not pick a number.
- Keep `slap-mapd-coupling` self-contained. Code, docstrings and comments must not mention files outside the repo,
  including `L4_design.md` and this folder.

## Writing in code

- Cite equations by name, never by label. Write "the communication graph", "the reward", "the field of view". The
  names are in `thesis/styles/eqnames.tex`. Sections and tables keep their `sec:` and `tab:` labels.
- Symbols follow `thesis/Chapters/2.Notation.tex`. Check the table before adding or renaming a symbol.
- Shorten docstrings you touch. Point to an issue number instead of long history. Do not rewrite files the package
  does not list.
- UK spelling. No dashes as punctuation. No colons or semicolons joining clauses.

## Commits

- One commit per step, each one self-consistent so the author's checks can pass at that commit.
- Commit message in UK spelling, ending with `Co-Authored-By: Claude <your model name> <noreply@anthropic.com>`.

## Golden comparison (packages that touch `environment/` or `evaluation/`)

The reference output is in
`/tmp/claude-1000/-home-bjarkek-Documents-thesis/daf10522-9c6a-4835-b075-d92920c89319/scratchpad/golden/`
(`golden/` folder, script `capture_golden.py`, compare script `compare_golden.sh`). If that folder is gone, rebuild
it from a clean `origin/main` worktree with the same script before you start.
```
cd <golden folder>
PYTHONPATH=<worktree>/src /home/bjarkek/.venvs/rl/bin/python capture_golden.py --out <new_run> --worktree <worktree>
./compare_golden.sh golden <new_run>
```
Metrics JSON files must be identical. Trace files may differ only in fields that read the task list after a step
(for example the released count). Classify every differing field. Any difference in positions, actions, overridden
flags, completed counts or backlog is a failure.
The capture script loads the example builders by path. If you change or delete an example it reads, copy the
builder into the script and say so.
Prioritised A\* example 01 is broken on `main`, and the author decided not to fix it. The script runs A\* on the
Token Passing example's instance for that reason.

## Hand back (every package)

1. Branch name, worktree path, commit hashes with one-line summaries.
2. The commands for the author, with the real worktree path filled in:
   ```
   cd <worktree path>
   export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD/src
   ~/.venvs/rl/bin/python -c "import slap_mapd_coupling; print(slap_mapd_coupling.__file__)"
   ~/.venvs/rl/bin/python -m pytest -q
   ~/.venvs/rl/bin/python -m black --check src tests examples
   ~/.venvs/rl/bin/python -m flake8 src tests examples
   ~/.venvs/rl/bin/python -m mypy src
   grep -rn 'eq:' <files you touched>   # should return nothing new
   git push -u origin <branch>
   ```
3. The single command that shows each new test failing without the fix (which line to revert, then one `pytest`
   command).
4. What you ran (golden comparison, scratch scripts) and the result. Say plainly what you did not run.
5. Every choice you made that the plan did not fix, and every place the plan did not match the code.
6. A drafted PR title and description following `../slap-mapd-coupling/.claude/skills/pr-description/SKILL.md`,
   with test results marked "to be filled in by the author".
