Thesis changes of 2026-10-20 ([A49] to [A51], logged in thesis-progress/decisions/GAPS.md) leave four places where the code on main (689a80b) no longer matches the thesis. The thesis text is not yet committed to Overleaf, so line numbers are from the working copy. One fix PR, measures.

Group: measures (after [A49] to [A51])

    drift: The keep-up check still has two parts, share finished >= f_up and backlog slope chi_T <= chi_max. [A49] drops the slope, so a run keeps up when throughput is at least f_up times the release rate, Lambda_T >= f_up (|C_T| + B_T) / T. Code evaluation/evaluator.py:171-193, 242, 345-346, evaluation/metrics.py:95-98, core/experiment_config.py:78-81 ↔ 2.Introduction.tex:1155 (eq:throughput). The stall count stays.
    drift: The result averages service time over every completed task, put-aways included. [A50] makes the result the mean service time of picks only, with the mean service time of put-aways reported next to it. Code evaluation/evaluator.py:255-268 ↔ 2.Introduction.tex:1180 (eq:meanservice).
    drift: The put-away distance is still computed and scored (mean_putaway_distance). [A50] removes it, since put-away time is already in the result. Code storage/arrival.py:57, 155, environment/multi_agent_env.py:218, 599, evaluation/evaluator.py:306, evaluation/metrics.py:37, 153, evaluation/comparison.py:74.
    drift: The relative gain divides by fixed storage's route time (travel plus blocked). [A51] makes it a percentage of fixed storage's mean service time, 100 * gain_n / zeta_bar_T(F_fix, pi). Code evaluation/comparison.py:183-196 ↔ 2.Introduction.tex:1311 (eq:relgain).

Open, not a code point yet: a line split over two shelves gives two picks, so the number of picks can differ between storage rules on one seed ([A50], "Open").