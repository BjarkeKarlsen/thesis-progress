"""
Reproducible thesis figures for the Problem Formulation chapter.

Run:  python figure.py
Out:  ../Images/instance.png ... ../Images/concentration.png
      (../Images is what both problem_formulation*.tex already point at
      via \\graphicspath{{\\subfix{../Images/}}} -- keep OUT in sync with that,
      not the other way around; see base.py)

Only matplotlib + networkx are required. Every figure is a *schematic*:
positions are hand-set so the same figure is produced on every run.

Each figure lives in its own fig_*.py module, built on the shared warehouse
graph / colours / draw helpers in base.py.
"""
import os

from base import OUT
from instance import instance
from instance_simple import instance_simple
from observation import observation
from loop import loop
from lifecycle import lifecycle
from conflicts import conflicts
from concentration import concentration
from congestion import congestion
from wellformed import wellformed

# Simple companions (tiny graphs, isolate one mechanic each) -- additive,
# nothing above this line is touched.
from instance_mini import instance_mini
from observation_mini import observation_mini
from congestion_mini import congestion_mini
from resolution_simple import resolution_simple
from methodloop_simple import methodloop_simple
from assignment_masking import assignment_masking
from architecture_simple import architecture_simple
from potential_example import potential_example

# thesis-guide-images.md worked examples -- additive, nothing above this
# line is touched.
from graph_basics import graph_basics
from actions_example import actions_example
from storage_matrix import storage_matrix
from storage_update_example import storage_update_example

from controllers_example import controllers_example
from posg_schematic import posg_schematic
from two_layer_feedback import two_layer_feedback
from scoring_run import scoring_run
from decision_problem_grid import decision_problem_grid
from timeline import timeline

if __name__ == "__main__":
    instance(); instance_simple(); observation(); loop()
    lifecycle(); conflicts(); concentration()
    congestion(); wellformed()
    instance_mini(); observation_mini(); congestion_mini()
    resolution_simple(); methodloop_simple(); assignment_masking()
    architecture_simple()
    potential_example()
    graph_basics(); actions_example(); storage_matrix()
    storage_update_example(); controllers_example(); posg_schematic()
    two_layer_feedback(); scoring_run(); decision_problem_grid()
    timeline()
    print("wrote figures to", os.path.abspath(OUT))
