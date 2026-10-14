"""Prompt templates: ``templates/<experiment>_<variant>.jinja``, rendered with strict context.

Prompts never live in Python. A template is addressed by experiment and variant name; a
changed template is a new variant name, and every run records the template's hash so a
silent edit is visible in the run config.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
SUFFIX = ".jinja"


def template_name(experiment: str, variant: str) -> str:
    return f"{experiment}_{variant}{SUFFIX}"


def template_path(experiment: str, variant: str, templates_dir: Path = TEMPLATES_DIR) -> Path:
    path = Path(templates_dir) / template_name(experiment, variant)
    if not path.is_file():
        known = list_variants(experiment, templates_dir)
        raise FileNotFoundError(f"no template {path.name}; variants of {experiment}: {known}")
    return path


def list_variants(experiment: str, templates_dir: Path = TEMPLATES_DIR) -> list[str]:
    """Variant names that have a template for ``experiment``."""
    prefix = f"{experiment}_"
    return sorted(p.stem[len(prefix) :] for p in Path(templates_dir).glob(f"{prefix}*{SUFFIX}"))


def template_hash(experiment: str, variant: str, templates_dir: Path = TEMPLATES_DIR) -> str:
    """SHA-256 of the template file, recorded in every run config."""
    return hashlib.sha256(
        template_path(experiment, variant, templates_dir).read_bytes()
    ).hexdigest()


def render(
    experiment: str, variant: str, templates_dir: Path = TEMPLATES_DIR, **context: Any
) -> str:
    """Render a template; a missing context variable is an error, not an empty string."""
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=False,
    )
    return env.get_template(template_name(experiment, variant)).render(**context).strip()
