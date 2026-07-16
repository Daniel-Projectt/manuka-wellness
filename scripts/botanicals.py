"""Genera las láminas de herbario de Manuka en SVG.

Las paredes del centro tienen flores prensadas enmarcadas y un mural
botánico con helechos, acianos azules y hojas anchas. Este script dibuja
esos tres especímenes en línea fina.

Los SVG se usan como CSS mask (el trazo va opaco, el color lo pone el CSS).

    python scripts/botanicals.py     # -> assets/fern.svg, flor.svg, hoja.svg
"""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")


# ─── utilidades de curva ───

def bez(p0, p1, p2, p3, t):
    mt = 1 - t
    x = mt**3*p0[0] + 3*mt*mt*t*p1[0] + 3*mt*t*t*p2[0] + t**3*p3[0]
    y = mt**3*p0[1] + 3*mt*mt*t*p1[1] + 3*mt*t*t*p2[1] + t**3*p3[1]
    return x, y


def bez_d(p0, p1, p2, p3, t):
    mt = 1 - t
    x = 3*mt*mt*(p1[0]-p0[0]) + 6*mt*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    y = 3*mt*mt*(p1[1]-p0[1]) + 6*mt*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return x, y


def wob(i, salt, amp):
    """Variación determinista: una planta real no es simétrica."""
    v = math.sin(i * 12.9898 + salt * 78.233) * 43758.5453
    return (v - math.floor(v) - 0.5) * 2 * amp


def leaf_path(cx, cy, ang, L, W):
    """Hoja tipo lente. Devuelve (contorno, nervio central, puntos del nervio)."""
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v):
        return (cx + u*ca - v*sa, cy + u*sa + v*ca)
    tip, base = P(L, 0), P(0, 0)
    b1, b2 = P(L*0.35, W), P(L*0.78, W*0.42)
    b3, b4 = P(L*0.35, -W), P(L*0.78, -W*0.42)
    d = (f"M{base[0]:.1f},{base[1]:.1f} "
         f"C{b1[0]:.1f},{b1[1]:.1f} {b2[0]:.1f},{b2[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} "
         f"C{b4[0]:.1f},{b4[1]:.1f} {b3[0]:.1f},{b3[1]:.1f} {base[0]:.1f},{base[1]:.1f} Z")
    vein = f"M{base[0]:.1f},{base[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f}"
    return d, vein, (P, base, tip)


def svg_wrap(w, h, body, width=1.1):
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="none">',
        f'<g stroke="#000" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">',
        body,
        "</g></svg>",
    ])


# ─── 1. Helecho ───

def fern(path, n=26, Lmax=56.0, peak=0.24, sweep=0.62, w=220, h=420):
    p0, p1, p2, p3 = path
    out = [f"<path d=\"M{p0[0]},{p0[1]} C{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}\"/>"]
    for i in range(n):
        t = 0.06 + (0.965 - 0.06) * (i / (n - 1))
        x, y = bez(p0, p1, p2, p3, t)
        dx, dy = bez_d(p0, p1, p2, p3, t)
        tang = math.atan2(dy, dx)
        k = (t/peak)**0.75 if t <= peak else ((1-t)/(1-peak))**1.15
        base_L = Lmax * max(k, 0.04)
        for side in (+1, -1):
            salt = 1.7 if side > 0 else 4.3
            L = base_L * (1 + wob(i, salt, 0.13))
            W = L * (0.30 + wob(i, salt + 9, 0.03))
            off = wob(i, salt + 3, 1.6)
            ang = tang + side*(math.pi/2) - side*(sweep + wob(i, salt + 5, 0.10))
            d, vein, _ = leaf_path(x + off*math.cos(tang), y + off*math.sin(tang), ang, L, W)
            out.append(f'<path d="{d}"/>')
            out.append(f'<path d="{vein}" stroke-opacity="0.55"/>')
    return svg_wrap(w, h, "\n".join(out))


# ─── 2. Aciano (las flores azules del mural) ───

def bloom(cx, cy, r, n=14, ang0=0.0, salt=3.0):
    """Cabezuela: pétalos radiales finos + centro."""
    out = []
    for i in range(n):
        a = ang0 + 2*math.pi*i/n + wob(i, salt, 0.08)
        L = r * (1 + wob(i, salt + 2, 0.16))
        d, _, _ = leaf_path(cx, cy, a, L, L*0.22)
        out.append(f'<path d="{d}"/>')
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.17:.1f}"/>')
    return out


def cornflower(w=200, h=420):
    out = []
    # tres tallos con una flor cada uno
    stems = [
        (((100, 415), (86, 320), (74, 210), (66, 96)), 26, 0.5),
        (((100, 415), (110, 320), (132, 232), (140, 150)), 21, 1.9),
        (((100, 415), (96, 340), (104, 268), (112, 214)), 15, 3.4),
    ]
    for (p0, p1, p2, p3), r, salt in stems:
        out.append(f"<path d=\"M{p0[0]},{p0[1]} C{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}\"/>")
        # hojas lanceoladas sobre el tallo
        for i, t in enumerate((0.30, 0.52, 0.72)):
            x, y = bez(p0, p1, p2, p3, t)
            dx, dy = bez_d(p0, p1, p2, p3, t)
            tang = math.atan2(dy, dx)
            side = 1 if i % 2 == 0 else -1
            L = 30 * (1 + wob(i, salt, 0.2))
            ang = tang + side*(math.pi/2) - side*1.05
            d, vein, _ = leaf_path(x, y, ang, L, L*0.16)
            out.append(f'<path d="{d}"/>')
            out.append(f'<path d="{vein}" stroke-opacity="0.5"/>')
        out += bloom(p3[0], p3[1], r, n=14, ang0=salt, salt=salt)
    return svg_wrap(w, h, "\n".join(out))


# ─── 3. Rama de hoja ancha (el mural de la recepción) ───

def broadleaf(w=240, h=420):
    p0, p1, p2, p3 = (120, 412), (76, 300), (156, 168), (104, 14)
    out = [f"<path d=\"M{p0[0]},{p0[1]} C{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}\"/>"]
    n = 7
    for i in range(n):
        t = 0.14 + (0.94 - 0.14) * (i / (n - 1))
        x, y = bez(p0, p1, p2, p3, t)
        dx, dy = bez_d(p0, p1, p2, p3, t)
        tang = math.atan2(dy, dx)
        side = 1 if i % 2 == 0 else -1
        L = (74 - 46*t) * (1 + wob(i, 2.1, 0.1))
        W = L * 0.42
        ang = tang + side*(math.pi/2) - side*(0.75 + wob(i, 5.5, 0.1))
        d, vein, (P, base, tip) = leaf_path(x, y, ang, L, W)
        out.append(f'<path d="{d}"/>')
        out.append(f'<path d="{vein}" stroke-opacity="0.6"/>')
        # Nervadura secundaria. El borde es la misma curva del contorno, así
        # que se muestrea ahí para que ningún nervio se salga de la hoja.
        edge = ((0.0, 0.0), (L*0.35, W), (L*0.78, W*0.42), (L, 0.0))
        for j in range(1, 5):
            s = 0.18 + 0.62 * (j - 1) / 3.0
            ex, ey = bez(*edge, s)
            a = P(max(ex - L*0.17, L*0.04), 0)
            for s2 in (+1, -1):
                b = P(ex * 0.97, s2 * ey * 0.78)
                out.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" stroke-opacity="0.4"/>')
    return svg_wrap(w, h, "\n".join(out))


if __name__ == "__main__":
    files = {
        "fern.svg": fern(((132, 415), (68, 296), (150, 158), (86, 10))),
        "flor.svg": cornflower(),
        "hoja.svg": broadleaf(),
    }
    for name, svg in files.items():
        p = os.path.join(OUT, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"{name}: {len(svg)} bytes")
