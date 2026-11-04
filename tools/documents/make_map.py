"""Carte de France des départements (projection conique conforme de Lambert),
Dauphiné en vert, halo du grand quart sud-est centré sur Grenoble."""
import json, math, sys

src, out = sys.argv[1], sys.argv[2]
data = json.load(open(src, encoding='utf-8'))

lat1, lat2, lat0, lon0 = map(math.radians, (44, 49, 46.5, 3))
n = math.log(math.cos(lat1) / math.cos(lat2)) / math.log(math.tan(math.pi / 4 + lat2 / 2) / math.tan(math.pi / 4 + lat1 / 2))
F = math.cos(lat1) * math.tan(math.pi / 4 + lat1 / 2) ** n / n
rho0 = F / math.tan(math.pi / 4 + lat0 / 2) ** n

def proj(lon, lat):
    lon, lat = math.radians(lon), math.radians(lat)
    rho = F / math.tan(math.pi / 4 + lat / 2) ** n
    th = n * (lon - lon0)
    return rho * math.sin(th), rho0 - rho * math.cos(th)

def rings(geom):
    if geom['type'] == 'Polygon':
        return geom['coordinates']
    return [r for poly in geom['coordinates'] for r in poly]

feats = []
xs, ys = [], []
for f in data['features']:
    code = f['properties']['code']
    rs = [[proj(lon, lat) for lon, lat in r] for r in rings(f['geometry'])]
    feats.append((code, f['properties']['nom'], rs))
    for r in rs:
        for x, y in r:
            xs.append(x); ys.append(y)

W = 1000.0
pad = 14.0
minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
s = (W - 2 * pad) / (maxx - minx)
H = (maxy - miny) * s + 2 * pad
EXTRA_RIGHT = 330  # place pour les étiquettes à l'est des Alpes

def P(x, y):
    return ((x - minx) * s + pad, (maxy - y) * s + pad)

def path(rs):
    out = []
    for r in rs:
        pts = [P(x, y) for x, y in r]
        simp = [pts[0]]
        for p in pts[1:]:
            if abs(p[0] - simp[-1][0]) + abs(p[1] - simp[-1][1]) > 2.0:
                simp.append(p)
        if len(simp) < 3:
            continue
        out.append('M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in simp) + 'Z')
    return ''.join(out)

DAUPHINE = {'38': 'Isère', '26': 'Drôme', '05': 'Hautes-Alpes'}
def pt(lon, lat):
    return P(*proj(lon, lat))

gx, gy = pt(5.7245, 45.1885)       # Grenoble
km = s / 6371.0                    # unités SVG par km
R = 360 * km                       # rayon du halo

parts = []
parts.append(f'<svg class="map" viewBox="0 0 {W + EXTRA_RIGHT:.0f} {H:.0f}" role="img" aria-label="Carte : le Dauphiné (Isère, Drôme, Hautes-Alpes) et le grand quart sud-est de la France">')
parts.append('<defs>')
parts.append(f'<radialGradient id="halo" gradientUnits="userSpaceOnUse" cx="{gx:.1f}" cy="{gy:.1f}" r="{R:.1f}">'
             '<stop offset="0" stop-color="var(--brand)" stop-opacity=".30"/>'
             '<stop offset=".55" stop-color="var(--brand)" stop-opacity=".16"/>'
             '<stop offset="1" stop-color="var(--brand)" stop-opacity="0"/></radialGradient>')
allpaths = ''.join(path(rs) for _, _, rs in feats)
parts.append(f'<path id="fr-shape" d="{allpaths}"/>')
parts.append('<clipPath id="fr"><use href="#fr-shape"/></clipPath>')
parts.append('</defs>')
parts.append('<use class="map-land" href="#fr-shape"/>')
parts.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="{R:.1f}" fill="url(#halo)" clip-path="url(#fr)"/>')
for code, nom, rs in feats:
    cls = 'map-dep map-dau' if code in DAUPHINE else 'map-dep'
    parts.append(f'<path class="{cls}" d="{path(rs)}"><title>{nom}</title></path>')
parts.append(f'<circle class="map-ring" cx="{gx:.1f}" cy="{gy:.1f}" r="{R:.1f}" clip-path="url(#fr)"/>')

# villes de repère
for name, lon, lat, dx, dy, anchor in [('Paris', 2.3522, 48.8566, 12, 5, 'start'), ('Lyon', 4.8357, 45.7640, -12, 4, 'end'),
                                      ('Marseille', 5.3698, 43.2965, -12, 14, 'end'), ('Nice', 7.2620, 43.7102, 10, 16, 'start'),
                                      ('Montpellier', 3.8767, 43.6108, -12, 14, 'end')]:
    x, y = pt(lon, lat)
    parts.append(f'<circle class="map-city" cx="{x:.1f}" cy="{y:.1f}" r="4"/>')
    parts.append(f'<text class="map-city-t" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}">{name}</text>')

# étiquettes des départements du Dauphiné, à l'est, avec filets
cent = {'38': (5.30, 45.52), '26': (5.20, 44.70), '05': (6.25, 44.62)}
lab_x = W - 10 + 120
lab_y = {'38': gy - 160, '26': gy + 34, '05': gy + 118}
for code in ('38', '26', '05'):
    cx, cy = pt(*cent[code])
    ly = lab_y[code]
    parts.append(f'<path class="map-lead" d="M{cx:.1f} {cy:.1f}L{lab_x - 70:.1f} {ly:.1f}H{lab_x - 8:.1f}"/>')
    parts.append(f'<circle class="map-lead-dot" cx="{cx:.1f}" cy="{cy:.1f}" r="3.2"/>')
    parts.append(f'<text class="map-dep-t" x="{lab_x:.1f}" y="{ly + 7:.1f}">{DAUPHINE[code].upper()}</text>')

# Grenoble : étoile (emblème) et mention des bureaux
star = ('M 126.18 80.7 L 122.3 66.25 L 107.86 62.38 L 139.48 49.07 Z M 152.78 17.45 L 156.66 31.9 L 171.11 35.77 L 139.48 49.07 Z '
        'M 171.11 62.38 L 156.66 66.25 L 152.78 80.7 L 139.48 49.07 Z M 107.86 35.77 L 122.3 31.9 L 126.18 17.45 L 139.48 49.07 Z')
sc = 0.62
parts.append(f'<g class="map-star" transform="translate({gx:.1f} {gy:.1f}) scale({sc}) translate(-139.48 -49.07)"><path d="{star}"/></g>')
parts.append(f'<path class="map-lead" d="M{gx + 20:.1f} {gy - 8:.1f}L{lab_x - 70:.1f} {gy - 72:.1f}H{lab_x - 8:.1f}"/>')
parts.append(f'<text class="map-gre-t" x="{lab_x:.1f}" y="{gy - 72 + 9:.1f}">Grenoble</text>')
parts.append(f'<text class="map-gre-s" x="{lab_x:.1f}" y="{gy - 72 + 31:.1f}">NOS BUREAUX</text>')

# mention du périmètre, en mer
mx, my = pt(5.9, 42.55)
parts.append(f'<text class="map-zone-t" x="{mx:.1f}" y="{my:.1f}" text-anchor="middle">GRAND QUART SUD-EST</text>')
parts.append('</svg>')
open(out, 'w', encoding='utf-8').write('\n'.join(parts))
print('carte', W + EXTRA_RIGHT, round(H), 'R=', round(R), 'octets', sum(len(p) for p in parts))
