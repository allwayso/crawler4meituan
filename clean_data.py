"""Clean restaurants workflow run test data.

Input : D:\\crawler\\data\\restaurants_workflow_run_test.json
Output: JSONL saved into D:\\crawler\\data\\

Rules:
  1) remove field y_min
  2) remove field is_main_dish
  3) drop restaurants whose menu is empty
  4) save as JSONL (one JSON object per line)
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, Iterable, Tuple


DEFAULT_INPUT = r"D:\\crawler\\data\\restaurants_workflow_run_test.json"


def iter_jsonl_like(path: str) -> Iterable[Dict[str, Any]]:
    """Iterate a file that contains one JSON object per line."""

    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Failed to parse JSON on line {line_no} of {path}: {e}"
                ) from e
            if not isinstance(obj, dict):
                raise ValueError(
                    f"Expected a JSON object per line, got {type(obj)} on line {line_no}"
                )
            yield obj


def clean_record(obj: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """Return (keep, cleaned_record)."""

    menu = obj.get("menu")
    if not menu:  # drop if [] / None / empty string / missing
        return False, obj

    # remove specified fields
    obj.pop("y_min", None)
    obj.pop("is_main_dish", None)

    # if there exist alternative keys, remove them as well (defensive)
    obj.pop("y min", None)
    obj.pop("is main dish", None)

    return True, obj


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Output JSONL file path. If not provided, will be auto-generated as "
            "restaurants_workflow_run_test_clean_<city>.jsonl under the input folder."
        ),
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(args.input)

    out_f = None
    out_path = None

    kept = 0
    dropped = 0

    city_expected = None

    # Stream parse so we can decide output filename based on city (first record)
    with open(args.input, "r", encoding="utf-8") as in_f:
        for line_no, line in enumerate(in_f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Failed to parse JSON on line {line_no} of {args.input}: {e}"
                ) from e
            if not isinstance(obj, dict):
                raise ValueError(
                    f"Expected a JSON object per line, got {type(obj)} on line {line_no}"
                )

            # Determine/validate city
            city = obj.get("city")
            if city_expected is None:
                city_expected = city
            else:
                if city != city_expected:
                    raise ValueError(
                        "Input JSON contains multiple city values; please split the file before cleaning. "
                        f"Got city={city} expected={city_expected} (line {line_no})."
                    )

            # Lazily create output file after we know city
            if out_f is None:
                if args.output:
                    out_path = args.output
                else:
                    in_dir = os.path.dirname(args.input)
                    out_path = os.path.join(
                        in_dir,
                        f"restaurants_workflow_run_test_clean_{city_expected}.jsonl",
                    )
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                out_f = open(out_path, "w", encoding="utf-8")

            ok, cleaned = clean_record(obj)
            if not ok:
                dropped += 1
                continue
            kept += 1
            out_f.write(json.dumps(cleaned, ensure_ascii=False) + "\n")

    if out_f is not None:
        out_f.close()

    print(f"Done. kept={kept}, dropped_empty_menu={dropped}")
    if out_path:
        print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
