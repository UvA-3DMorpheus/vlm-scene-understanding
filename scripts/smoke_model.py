"""Send one image and one question through a named model, print the answer.

Usage::

    python scripts/smoke_model.py --model dummy --image data/smoke/steel_ball.jpg \
        --prompt "What material is this ball made of?"

Consumes: a model config name, an image path and a prompt. Produces: the model text
and latency on stdout. Implemented in Step 3.
"""

from __future__ import annotations


def main() -> int:
    """Entry point. Returns a process exit code."""
    raise SystemExit("smoke_model.py is implemented in Step 3.")


if __name__ == "__main__":
    raise SystemExit(main())
