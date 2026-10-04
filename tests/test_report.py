from datetime import date

from digest import report

RELEASES = {
    "Terraform": {"tag": "v1.10.0", "published_at": "2026-10-01T10:00:00Z", "url": "https://x/tf"},
    "Helm": {"tag": "v3.17.0", "published_at": "2026-09-20T10:00:00Z", "url": "https://x/helm"},
    "Broken": None,
}


def test_diff_detects_new_version():
    previous = {"Terraform": {"tag": "v1.9.8"}, "Helm": {"tag": "v3.17.0"}}
    assert report.diff_versions(previous, RELEASES) == ["Terraform"]


def test_diff_ignores_tools_seen_first_time():
    assert report.diff_versions({}, RELEASES) == []


def test_render_contains_sections():
    advisories = {
        "pip": [
            {
                "id": "CVE-2026-0001",
                "severity": "critical",
                "summary": "RCE in parser | bad",
                "packages": ["example"],
                "url": "https://x/adv",
                "published_at": "2026-10-04",
            }
        ]
    }
    md = report.render(date(2026, 10, 5), RELEASES, ["Terraform"], advisories)
    assert "# DevOps digest — 2026-10-05" in md
    assert "**Terraform** → [v1.10.0]" in md
    assert "| Broken | n/a | |" in md
    assert "CVE-2026-0001" in md
    assert "RCE in parser \\| bad" in md


def test_render_without_changes_or_advisories():
    md = report.render(date(2026, 10, 5), RELEASES, [], {"pip": []})
    assert "_No new releases._" in md
    assert "_No advisories fetched._" in md
