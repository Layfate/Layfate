// Regenerate: npm i simple-icons si9@npm:simple-icons@9.0.0 && node scripts/tools-marquee.js assets/tools/tools-marquee.svg
// Generates assets/tools/tools-marquee.svg: four rows of tool logos (one per category)
// scrolling left, with each tool name printed under its logo.
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
// Kept deliberately cheap to paint (no filters, masks or per-logo animations):
// only one transform per row animates, so browsers redraw at the display's
// full refresh rate (60/120/144 Hz).
const W = 900;
const TILE = 56, PITCH = 96, ICON = 30;
const ROW_H = 124, TOP = 14, CY = 64;   // tile centre sits CY below the row top
const NAME_Y = CY + TILE / 2 + 18;      // name baseline below the tile
const H = TOP * 2 + ROW_H * 4 - 12;
const BG = '#0D1117';
const SPEEDS = [40, 34, 38, 32];        // px per second, per row
const LABELS = ['Languages & Runtimes', 'Frameworks & Game Engines', 'Cloud, Databases & DevOps', 'Development & Design Tools'];
const FONT = `'Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif`;

tools.forEach((t, i) => { t.idx = i; });
const rows = Object.keys(groups).map((cat, k) => {
  const list = tools.filter((t) => t.cat === cat);
  const loop = list.length * PITCH;
  return { k, list, loop, T: +(loop / SPEEDS[k]).toFixed(2),
    copies: Math.ceil((W + PITCH) / loop) + 1, y0: TOP + k * ROW_H };
});

const tile = (row, t, x) => {
  const h = TILE / 2;
  return `<g transform="translate(${x} ${row.y0 + CY})">` +
    `<rect x="${-h}" y="${-h}" width="${TILE}" height="${TILE}" rx="15" fill="#161B22" stroke="#${t.color}" stroke-opacity=".45" stroke-width="1.5"/>` +
    `<use href="#i${t.idx}" x="${-ICON / 2}" y="${-ICON / 2}" width="${ICON}" height="${ICON}" fill="#${t.color}"/>` +
    `<text y="${NAME_Y - CY}" class="nm">${esc(t.name)}</text></g>`;
};

const rowSvg = (row) => {
  const tiles = [];
  for (let copy = 0; copy < row.copies; copy++) {
    row.list.forEach((t, i) => tiles.push(tile(row, t, PITCH / 2 + i * PITCH + copy * row.loop)));
  }
  return `<g class="s s${row.k}">
${tiles.join('\n')}
</g>`;
};

const rowLabel = (row) => `<rect x="28" y="${row.y0 + 10}" width="3" height="12" rx="1.5" fill="#E9A23B"/>
<text x="38" y="${row.y0 + 20}" class="lb">${esc(LABELS[row.k].toUpperCase())}<tspan class="ct" dx="8">${row.list.length}</tspan></text>`;

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="My favorite tools: ${esc(tools.map((t) => t.name).join(', '))}">
<title>${esc(tools.map((t) => t.name).join(' · '))}</title>
<style>
.s{will-change:transform}
${rows.map((row) => `.s${row.k}{animation:m${row.k} ${row.T}s linear infinite}
@keyframes m${row.k}{from{transform:translate3d(0,0,0)}to{transform:translate3d(-${row.loop}px,0,0)}}`).join('\n')}
.nm{font:600 11px ${FONT};fill:#9DA7B3;text-anchor:middle}
.lb{font:700 11.5px ${FONT};fill:#E9A23B;letter-spacing:1.4px}
.ct{font-size:11px;font-weight:600;fill:#6E7681;letter-spacing:0}
@media (prefers-reduced-motion:reduce){.s{animation:none}}
</style>
<defs>
${tools.map((t, i) => `<symbol id="i${i}" viewBox="0 0 24 24"><path d="${t.path}"/></symbol>`).join('\n')}
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E9A23B" stop-opacity="0"/><stop offset=".5" stop-color="#E9A23B" stop-opacity=".7"/><stop offset="1" stop-color="#E9A23B" stop-opacity="0"/></linearGradient>
<linearGradient id="fl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${BG}"/><stop offset="1" stop-color="${BG}" stop-opacity="0"/></linearGradient>
<linearGradient id="fr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${BG}" stop-opacity="0"/><stop offset="1" stop-color="${BG}"/></linearGradient>
<clipPath id="card"><rect width="${W}" height="${H}" rx="20"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="${W}" height="${H}" fill="${BG}"/>
${rows.map(rowSvg).join('\n')}
<rect x="0" y="0" width="90" height="${H}" fill="url(#fl)"/>
<rect x="${W - 90}" y="0" width="90" height="${H}" fill="url(#fr)"/>
${rows.map(rowLabel).join('\n')}
<rect x="0" y="0" width="${W}" height="1.5" fill="url(#edge)"/>
<rect x="0" y="${H - 1.5}" width="${W}" height="1.5" fill="url(#edge)"/>
</g>
<rect x=".75" y=".75" width="${W - 1.5}" height="${H - 1.5}" rx="19.5" fill="none" stroke="#30363D"/>
</svg>
`;

const out = process.argv[2];
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, svg);
console.log(rows.map((x) => `row${x.k}: ${x.list.length} tools, ${x.T}s, ${x.copies} copies`).join('\n') + `\n${W}x${H}, ${(svg.length / 1024).toFixed(1)} KB`);
