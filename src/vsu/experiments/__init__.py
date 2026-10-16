"""Experiments: build_questions / run / score / report pipelines of files."""

from vsu.experiments.base import (
    Experiment,
    ExperimentConfig,
    Question,
    RawRecord,
    RunDir,
    ScoredRecord,
    load_experiment_config,
)
from vsu.experiments.material import (
    MatchingExperiment,
    MaterialExperiment,
    VerificationExperiment,
)

#: experiment name -> class. Register new experiments here.
EXPERIMENTS: dict[str, type[Experiment]] = {
    MaterialExperiment.name: MaterialExperiment,
    VerificationExperiment.name: VerificationExperiment,
    MatchingExperiment.name: MatchingExperiment,
}


def get_experiment(name: str) -> type[Experiment]:
    try:
        return EXPERIMENTS[name]
    except KeyError as exc:
        raise KeyError(f"unknown experiment {name!r}; known: {sorted(EXPERIMENTS)}") from exc


__all__ = [
    "EXPERIMENTS",
    "Experiment",
    "ExperimentConfig",
    "Question",
    "RawRecord",
    "RunDir",
    "MatchingExperiment",
    "MaterialExperiment",
    "ScoredRecord",
    "VerificationExperiment",
    "get_experiment",
    "load_experiment_config",
]
