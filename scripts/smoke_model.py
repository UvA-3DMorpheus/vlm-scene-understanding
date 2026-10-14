"""Send one image and one question through a named model, print the answer.

    python scripts/smoke_model.py --model dummy
    python scripts/smoke_model.py --model qwen3vl-8b --image data/smoke/metal_01.jpg \
        --prompt "What material is this object made of? Answer with JSON: {\"material\": ...}"
    python scripts/smoke_model.py --model qwen3vl-8b --schema material --no-cache

Consumes: a model config name, an image (default: the first smoke set image), a prompt and
an optional answer schema (material, properties, comparative, scene). Produces: the model
text, latency, token usage, cache status and, with a schema, the parse result. Exit code
1 if the answer does not parse.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from vsu.data.smoke import load_smoke_set
from vsu.models.registry import build_model, list_models
from vsu.schemas import ComparativeAnswer, MaterialAnswer, PropertiesAnswer, SceneInitAnswer
from vsu.settings import get_settings
from vsu.utils.parsing import parse_answer

SCHEMAS = {
    "material": MaterialAnswer,
    "properties": PropertiesAnswer,
    "comparative": ComparativeAnswer,
    "scene": SceneInitAnswer,
}
DEFAULT_PROMPT = (
    "What material is the main object in this image made of? Choose one of: ceramic, metal, "
    "plastic, cardboard, book_paper_cover, rubber, wood, glass, foam. Answer with a JSON "
    'object {"material": "<label>", "confidence": <0 to 1>} and nothing else.'
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--model", default="dummy", help=f"one of {list_models()}")
    parser.add_argument("--image", type=Path, default=None, help="default: first smoke image")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--schema", choices=sorted(SCHEMAS), default="material")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING, format="%(message)s"
    )

    settings = get_settings()
    image = args.image or load_smoke_set(settings=settings)[0].path
    schema = SCHEMAS[args.schema]
    decoding = {} if args.max_tokens is None else {"max_tokens": args.max_tokens}
    with build_model(args.model, settings=settings, use_cache=not args.no_cache) as model:
        response = model.generate([image], args.prompt, schema=schema, **decoding)
    print(f"model      {response.model_id} ({response.backend_model})")
    print(f"image      {image}")
    usage = response.usage
    print(f"latency    {response.latency_s:.2f}s  cached={response.cached}")
    print(f"finish     {response.finish_reason}")
    print(f"tokens     prompt={usage.prompt_tokens} completion={usage.completion_tokens}")
    print(f"extra      {response.extra}")
    print("--- text ---")
    print(response.text)
    print("--- parse ---")
    parsed = parse_answer(response.text, schema, "smoke", bare_label_field="material")
    print("ok" if parsed.ok else f"FAILED: {parsed.error}")
    if parsed.ok:
        print(parsed.answer.model_dump_json(indent=1) if parsed.answer else "")
    return 0 if parsed.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
