"""Entry point: collect data, write the daily report and update state."""

import json
from datetime import UTC, datetime
from pathlib import Path

from digest import config, github_api, report

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "data" / "versions.json"
REPORTS_DIR = ROOT / "reports"
README = ROOT / "README.md"
MARK_START = "<!-- LATEST:START -->"
MARK_END = "<!-- LATEST:END -->"


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def update_readme(day: str, changed: list[str], report_path: Path) -> None:
    text = README.read_text()
    if MARK_START not in text:
        return
    rel = report_path.relative_to(ROOT).as_posix()
    summary = ", ".join(changed) if changed else "no new releases"
    block = f"{MARK_START}\n**{day}** — {summary}. [Full report]({rel})\n{MARK_END}"
    before, rest = text.split(MARK_START, 1)
    _, after = rest.split(MARK_END, 1)
    README.write_text(before + block + after)


def main() -> None:
    today = datetime.now(UTC).date()

    releases = {
        name: github_api.latest_release(repo) for name, repo in config.TRACKED_REPOS.items()
    }
    advisories = {
        eco: github_api.advisories(eco, config.ADVISORY_SEVERITIES, config.ADVISORY_LIMIT)
        for eco in config.ADVISORY_ECOSYSTEMS
    }

    previous = load_state()
    changed = report.diff_versions(previous, releases)

    out = REPORTS_DIR / f"{today:%Y}" / f"{today:%m}" / f"{today.isoformat()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report.render(today, releases, changed, advisories))

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    merged = {**previous, **{k: v for k, v in releases.items() if v}}
    STATE_FILE.write_text(json.dumps(merged, indent=2, sort_keys=True) + "\n")

    update_readme(today.isoformat(), changed, out)
    print(f"report written: {out.relative_to(ROOT)}; changed: {changed or 'none'}")


if __name__ == "__main__":
    main()
