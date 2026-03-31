"""Small logging helper for crawler.

Goal: minimize terminal IO by default while still printing errors.

Control:
- Set env var CRAWLER_DEBUG=1 to enable DEBUG logs.
"""

from __future__ import annotations

import logging
import os
from typing import Optional


_configured = False


def _configure_logging() -> None:
    global _configured
    if _configured:
        return

    level = logging.DEBUG if os.environ.get("CRAWLER_DEBUG", "0") not in ("0", "false", "False", "") else logging.INFO

    # Keep it simple: single stream handler.
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(name)s: %(message)s",
    )
    _configured = True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    _configure_logging()
    return logging.getLogger(name or "crawler")
