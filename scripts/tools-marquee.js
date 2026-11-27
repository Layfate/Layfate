// Regenerate: npm i simple-icons si9@npm:simple-icons@9.0.0 && node scripts/tools-marquee.js assets/tools/tools-marquee.svg
// Generates assets/tools/tools-marquee.svg: one animated strip of tool logos
// scrolling left, each logo popping a tooltip as it passes the centre.
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

// Geometry
const W = 900, H = 200;
const TILE = 68, PITCH = 92, ICON = 38;
const STRIP_Y = 124;              // tile centre line
const C = W / 2;                  // spotlight x
const LOOP = tools.length * PITCH; // width of one set
const SPEED = 42;                 // px per second
const T = +(LOOP / SPEED).toFixed(2);
const X0 = 0;                     // strip start (first tile centre = X0 + PITCH/2)
const win = PITCH / LOOP;         // fraction of the cycle one pitch takes
const r = (n) => +n.toFixed(3);

const tipFor = (t) => {
  const nameW = t.name.length * 8.1 + 28;
  const catW = t.cat.length * 6.1 + 28;
  const bw = Math.max(nameW, catW, 96);
  const bh = 44, top = -TILE / 2 - 14 - bh;
  return `<g class="tip">` +
    `<rect x="${r(-bw / 2)}" y="${top}" width="${r(bw)}" height="${bh}" rx="10" fill="url(#tipFill)"/>` +
    `<path d="M-7 ${top + bh - 0.5}h14l-7 8z" fill="#E9A23B"/>` +
    `<text y="${top + 19}" class="tn">${esc(t.name)}</text>` +
    `<text y="${top + 35}" class="tc">${esc(t.cat)}</text></g>`;
};

const tile = (t, i, copy) => {
  const x = X0 + PITCH / 2 + i * PITCH + copy * LOOP;
  // When does this tile's centre reach the spotlight? (fraction of cycle)
  const phase = ((((X0 + PITCH / 2 + i * PITCH - C) / LOOP) % 1) + 1) % 1;
  const start = (phase - win / 2 + 1) % 1;
  const delay = r(-((1 - start) % 1) * T);
  const s = ICON / 24;
  return `<g transform="translate(${x} ${STRIP_Y})"><g class="t" style="animation-delay:${delay}s">` +
    `<rect class="glow" x="${-TILE / 2 - 6}" y="${-TILE / 2 - 6}" width="${TILE + 12}" height="${TILE + 12}" rx="24" fill="#${t.color}"/>` +
    `<rect x="${-TILE / 2}" y="${-TILE / 2}" width="${TILE}" height="${TILE}" rx="18" fill="#161B22" stroke="#${t.color}" stroke-opacity=".35" stroke-width="1.5"/>` +
    `<rect class="ring" x="${-TILE / 2}" y="${-TILE / 2}" width="${TILE}" height="${TILE}" rx="18" fill="none" stroke="#${t.color}" stroke-width="2"/>` +
    `<use href="#i${i}" x="${-ICON / 2}" y="${-ICON / 2}" width="${ICON}" height="${ICON}" fill="#${t.color}"/>` +
    tipFor(t) + `</g></g>`;
};

const tiles = [0, 1].map((copy) => tools.map((t, i) => tile(t, i, copy)).join('\n')).join('\n');
const pctIn = r(win * 100 * 0.18), pctHold = r(win * 100 * 0.82), pctOut = r(win * 100);

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="My favorite tools: ${esc(tools.map((t) => t.name).join(', '))}">
<title>${esc(tools.map((t) => t.name).join(' · '))}</title>
<style>
.strip{animation:scroll ${T}s linear infinite}
.t{transform-box:fill-box;transform-origin:center;animation:pop ${T}s linear infinite}
.t .tip,.t .ring,.t .glow{opacity:0;animation:inherit;animation-name:show}
.t .glow{animation-name:glow;filter:url(#blur)}
.tn{font:700 14px 'Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif;fill:#1A1206;text-anchor:middle}
.tc{font:600 10.5px 'Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif;fill:#4A3410;text-anchor:middle;letter-spacing:.3px}
@keyframes scroll{from{transform:translateX(0)}to{transform:translateX(-${LOOP}px)}}
@keyframes pop{0%{transform:scale(1)}${pctIn}%,${pctHold}%{transform:scale(1.16)}${pctOut}%,100%{transform:scale(1)}}
@keyframes show{0%{opacity:0}${pctIn}%,${pctHold}%{opacity:1}${pctOut}%,100%{opacity:0}}
@keyframes glow{0%{opacity:0}${pctIn}%,${pctHold}%{opacity:.45}${pctOut}%,100%{opacity:0}}
@media (prefers-reduced-motion:reduce){.strip,.t,.t .tip,.t .ring,.t .glow{animation:none}}
</style>
<defs>
${tools.map((t, i) => `<symbol id="i${i}" viewBox="0 0 24 24"><path d="${t.path}"/></symbol>`).join('\n')}
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#11161D"/><stop offset="1" stop-color="#0B0F14"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E9A23B" stop-opacity="0"/><stop offset=".5" stop-color="#E9A23B" stop-opacity=".7"/><stop offset="1" stop-color="#E9A23B" stop-opacity="0"/></linearGradient>
<linearGradient id="tipFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFC861"/><stop offset="1" stop-color="#E9A23B"/></linearGradient>
<radialGradient id="spot" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#E9A23B" stop-opacity=".16"/><stop offset="1" stop-color="#E9A23B" stop-opacity="0"/></radialGradient>
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".12" stop-color="#fff"/><stop offset=".88" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="m"><rect width="${W}" height="${H}" fill="url(#fade)"/></mask>
<clipPath id="card"><rect width="${W}" height="${H}" rx="20"/></clipPath>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
</defs>
<g clip-path="url(#card)">
<rect width="${W}" height="${H}" fill="url(#bg)"/>
<ellipse cx="${C}" cy="${STRIP_Y}" rx="150" ry="95" fill="url(#spot)"/>
<rect x="0" y="0" width="${W}" height="1.5" fill="url(#edge)"/>
<rect x="0" y="${H - 1.5}" width="${W}" height="1.5" fill="url(#edge)"/>
<g mask="url(#m)"><g class="strip">
${tiles}
</g></g>
</g>
<rect x=".75" y=".75" width="${W - 1.5}" height="${H - 1.5}" rx="19.5" fill="none" stroke="#30363D"/>
</svg>
`;

const out = process.argv[2];
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, svg);
console.log(`${tools.length} tools, loop ${LOOP}px, ${T}s, ${(svg.length / 1024).toFixed(1)} KB`);
