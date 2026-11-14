#!/usr/bin/env python3
"""Build a preview PNG from actual exported SVGs (not a simulated design)."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import cairosvg

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
W,H=904,1760
im=Image.new('RGB',(W,H),'#0D1117')
d=ImageDraw.Draw(im)
REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font_sm=ImageFont.truetype(REG,14)
font_md=ImageFont.truetype(REG,18)
font_bold=ImageFont.truetype(BOLD,21)
font_section=ImageFont.truetype(BOLD,22)
CYAN='#22D3EE'


def put_svg(path,x,y,w):
    data=cairosvg.svg2png(url=str(ASSETS/path),output_width=w)
    asset=Image.open(BytesIO(data)).convert('RGBA')
    im.paste(asset,(x,y),asset)
    return asset.size[1]

# file-shaped panel border
panel=(18,18,886,H-18)
d.rounded_rectangle(panel,radius=16,outline='#293844',width=2)
put_svg('brand/zense.svg',229,35,450)
with Image.open(ASSETS/'brand/typing.gif') as anim:
    gif=anim.convert('RGB').resize((532,51))
    im.paste(gif,(186,145))
for i, f in enumerate(['social/linkedin.svg','social/discord.svg','social/coffee.svg']):
    put_svg(f,377+i*57,216,33)
d.text((452,264),'Discord  @zensyi',font=font_sm,fill='#A6C7D2',anchor='mt')
d.line((44,299,860,299),fill='#263542',width=1)

d.text((48,330),'▾',font=font_section,fill=CYAN)
d.text((82,330),'My Top Open Source Projects',font=font_section,fill='#E8F6FB')

cards=['constella.svg','skele.svg','retra.svg','framewarp.svg','slot-05.svg','slot-06.svg','slot-07.svg','slot-08.svg','slot-09.svg']
cardw=240
cardh=round(cardw*298/470)
x0=(W-(3*cardw+2*13))//2
y0=380
for i,f in enumerate(cards):
    put_svg('cards/'+f,x0+(i%3)*(cardw+13),y0+(i//3)*(cardh+13),cardw)
put_svg('all-repositories.svg',(W-246)//2,870,246)
d.line((44,935,860,935),fill='#263542',width=1)
d.text((48,962),'▸',font=font_section,fill=CYAN)
d.text((82,962),'My Favorite Tools',font=font_section,fill='#E8F6FB')
d.line((44,1010,860,1010),fill='#263542',width=1)
d.text((48,1040),'▾',font=font_section,fill=CYAN)
d.text((82,1040),'Stats and Activity',font=font_section,fill='#E8F6FB')

d.text((64,1091),'GitHub Profile Stats',font=font_md,fill='#D7EDF3')
put_svg('stats.svg',(W-780)//2,1125,780)
d.text((64,1392),'Recent GitHub Activity',font=font_md,fill='#D7EDF3')
put_svg('activity.svg',(W-780)//2,1424,780)
# Activity ends at y1721, too tall; we'll adjust H accordingly.

out=ROOT.parent/'Zense-Cyan-README-Preview.png'
im.save(out)
print(out)
