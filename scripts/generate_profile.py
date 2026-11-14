#!/usr/bin/env python3
"""Generate modern, self-hosted SVG profile cards for a GitHub README.

No third-party SVG renderer or Python packages required. The workflow supplies
GITHUB_REPOSITORY_OWNER and GITHUB_TOKEN to use public GitHub profile data.
"""
import datetime as dt
import html
import json
import os
from pathlib import Path
import textwrap
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER", "").strip()
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()

BACKGROUND = "#161B22"
SURFACE = "#1D2430"
BORDER = "#303847"
TEXT = "#F0F3F8"
MUTED = "#94A3B8"
SUBTLE = "#75849B"
ACCENT = "#FF638B"
SOFT = "#FFC0D0"

# Descriptions and classifications are authored metadata, not GitHub statistics.
PROJECTS = [
    ("Constella", "A multifunction utility framework for Roblox development.", "FRAMEWORK", "Roblox development"),
    ("Skele", "A desktop workspace for notes, projects, and organization.", "DESKTOP APP", "Productivity"),
    ("Retra", "A game library and emulator-focused application project.", "GAME LIBRARY", "Desktop software"),
    ("Framewarp", "A Figma-to-Roblox Studio workflow and UI tooling project.", "DESIGN TOOL", "UI workflow"),
]


def esc(obj):
    return html.escape(str(obj), quote=True)


def txt(x, y, val, size=13, color=TEXT, weight=400, *, anchor="start", spacing=None):
    letter_spacing = f' letter-spacing="{spacing}"' if spacing is not None else ""
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}"{letter_spacing} '
            f'font-family="Segoe UI, Inter, Arial, sans-serif">{esc(val)}</text>')


def bg(w, h, suffix):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">',
        '<defs>',
        f'<linearGradient id="panel-{suffix}" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0%" stop-color="{SURFACE}"/><stop offset="100%" stop-color="{BACKGROUND}"/>',
        '</linearGradient>',
        f'<linearGradient id="accent-{suffix}" x1="0" y1="0" x2="1" y2="0">',
        f'<stop offset="0%" stop-color="{ACCENT}"/><stop offset="100%" stop-color="#C76DAF"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect x="0.75" y="0.75" width="{w-1.5}" height="{h-1.5}" rx="15" '
        f'fill="url(#panel-{suffix})" stroke="{BORDER}" stroke-width="1.5"/>',
    ]


def save(path, svg):
    out = ASSETS / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print("Generated", out.relative_to(ROOT))


def api(path=None, *, graphql_data=None):
    if graphql_data is not None:
        request = urllib.request.Request(
            "https://api.github.com/graphql", data=json.dumps(graphql_data).encode("utf8"), method="POST"
        )
        request.add_header("Content-Type", "application/json")
    else:
        request = urllib.request.Request("https://api.github.com" + path)
    request.add_header("User-Agent", "Zense-Profile-Readme")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    if TOKEN:
        request.add_header("Authorization", "Bearer " + TOKEN)
    with urllib.request.urlopen(request, timeout=25) as result:
        return json.load(result)


def lines(description, width=41, limit=3):
    wrapped = textwrap.wrap(description, width, break_long_words=False, break_on_hyphens=False)
    if len(wrapped) > limit:
        wrapped = wrapped[:limit]
        wrapped[-1] = wrapped[-1].rstrip(" .") + "…"
    return wrapped


def project_svg(name, description, kind, scope, index, repo=None):
    w, h = 365, 194
    s = bg(w, h, f"project-{index}")
    # Minimal accent and a lightweight corner icon.
    s += [
        f'<rect x="22" y="20" width="4" height="12" rx="2" fill="{ACCENT}"/>',
        txt(36, 30, f"FEATURED PROJECT  /  {index:02d}", 10, MUTED, 600, spacing=1.2),
        f'<rect x="311" y="19" width="33" height="33" rx="9" fill="#262E3D"/>',
        '<path d="M323 38 L333 28 M326 28 H333 V35" fill="none" '
        f'stroke="{SOFT}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
        txt(22, 68, name, 22, TEXT, 700),
    ]
    summary = (repo or {}).get("description") or description
    for line_no, line in enumerate(lines(summary, 44, 3)):
        s.append(txt(22, 94 + 18 * line_no, line, 12.2, "#C4CEDD"))
    s.append(f'<path d="M22 147 H343" stroke="{BORDER}" stroke-width="1"/>')
    pill_width = 33 + len(kind) * 6.9
    s += [
        f'<rect x="22" y="158" width="{pill_width:.0f}" height="24" rx="7" fill="#2B2738"/>',
        txt(33, 174, kind, 10, SOFT, 700, spacing=0.55),
    ]
    if repo:
        # GitHub API values are real; stars and forks are not shown before sync.
        lang = repo.get("language") or "Repository"
        stars = int(repo.get("stargazers_count", 0))
        forks = int(repo.get("forks_count", 0))
        s.append(txt(343, 174, f"★ {stars:,}   ⑂ {forks:,}", 11.5, MUTED, 500, anchor="end"))
        s.append(txt(343, 189, lang, 9, SUBTLE, anchor="end"))
    else:
        s.append(txt(343, 173, scope, 11, MUTED, 500, anchor="end"))
    s.append("</svg>")
    return "\n".join(s)


def stats_svg(data=None):
    w, h = 748, 207
    s = bg(w, h, "stats")
    s += [
        txt(23, 34, "GitHub overview", 20, TEXT, 700),
        f'<circle cx="{w-160}" cy="28" r="4.5" fill="{ACCENT if data else SUBTLE}"/>',
        txt(w-24, 32, "LIVE PROFILE DATA" if data else "AWAITING FIRST SYNC", 10, MUTED, 600, anchor="end", spacing=0.8),
        f'<path d="M23 53 H725" stroke="{BORDER}" stroke-width="1"/>',
    ]
    fields = [
        ("REPOSITORIES", (data or {}).get("public_repos")),
        ("TOTAL STARS", (data or {}).get("stars")),
        ("FOLLOWERS", (data or {}).get("followers")),
        ("CONTRIBUTIONS", (data or {}).get("contributions")),
    ]
    for i, (caption, value) in enumerate(fields):
        x = 22 + 180 * i
        s += [
            f'<rect x="{x}" y="71" width="166" height="104" rx="11" fill="#242D3B"/>',
            f'<rect x="{x+14}" y="88" width="21" height="3" rx="1.5" fill="{ACCENT}" opacity="0.85"/>',
            txt(x+14, 109, caption, 9.6, MUTED, 700, spacing=0.5),
            txt(x+14, 152, f"{value:,}" if value is not None else "—", 31, TEXT, 700),
        ]
    caption = ("Updated automatically from your public GitHub account" if data else
               "Metrics appear after the included GitHub Actions workflow runs")
    s.append(txt(23, 194, caption, 10.5, MUTED))
    s.append("</svg>")
    return "\n".join(s)


def activity_svg(days=None, *, today=None):
    w, h = 748, 253
    s = bg(w, h, "activity")
    current = today or dt.datetime.now(dt.timezone.utc).date()
    monday = current - dt.timedelta(days=current.weekday())
    start = monday - dt.timedelta(weeks=51)
    s += [
        txt(23, 34, "Contribution activity", 20, TEXT, 700),
        txt(w-23, 33, "PAST 52 WEEKS", 10, MUTED, 700, anchor="end", spacing=1),
        f'<path d="M23 53 H725" stroke="{BORDER}" stroke-width="1"/>',
        txt(23, 77, "Daily contributions" if days is not None else
            "Your contribution calendar appears after the first sync", 11, MUTED),
    ]
    colors = ["#293342", "#683D58", "#9F476A", "#CE5279", "#FF638B"]
    x0, y0, step, cell = 48, 95, 12.5, 9.5
    for d, label in [(0, "M"), (2, "W"), (4, "F")]:
        s.append(txt(25, y0 + d * step + 8, label, 10, SUBTLE, 500))
    month_labels = set()
    for week in range(52):
        first_day = start + dt.timedelta(days=week*7)
        month_token = (first_day.year, first_day.month)
        if first_day.day <= 7 and month_token not in month_labels:
            month_labels.add(month_token)
            s.append(txt(round(x0+week*step, 1), 207, first_day.strftime("%b"), 10, MUTED))
        for day_idx in range(7):
            day = first_day + dt.timedelta(days=day_idx)
            value = int((days or {}).get(day.isoformat(), 0))
            level = 0 if value == 0 else (1 if value < 3 else 2 if value < 6 else 3 if value < 10 else 4)
            fill = colors[level] if days is not None else "#293342"
            x = round(x0 + week * step, 1)
            y = round(y0 + day_idx * step, 1)
            s.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                     f'rx="2.2" fill="{fill}"/>')
    s.append(f'<path d="M23 221 H725" stroke="{BORDER}" stroke-width="1"/>')
    s.append(txt(23, 240, f"{start:%b %Y} – {current:%b %Y}", 10, MUTED))
    s.append(txt(558, 240, "Less", 10, MUTED))
    for i, color in enumerate(colors):
        s.append(f'<rect x="{588+14*i}" y="230" width="10" height="10" rx="2" fill="{color}"/>')
    s.append(txt(677, 240, "More", 10, MUTED))
    s.append("</svg>")
    return "\n".join(s)


def load_data():
    if not OWNER:
        print("No GitHub owner configured; generating placeholders with no fabricated data.")
        return None, {}, None
    owner_path = urllib.parse.quote(OWNER)
    user = api(f"/users/{owner_path}")
    repos = []
    for page in range(1, 11):
        batch = api(f"/users/{owner_path}/repos?type=owner&per_page=100&page={page}")
        if not isinstance(batch, list):
            raise ValueError("GitHub returned an unexpected repository list")
        repos.extend(batch)
        if len(batch) < 100:
            break
    data = {
        "public_repos": user.get("public_repos"),
        "followers": user.get("followers"),
        "stars": sum(int(repo.get("stargazers_count") or 0) for repo in repos),
        "contributions": None,
    }
    days = None
    try:
        result = api(graphql_data={
            "query": "query($user:String!){ user(login:$user){ contributionsCollection{ contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } } } }",
            "variables": {"user": OWNER},
        })
        calendar = result["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        data["contributions"] = int(calendar["totalContributions"])
        days = {day["date"]: int(day["contributionCount"])
                for week in calendar["weeks"] for day in week["contributionDays"]}
    except Exception as exc:
        print("Contributions API unavailable; graph will not claim fabricated activity:", exc)
    by_name = {repo["name"].lower(): repo for repo in repos}
    return data, by_name, days


def main():
    try:
        data, repos, days = load_data()
    except Exception as exc:
        print("GitHub API failed; keeping existing generated assets:", exc)
        raise SystemExit(1)
    for index, (name, desc, kind, scope) in enumerate(PROJECTS, start=1):
        save(f"cards/{name.lower()}.svg", project_svg(name, desc, kind, scope, index, repos.get(name.lower())))
    save("stats.svg", stats_svg(data))
    save("activity.svg", activity_svg(days))


if __name__ == "__main__":
    main()
