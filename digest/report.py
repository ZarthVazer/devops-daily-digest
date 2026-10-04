"""Turns collected data into a Markdown report."""

from datetime import date


def diff_versions(previous: dict, current: dict) -> list[str]:
    """Names of tools whose latest version changed since the previous run."""
    changed = []
    for name, info in current.items():
        if info and previous.get(name) and previous[name].get("tag") != info.get("tag"):
            changed.append(name)
    return sorted(changed)


def render(day: date, releases: dict, changed: list[str], advisories: dict) -> str:
    lines = [f"# DevOps digest — {day.isoformat()}", ""]

    lines += ["## New releases since last run", ""]
    if changed:
        for name in changed:
            r = releases[name]
            lines.append(f"- **{name}** → [{r['tag']}]({r['url']})")
    else:
        lines.append("_No new releases._")
    lines.append("")

    lines += ["## Current versions", "", "| Tool | Version | Released |", "|---|---|---|"]
    for name in sorted(releases):
        r = releases[name]
        if r:
            published = (r.get("published_at") or "")[:10]
            lines.append(f"| {name} | [{r['tag']}]({r['url']}) | {published} |")
        else:
            lines.append(f"| {name} | n/a | |")
    lines.append("")

    lines += ["## Recent high/critical security advisories", ""]
    any_adv = False
    for ecosystem, items in advisories.items():
        if not items:
            continue
        any_adv = True
        lines += [f"### {ecosystem}", ""]
        for a in items:
            pkgs = ", ".join(a["packages"]) or "—"
            summary = a["summary"].replace("|", "\\|")
            lines.append(f"- [{a['id']}]({a['url']}) `{a['severity']}` **{pkgs}**: {summary}")
        lines.append("")
    if not any_adv:
        lines += ["_No advisories fetched._", ""]

    return "\n".join(lines)
