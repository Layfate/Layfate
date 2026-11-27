// Regenerate: npm i simple-icons si9@npm:simple-icons@9.0.0 && node scripts/tools-marquee.js assets/tools/tools-marquee.svg
// Generates assets/tools/tools-marquee.svg: four animated rows of tool logos (one per
// category) scrolling left, each logo popping a tooltip as it passes the centre.
const fs = require('fs');
const path = require('path');
const si = Object.values(require('simple-icons'));
const si9 = Object.values(require('si9'));

const find = (slug) => si.find((i) => i && i.slug === slug) || si9.find((i) => i && i.slug === slug);

// Plain database cylinder for "SQL" (no vendor logo fits a language).
const DB_PATH =
  'M12 2C7.03 2 3 3.57 3 5.5v13C3 20.43 7.03 22 12 22s9-1.57 9-3.5v-13C21 3.57 16.97 2 12 2zm0 2c4.42 0 7 1.3 7 1.5S16.42 7 12 7 5 5.7 5 5.5 7.58 4 12 4zM5 8.2C6.7 8.96 9.2 9.4 12 9.4s5.3-.44 7-1.2v3.3c0 .2-2.58 1.5-7 1.5s-7-1.3-7-1.5V8.2zm0 6C6.7 14.96 9.2 15.4 12 15.4s5.3-.44 7-1.2v4.3c0 .2-2.58 1.5-7 1.5s-7-1.3-7-1.5v-4.3z';

const groups = {
  'Language / Runtime': [
    ['Luau', 'robloxstudio', '00A2FF'], ['Lua', 'lua', '2C2D72'], ['Python', 'python'], ['Rust', 'rust'],
    ['Zig', 'zig'], ['C#', 'dotnet'], ['TypeScript', 'typescript'], ['JavaScript', 'javascript'],
    ['HTML5', 'html5'], ['CSS3', 'css3'], ['SQL', null, '336791'], ['Node.js', 'nodedotjs', '339933'],
    ['Go', 'go'], ['Kotlin', 'kotlin'], ['Swift', 'swift'], ['Dart', 'dart'], ['C++', 'cplusplus'],
  ],
  'Framework / Engine': [
    ['Vue.js', 'vuedotjs'], ['React', 'react'], ['Next.js', 'nextdotjs'], ['Svelte', 'svelte'],
    ['SvelteKit', 'svelte'], ['Astro', 'astro'], ['Tailwind CSS', 'tailwindcss'], ['React Native', 'react'],
    ['Flutter', 'flutter'], ['Tauri', 'tauri'], ['Iced', 'iced'], ['FastAPI', 'fastapi'], ['NestJS', 'nestjs'],
    ['ASP.NET Core', 'dotnet'], ['Roblox Studio', 'robloxstudio', 'E6EDF3'], ['Unity', 'unity'], ['Godot', 'godotengine'],
  ],
  'Cloud / Database / DevOps': [
    ['Azure', 'microsoftazure'], ['Google Cloud', 'googlecloud'], ['Vercel', 'vercel'], ['Cloudflare', 'cloudflare'],
    ['Docker', 'docker'], ['Supabase', 'supabase'], ['Firebase', 'firebase', 'FFCA28'], ['Neon', 'neon', '00E5A0'],
    ['PostgreSQL', 'postgresql'], ['SQLite', 'sqlite', '0F80CC'],
  ],
  'Dev & Design Tool': [
    ['VS Code', 'visualstudiocode'], ['Visual Studio', 'visualstudio'], ['Figma', 'figma'], ['Photoshop', 'adobephotoshop'],
    ['Aseprite', 'aseprite'], ['Git', 'git', 'F05032'], ['GitHub', 'github'], ['Android Studio', 'androidstudio'],
  ],
};

const lum = (hex) => {
  const c = [0, 2, 4].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map((v) => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
};
const mix = (hex, t) => [0, 2, 4].map((i) => {
  const v = parseInt(hex.slice(i, i + 2), 16);
  return Math.round(v + (255 - v) * t).toString(16).padStart(2, '0');
}).join('');
// Keep brand colours readable on the dark card.
const readable = (hex) => {
  const L = lum(hex);
  if (L < 0.02) return 'E6EDF3';
  if (L < 0.12) return mix(hex, 0.45);
  return hex;
};
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

const tools = [];
for (const [cat, list] of Object.entries(groups)) {
  for (const [name, slug, hex] of list) {
    const icon = slug ? find(slug) : null;
    if (slug && !icon) throw new Error('missing icon ' + slug);
    tools.push({ name, cat, path: icon ? icon.path : DB_PATH, color: readable(hex || icon.hex) });
  }
}

// Geometry: four rows, one per category, each scrolling left on its own loop.
const W = 900;
const TILE = 56, PITCH = 76, ICON = 30, POP = 1.14;
const ROW_H = 110, TOP = 14, CY = 66;  // tile centre sits CY below the row top
const H = TOP * 2 + ROW_H * 4 - 18;
const C = W / 2;                      // spotlight x
const SPEEDS = [38, 32, 36, 30];      // px per second, per row
const LABELS = ['Languages & Runtimes', 'Frameworks & Game Engines', 'Cloud, Databases & DevOps', 'Development & Design Tools'];
const r = (n) => +n.toFixed(3);
const FONT = `'Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif`;

tools.forEach((t, i) => { t.idx = i; });
const rows = Object.keys(groups).map((cat, k) => {
  const list = tools.filter((t) => t.cat === cat);
  const loop = list.length * PITCH;
  return { k, list, loop, T: +(loop / SPEEDS[k]).toFixed(2), win: PITCH / loop,
    copies: Math.ceil((W + PITCH) / loop) + 1, y0: TOP + k * ROW_H };
});

const tipFor = (t) => {
  const bw = Math.max(t.name.length * 7.8 + 24, 60), bh = 26, top = -TILE / 2 - 10 - bh;
  return `<g class="tip">` +
    `<rect x="${r(-bw / 2)}" y="${top}" width="${r(bw)}" height="${bh}" rx="8" fill="url(#tipFill)"/>` +
    `<path d="M-6 ${top + bh - 0.5}h12l-6 6z" fill="#EDA93F"/>` +
    `<text y="${top + 17.5}" class="tn">${esc(t.name)}</text></g>`;
};

const tile = (row, t, i, copy) => {
  const x0 = PITCH / 2 + i * PITCH;
  const x = x0 + copy * row.loop;
  // Fraction of the cycle at which this tile's centre reaches the spotlight.
  const phase = ((((x0 - C) / row.loop) % 1) + 1) % 1;
  const start = (phase - row.win / 2 + 1) % 1;
  const delay = r(-((1 - start) % 1) * row.T);
  const h = TILE / 2;
  return `<g transform="translate(${x} ${row.y0 + CY})"><g class="t" style="animation-delay:${delay}s">` +
    `<rect class="glow" x="${-h - 5}" y="${-h - 5}" width="${TILE + 10}" height="${TILE + 10}" rx="20" fill="#${t.color}"/>` +
    `<rect x="${-h}" y="${-h}" width="${TILE}" height="${TILE}" rx="15" fill="#161B22" stroke="#${t.color}" stroke-opacity=".35" stroke-width="1.5"/>` +
    `<rect class="ring" x="${-h}" y="${-h}" width="${TILE}" height="${TILE}" rx="15" fill="none" stroke="#${t.color}" stroke-width="2"/>` +
    `<use href="#i${t.idx}" x="${-ICON / 2}" y="${-ICON / 2}" width="${ICON}" height="${ICON}" fill="#${t.color}"/>` +
    tipFor(t) + `</g></g>`;
};

const rowCss = (row) => {
  const a = r(row.win * 18), b = r(row.win * 82), c = r(row.win * 100), k = row.k;
  return `.r${k} .strip{animation:scroll${k} ${row.T}s linear infinite}
.r${k} .t{animation:pop${k} ${row.T}s linear infinite}
.r${k} .t .tip,.r${k} .t .ring{animation-name:show${k}}
.r${k} .t .glow{animation-name:glow${k}}
@keyframes scroll${k}{from{transform:translateX(0)}to{transform:translateX(-${row.loop}px)}}
@keyframes pop${k}{0%{transform:scale(1)}${a}%,${b}%{transform:scale(${POP})}${c}%,100%{transform:scale(1)}}
@keyframes show${k}{0%{opacity:0}${a}%,${b}%{opacity:1}${c}%,100%{opacity:0}}
@keyframes glow${k}{0%{opacity:0}${a}%,${b}%{opacity:.45}${c}%,100%{opacity:0}}`;
};

const rowSvg = (row) => {
  const label = LABELS[row.k];
  const tiles = [];
  for (let copy = 0; copy < row.copies; copy++) row.list.forEach((t, i) => tiles.push(tile(row, t, i, copy)));
  return `<g class="r${row.k}">
<ellipse cx="${C}" cy="${row.y0 + CY}" rx="120" ry="52" fill="url(#spot)"/>
<rect x="28" y="${row.y0 + 12}" width="3" height="12" rx="1.5" fill="#E9A23B"/>
<text x="38" y="${row.y0 + 22}" class="lb">${esc(label.toUpperCase())}<tspan class="ct" dx="8">${row.list.length}</tspan></text>
<g mask="url(#m)"><g class="strip">
${tiles.join('\n')}
</g></g></g>`;
};

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="My favorite tools: ${esc(tools.map((t) => t.name).join(', '))}">
<title>${esc(tools.map((t) => t.name).join(' · '))}</title>
<style>
.t{transform-box:fill-box;transform-origin:center}
.t .tip,.t .ring,.t .glow{opacity:0;animation:inherit}
.t .glow{filter:url(#blur)}
.tn{font:700 13px ${FONT};fill:#1A1206;text-anchor:middle}
.lb{font:700 11.5px ${FONT};fill:#E9A23B;letter-spacing:1.4px}
.ct{font-size:11px;font-weight:600;fill:#6E7681;letter-spacing:0}
${rows.map(rowCss).join('\n')}
@media (prefers-reduced-motion:reduce){.strip,.t,.t .tip,.t .ring,.t .glow{animation:none!important}}
</style>
<defs>
${tools.map((t, i) => `<symbol id="i${i}" viewBox="0 0 24 24"><path d="${t.path}"/></symbol>`).join('\n')}
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#11161D"/><stop offset="1" stop-color="#0B0F14"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E9A23B" stop-opacity="0"/><stop offset=".5" stop-color="#E9A23B" stop-opacity=".7"/><stop offset="1" stop-color="#E9A23B" stop-opacity="0"/></linearGradient>
<linearGradient id="tipFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFC861"/><stop offset="1" stop-color="#EDA93F"/></linearGradient>
<radialGradient id="spot" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#E9A23B" stop-opacity=".13"/><stop offset="1" stop-color="#E9A23B" stop-opacity="0"/></radialGradient>
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".1" stop-color="#fff"/><stop offset=".9" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="m" maskUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}"><rect width="${W}" height="${H}" fill="url(#fade)"/></mask>
<clipPath id="card"><rect width="${W}" height="${H}" rx="20"/></clipPath>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
</defs>
<g clip-path="url(#card)">
<rect width="${W}" height="${H}" fill="url(#bg)"/>
<rect x="0" y="0" width="${W}" height="1.5" fill="url(#edge)"/>
<rect x="0" y="${H - 1.5}" width="${W}" height="1.5" fill="url(#edge)"/>
${rows.map(rowSvg).join('\n')}
</g>
<rect x=".75" y=".75" width="${W - 1.5}" height="${H - 1.5}" rx="19.5" fill="none" stroke="#30363D"/>
</svg>
`;

const out = process.argv[2];
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, svg);
console.log(rows.map((x) => `row${x.k}: ${x.list.length} tools, ${x.T}s, ${x.copies} copies`).join('\n') + `\n${W}x${H}, ${(svg.length / 1024).toFixed(1)} KB`);
