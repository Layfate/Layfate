#!/usr/bin/env python3
"""Generate self-hosted GitHub profile SVG cards without third-party image services.

Requires only Python's standard library. In GitHub Actions GITHUB_TOKEN and
GITHUB_REPOSITORY_OWNER are provided by the workflow.
"""
import datetime as dt
import html
import json
import os
from pathlib import Path
import textwrap
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
OWNER = os.environ.get('GITHUB_REPOSITORY_OWNER', '').strip()
TOKEN = os.environ.get('GITHUB_TOKEN', '').strip()
PINK, BACK, MUTED, LIGHT, BORDER = '#F75C7E', '#1F222E', '#9EA8BA', '#E9EDF5', '#363B4A'
PROJECTS = [
    ('Constella', 'A multifunction utility framework for Roblox development.'),
    ('Skele', 'A desktop workspace for notes, projects, and organization.'),
    ('Retra', 'A game library and emulator-focused application project.'),
    ('Framewarp', 'A Figma-to-Roblox Studio workflow and UI tooling project.'),
]


def esc(value):
    return html.escape(str(value), quote=True)


def api(endpoint, *, graphql_data=None):
    if graphql_data is not None:
        body = json.dumps(graphql_data).encode('utf-8')
        req = urllib.request.Request('https://api.github.com/graphql', body, method='POST')
        req.add_header('Content-Type', 'application/json')
    else:
        req = urllib.request.Request(f'https://api.github.com{endpoint}')
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('User-Agent', 'Zense-GitHub-README')
    req.add_header('X-GitHub-Api-Version', '2022-11-28')
    if TOKEN:
        req.add_header('Authorization', f'Bearer {TOKEN}')
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.load(response)


def save(name, data):
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding='utf-8')
    print('Generated', path.relative_to(ROOT))


def svg_head(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">'
            '<rect width="100%" height="100%" rx="10" fill="#1F222E" />'
            '<rect x=".5" y=".5" width="99.9%" height="99%" rx="10" '
            'fill="none" stroke="#363B4A" stroke-width="1" />')


def text(x, y, label, size=12, color=LIGHT, weight='normal', anchor='start'):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" '
            f'font-family="Segoe UI, Arial, sans-serif">{esc(label)}</text>')


def split_lines(sentence, max_chars=40, limit=3):
    parts = textwrap.wrap(sentence or '', width=max_chars, break_long_words=False, break_on_hyphens=False)
    if len(parts) > limit:
        parts = parts[:limit]
        parts[-1] = parts[-1].rstrip(' .') + '…'
    return parts


def project_svg(name, description, repo=None):
    s = [svg_head(278, 145), text(18, 29, name, 16, PINK, 'bold')]
    summary = (repo or {}).get('description') or description
    for i, ln in enumerate(split_lines(summary, 37, 3)):
        s.append(text(18, 55 + i * 17, ln, 11, LIGHT))
    if repo:
        lang = repo.get('language') or 'Repository'
        stars, forks = repo.get('stargazers_count', 0), repo.get('forks_count', 0)
        s.extend([
            '<circle cx="23" cy="125" r="5" fill="#6B86C9"/>',
            text(35, 129, lang, 10),
            text(159, 129, f'★ {stars:,}', 11, '#F8D866'),
            text(221, 129, f'⑂ {forks:,}', 10, '#F8D866'),
        ])
    else:
        s.append(text(18, 129, 'Repository data appears after sync', 10, MUTED))
    s.append('</svg>')
    return '\n'.join(s)


def stats_svg(data=None):
    if data:
        fields = [
            ('PUBLIC REPOSITORIES', data.get('public_repos')),
            ('TOTAL STARS', data.get('stars')),
            ('FOLLOWERS', data.get('followers')),
            ('CONTRIBUTIONS (YEAR)', data.get('contributions')),
        ]
    else:
        fields = [(k, None) for k in ['PUBLIC REPOSITORIES', 'TOTAL STARS', 'FOLLOWERS', 'CONTRIBUTIONS (YEAR)']]
    s = [svg_head(850, 177), text(23, 31, 'GitHub Profile Stats', 20, PINK, 'bold')]
    for i, (name, value) in enumerate(fields):
        x = 26 + 212 * i
        s.append(f'<rect x="{x}" y="51" width="192" height="99" rx="7" fill="#272D3B"/>')
        s.append(text(x + 13, 77, name, 10, MUTED, 'bold'))
        s.append(text(x + 13, 122, f'{value:,}' if value is not None else '—', 33, LIGHT, 'bold'))
    if not data:
        s.append(text(26, 168, 'Run the included GitHub Actions workflow to show your real stats.', 10, MUTED))
    s.append('</svg>')
    return '\n'.join(s)


def activity_svg(days=None):
    width, height = 850, 197
    s = [svg_head(width, height), text(22, 31, 'Contribution Activity', 20, PINK, 'bold')]
    # 52 weeks, aligned Monday to Sunday, ending this week.
    today = dt.datetime.now(dt.timezone.utc).date()
    end_week_monday = today - dt.timedelta(days=today.weekday())
    start = end_week_monday - dt.timedelta(weeks=51)
    levels = ['#303646', '#6E374F', '#A63D61', '#D74B74', '#F75C7E']
    if days is None:
        s.append(text(22, 58, 'Your contribution calendar will appear after the workflow runs.', 12, MUTED))
    else:
        s.append(text(22, 58, 'Actual daily contributions from your GitHub account', 12, MUTED))
    ox, oy, box, space = 25, 72, 10, 4
    for w in range(52):
        for d in range(7):
            day = start + dt.timedelta(days=w * 7 + d)
            value = (days or {}).get(day.isoformat(), 0)
            level = 0 if value == 0 else (1 if value < 3 else 2 if value < 6 else 3 if value < 10 else 4)
            # Initial placeholder is a neutral, intentionally blank heat map.
            fill = levels[level] if days is not None else '#303646'
            s.append(f'<rect x="{ox+w*(box+space)}" y="{oy+d*(box+space)}" '
                     f'width="{box}" height="{box}" rx="2" fill="{fill}"/>')
    s.append(text(25, 188, f'{start:%b %Y}', 11, MUTED))
    s.append(text(752, 188, f'{today:%b %Y}', 11, MUTED))
    s.append('</svg>')
    return '\n'.join(s)


def load_data():
    if not OWNER:
        print('No GITHUB_REPOSITORY_OWNER. Using honest placeholders.')
        return None, {}, None
    account = api('/users/' + urllib.parse.quote(OWNER))
    repos = []
    for page in range(1, 11):
        batch = api(f'/users/{urllib.parse.quote(OWNER)}/repos?type=owner&per_page=100&page={page}')
        if not isinstance(batch, list):
            raise ValueError('Repository API did not return a list')
        repos.extend(batch)
        if len(batch) < 100:
            break
    # Includes owned public repositories returned by REST.
    data = {
        'public_repos': account.get('public_repos'),
        'followers': account.get('followers'),
        'stars': sum(int(r.get('stargazers_count', 0)) for r in repos),
        'contributions': None,
    }
    days = None
    try:
        result = api('', graphql_data={
            'query': 'query($user:String!){ user(login:$user){ contributionsCollection{ contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } } } }',
            'variables': {'user': OWNER},
        })
        calendar = result['data']['user']['contributionsCollection']['contributionCalendar']
        data['contributions'] = calendar['totalContributions']
        days = {day['date']: day['contributionCount'] for week in calendar['weeks'] for day in week['contributionDays']}
    except Exception as exc:
        print('Contribution API unavailable; leaving the calendar blank:', exc)
    names = {r['name'].lower(): r for r in repos}
    return data, names, days


def main():
    try:
        data, repos, days = load_data()
    except Exception as exc:
        print('GitHub API fetch failed. Keeping any existing assets:', exc)
        raise SystemExit(1)
    for name, description in PROJECTS:
        save(f'cards/{name.lower()}.svg', project_svg(name, description, repos.get(name.lower())))
    save('stats.svg', stats_svg(data))
    save('activity.svg', activity_svg(days))


if __name__ == '__main__':
    main()
