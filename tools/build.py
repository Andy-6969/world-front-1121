"""Fill the map placeholders in src/front.html and write out/front.html.

The coastlines come from Natural Earth (public domain), read from the folder in the
NE_DIR environment variable and not committed: ne_110m_land.geojson for the world map
and ne_50m_admin_0_countries.geojson for the Gulf map. Each polygon ring is projected
onto its map box (equirectangular, longitude scaled by cos of the box's middle latitude)
and thinned to points at least 0.7 px apart.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NE = os.environ.get("NE_DIR")
if not NE:
    sys.exit("set NE_DIR to a folder holding the Natural Earth GeoJSON files")


def rings(geom):
    if geom["type"] == "Polygon":
        yield from geom["coordinates"]
    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            yield from poly


def projector(lon0, lon1, lat0, lat1, width, height):
    """Equirectangular box: lon0..lon1 fills the width, latitude keeps true proportions."""
    k = math.cos(math.radians((lat0 + lat1) / 2))
    s = width / ((lon1 - lon0) * k)
    top = (lat0 + lat1) / 2 + height / s / 2

    def p(lon, lat):
        return (lon - lon0) * k * s, (top - lat) * s

    return p


def path_for(features, proj, box, min_step=0.7):
    w, h = box
    out = []
    for f in features:
        for ring in rings(f["geometry"]):
            pts = [proj(lon, lat) for lon, lat in ring]
            xs = [x for x, _ in pts]
            ys = [y for _, y in pts]
            if max(xs) < -5 or min(xs) > w + 5 or max(ys) < -5 or min(ys) > h + 5:
                continue
            keep = [pts[0]]
            for x, y in pts[1:]:
                lx, ly = keep[-1]
                if abs(x - lx) + abs(y - ly) >= min_step:
                    keep.append((x, y))
            if len(keep) < 3:
                continue
            out.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in keep) + "Z")
    return "".join(out)


def load(name):
    with open(os.path.join(NE, name), encoding="utf-8") as fh:
        return json.load(fh)["features"]


def main():
    # world map box, must match the 'world' svg viewBox in src/front.html
    ww, wh = 300, 138
    world = projector(-170, 180, -56, 76, ww, wh)
    land = load("ne_110m_land.geojson")
    land = [f for f in land if min(lat for r in rings(f["geometry"]) for _, lat in r) > -60]
    world_d = path_for(land, world, (ww, wh), 0.9)

    # Gulf map box, must match the 'gulf' svg viewBox in src/front.html
    gw, gh = 600, 200
    k = math.cos(math.radians(26.3))
    s = gw / ((60.2 - 44.6) * k)
    top = 26.3 + gh / s / 2

    def gulf_p(lon, lat):
        return (lon - 44.6) * k * s, (top - lat) * s

    countries = load("ne_50m_admin_0_countries.geojson")
    named = {}
    for f in countries:
        named.setdefault(f["properties"].get("ADM0_A3"), []).append(f)
    gulf_land = path_for(countries, gulf_p, (gw, gh), 0.7)
    iran = path_for(named.get("IRN", []), gulf_p, (gw, gh), 0.7)
    bahrain = path_for(named.get("BHR", []), gulf_p, (gw, gh), 0.3)

    # place names used by the page: projected once here so the labels sit on the coast
    places = {
        "bahrain": (50.55, 26.07), "sitra": (50.63, 26.15), "khasab": (56.25, 26.18),
        "qeshm": (55.9, 26.75), "riyadh": (46.72, 24.71), "doha": (51.53, 25.29),
        "hormuz": (56.45, 26.55), "gulf_lbl": (50.9, 27.25), "uae": (54.4, 24.45),
        "oman": (57.0, 24.55), "saudi": (46.6, 26.9), "iran": (52.6, 28.45), "qatar": (51.25, 24.85),
    }
    pts = {k2: [round(c, 1) for c in gulf_p(*v)] for k2, v in places.items()}

    pins = {
        # story number -> lon, lat, for the world map
        "1": (50.6, 26.1), "2": (26.3, 60.4), "3": (30.7, 36.9), "4": (4.35, 50.85),
        "5": (-108.5, 25.6), "6": (6.14, 46.2), "8": (-76, -10.9),
        "8b": (127.5, -7.7), "9": (6.1, 4.8), "10": (47.8, 30.5), "11": (2.35, 48.86),
        "12": (-0.34, 51.46), "13": (135.5, 34.7),
    }
    wpins = {k2: [round(c, 1) for c in world(*v)] for k2, v in pins.items()}

    with open(os.path.join(ROOT, "src", "front.html"), encoding="utf-8") as fh:
        page = fh.read()
    page = (page.replace("{{WORLD_LAND}}", world_d)
                .replace("{{GULF_LAND}}", gulf_land)
                .replace("{{GULF_IRAN}}", iran)
                .replace("{{GULF_BAHRAIN}}", bahrain)
                .replace("{{GULF_POINTS}}", json.dumps(pts))
                .replace("{{WORLD_PINS}}", json.dumps(wpins)))
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    with open(os.path.join(ROOT, "out", "front.html"), "w", encoding="utf-8") as fh:
        fh.write(page)
    print("out/front.html:", len(page), "chars; gulf points", pts)


if __name__ == "__main__":
    main()
