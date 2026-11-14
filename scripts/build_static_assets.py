#!/usr/bin/env python3
"""Generate repository-local cyan social icons, title image, and typing GIF.
Only Pillow is needed for the animated GIF; the GitHub Actions workflow does not run this script.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'

# Recolor original vector social icons, keeping the recognizable logos.
for path in (ASSETS / 'social').glob('*.svg'):
    original = path.read_text(encoding='utf-8')
    new = original.replace('#F75C7E', '#22D3EE').replace('#11151B', '#0D151D')
    path.write_text(new, encoding='utf-8')

(ASSETS / 'brand').mkdir(parents=True, exist_ok=True)
# A real cyan vector wordmark rather than GitHub's default white/gray Markdown H1.
(ASSETS / 'brand' / 'zense.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 790 144" width="790" height="144" role="img">
<title>Zense</title>
<defs>
 <linearGradient id="glow" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#22D3EE"/><stop offset="1" stop-color="#67E8F9"/></linearGradient>
</defs>
<g transform="translate(168 17)">
  <rect x="1.5" y="1.5" width="100" height="100" rx="26" fill="#0D2631" stroke="#17798E" stroke-width="3"/>
  <path d="M28 30 H78 L28 76 H78" fill="none" stroke="url(#glow)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="80" cy="24" r="5.5" fill="#67E8F9"/>
</g>
<text x="296" y="102" fill="url(#glow)" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="101" font-weight="800" letter-spacing="0">Zense</text>
</svg>''', encoding='utf-8')

# Consistent flat and readable 'Explore All Repos' call-to-action.
(ASSETS / 'all-repositories.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="510" height="90" viewBox="0 0 510 90" role="img">
<title>Explore all repositories</title>
<rect x="1" y="1" width="508" height="88" rx="22" fill="#122633" stroke="#275666" stroke-width="2"/>
<rect x="22" y="24" width="42" height="42" rx="11" fill="#0C3543"/>
<path d="M33 35 H53 M33 45 H53 M33 55 H49" stroke="#22D3EE" stroke-width="3.5" stroke-linecap="round"/>
<text x="82" y="54" fill="#DDF8FC" font-size="23" font-weight="750" font-family="Inter, Segoe UI, Arial, sans-serif" letter-spacing="1.2">EXPLORE ALL REPOS</text>
<path d="M442 45 H478 M465 31 L479 45 L465 59" stroke="#22D3EE" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''', encoding='utf-8')

# Self-hosted animated typing banner; no readme-typing-svg external dependency.
WIDTH, HEIGHT = 720, 69
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 30)
PHRASES = ['Software Developer', 'Game Developer', 'Open-Source Creator', 'Always learning new things']
frames = []
durations = []

def frame(word, cursor=True):
    img = Image.new('RGB', (WIDTH, HEIGHT), '#0D1117')
    draw = ImageDraw.Draw(img)
    width = draw.textbbox((0, 0), word, font=FONT)[2]
    x = int((WIDTH - width - (15 if cursor else 0)) / 2)
    draw.text((x, 15), word, fill='#5EEAFF', font=FONT)
    if cursor:
        draw.rounded_rectangle((x+width+5, 20, x+width+11, 53), radius=1, fill='#22D3EE')
    return img

for idx, phrase in enumerate(PHRASES):
    # Start with a complete phrase so the README looks good in reduced-motion previews.
    if idx == 0:
        frames.append(frame(phrase))
        durations.append(950)
    else:
        for letters in range(1, len(phrase)+1):
            frames.append(frame(phrase[:letters]))
            durations.append(61)
    frames.append(frame(phrase, False))
    durations.append(1100)
    for letters in range(len(phrase)-1, -1, -1):
        frames.append(frame(phrase[:letters]))
        durations.append(34)

out = ASSETS / 'brand' / 'typing.gif'
frames[0].save(out, format='GIF', save_all=True, append_images=frames[1:], duration=durations,
               loop=0, optimize=True, disposal=2)
print('Generated', out.relative_to(ROOT), 'frames=', len(frames), 'bytes=', out.stat().st_size)
