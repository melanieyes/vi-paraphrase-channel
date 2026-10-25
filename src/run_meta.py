"""Config hash, git commit, cost estimate. Read on the laptop, stamped on every record."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_cfg() -> dict[str, Any]:
    return yaml.safe_load((ROOT / "configs" / "study.yaml").read_text())


def config_hash(cfg: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()[:12]


def git_commit() -> str:
    try:
        sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                                      text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--porcelain", "--", "src", "scripts", "configs"],
                                        cwd=ROOT, text=True).strip()
        return sha + ("-dirty" if dirty else "")
    except Exception:  # noqa: BLE001
        return "no-commit"


def estimate_episode_cost(cfg: dict[str, Any], n: int) -> float:
    c = cfg["cost"]
    pin, pout = c["prices_per_mtok"][cfg["agent"]["model"]]
    return (c["est_input_tokens_per_episode"] * pin
            + c["est_output_tokens_per_episode"] * pout) * n / 1e6
