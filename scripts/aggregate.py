#!/usr/bin/env python3
"""
Aggregate weight responses from GitHub Issues.

Usage:
    python aggregate.py --repo owner/repo-name [--token ghp_xxx]

Fetches all issues labeled 'weight-response', parses the structured form
data, and outputs summary statistics (mean, median, std dev per category).
"""

import argparse
import json
import re
import statistics
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError


def fetch_issues(repo: str, token: str | None = None) -> list[dict]:
    """Fetch all open+closed issues with the weight-response label."""
    issues = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/repos/{repo}/issues"
            f"?labels=weight-response&state=all&per_page=100&page={page}"
        )
        req = Request(url)
        req.add_header("Accept", "application/vnd.github.v3+json")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        try:
            with urlopen(req) as resp:
                batch = json.loads(resp.read())
        except HTTPError as e:
            print(f"Error fetching issues: {e.code} {e.reason}", file=sys.stderr)
            sys.exit(1)
        if not batch:
            break
        issues.extend(batch)
        page += 1
    return issues


def parse_weight(text: str) -> float | None:
    """Extract a numeric weight from form field text."""
    match = re.search(r"(\d+(?:\.\d+)?)", text.strip())
    return float(match.group(1)) if match else None


def parse_issue_body(body: str) -> dict | None:
    """Parse the structured form response from an issue body."""
    if not body:
        return None

    response = {
        "role": None,
        "org_size": None,
        "honeypot_experience": None,
        "weights": {},
        "sub_weights": {},
        "rationale": None,
    }

    # Map form field headers to keys
    weight_fields = {
        "Cost & Resources (%)": "cost",
        "Deployment Complexity (%)": "deployment",
        "Detection Effectiveness (%)": "detection",
        "Operational Manageability (%)": "operations",
    }

    lines = body.split("\n")
    current_section = None

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Parse dropdown/input fields (### Header followed by value)
        if stripped.startswith("### "):
            current_section = stripped[4:].strip()
            continue

        if current_section and stripped and not stripped.startswith("_"):
            # Category weights
            if current_section in weight_fields:
                val = parse_weight(stripped)
                if val is not None:
                    response["weights"][weight_fields[current_section]] = val
                current_section = None

            # Demographic fields
            elif current_section == "Your primary role":
                response["role"] = stripped
                current_section = None
            elif current_section == "Organisation size (employees)":
                response["org_size"] = stripped
                current_section = None
            elif current_section == "Have you deployed or managed a honeypot?":
                response["honeypot_experience"] = stripped
                current_section = None
            elif current_section == "Rationale (optional)":
                response["rationale"] = stripped
                current_section = None

    # Validate weights sum to ~100
    w = response["weights"]
    if len(w) < 4:
        return None
    total = sum(w.values())
    if abs(total - 100) > 2:
        return None  # invalid response

    return response


def compute_stats(responses: list[dict]) -> dict:
    """Compute aggregate statistics across all valid responses."""
    categories = ["cost", "deployment", "detection", "operations"]
    stats = {}

    for cat in categories:
        values = [r["weights"][cat] for r in responses if cat in r["weights"]]
        if not values:
            continue
        stats[cat] = {
            "n": len(values),
            "mean": round(statistics.mean(values), 1),
            "median": round(statistics.median(values), 1),
            "stdev": round(statistics.stdev(values), 1) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
        }

    return stats


def print_report(stats: dict, responses: list[dict], base_weights: dict):
    """Print a formatted summary report."""
    print("=" * 65)
    print("  HONEYPOT FRAMEWORK — WEIGHT RESPONSE AGGREGATION")
    print("=" * 65)
    print(f"\n  Valid responses: {len(responses)}\n")

    # Role breakdown
    roles = {}
    for r in responses:
        role = r.get("role") or "Not specified"
        roles[role] = roles.get(role, 0) + 1
    print("  Respondent roles:")
    for role, count in sorted(roles.items(), key=lambda x: -x[1]):
        print(f"    {role}: {count}")

    print(f"\n{'─' * 65}")
    print(f"  {'Category':<28} {'Base':>6} {'Mean':>6} {'Med':>6} {'StdDev':>7} {'Range':>10}")
    print(f"{'─' * 65}")

    cat_labels = {
        "cost": "Cost & Resources",
        "deployment": "Deployment Complexity",
        "detection": "Detection Effectiveness",
        "operations": "Operational Manageability",
    }

    for cat, label in cat_labels.items():
        if cat not in stats:
            continue
        s = stats[cat]
        base = base_weights.get(cat, "?")
        delta = s["mean"] - base if isinstance(base, (int, float)) else ""
        delta_str = f" ({'+' if delta > 0 else ''}{delta:.1f})" if delta else ""
        print(
            f"  {label:<28} {base:>5}% {s['mean']:>5.1f}% {s['median']:>5.1f}% "
            f"{s['stdev']:>6.1f}  {s['min']:>4.0f}–{s['max']:<4.0f}{delta_str}"
        )

    print(f"{'─' * 65}")
    print("\n  Key findings:")

    # Compare community vs base
    for cat, label in cat_labels.items():
        if cat not in stats:
            continue
        base = base_weights.get(cat, 0)
        diff = stats[cat]["mean"] - base
        if abs(diff) >= 3:
            direction = "higher" if diff > 0 else "lower"
            print(f"    • Community rates {label} {abs(diff):.1f}pp {direction} than base")

    consensus = min(stats.values(), key=lambda s: s["stdev"])
    divergent = max(stats.values(), key=lambda s: s["stdev"])
    for cat, s in stats.items():
        if s is consensus:
            print(f"    • Strongest consensus: {cat_labels[cat]} (σ={s['stdev']})")
        if s is divergent:
            print(f"    • Most divergent: {cat_labels[cat]} (σ={s['stdev']})")

    print()


def main():
    parser = argparse.ArgumentParser(description="Aggregate framework weight responses")
    parser.add_argument("--repo", required=True, help="GitHub repo (owner/name)")
    parser.add_argument("--token", default=None, help="GitHub personal access token")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of report")
    args = parser.parse_args()

    base_weights = {"cost": 25, "deployment": 30, "detection": 25, "operations": 20}

    print(f"Fetching issues from {args.repo}...", file=sys.stderr)
    issues = fetch_issues(args.repo, args.token)
    print(f"Found {len(issues)} issues with 'weight-response' label", file=sys.stderr)

    responses = []
    for issue in issues:
        parsed = parse_issue_body(issue.get("body", ""))
        if parsed:
            parsed["issue_number"] = issue["number"]
            parsed["author"] = issue.get("user", {}).get("login", "unknown")
            responses.append(parsed)

    print(f"Parsed {len(responses)} valid responses\n", file=sys.stderr)

    if not responses:
        print("No valid responses found.", file=sys.stderr)
        sys.exit(0)

    stats = compute_stats(responses)

    if args.json:
        output = {"stats": stats, "responses": responses, "n": len(responses)}
        print(json.dumps(output, indent=2))
    else:
        print_report(stats, responses, base_weights)


if __name__ == "__main__":
    main()
