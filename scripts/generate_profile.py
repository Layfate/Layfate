#!/usr/bin/env python3
"""Generate cyan GitHub README SVG assets. Standard-library-only, no external renderers.

Run `python3 scripts/generate_profile.py` locally to build honest placeholder cards.
A GitHub Actions workflow runs the same script with an owner/token to add real
repository and contribution information. No fake counters are ever generated.
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
ASSETS = ROOT / 'assets'
OWNER = os.environ.get('GITHUB_REPOSITORY_OWNER', '').strip()
TOKEN = os.environ.get('GITHUB_TOKEN', '').strip()

BG = '#0D151D'
SURFACE = '#14212C'
SURFACE_2 = '#182935'
STROKE = '#2B4350'
TEXT = '#EDF7FA'
MUTED = '#9DB5C1'
FAINT = '#71929F'
ACCENT = '#22D3EE'
ACCENT_2 = '#06B6D4'
ACCENT_DIM = '#0C3543'
SOFT = '#A5F3FC'

PROJECTS = [
    ('Constella', 'A multi-purpose utility framework for Roblox development.', 'FRAMEWORK', 'Roblox / Luau'),
    ('Skele', 'A desktop workspace for notes, projects, and organization.', 'DESKTOP APP', 'Productivity'),
    ('Retra', 'An emulator-focused game library and application project.', 'GAME LIBRARY', 'Game tools'),
    ('Framewarp', 'A Figma-to-Roblox Studio UI workflow and tooling project.', 'DESIGN TOOL', 'UI workflow'),
]


def esc(value):
    return html.escape(str(value), quote=True)


def text(x, y, value, size=24, color=TEXT, weight=400, anchor='start', spacing=None):
    extra = f' letter-spacing="{spacing}"' if spacing is not None else ''
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}"{extra} font-family="Inter, Segoe UI, Arial, sans-serif">{esc(value)}</text>')


def wrap(value, width=34, limit=2):
    ls = textwrap.wrap(value or '', width, break_long_words=False, break_on_hyphens=False)
    if len(ls) > limit:
        ls = ls[:limit]
        ls[-1] = ls[-1].rstrip(' .,') + '…'
    return ls


def svg_bg(w, h, name):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">',
        '<defs>',
        f'<linearGradient id="bg-{name}" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0%" stop-color="{SURFACE_2}"/><stop offset="100%" stop-color="{BG}"/>',
        '</linearGradient>',
        f'<linearGradient id="accent-{name}" x1="0" y1="0" x2="1" y2="0">',
        f'<stop offset="0%" stop-color="{ACCENT}"/><stop offset="100%" stop-color="#67E8F9"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="url(#bg-{name})" stroke="{STROKE}" stroke-width="2"/>',
    ]


def save(path, data):
    out = ASSETS / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(data, encoding='utf-8')
    print('Generated', out.relative_to(ROOT))


def api(path='', *, query=None):
    if query is None:
        req = urllib.request.Request('https://api.github.com' + path)
    else:
        req = urllib.request.Request('https://api.github.com/graphql',
                                     data=json.dumps(query).encode('utf-8'), method='POST')
        req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Zense-Cyan-Profile-Generator')
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('X-GitHub-Api-Version', '2022-11-28')
    if TOKEN:
        req.add_header('Authorization', 'Bearer ' + TOKEN)
    with urllib.request.urlopen(req, timeout=25) as f:
        return json.load(f)


def project_svg(name, description, category, scope, index, repo=None):
    """High-resolution 470x298 asset, displayed at 232-235px width in 3-col grid."""
    w, h = 470, 298
    s = svg_bg(w, h, f'project{index}')
    s += [
        f'<rect x="26" y="32" width="6" height="18" rx="3" fill="{ACCENT}"/>',
        text(45, 47, f'PROJECT  /  {index:02d}', 18, FAINT, 700, spacing=1.5),
        f'<rect x="393" y="24" width="52" height="52" rx="14" fill="{ACCENT_DIM}" stroke="#205263"/>',
        f'<path d="M408 53 L430 34 M416 34 H430 V48" fill="none" stroke="{ACCENT}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
        text(27, 119, name, 39, ACCENT, 730),
    ]
    summary = (repo or {}).get('description') or description
    for i, l in enumerate(wrap(summary, 34, 3)):
        s.append(text(28, 160 + i * 29, l, 23, '#CEE1E9'))
    s += [f'<path d="M28 240 H442" stroke="{STROKE}" stroke-width="1.5"/>',
          f'<rect x="28" y="252" width="{min(230, 35+len(category)*13)}" height="29" rx="9" fill="{ACCENT_DIM}"/>',
          text(40, 272, category, 17, SOFT, 650, spacing=.7)]
    if repo:
        stars = int(repo.get('stargazers_count') or 0)
        forks = int(repo.get('forks_count') or 0)
        s.append(text(440, 273, f'★ {stars:,}  ·  Forks {forks:,}', 19, MUTED, 560, anchor='end'))
    else:
        s.append(text(439, 273, scope, 19, MUTED, 500, anchor='end'))
    s.append('</svg>')
    return '\n'.join(s)


def placeholder_svg(index):
    w, h = 470, 298
    s = svg_bg(w, h, f'open{index}')
    # An unfilled space is deliberately styled as a placeholder, not as a real project.
    s += [
        f'<rect x="27" y="27" width="416" height="242" rx="15" fill="none" stroke="#24505D" stroke-width="2" stroke-dasharray="7 9" opacity=".55"/>',
        text(45, 53, f'PROJECT SLOT  /  {index:02d}', 18, FAINT, 650, spacing=1.3),
        f'<circle cx="236" cy="132" r="27" fill="{ACCENT_DIM}"/>',
        f'<path d="M236 118 V146 M222 132 H250" stroke="{ACCENT}" stroke-width="3.2" stroke-linecap="round"/>',
        text(235, 202, 'Coming soon', 29, SOFT, 690, anchor='middle'),
        text(235, 231, 'Reserved for a future project', 19, MUTED, anchor='middle'),
    ]
    s.append('</svg>')
    return '\n'.join(s)


def stats_svg(data=None):
    w, h = 958, 298
    s = svg_bg(w, h, 'stats')
    s += [
        f'<circle cx="40" cy="43" r="6" fill="{ACCENT}"/>',
        text(60, 49, 'ZENSE   /   PROFILE OVERVIEW', 17, SOFT, 690, spacing=1.4),
        text(32, 100, 'GitHub at a glance', 35, TEXT, 720),
        f'<rect x="{w-239}" y="37" width="205" height="37" rx="18" fill="{ACCENT_DIM}"/>',
        text(w-136, 61, 'SYNCED DATA' if data else 'FIRST SYNC NEEDED', 15, ACCENT, 710, anchor='middle', spacing=.8),
    ]
    fields = [
        ('PUBLIC REPOS', (data or {}).get('public_repos')),
        ('TOTAL STARS', (data or {}).get('stars')),
        ('FOLLOWERS', (data or {}).get('followers')),
        ('CONTRIBUTIONS / YEAR', (data or {}).get('contributions')),
    ]
    for i, (title, value) in enumerate(fields):
        x = 33 + 227 * i
        s += [
            f'<rect x="{x}" y="124" width="210" height="125" rx="15" fill="{SURFACE_2}" stroke="{STROKE}" stroke-width="1"/>',
            f'<rect x="{x+17}" y="143" width="22" height="4" rx="2" fill="{ACCENT}"/>',
            text(x+17, 170, title, 15.8, MUTED, 700, spacing=.45),
            text(x+18, 225, f'{value:,}' if value is not None else '—', 42, SOFT if value is None else TEXT, 740),
        ]
    s.append(text(33, 281, 'Updated automatically using public GitHub data' if data else
                  'Your real numbers appear here after GitHub Actions completes the first sync.', 17, MUTED))
    s.append('</svg>')
    return '\n'.join(s)


def activity_svg(days=None, *, today=None):
    w, h = 958, 365
    s = svg_bg(w, h, 'activity')
    current = today or dt.datetime.now(dt.timezone.utc).date()
    monday = current - dt.timedelta(days=current.weekday())
    start = monday - dt.timedelta(weeks=51)
    s += [
        f'<circle cx="40" cy="43" r="6" fill="{ACCENT}"/>',
        text(60, 49, 'ZENSE   /   CONTRIBUTION TIMELINE', 17, SOFT, 690, spacing=1.4),
        text(32, 101, 'Activity over time', 35, TEXT, 720),
        f'<rect x="{w-239}" y="37" width="205" height="37" rx="18" fill="{ACCENT_DIM}"/>',
        text(w-136, 61, 'PAST 52 WEEKS', 15, ACCENT, 710, anchor='middle', spacing=.8),
        text(34, 136, 'Daily contributions' if days is not None else 'Your contribution calendar will appear after the first sync', 18, MUTED),
    ]
    colors = ['#203540', '#0D5966', '#118DA2', '#16B8D2', '#67E8F9']
    x0, y0, step, cell = 70, 161, 16.3, 12.5
    for idx, label in [(0, 'Mon'), (2, 'Wed'), (4, 'Fri')]:
        s.append(text(34, y0 + idx*19.4 + 11, label, 15, FAINT))
    months = set()
    for week in range(52):
        first = start + dt.timedelta(days=week*7)
        key = (first.year, first.month)
        if first.day <= 7 and key not in months:
            months.add(key)
            s.append(text(round(x0+week*step, 1), 310, first.strftime('%b'), 14, MUTED))
        for i in range(7):
            day = first + dt.timedelta(days=i)
            n = int((days or {}).get(day.isoformat(), 0))
            level = 0 if n == 0 else 1 if n < 3 else 2 if n < 6 else 3 if n < 10 else 4
            color = colors[level] if days is not None else colors[0]
            s.append(f'<rect x="{round(x0+week*step, 1)}" y="{round(y0+i*19.4, 1)}" width="{cell}" height="{cell}" rx="3.2" fill="{color}"/>')
    s += [
        f'<path d="M33 327 H925" stroke="{STROKE}" stroke-width="1.4"/>',
        text(34, 349, f'{start:%b %Y} – {current:%b %Y}', 15, MUTED),
        text(700, 349, 'Less', 15, MUTED),
    ]
    for i, color in enumerate(colors):
        s.append(f'<rect x="{750+21*i}" y="336" width="15" height="15" rx="3" fill="{color}"/>')
    s.append(text(928, 349, 'More', 15, MUTED, anchor='end'))
    s.append('</svg>')
    return '\n'.join(s)


def load_data():
    if not OWNER:
        print('No GitHub owner configured: keeping all metrics as honest placeholders.')
        return None, {}, None
    q_owner = urllib.parse.quote(OWNER)
    user = api(f'/users/{q_owner}')
    repos = []
    for page in range(1, 11):
        group = api(f'/users/{q_owner}/repos?type=owner&per_page=100&page={page}')
        if not isinstance(group, list):
            raise ValueError('Repository data was not a list')
        repos += group
        if len(group) < 100:
            break
    values = {'public_repos': user.get('public_repos'),
              'stars': sum(int(r.get('stargazers_count') or 0) for r in repos),
              'followers': user.get('followers'), 'contributions': None}
    days = None
    try:
        result = api(query={
            'query': 'query($user:String!){user(login:$user){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}',
            'variables': {'user': OWNER},
        })
        calendar = result['data']['user']['contributionsCollection']['contributionCalendar']
        values['contributions'] = int(calendar['totalContributions'])
        days = {d['date']: int(d['contributionCount']) for week in calendar['weeks'] for d in week['contributionDays']}
    except Exception as exc:
        print('Contributions unavailable. Keeping contribution graphics as placeholders:', exc)
    return values, {r['name'].lower(): r for r in repos}, days


def main():
    try:
        data, repos, days = load_data()
    except Exception as exc:
        print('GitHub API error; leaving previous assets unchanged:', exc)
        raise SystemExit(1)
    for index, (name, description, category, scope) in enumerate(PROJECTS, 1):
        save(f'cards/{name.lower()}.svg', project_svg(name, description, category, scope, index, repos.get(name.lower())))
    for index in range(5, 10):
        save(f'cards/slot-{index:02d}.svg', placeholder_svg(index))
    save('stats.svg', stats_svg(data))
    save('activity.svg', activity_svg(days))


if __name__ == '__main__':
    main()
