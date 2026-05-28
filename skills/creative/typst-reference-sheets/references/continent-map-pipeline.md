# Continent Map Generation Pipeline

Proven GeoPandas + Natural Earth pipeline for generating accurate continent maps with shaded target countries and numbered circles. Updated May 2026 with 6-continent production run learnings.

## One-time setup
```bash
pip3 install geopandas matplotlib pandas pillow
```

Shapefiles (install at `ne_data/` relative to project):
- **110m** (default): `ne_110m_admin_0_countries.shp` — 39 European countries, fast. Missing microstates < ~2,500 km².
- **50m** (fallback): `ne_50m_admin_0_countries.shp` — 13 South American countries, 31-part Chile polygons. Use when 110m fragments narrow countries (Chile's southern fjords render as disconnected islands at 110m). Download: `https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip`

## Country name matching
Natural Earth uses specific names that differ from user lists. Always maintain a NAME_FIX mapping:
```python
NAME_FIX = {
    "Czech Republic": "Czechia", "United States": "United States of America",
    "Bahama Islands": "Bahamas", "South Africa": "South Africa",
    "Dominican Republic": "Dominican Rep.", "Puerto Rico": "Puerto Rico",
    "Russia": "Russia", "Turkey": "Turkey", "South Korea": "South Korea",
    "Greenland": "Greenland", "Bolivia": "Bolivia",
}
```

## Microstates NOT in 110m resolution
Excluded: Liechtenstein (160 km²), Monaco, Andorra, San Marino, Malta, Vatican City. Luxembourg (2,586 km²) IS included. If user list includes microstates, either remove them or switch to 50m data. Check with: `world[world['NAME'].str.contains('Liechtenstein', case=False)]` — empty means excluded.

## Color palette (proven, 6-continent run)
```python
BG = '#fdfaf3'           # page background (warm off-white)
LAND_UNSHADED = '#e8e0d0'  # unshaded land — MUST be visibly distinct from BG
LAND_TARGET = '#7a9f58'    # shaded target countries
EDGE_ALL = '#b8af9a'       # country borders — visible on both land colors
EDGE_TARGET = '#5a7a3a'    # target country borders
```
Key lesson: unshaded land at `#f0ead6` was too close to `#fdfaf3` — continent looked like floating green blobs. `#e8e0d0` provides visible contrast.

## Mercator compensation (CRITICAL for high-latitude continents)
WGS84 geographic coordinates plotted without projection stretch countries horizontally at high latitudes. Scale factor = 1/cos(latitude). Europe at 52°N: 1.6× horizontal stretch — Italy looks fat, Scandinavia looks squashed.

Fix: `ax.set_aspect(1.0 / np.cos(np.radians(mid_lat)))` where mid_lat = (ymin+ymax)/2.

This stretches the y-axis display units to compensate. IMPORTANT: this means `Circle()` patches in data coordinates become oval. Use `scatter()` instead (markers are always round in display space).

## Numbered circles — MUST be perfectly round
**Use `ax.scatter()`, never `mpatches.Circle()`.** Circle patches in data coordinates get stretched by `set_aspect()`. Scatter markers are always circular in display space.

```python
# Compute circle size proportional to map width
pixels_per_deg = figsize[0] * dpi / (xmax - xmin)
marker_diameter_pt = 40 * 72 / dpi  # 40px diameter
scatter_size = np.pi * (marker_diameter_pt / 2) ** 2  # area in pt^2

# Perfectly round white circle
ax.scatter(cx, cy, s=scatter_size, c='white', edgecolors='none', zorder=10)
ax.annotate(str(i), (cx, cy), fontsize=6.5, fontweight='bold',
            color='#3a4f1f', ha='center', va='center', zorder=11)
```

## Point placement
Use `geom.representative_point()` — guaranteed inside polygon. `centroid` can fall outside for irregular shapes (crescents, multi-polygons, island chains).

A `near_edge` check (distance to bbox edge < circle_radius) was tried but produced excessive false positives — Italy, Switzerland, Belgium all triggered it despite being large enough. Removed. Use area threshold only for leader lines.

## Leader lines for tiny countries
For countries with area < 2.0 deg² at 110m (Qatar 1.0, Lebanon 1.0, Jamaica 1.1, Puerto Rico 0.8, Bahamas 1.4):

```python
if geom.area < 2.0:
    # Small dot on the country
    ax.scatter(cx, cy, s=scatter_size * 0.3, c='white', edgecolors='none', zorder=10)
    # Offset away from continent center, 4% of map width
    offset = (xmax - xmin) * 0.04
    label_x = cx + dx * offset; label_y = cy + dy * offset
    # Visible leader line (linewidth 1.2, not 0.6 — too thin to see)
    ax.plot([cx, label_x], [cy, label_y], color='#444444', linewidth=1.2, zorder=9)
    # Numbered circle at external label position
    ax.scatter(label_x, label_y, s=scatter_size, facecolors='white', edgecolors='none', zorder=10)
    ax.annotate(str(i), (label_x, label_y), fontsize=6.5, fontweight='bold',
                color='#3a4f1f', ha='center', va='center', zorder=11)
```

Pitfalls: linewidth < 1.0 is invisible at map scale. Offset of circle_radius × 3.5 was too small — use map-width percentage instead.

## Proven continent parameters (v4, 50m data, May 2026)

| Continent | NE field | Bbox [xmin,xmax,ymin,ymax] | Figsize | Notes |
|-----------|----------|----------------------------|---------|-------|
| Africa | 'Africa' | -25,60,-40,42 | 8×10 | |
| Europe | 'Europe' | -30,45,33,82 | 8×10 | Wider west for Greenland. 50m data. |
| Asia | 'Asia' | 25,150,-10,60 | 12×7 | |
| North America | 'North America' | -170,-30,5,85 | 9×10 | |
| South America | 'South America' | -85,-33,-58,15 | 6×11 | 50m data required — 110m fragments Chile. |
| Oceania | 'Oceania' | 110,180,-52,-5 | 10×8 | Wider west for Australia. 50m data. |

## Special continent handling
- **Greenland → Europe**: Politically Danish territory. Add to Europe continent list, remove from North America. Use `pd.concat([europe_region, greenland_row])`.
- **Australia → Oceania**: Add for geographical context even if not on user's list. Same concat pattern.
- **South America → 50m mandatory**: 110m Chile is a 2-part MultiPolygon with a visual gap in the southern fjords. 50m Chile has 31 connected parts — the country renders as continuous.

## Why GeoPandas, not AI image gen
AI models cannot do political geography: wrong countries shaded, numbers dropped/misplaced, borders approximate. File sizes 5-6× larger (1.2MB AI vs 200KB GeoPandas). GeoPandas = pixel-perfect borders, correct centroids, deterministic, smaller files.
