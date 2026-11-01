(() => {
  'use strict';

  /* ---------- Planches dessinées (générées en SVG) ---------- */
  const TAU = Math.PI * 2;
  const n2 = v => Math.round(v * 100) / 100;
  const pt = (x, y) => `${n2(x)} ${n2(y)}`;
  const pol = (cx, cy, r, a) => [cx + Math.cos(a) * r, cy + Math.sin(a) * r];
  const P = (d, c) => `<path d="${d}"${c ? ` class="${c}"` : ''}/>`;
  const R = (x, y, w, h, c) => P(`M${pt(x, y)}h${n2(w)}v${n2(h)}h${n2(-w)}z`, c);
  const L = (x1, y1, x2, y2, c) => P(`M${pt(x1, y1)}L${pt(x2, y2)}`, c);
  const Ci = (cx, cy, r, c) => { const q = n2(r); return P(`M${pt(cx - r, cy)}a${q} ${q} 0 1 0 ${n2(2 * r)} 0a${q} ${q} 0 1 0 ${n2(-2 * r)} 0`, c); };
  const Tx = (x, y, t, c, a) => `<text x="${n2(x)}" y="${n2(y)}" class="${c || 'lbl'}" text-anchor="${a || 'start'}">${t}</text>`;

  function win(x, y, w, h, o = {}) {
    const sur = 1.8;
    let s = R(x - sur, y - sur, w + 2 * sur, h + sur, 'thin');
    s += R(x, y, w, h, 'glass');
    const ih = o.imposte ? h * 0.2 : 0;
    if (ih) s += L(x, y + ih, x + w, y + ih, 'thin');
    s += L(x + w / 2, y + ih, x + w / 2, y + h, 'thin');
    const rows = o.panes || 4;
    for (let k = 1; k < rows; k++) { const yy = y + ih + (h - ih) * k / rows; s += L(x, yy, x + w, yy, 'hair'); }
    if (o.key) s += P(`M${pt(x + w / 2 - 2.2, y - sur)}h4.4l-.8 3.6h-2.8z`, 'mask');
    if (o.ped === 'tri') s += P(`M${pt(x - sur - 1.6, y - sur - 1)}L${pt(x + w / 2, y - sur - 6)}L${pt(x + w + sur + 1.6, y - sur - 1)}Z`, 'thin');
    if (o.ped === 'seg') s += P(`M${pt(x - sur - 1.6, y - sur - 1)}Q${pt(x + w / 2, y - sur - 9.5)} ${pt(x + w + sur + 1.6, y - sur - 1)}Z`, 'thin');
    if (o.ped) s += R(x - sur - 1.6, y - sur - 1, w + 2 * sur + 3.2, 1, 'hair');
    return s;
  }

  function railing(x, y, w, h) {
    let s = L(x, y, x + w, y, 'thin') + L(x, y + .9, x + w, y + .9, 'hair') + L(x, y + h, x + w, y + h, 'hair');
    const n = Math.max(3, Math.round(w / 2.4));
    for (let i = 0; i <= n; i++) { const xx = x + w * i / n; s += L(xx, y + .9, xx, y + h, 'hair'); }
    const m = Math.max(1, Math.round(w / 7.5));
    const r = Math.min(h * .27, w / m * .3);
    for (let i = 0; i < m; i++) s += Ci(x + w * (i + .5) / m, y + h * .56, r, 'hair mask');
    return s;
  }

  function immeuble(o) {
    const X0 = 34, W = 184, G = 300, N = 5, bw = W / N;
    const lv = [300, 254, 220, 189, 158, 127, 98];
    const yb0 = lv[6] - 4, yBr = 64, yTop = 58;
    let s = '';
    s += P(`M${pt(X0 + 6, yBr)}L${pt(X0 + 16, yTop)}H${n2(X0 + W - 16)}L${pt(X0 + W - 6, yBr)}`, 'thin');
    [X0 + 28, X0 + W - 36].forEach(x => {
      s += R(x, yTop - 14, 8, 14.5, 'mask'); s += R(x - 1, yTop - 16.2, 10, 2.2, 'mask');
      s += L(x + 2.5, yTop - 16.2, x + 2.5, yTop - 19.5, 'thin'); s += L(x + 5.5, yTop - 16.2, x + 5.5, yTop - 19, 'thin');
    });
    s += P(`M${pt(X0 - 2, yb0)}L${pt(X0 + 6, yBr)}H${n2(X0 + W - 6)}L${pt(X0 + W + 2, yb0)}Z`, 'mask');
    for (let x = X0 + .5; x < X0 + W; x += 3.2) {
      let yt = yBr;
      if (x < X0 + 6) yt = yb0 - (x - (X0 - 2)) * (yb0 - yBr) / 8;
      if (x > X0 + W - 6) yt = yb0 - ((X0 + W + 2) - x) * (yb0 - yBr) / 8;
      s += L(x, yt + .6, x, yb0, 'hair');
    }
    for (let i = 0; i < N; i++) {
      const cx = X0 + bw * (i + .5);
      s += P(`M${pt(cx - 7, yb0)}V${n2(yb0 - 15)}H${n2(cx + 7)}V${n2(yb0)}Z`, 'mask');
      s += P(`M${pt(cx - 8.6, yb0 - 15)}Q${pt(cx, yb0 - 24)} ${pt(cx + 8.6, yb0 - 15)}Z`, 'mask');
      s += R(cx - 4.5, yb0 - 13, 9, 12, 'thin glass');
      s += L(cx, yb0 - 13, cx, yb0 - 1, 'hair'); s += L(cx - 4.5, yb0 - 7, cx + 4.5, yb0 - 7, 'hair');
    }
    s += R(X0 - 4, yb0, W + 8, 4, 'mask'); s += L(X0 - 4, yb0 + 2, X0 + W + 4, yb0 + 2, 'hair');
    for (let x = X0 + 2; x <= X0 + W - 1; x += 4) s += R(x - .8, lv[6], 1.6, 1.8, 'hair');
    s += R(X0, lv[6], W, G - lv[6]);
    for (let y = G - 4.6; y > lv[1] + 1; y -= 4.6) s += L(X0, y, X0 + W, y, 'hair');
    for (let i = 0; i < N; i++) {
      const cx = X0 + bw * (i + .5);
      if (i === 2) {
        const w = 20, h = 40, x = cx - w / 2, y = G - h;
        s += P(`M${pt(x, G)}V${n2(y + w / 2)}A${w / 2} ${w / 2} 0 0 1 ${pt(x + w, y + w / 2)}V${n2(G)}Z`, 'mask');
        s += P(`M${pt(x - 3, y + w / 2)}A${w / 2 + 3} ${w / 2 + 3} 0 0 1 ${pt(x + w + 3, y + w / 2)}`, 'thin');
        s += L(cx, y + w / 2, cx, G, 'thin');
        s += R(x + 2, y + w / 2 + 4, w / 2 - 4, 11, 'hair'); s += R(cx + 2, y + w / 2 + 4, w / 2 - 4, 11, 'hair');
        s += R(x + 2, y + w / 2 + 18, w / 2 - 4, 10, 'hair'); s += R(cx + 2, y + w / 2 + 18, w / 2 - 4, 10, 'hair');
        for (let k = 1; k < 6; k++) { const [px, py] = pol(cx, y + w / 2, w / 2, Math.PI * (1 + k / 6)); s += L(cx, y + w / 2, px, py, 'hair'); }
        s += P(`M${pt(cx - 3, y - 2.4)}h6l-1 6h-4z`, 'mask');
      } else {
        const w = 26, h = 34, x = cx - w / 2, y = G - h;
        s += P(`M${pt(x, G)}V${n2(y + 4)}Q${pt(cx, y - 3)} ${pt(x + w, y + 4)}V${n2(G)}Z`, 'mask');
        s += L(x, y + 11, x + w, y + 11, 'thin');
        s += L(x + w / 3, y + 11, x + w / 3, G, 'hair'); s += L(x + 2 * w / 3, y + 11, x + 2 * w / 3, G, 'hair');
        s += L(x + 2, G - 8, x + w - 2, G - 8, 'hair');
      }
    }
    s += R(X0 - 1.5, lv[1] - 1.6, W + 3, 3.2, 'mask');
    const floors = [
      { f: 1, wh: 22, ped: true, balcnt: true, imposte: true },
      { f: 2, wh: 21, filant: true, key: true, imposte: true },
      { f: 3, wh: 20, balcnt: true, key: true },
      { f: 4, wh: 20, balcnt: true, key: true },
      { f: 5, wh: 18, filant: true, panes: 3 }
    ];
    floors.forEach(c => {
      const yb = lv[c.f];
      for (let i = 0; i < N; i++) {
        const cx = X0 + bw * (i + .5), ww = 14, x = cx - ww / 2, y = yb - 1.6 - c.wh;
        s += win(x, y, ww, c.wh, { ped: c.ped ? (i % 2 ? 'tri' : 'seg') : null, key: c.key, panes: c.panes || 4, imposte: c.imposte });
        if (c.balcnt) s += railing(x - 1.8, yb - 1.6 - 8.5, ww + 3.6, 8.5);
      }
      if (c.filant) {
        s += R(X0 - 3, yb - 1.2, W + 6, 2.4, 'mask');
        for (let i = 0; i <= N; i++) { const px = X0 + bw * i + (i === 0 ? 4 : i === N ? -4 : 0); s += P(`M${pt(px - 2, yb + 1.2)}h4l-1 4h-2z`, 'mask'); }
        s += railing(X0 - 3, yb - 1.2 - 9, W + 6, 9);
      } else {
        s += L(X0, yb, X0 + W, yb, 'thin'); s += L(X0, yb + 1.1, X0 + W, yb + 1.1, 'hair');
      }
    });
    s += L(X0 - 22, G, X0 + W + 22, G, 'bold');
    if (o.annot) {
      const ax = X0 + W + 9;
      [[G, '±0,00'], [lv[1], '+4,60'], [lv[2], '+8,00'], [lv[3], '+11,10'], [lv[4], '+14,20'], [lv[5], '+17,30'], [lv[6], '+20,20'], [yTop, '+24,20']].forEach(([y, t]) => {
        s += L(ax - 6, y, ax + 16, y, 'acc-hair');
        s += P(`M${pt(ax, y)}l2.4 -2.6h-4.8z`, 'acc');
        s += Tx(ax + 3.6, y - 1.4, t, 'lbl acc-t');
      });
      ['RDC', 'R+1', 'R+2', 'R+3', 'R+4', 'R+5'].forEach((t, i) => { s += Tx(X0 - 7, (lv[i] + lv[i + 1]) / 2 + 1.6, t, 'lbl', 'end'); });
      s += Tx(X0 - 7, (yb0 + yTop) / 2 + 1.6, 'Comble', 'lbl', 'end');
      const dy = G + 12;
      s += L(X0, dy, X0 + W, dy, 'acc-hair');
      for (let i = 0; i <= N; i++) { const xx = X0 + bw * i; s += L(xx - 1.6, dy + 1.6, xx + 1.6, dy - 1.6, 'acc-hair'); s += L(xx, G + 4, xx, dy + 2.5, 'acc-hair'); }
      for (let i = 0; i < N; i++) s += Tx(X0 + bw * (i + .5), dy - 2, '3,68', 'sm', 'middle');
      s += Tx(X0 + W / 2, dy + 7.6, '18,40 m', 'lbl acc-t', 'middle');
      for (let x = X0 - 20; x < X0 + W + 22; x += 3) s += L(x, G + .6, x - 3, G + 3.6, 'hair');
      s += Tx(X0 - 20, G + 28, 'ÉLÉVATION SUR RUE · ÉCH. 1/100', 'cap');
      return { vb: '0 30 252 304', body: s, fs: 6.4, sw: .78 };
    }
    return { vb: `${X0 - 12} 34 ${W + 24} ${G - 29}`, body: s, sw: .78 };
  }

  function moulure(o) {
    const id = 'hatch' + o.uid;
    let s = `<defs><pattern id="${id}" width="2.6" height="2.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0V2.6" class="hatch"/></pattern></defs>`;
    s += `<path d="M14 118V40H30V118Z" class="thin" style="fill:url(#${id})"/>`;
    s += `<path d="M30 48V40H150V48Z" class="thin" style="fill:url(#${id})"/>`;
    const prof = 'M30 108V100H36V98A8 8 0 0 0 44 90H46V87A10 10 0 0 1 56 77H60V74H78V64H76C84 64 82 52 90 52H92V48H30Z';
    s += P(prof, 'mask');
    const lab = (x, y, tx, ty, t) => L(x, y, tx - 2.5, ty, 'acc-hair') + Ci(x, y, .7, 'acc') + Tx(tx, ty + 1.5, t, 'lbl acc-t');
    s += lab(83, 58, 108, 60, 'doucine');
    s += lab(78, 69, 108, 72, 'larmier');
    s += lab(49, 80, 108, 84, 'cavet');
    s += lab(41.7, 95.7, 108, 96, 'quart-de-rond');
    s += lab(33, 100, 108, 108, 'filet');
    s += Tx(15, 125, 'MUR', 'cap');
    s += Tx(150, 35, 'PLAFOND', 'cap', 'end');
    return { vb: '0 22 160 108', body: s, fs: 5.4 };
  }

  function parquet(o) {
    const id = 'clip' + o.uid;
    let s = `<defs><clipPath id="${id}"><rect x="14" y="12" width="132" height="96"/></clipPath></defs>`;
    s += R(6, 4, 148, 112, 'thin'); s += R(14, 12, 132, 96, 'thin');
    for (let x = 10; x < 151; x += 7.4) { s += L(x, 4, x, 12, 'hair'); s += L(x, 108, x, 116, 'hair'); }
    for (let y = 8; y < 113; y += 7.4) { s += L(6, y, 14, y, 'hair'); s += L(146, y, 154, y, 'hair'); }
    const cw = 13.2, dy = 8.2;
    let g = '';
    for (let k = -14; k < 16; k++) {
      const pts = [];
      for (let i = 0; i <= 10; i++) pts.push(pt(14 + cw * i, 12 + k * dy + (i % 2 ? 0 : cw * .95)));
      g += P('M' + pts.join('L'), 'hair');
    }
    for (let i = 1; i < 10; i++) g += L(14 + cw * i, 12, 14 + cw * i, 108, i % 2 ? 'thin' : 'hair');
    s += `<g clip-path="url(#${id})">${g}</g>`;
    return { vb: '0 0 160 120', body: s };
  }

  function ferronnerie() {
    const x0 = 12, x1 = 148, y0 = 26, y1 = 104;
    let s = R(x0, y0, x1 - x0, y1 - y0, 'thin');
    s += R(x0 - 4, y0 - 6, x1 - x0 + 8, 6, 'mask'); s += L(x0 - 4, y0 - 3, x1 + 4, y0 - 3, 'hair');
    s += L(x0, y1 - 6, x1, y1 - 6, 'hair');
    [56, 104].forEach(x => { s += L(x, y0, x, y1, 'thin'); s += L(x + 2.2, y0, x + 2.2, y1, 'hair'); });
    s += Ci(80, 61, 17, 'thin'); s += Ci(80, 61, 13.4, 'hair');
    for (let i = 0; i < 8; i++) {
      const a = i / 8 * TAU, [ax, ay] = pol(80, 61, 3.2, a), [bx, by] = pol(80, 61, 12, a);
      const [c1x, c1y] = pol(80, 61, 8, a - .32), [c2x, c2y] = pol(80, 61, 8, a + .32);
      s += P(`M${pt(ax, ay)}Q${pt(c1x, c1y)} ${pt(bx, by)}Q${pt(c2x, c2y)} ${pt(ax, ay)}Z`, 'hair');
    }
    s += Ci(80, 61, 2.6, 'thin mask');
    s += L(58.2, 61, 63, 61, 'thin'); s += L(97, 61, 104, 61, 'thin');
    s += L(80, y0, 80, 44, 'thin'); s += L(80, 78, 80, y1 - 6, 'thin');
    const spiral = (cx, cy, r, a0, dir) => {
      const pts = [];
      for (let i = 0; i <= 46; i++) { const t = i / 46, a = a0 + dir * t * 1.45 * TAU, rr = r * (1 - .8 * t); pts.push(pt(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr)); }
      return P('M' + pts.join('L'), 'thin');
    };
    [[34, 61], [126, 61]].forEach(([px, py]) => {
      s += spiral(px - 9.5, py - 15, 10, Math.PI * .5, 1);
      s += spiral(px + 9.5, py - 15, 10, Math.PI * .5, -1);
      s += spiral(px - 9.5, py + 15, 10, -Math.PI * .5, -1);
      s += spiral(px + 9.5, py + 15, 10, -Math.PI * .5, 1);
      s += Ci(px, py, 2.4, 'thin mask');
    });
    return { vb: '0 14 160 96', body: s };
  }

  function menuiserie() {
    let s = R(46, 4, 68, 112, 'thin');
    s += R(52, 10, 56, 100);
    s += L(52, 30, 108, 30, 'thin');
    s += R(54, 12, 52, 16, 'hair glass');
    [67, 80, 93].forEach(x => { s += L(x, 12, x, 28, 'hair'); });
    [[54, 32], [81, 32]].forEach(([x, y]) => {
      s += R(x, y, 25, 72, 'thin'); s += R(x + 2.5, y + 2.5, 20, 64, 'hair glass');
      for (let k = 1; k < 4; k++) { const yy = y + 2.5 + 64 * k / 4; s += L(x + 2.5, yy, x + 22.5, yy, 'hair'); }
      s += L(x + 12.5, y + 2.5, x + 12.5, y + 66.5, 'hair');
      s += P(`M${pt(x, y + 69)}h25v3h-25z`, 'hair');
    });
    s += L(80.5, 33, 80.5, 103, 'thin');
    s += P('M80.5 66c3.2 0 4.4 1.8 4.4 3.6s-1.2 3.6-4.4 3.6', 'thin');
    s += R(42, 110, 76, 4, 'mask');
    return { vb: '0 0 160 120', body: s };
  }

  function lambris() {
    let s = R(6, 8, 148, 4, 'thin'); s += L(6, 14, 154, 14, 'hair');
    s += R(6, 82, 148, 2.6, 'thin'); s += R(6, 108, 148, 4, 'thin');
    const panel = (x, y, w, h, r, c) => P(`M${pt(x + r, y)}H${n2(x + w - r)}A${r} ${r} 0 0 0 ${pt(x + w, y + r)}V${n2(y + h - r)}A${r} ${r} 0 0 0 ${pt(x + w - r, y + h)}H${n2(x + r)}A${r} ${r} 0 0 0 ${pt(x, y + h - r)}V${n2(y + r)}A${r} ${r} 0 0 0 ${pt(x + r, y)}Z`, c);
    [12, 48, 84, 120].forEach(x => {
      s += panel(x, 20, 28, 56, 4, 'thin'); s += panel(x + 3, 23, 22, 50, 3, 'hair');
      s += panel(x, 89, 28, 15, 2.5, 'thin');
    });
    [48, 84].forEach(x => { s += P(`M${pt(x + 14, 40)}a5 7 0 1 0 .01 0z`, 'hair'); s += L(x + 14, 33, x + 14, 47, 'hair'); });
    return { vb: '0 0 160 120', body: s };
  }

  function plan() {
    const t = 2.4;
    let s = R(10, 12, 140, 96, 'bold') + R(13, 15, 134, 90, 'thin');
    [27, 53, 80, 107, 134].forEach(x => { s += R(x - 6, 10.6, 12, 5.8, 'mask') + L(x - 6, 13.5, x + 6, 13.5, 'hair'); });
    [29.5, 66, 102].forEach(x => { s += R(x - 5, 103.6, 10, 5.8, 'mask') + L(x - 5, 106.5, x + 5, 106.5, 'hair'); });
    s += R(56, 15, t, 45, 'thin mask') + R(102, 15, t, 45, 'thin mask');
    s += R(13, 60, 134, t, 'thin mask') + R(13, 72, 105, t, 'thin mask');
    s += R(46, 74.4, t, 30.6, 'thin mask') + R(84, 74.4, t, 30.6, 'thin mask') + R(118, 72, t, 33, 'thin mask');
    [56, 102].forEach(x => {
      s += R(x - .4, 31, t + .8, 16, 'cut');
      s += L(x + t, 31, x + t + 8, 31, 'hair') + P(`M${pt(x + t + 8, 31)}A8 8 0 0 1 ${pt(x + t, 39)}`, 'hair');
      s += L(x + t, 47, x + t + 8, 47, 'hair') + P(`M${pt(x + t + 8, 47)}A8 8 0 0 0 ${pt(x + t, 39)}`, 'hair');
    });
    const door = (x, yw, dir) => {
      const y0 = dir > 0 ? yw + t : yw, y1 = y0 + dir * 8;
      return R(x, yw - .4, 8, t + .8, 'cut') + L(x, y0, x, y1, 'hair') + P(`M${pt(x, y1)}A8 8 0 0 ${dir > 0 ? 0 : 1} ${pt(x + 8, y0)}`, 'hair');
    };
    s += door(24, 60, -1) + door(72, 60, -1) + door(126, 60, -1);
    s += door(25, 72, 1) + door(58, 72, 1) + door(96, 72, 1);
    s += R(127, 104.3, 10, 4.6, 'cut') + L(127, 105, 127, 95, 'hair') + P(`M${pt(127, 95)}A10 10 0 0 1 ${pt(137, 105)}`, 'hair');
    [[34.5, 25, 'Salon'], [80.2, 25, 'Salle à manger'], [125.7, 25, 'Cuisine'], [29.5, 91, 'Chambre'], [66.2, 91, 'Bains'], [102.2, 91, 'Chambre'], [133.7, 86, 'Entrée']].forEach(([x, y, txt]) => { s += Tx(x, y, txt, 'lbl', 'middle'); });
    s += Tx(65.5, 68.4, 'Dégagement', 'sm', 'middle');
    s += L(10, 115, 48, 115, 'acc-hair');
    [10, 29, 48].forEach(x => { s += L(x, 113.6, x, 116.4, 'acc-hair'); });
    s += Tx(52, 116.6, '5 m', 'sm');
    return { vb: '0 4 160 116', body: s, fs: 4.6, sw: .55 };
  }

  function consoleV(o) {
    const id = 'hatchc' + o.uid;
    let s = `<defs><pattern id="${id}" width="2.6" height="2.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0V2.6" class="hatch"/></pattern></defs>`;
    s += `<path d="M24 114V6H40V114Z" class="thin" style="fill:url(#${id})"/>`;
    s += `<path d="M40 16H144V26H40Z" class="thin" style="fill:url(#${id})"/>`;
    s += L(40, 4, 144, 4, 'thin');
    for (let x = 46; x <= 140; x += 5.6) s += L(x, 4, x, 16, 'hair');
    s += P('M40 26H98A20 20 0 0 1 98 66C86 66 76 70 70 76C64 82 62 86 62 90A10 10 0 0 1 42 90L40 90Z', 'mask');
    const spiral = (cx, cy, r, a0, turns) => {
      const pts = [];
      for (let i = 0; i <= 64; i++) { const k = i / 64, a = a0 + k * turns * TAU, rr = r * (1 - .8 * k); pts.push(pt(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr)); }
      return P('M' + pts.join('L'), 'thin');
    };
    s += spiral(98, 46, 17, -Math.PI / 2, 1.3) + Ci(98, 46, 2.6, 'thin mask');
    s += spiral(52, 90, 8, 0, 1.2) + Ci(52, 90, 1.6, 'thin mask');
    s += P('M90 62C82 64 76 68 70 76', 'thin');
    s += P('M86 63C85 67 82 69 78 69', 'hair') + P('M80 66C79 70 76 72 73 73', 'hair') + P('M75 70C75 74 72 77 69 78', 'hair');
    s += L(40, 31, 84, 31, 'hair');
    return { vb: '0 0 160 118', body: s, sw: .62 };
  }

  const DRAW = { immeuble, moulure, parquet, ferronnerie, menuiserie, lambris, plan, console: consoleV };
  const reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  let uid = 0;

  function renderPlate(el) {
    const fn = DRAW[el.dataset.draw];
    if (!fn || el.querySelector('svg')) return;
    const { vb, body, fs, sw } = fn({ annot: el.hasAttribute('data-annot'), uid: ++uid });
    const label = el.dataset.label || '';
    const animate = el.hasAttribute('data-animate') && !reduce && 'IntersectionObserver' in window && el.offsetParent !== null;
    const attrs = label ? ` role="img" aria-label="${label}"` : ' aria-hidden="true"';
    el.insertAdjacentHTML('afterbegin', `<svg class="drw${animate ? ' drw-anim' : ''}" viewBox="${vb}" preserveAspectRatio="xMidYMid meet" style="--fs:${fs || 4.4}px;--sw:${sw || .6}"${attrs}>${animate ? `<g class="ghost">${body}</g><g class="ink">${body}</g>` : body}</svg>`);
    if (!animate) return;
    const svg = el.querySelector('svg');
    const paths = [...svg.querySelectorAll('.ink path')];
    const ys = paths.map(p => { try { const b = p.getBBox(); return b.y + b.height; } catch (e) { return 0; } });
    const max = Math.max(...ys), min = Math.min(...ys), span = (max - min) || 1;
    paths.forEach((p, i) => { p.setAttribute('pathLength', '1'); p.style.setProperty('--d', ((max - ys[i]) / span * 1.6).toFixed(3) + 's'); });
    const io = new IntersectionObserver(entries => {
      if (entries.some(e => e.isIntersecting)) { el.classList.add('is-drawing'); io.disconnect(); }
    }, { threshold: .35 });
    io.observe(el);
  }

  /* ---------- Page courante ---------- */
  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('.menu-toggle');
  const page = document.body.dataset.page || '';
  document.querySelectorAll('[data-nav]').forEach(a => { if (a.dataset.nav === page) a.setAttribute('aria-current', 'page'); });
  document.querySelectorAll('[data-draw]').forEach(renderPlate);
  const objet = new URLSearchParams(location.search).get('objet');
  const objetSelect = document.getElementById('c-objet');
  if (objet && objetSelect && [...objetSelect.options].some(o => o.value === objet)) objetSelect.value = objet;

  toggle.addEventListener('click', () => { const open = header.classList.toggle('menu-open'); toggle.setAttribute('aria-expanded', String(open)); });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && header.classList.contains('menu-open')) { header.classList.remove('menu-open'); toggle.setAttribute('aria-expanded', 'false'); toggle.focus(); }
  });
  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 8);
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  const skip = document.querySelector('[data-skip]');
  if (skip) skip.addEventListener('click', () => { const m = document.getElementById('main'); m.focus(); m.scrollIntoView(); });

  /* ---------- Formulaires (maquette) ---------- */
  document.querySelectorAll('form[data-demo]').forEach(f => {
    f.addEventListener('submit', e => {
      e.preventDefault();
      if (!f.reportValidity()) return;
      const done = f.querySelector('.form-done');
      const who = f.elements.prenom && f.elements.prenom.value.trim();
      done.querySelector('[data-who]').textContent = who ? `, ${who}` : '';
      done.hidden = false;
      done.focus({ preventScroll: true });
      done.scrollIntoView({ block: 'nearest' });
    });
  });

  /* ---------- Copie de l’adresse ---------- */
  document.querySelectorAll('[data-copy]').forEach(btn => btn.addEventListener('click', () => {
    const src = document.querySelector(btn.dataset.copy);
    if (!src) return;
    const text = src.innerText.replace(/\s*\n\s*/g, ', ').trim();
    const msg = btn.closest('.coord') && btn.closest('.coord').querySelector('.copy-msg');
    const say = t => { if (msg) msg.textContent = t; };
    const fallback = () => {
      const r = document.createRange(); r.selectNodeContents(src);
      const sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
      say('Adresse sélectionnée : copiez-la avec Ctrl+C ou ⌘+C.');
    };
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(() => say('Adresse copiée.'), fallback);
      else fallback();
    } catch (err) { fallback(); }
  }));

})();
