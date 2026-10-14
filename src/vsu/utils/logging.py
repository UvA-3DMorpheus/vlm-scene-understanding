"""Uniform logging: one format, optional log file per run, quiet third party loggers."""

from __future__ import annotations

import logging
from pathlib import Path

FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def setup_logging(level: int = logging.INFO, logfile: Path | None = None) -> None:
    """Configure the root logger once; a later call only adds the file handler."""
    root = logging.getLogger()
    if not root.handlers:
        logging.basicConfig(level=level, format=FORMAT, datefmt="%H:%M:%S")
    root.setLevel(level)
    if logfile is not None:
        logfile = Path(logfile)
        logfile.parent.mkdir(parents=True, exist_ok=True)
        if not any(
            isinstance(h, logging.FileHandler) and Path(h.baseFilename) == logfile
            for h in root.handlers
        ):
            handler = logging.FileHandler(logfile)
            handler.setFormatter(logging.Formatter(FORMAT, datefmt="%H:%M:%S"))
            root.addHandler(handler)
    for noisy in ("httpx", "urllib3", "PIL", "transformers", "huggingface_hub"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
