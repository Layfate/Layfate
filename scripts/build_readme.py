#!/usr/bin/env python3
"""Build the README with a 3x3 project grid and four compact tool categories."""
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]

# Tool icons come from the Shields/Simple Icons service, while all project, social,
# activity and branding assets are stored in the repo.
CATEGORIES = [
    ('💻 Languages & Runtimes', [
        ('Luau', 'robloxstudio'), ('Lua', 'lua'), ('Python', 'python'), ('C#', 'dotnet'),
        ('TypeScript', 'typescript'), ('JavaScript', 'javascript'), ('PHP', 'php'),
        ('HTML5', 'html5'), ('CSS3', 'css3'), ('SQL', 'databricks'), ('Node.js', 'nodedotjs'),
    ]),
    ('🧩 Frameworks & Game Engines', [
        ('Vue.js', 'vuedotjs'), ('React', 'react'), ('Astro', 'astro'),
        ('Tailwind CSS', 'tailwindcss'), ('D3.js', 'd3'), ('Ionic', 'ionic'),
        ('React Native', 'react'), ('Roblox Studio', 'robloxstudio'),
        ('Unity', 'unity'), ('Godot', 'godotengine'), ('Pygame', 'python'),
    ]),
    ('☁️ Cloud, Databases & DevOps', [
        ('Azure', 'microsoftazure'), ('Heroku', 'heroku'), ('Netlify', 'netlify'),
        ('Google Cloud', 'googlecloud'), ('DigitalOcean', 'digitalocean'),
        ('Vercel', 'vercel'), ('Cloudflare', 'cloudflare'), ('Docker', 'docker'),
        ('Ansible', 'ansible'), ('CircleCI', 'circleci'), ('GitHub Actions', 'githubactions'),
        ('MS SQL Server', 'microsoftsqlserver'), ('SQLite', 'sqlite'),
    ]),
    ('🎨 Development & Design Tools', [
        ('VS Code', 'visualstudiocode'), ('Visual Studio', 'visualstudio'),
        ('Figma', 'figma'), ('Photoshop', 'adobephotoshop'),
        ('Git', 'git'), ('GitHub', 'github'), ('Android Studio', 'androidstudio'),
    ]),
]


def badge(name, icon):
    path = quote(name.replace(' ', '_'), safe='')
    # One dark/cyan badge treatment across every category; official marks where supported.
    url = f'https://img.shields.io/badge/{path}-17313D?style=flat-square&logo={icon}&logoColor=22D3EE'
    return f'  <img alt="{name}" src="{url}" />'


out = [
'''<!--
  ZENSE / CYAN GITHUB PROFILE
  Install: upload README.md and the assets/, scripts/, .github/ folders together.
  Replace YOUR_GITHUB_USERNAME, YOUR_DISCORD_URL, and YOUR_LINKEDIN_URL.
  @zensyi is your Discord handle, not a direct URL.
  Project slots 05–09 are intentionally empty: replace with real projects as needed.
  Real GitHub stats appear after running Actions > Update profile cards and stats.
  The 3x3 grid is responsive as GitHub wraps images on smaller screens.
-->
<div align="center">

<img src="assets/brand/zense.svg" width="440" alt="Zense" />

<br />

<img src="assets/brand/typing.gif" width="520" alt="Software Developer · Game Developer · Open-Source Creator · Always learning new things" />

<p align="center">
  <a href="YOUR_LINKEDIN_URL"><img src="assets/social/linkedin.svg" width="34" height="34" alt="LinkedIn: Zense" title="LinkedIn: Zense" /></a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="YOUR_DISCORD_URL"><img src="assets/social/discord.svg" width="34" height="34" alt="Discord: @zensyi" title="Discord: @zensyi" /></a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://buymeacoffee.com/zense"><img src="assets/social/coffee.svg" width="34" height="34" alt="Buy Me a Coffee — Zense" title="Buy Me a Coffee" /></a>
</p>
<p><sub>Discord: <strong>@zensyi</strong></sub></p>

</div>

<details open>
<summary><h2>📘 My Top Open Source Projects</h2></summary>

<!-- 3 columns by 3 rows. Only the four named cards are existing projects;
     the remaining five are honest upcoming-project placeholders. -->
<p align="center">
  <a href="https://github.com/YOUR_GITHUB_USERNAME/Constella"><img src="assets/cards/constella.svg" width="232" alt="Constella — Roblox utility framework" /></a>&nbsp;
  <a href="https://github.com/YOUR_GITHUB_USERNAME/Skele"><img src="assets/cards/skele.svg" width="232" alt="Skele — desktop workspace" /></a>&nbsp;
  <a href="https://github.com/YOUR_GITHUB_USERNAME/Retra"><img src="assets/cards/retra.svg" width="232" alt="Retra — game library" /></a>
</p>
<p align="center">
  <a href="https://github.com/YOUR_GITHUB_USERNAME/Framewarp"><img src="assets/cards/framewarp.svg" width="232" alt="Framewarp — Figma to Roblox UI workflow" /></a>&nbsp;
  <img src="assets/cards/slot-05.svg" width="232" alt="Project slot 5 — coming soon" />&nbsp;
  <img src="assets/cards/slot-06.svg" width="232" alt="Project slot 6 — coming soon" />
</p>
<p align="center">
  <img src="assets/cards/slot-07.svg" width="232" alt="Project slot 7 — coming soon" />&nbsp;
  <img src="assets/cards/slot-08.svg" width="232" alt="Project slot 8 — coming soon" />&nbsp;
  <img src="assets/cards/slot-09.svg" width="232" alt="Project slot 9 — coming soon" />
</p>

<p align="center">
  <a href="https://github.com/YOUR_GITHUB_USERNAME?tab=repositories"><img src="assets/all-repositories.svg" width="255" alt="Explore all repositories" /></a>
</p>
</details>

<details>
<summary><h2>🛠️ My Favorite Tools</h2></summary>
''']
for title, tools in CATEGORIES:
    out += [f'\n### {title}\n', '<p>']
    out += [badge(name, icon) for name, icon in tools]
    out += ['</p>\n']
out += [
'''</details>

<details>
<summary><h2>📊 Stats and Activity</h2></summary>

### 💻 GitHub Profile Stats

<p align="center">
  <img src="assets/stats.svg" width="748" alt="GitHub overview — updated using real public GitHub data after syncing" />
</p>

### ⚡ Recent GitHub Activity

<p align="center">
  <img src="assets/activity.svg" width="748" alt="GitHub contribution activity — updated from GitHub data after syncing" />
</p>

</details>

---

<div align="center"><sub>Designed with clarity. Built with curiosity.</sub></div>
''']
(ROOT / 'README.md').write_text('\n'.join(out), encoding='utf-8')
print('README created with', sum(len(group) for _, group in CATEGORIES), 'tool badges in', len(CATEGORIES), 'groups')
