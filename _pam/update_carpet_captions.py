#!/usr/bin/env python3
"""Update public carpet-page copy without changing saved simulation data."""
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
COPY_PATH = Path(__file__).with_name("copy-carpet.json")
PAGES = (
    ROOT / "simulations" / "carpet-pam-lambda1-startupframes.html",
    ROOT / "simulations" / "carpet-pam-low-noise-startupframes.html",
)
COPY_SCRIPT = re.compile(
    r'(<script type="application/json" id="sc-copy">)(.*?)(</script>)', re.S
)
TRAJECTORY_SCRIPT = re.compile(
    r'<script type="application/json" id="sc-trajectory">(.*?)</script>', re.S
)


def update(page: Path, copy: dict) -> None:
    html = page.read_text()
    trajectory = TRAJECTORY_SCRIPT.search(html)
    match = COPY_SCRIPT.search(html)
    if trajectory is None or match is None:
        raise ValueError(f"No embedded carpet viewer data found in {page}")
    trajectory_before = trajectory.group(1)
    replacement = json.dumps(copy, ensure_ascii=False, separators=(",", ":"))
    updated = html[:match.start(2)] + replacement + html[match.end(2):]
    trajectory_after = TRAJECTORY_SCRIPT.search(updated)
    if trajectory_after is None or trajectory_after.group(1) != trajectory_before:
        raise AssertionError(f"Updating copy changed simulation data in {page}")
    page.write_text(updated)
    print(f"Updated {page.relative_to(ROOT)}; trajectory payload unchanged")


def main() -> None:
    copy = json.loads(COPY_PATH.read_text())
    for page in PAGES:
        update(page, copy)


if __name__ == "__main__":
    main()
