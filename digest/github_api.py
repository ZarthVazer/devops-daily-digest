"""Minimal GitHub REST API client (standard library only)."""

import json
import os
import urllib.parse
import urllib.request

API = "https://api.github.com"


def _get(path: str, params: dict | None = None):
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "devops-daily-digest",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def latest_release(repo: str) -> dict | None:
    """Return the latest stable release of a repository, or None."""
    try:
        data = _get(f"/repos/{repo}/releases/latest")
    except Exception:  # noqa: BLE001 - one failing repo must not break the digest
        return None
    return {
        "tag": data.get("tag_name"),
        "published_at": data.get("published_at"),
        "url": data.get("html_url"),
    }


def advisories(ecosystem: str, severity: str, limit: int) -> list[dict]:
    """Return recent reviewed advisories for an ecosystem."""
    try:
        data = _get(
            "/advisories",
            {
                "type": "reviewed",
                "ecosystem": ecosystem,
                "severity": severity,
                "per_page": limit,
                "sort": "published",
                "direction": "desc",
            },
        )
    except Exception:  # noqa: BLE001
        return []
    result = []
    for adv in data:
        packages = sorted(
            {v["package"]["name"] for v in adv.get("vulnerabilities") or [] if v.get("package")}
        )
        result.append(
            {
                "id": adv.get("cve_id") or adv.get("ghsa_id"),
                "severity": adv.get("severity"),
                "summary": (adv.get("summary") or "").strip(),
                "packages": packages,
                "url": adv.get("html_url"),
                "published_at": adv.get("published_at"),
            }
        )
    return result
