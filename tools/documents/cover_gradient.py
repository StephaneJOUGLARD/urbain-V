"""Intègre le dégradé de couverture directement dans la photo (aucun effet de transparence
dans le PDF) : le haut de l'image reste intact, puis la photo se désature et se fond dans le
vert approfondi de la charte (#2A7350), et éventuellement dans l'anthracite (#2B363F)."""
import sys, json
import numpy as np
from PIL import Image

GREEN = np.array([0x2A, 0x73, 0x50], float)
ANTHRACITE = np.array([0x2B, 0x36, 0x3F], float)

def fit_cover(im, W, H, px, py):
    sw, sh = im.size
    scale = max(W / sw, H / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    x, y = round((nw - W) * px), round((nh - H) * py)
    return im.crop((x, y, x + W, y + H))

def ramp(stops, t):
    """Interpolation par paliers avec lissage (smoothstep) dans chaque segment."""
    ts = np.array([p for p, _ in stops], float)
    vs = [np.atleast_1d(np.array(v, float)) for _, v in stops]
    out = np.zeros((len(t), vs[0].size))
    for i, x in enumerate(t):
        k = np.searchsorted(ts, x, side='right') - 1
        k = min(max(k, 0), len(ts) - 2)
        u = 0 if ts[k + 1] == ts[k] else min(max((x - ts[k]) / (ts[k + 1] - ts[k]), 0), 1)
        u = u * u * (3 - 2 * u)
        out[i] = vs[k] * (1 - u) + vs[k + 1] * u
    return out

def main():
    src, dst, spec = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
    W, H = spec['size']
    im = fit_cover(Image.open(src).convert('RGB'), W, H, *spec['position'])
    a = np.asarray(im, float)
    t = (np.arange(H) + .5) / H
    blend = ramp(spec['blend'], t)[:, 0][:, None, None]
    desat = ramp(spec['desat'], t)[:, 0][:, None, None]
    colors = {'green': GREEN, 'anthracite': ANTHRACITE}
    target = ramp([(p, colors[c]) for p, c in spec['color']], t)[:, None, :]
    gray = (a @ np.array([.2126, .7152, .0722]))[..., None]
    a = a * (1 - desat) + gray * desat
    a = a * (1 - blend) + target * blend
    out = Image.fromarray(np.clip(a + np.random.default_rng(1).uniform(-.5, .5, a.shape), 0, 255).astype(np.uint8))
    out.save(dst, quality=90, subsampling=0, optimize=True, progressive=True)
    print(dst, out.size)

main()
