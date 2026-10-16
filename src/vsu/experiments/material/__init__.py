"""Experiment 1: material recognition, in three forms on the same objects and views.

- :mod:`.items`: the labelled objects and their views, shared by all three experiments.
- :mod:`.identify`: 1.0, name the material (``exp1``).
- :mod:`.verify`: 1.1, confirm a named material, yes/no or two options (``exp1_1``).
- :mod:`.match`: 1.2, tell two objects of different materials apart (``exp1_2``).
- :mod:`.consistency`: each model's 1.1 and 1.2 answers against its own 1.0 labels.
- :mod:`.tables`: the report tables and writers of all of the above.
"""

from vsu.experiments.material.identify import MaterialExperiment
from vsu.experiments.material.match import MatchingExperiment
from vsu.experiments.material.verify import VerificationExperiment

__all__ = ["MatchingExperiment", "MaterialExperiment", "VerificationExperiment"]
