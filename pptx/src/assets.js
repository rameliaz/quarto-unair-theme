// Rasterizes the brand graphics used by build.py into ./assets.
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const React = require('react');
const { renderToStaticMarkup } = require('react-dom/server');
const { FaGraduationCap, FaHandshake, FaChartBar } = require('react-icons/fa');

const EXT = path.join(__dirname, '..', '..', '_extensions', 'unair');
const OUT = path.join(__dirname, 'assets');
fs.mkdirSync(OUT, { recursive: true });

const tileSvg = fs.readFileSync(path.join(EXT, 'keypattern.svg'), 'utf8');
const PATTERN_D = tileSvg.match(/ d="([^"]+)"/)[1];
const keySvg = fs.readFileSync(path.join(EXT, 'keygraphic.svg'), 'utf8');
const KEY_D = keySvg.match(/ d="([^"]+)"/)[1];
const keyVB = keySvg.match(/viewBox="([^"]+)"/)[1];

const png = (svg, file) => sharp(Buffer.from(svg)).png().toFile(path.join(OUT, file));

// Batik strip: 3 tiles wide, full slide height (7.5in). Tile = 31.5 x 59.84.
// Strip is 1.26in wide -> tile 0.42in wide, 0.798in tall.
function strip(fill) {
  const tileW = 31.5, tileH = 59.84;
  const hUnits = (7.5 / 0.42) * tileW; // strip height in tile units
  let uses = '';
  for (let r = 0; r * tileH < hUnits; r++)
    for (let c = 0; c < 3; c++)
      uses += `<path transform="translate(${c * tileW} ${r * tileH})" d="${PATTERN_D}"/>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="378" height="2250" viewBox="0 0 ${3 * tileW} ${hUnits}" preserveAspectRatio="none"><g fill="#${fill}">${uses}</g></svg>`;
}

// Scrim for the dark quote: 120deg gradient, UNAIR blue .88 -> black .6.
const scrim = `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
<defs><linearGradient id="g" x1="0" y1="0.21" x2="1" y2="0.79">
<stop offset="0" stop-color="#14497F" stop-opacity="0.88"/><stop offset="1" stop-color="#000000" stop-opacity="0.6"/>
</linearGradient></defs><rect width="1920" height="1080" fill="url(#g)"/></svg>`;

// Abstract brand artwork standing in for photos in the sample deck.
function art(w, h, bg1, bg2, fill, opacity, scale) {
  const tileW = 31.5 * scale, tileH = 59.84 * scale;
  let uses = '';
  for (let r = -1; r * tileH < h; r++)
    for (let c = -1; c * tileW < w; c++)
      uses += `<path transform="translate(${c * tileW + (r % 2 ? tileW / 2 : 0)} ${r * tileH}) scale(${scale})" d="${PATTERN_D}"/>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#${bg1}"/><stop offset="1" stop-color="#${bg2}"/></linearGradient></defs>
<rect width="${w}" height="${h}" fill="url(#g)"/><g fill="#${fill}" fill-opacity="${opacity}">${uses}</g></svg>`;
}

function icon(Comp, color) {
  const svg = renderToStaticMarkup(React.createElement(Comp, { color: '#' + color, size: 512 }));
  return sharp(Buffer.from(svg)).resize(512, 512).png().toFile(path.join(OUT, Comp.name + '.png'));
}

(async () => {
  await sharp(path.join(EXT, 'logo.png')).resize({ width: 1400 }).png().toFile(path.join(OUT, 'logo.png'));
  await sharp(path.join(EXT, 'logo_white.png')).resize({ width: 1400 }).png().toFile(path.join(OUT, 'logo_white.png'));
  await png(`<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="${keyVB}"><path fill="#FFFFFF" d="${KEY_D}"/></svg>`, 'keygraphic_white.png');
  await png(strip('14497F'), 'strip_blue.png');
  await png(strip('FFCB05'), 'strip_yellow.png');
  await png(scrim, 'scrim.png');
  await sharp(Buffer.from(art(1600, 1800, '1B5A9A', '0E3560', 'FFFFFF', 0.08, 3.2))).jpeg({ quality: 85 }).toFile(path.join(OUT, 'art_blue.jpg'));
  await sharp(Buffer.from(art(1600, 1800, 'FFD633', 'F2B800', '14497F', 0.12, 3.2))).jpeg({ quality: 85 }).toFile(path.join(OUT, 'art_yellow.jpg'));
  await sharp(Buffer.from(art(1200, 800, '14497F', '0B2E52', 'FFCB05', 0.18, 2.2))).jpeg({ quality: 85 }).toFile(path.join(OUT, 'art_a.jpg'));
  await sharp(Buffer.from(art(1200, 800, 'F4F6F9', 'DCE3EC', '14497F', 0.10, 2.2))).jpeg({ quality: 85 }).toFile(path.join(OUT, 'art_b.jpg'));
  await sharp(Buffer.from(art(1200, 800, 'FFCB05', 'F0B400', 'FFFFFF', 0.30, 2.2))).jpeg({ quality: 85 }).toFile(path.join(OUT, 'art_c.jpg'));
  await sharp(Buffer.from(art(1920, 1080, '2D6CAB', '101820', 'FFFFFF', 0.06, 4))).jpeg({ quality: 85 }).toFile(path.join(OUT, 'art_photo.jpg'));
  await icon(FaGraduationCap, 'E6282B');
  await icon(FaHandshake, 'E6282B');
  await icon(FaChartBar, 'E6282B');
  console.log('assets done');
})();
