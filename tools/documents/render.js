// Assemble un gabarit HTML (planches, carte) puis l'imprime en PDF A4 avec Chromium.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const dir = __dirname;
const [name, outPdf] = process.argv.slice(2);
let html = fs.readFileSync(path.join(dir, name + '.html'), 'utf8');
html = html.replace(/\{\{plate:([a-z]+)\}\}/g, (_, k) => fs.readFileSync(path.join(dir, 'plates', k + '.svg.html'), 'utf8'));
html = html.replace('{{map}}', () => fs.readFileSync(path.join(dir, 'build', 'map.svg.html'), 'utf8'));
const built = path.join(dir, name + '.build.html');
fs.writeFileSync(built, html);
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + built, { waitUntil: 'load' });
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
  const missing = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'error').map(f => f.family + ' ' + f.weight));
  if (missing.length) console.log('polices en erreur :', missing);
  // contrôle de débordement : éléments qui sortent de leur page
  const over = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('.page').forEach((pg, i) => {
      const r = pg.getBoundingClientRect();
      pg.querySelectorAll('p, h1, h2, h3, h4, li, .frame, table').forEach(el => {
        const b = el.getBoundingClientRect();
        if (b.height && (b.bottom > r.bottom - 1 || b.right > r.right + 1)) out.push(`page ${i + 1} : ${el.tagName}.${el.className} « ${(el.textContent || '').trim().slice(0, 40)} »`);
      });
    });
    return out;
  });
  if (over.length) console.log('débordements :\n' + over.join('\n'));
  await page.pdf({ path: outPdf, width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('PDF', outPdf, Math.round(fs.statSync(outPdf).size / 1024), 'Ko');
})();
