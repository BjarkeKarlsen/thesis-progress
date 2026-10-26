# 07. Reasons and scope to write into the thesis

**Decisions** D11 to D13 of `README.md`. No model change, only the reason for a value or a scope line. Each
goes in with the step it belongs to. Propose the sentence to the author first.

## Assignment stays oldest first (D11)

`thesis/Chapters/4.Implementation.tex`, around line 145 (the shared assignment rule). Waiting tasks are taken
oldest first, picks and put-aways alike. One clause on why put-aways get no priority of their own: it is the
simplest rule and adds no parameter.

## Δ = 100 (D12)

`thesis/Appendices/G.StorageValues.tex`, `app:cal:period`, and `B.Parameters.tex`. Δ is half the rotation
period, so the storage rule sees every change in the ranking within one period. The graph v1 sweep agrees:
the gain held up to 200 and fell at 400, where every other rotation step is missed. With step 05, Δ is also
the review period.

## β = 1 (D12)

`thesis/Appendices/G.StorageValues.tex`, `app:cal:beta`, and `B.Parameters.tex`. Both terms of
`eq:storagegreedy` count steps, so β = 1 weighs a step of expected waiting the same as a step of travel. The
graph v1 sweep shows why β did little under Token Passing: the big wait there is before assignment, while a
task is held because its shelf is taken, and no edge sees that wait.

## Outside the model (D13)

`thesis/Chapters/2.Introduction.tex`, the scope list (around line 1345, next to "No handling time"). Proposed
item: an order leaves the model at its workstation. Packing, holding an order until its last line arrives,
and the trip to the outbound dock are done by people and conveyors, and a workstation has room for every
order waiting there.

## Random storage as a check, not a reference (D17)

`thesis/Appendices/G.StorageValues.tex`, a short subsection, and one sentence where the main result is read.
Fixed storage stays the reference of the main result. Random storage runs only under Token Passing at the main
load, paired by seed, to answer whether demand storage's gain comes from knowing demand or only from spreading
stock over more slots. On graph v1 random matched demand on picks (24.8 against 24.7 at 8 agents), so the check
is needed. Random storage exists in the pilot code (`~/worktrees/pilot-learned-storage`). Check whether it is in
`slap-mapd-coupling` `main` (`src/slap_mapd_coupling/storage/registry.py`) before the reruns.
