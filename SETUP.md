# Zense GitHub Profile — Cyan Edition

This package contains a GitHub profile README, local cyan SVG cards, an animated typing GIF, social icons, and a workflow for real GitHub statistics.

## Install

1. Create a **public repository with exactly the same name as your GitHub username** (unless it already exists).
2. Upload the entire package contents to the root of that repository: `README.md`, `assets/`, `scripts/`, and `.github/`.
3. Open `README.md` and replace `YOUR_GITHUB_USERNAME` in every project and repository link. Replace `YOUR_LINKEDIN_URL` and `YOUR_DISCORD_URL` with your actual links.
4. Open **Actions > Update profile cards and stats > Run workflow**. In repository settings, Actions may need read/write workflow permissions. GitHub Actions updates `assets/stats.svg`, `assets/activity.svg`, and project cards when real data is available.
5. The scheduled workflow runs every Monday, refreshing the public metrics. Private contributions and restricted data may not be available to this workflow.

## Customize the 3×3 project grid

- The existing named cards are **Constella**, **Skele**, **Retra**, and **Framewarp**.
- Five more cards (`assets/cards/slot-05.svg` through `slot-09.svg`) are intentionally marked *Coming soon*. They are placeholders, not claimed repositories.
- To add a new real project, add its name and description in `scripts/generate_profile.py` under `PROJECTS`; run the workflow to generate its SVG, then replace a placeholder `<img>` in `README.md` with a link to that project's GitHub URL.
- Three cards per row render at typical desktop GitHub profile widths. On narrower displays, GitHub may wrap cards. GitHub README files do not offer full responsive CSS control.

## About the graphics

- `assets/brand/typing.gif` is a real, self-hosted animated typing GIF; no external typing-image service is required.
- Project cards, statistics, contribution graph, wordmark, and social icons are SVG files stored in this repository. Their colors use the cyan theme.
- Technology badges use Shields.io and Simple Icons (external image service) so each tool can show its recognizable icon. The rest of the design does not depend on external image APIs.
- `scripts/generate_profile.py` needs only Python 3 (standard library). `scripts/build_static_assets.py` and `scripts/build_preview.py` are optional design utilities, which use Pillow (preview also uses CairoSVG).

## Discord

The displayed username is **@zensyi**. Direct-linking a Discord user's profile generally requires the account's numeric user ID. Replace `YOUR_DISCORD_URL` when you have an appropriate URL.
