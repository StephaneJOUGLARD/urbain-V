// Sert le dépôt du site et récupère le SVG des planches dessinées (data-draw).
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const root = process.argv[2], out = process.argv[3];
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg' };
const srv = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p);
  if (!f.startsWith(root) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
}).listen(0, async () => {
  const port = srv.address().port;
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ reducedMotion: 'reduce', viewport: { width: 1400, height: 1000 } });
  const page = await ctx.newPage();
  for (const u of ['/', '/savoir-faire/', '/operations/']) {
    await page.goto(`http://127.0.0.1:${port}${u}`, { waitUntil: 'networkidle' });
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(400);
    const items = await page.$$eval('[data-draw]', els => els.map(e => ({ k: e.dataset.draw, svg: e.querySelector('svg') ? e.querySelector('svg').outerHTML : null })));
    for (const it of items) { if (it.svg) { fs.writeFileSync(path.join(out, it.k + '.svg.html'), it.svg); console.log('ok', it.k, it.svg.length); } else console.log('vide', it.k); }
  }
  await browser.close(); srv.close();
});
