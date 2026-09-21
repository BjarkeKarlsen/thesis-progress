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

if __name__ == "__main__":
    instance(); instance_simple(); observation(); loop()
    lifecycle(); conflicts(); concentration()
    congestion(); wellformed()
    print("wrote figures to", os.path.abspath(OUT))
