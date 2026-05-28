# Continent Map Pipeline — GeoPandas + Natural Earth → Typst PDF

Full pipeline for generating accurate continent reference maps with shaded target
countries and numbered circles. Avoids AI image generation (unreliable geography)
and uses real shapefile data.

## Setup (one-time)

```bash
brew install geopandas poppler typst
# Natural Earth 110m cultural vectors
mkdir -p ne_data
cd ne_data
curl -O https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip
unzip ne_110m_admin_0_countries.zip
```

## Map generation — Python script pattern (UPDATED v2)

```python
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image

world = gpd.read_file("ne_data/ne_110m_admin_0_countries.shp")
region = world[world['CONTINENT'] == 'Europe'].copy()
region['target'] = region['NAME'].isin(target_ne_names)

fig, ax = plt.subplots(1, 1, figsize=(7, 10), dpi=200)
fig.patch.set_facecolor('#fdfaf3'); ax.set_facecolor('#fdfaf3')

# Non-target: distinct beige — must be visibly different from BG
non = region[~region['target']]
non.plot(ax=ax, facecolor='#e8e0d0', edgecolor='#b8af9a', linewidth=0.4)
tgt = region[region['target']]
tgt.plot(ax=ax, facecolor='#7a9f58', edgecolor='#5a7a3a', linewidth=0.5)

# Mercator compensation
mid_lat = np.radians((ymin + ymax) / 2)
ax.set_aspect(1.0 / np.cos(mid_lat))

# Compute circle size proportional to figure
pixels_per_deg = figsize[0] * 200 / (xmax - xmin)  # 200=dpi
circle_radius_deg = 20 / pixels_per_deg  # ~40px diameter
marker_diameter_pt = 40 * 72 / 200  # 14.4 pt
scatter_size = np.pi * (marker_diameter_pt / 2) ** 2

# Place markers — use scatter() NOT Circle patches (patches stretch with aspect)
for i, name in enumerate(target_ne_names, 1):
    row = region[region['NAME'] == name]
    geom = row.geometry.iloc[0]
    rp = geom.representative_point()  # guaranteed inside polygon (not centroid!)
    cx, cy = rp.x, rp.y
    
    area_deg2 = geom.area
    is_tiny = area_deg2 < 2.0  # Qatar, Lebanon, Jamaica, Caribbean islands
    
    if is_tiny:
        # LEADER LINE: dot on country → line → circle outside
        ax.scatter(cx, cy, s=scatter_size * 0.3, c='white', edgecolors='none', zorder=10)
        # Offset away from continent center
        cont_cx = (xmin + xmax) / 2; cont_cy = (ymin + ymax) / 2
        dx, dy = cx - cont_cx, cy - cont_cy
        dist = np.sqrt(dx**2 + dy**2) or 0.01
        dx, dy = dx/dist, dy/dist
        offset = (xmax - xmin) * 0.04  # 4% of map width
        lx, ly = cx + dx * offset, cy + dy * offset
        ax.plot([cx, lx], [cy, ly], color='#444444', linewidth=1.2, zorder=9)
        ax.scatter(lx, ly, s=scatter_size, facecolors='white', edgecolors='none', zorder=10)
        ax.annotate(str(i), (lx, ly), fontsize=6.5, fontweight='bold',
                    color='#3a4f1f', ha='center', va='center', zorder=11)
    else:
        # Direct circle — scatter() stays perfectly round regardless of aspect
        ax.scatter(cx, cy, s=scatter_size, c='white', edgecolors='none', zorder=10)
        ax.annotate(str(i), (cx, cy), fontsize=6.5, fontweight='bold',
                    color='#3a4f1f', ha='center', va='center', zorder=11)

ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
ax.axis('off')
fig.savefig("continent_map.png", dpi=200, bbox_inches='tight', pad_inches=0.1,
            facecolor='#fdfaf3', edgecolor='none')
```

**Key: scatter() vs Circle patches.** Matplotlib `Circle` patches stretch with
`set_aspect()` — they become ovals at Mercator-compensated aspect ratios. `scatter()`
markers are defined in display space (points) and stay perfectly round. Prefer scatter
for all map markers.

**Key: representative_point() vs centroid.** `centroid` can fall outside irregular
polygons (especially multi-part countries like Italy with islands). `representative_point()`
is guaranteed inside the polygon. Always use it for marker placement.

**Key: Leader lines for tiny countries.** Countries with area < 2.0 square degrees
(Qatar, Lebanon, Jamaica, Puerto Rico, Bahamas) cannot fit a numbered circle without
border overlap. Pattern: small dot ON the country → visible dark line (1.2pt) → full-size
white circle placed 4% of map width away from continent center. Thicker lines are
essential — 0.6pt lines are invisible at map resolution.

## Per-continent bounding boxes and settings

| Continent      | BBox (xmin,xmax,ymin,ymax) | Figsize | Mid-lat | Aspect | Map height (Typst) |
|----------------|---------------------------|---------|---------|--------|-------------------|
| Africa         | (-25, 60, -40, 42)        | (8,10)  | 1°N     | ~1.0   | 155mm             |
| Europe         | (-15, 42, 33, 72)         | (7,10)  | 52.5°N  | ~1.64  | 120mm             |
| Asia           | (25, 150, -8, 58)         | (12,7)  | 25°N    | ~1.10  | 125mm             |
| North America  | (-170, -30, 5, 85)        | (9,10)  | 45°N    | ~1.41  | 140mm             |
| South America  | (-85, -33, -58, 15)       | (6,11)  | 21.5°S  | ~1.07  | 155mm             |
| Oceania        | (110, 180, -52, -5)       | (10,8)  | 28.5°S  | ~1.14  | 155mm             |

**Oceania:** Extend bbox west to 110°E to include Australia even when it's not in Natural Earth's "Oceania" continent (NE puts Australia in its own continent). Merge Australia from NE into the Oceania region: `region = gpd.GeoDataFrame(pd.concat([oceania, australia_row], ignore_index=True))`. Always include Australia even if not on the original list — an Oceania map without Australia looks empty and confusing.

**Greenland:** Politically a Danish territory — include in Europe, not North America. Natural Earth classifies it as "North America", so manually add it to the Europe region and remove from North America targets. Update both continent lists.

## Natural Earth name mappings

The 110m shapefile uses abbreviated/alternate names. Common mismatches:

| User name           | Natural Earth NAME    |
|---------------------|-----------------------|
| United Kingdom      | United Kingdom        |
| Czech Republic      | Czechia               |
| Russia              | Russia                |
| Turkey              | Turkey                |
| South Korea         | South Korea           |
| United States       | United States of America |
| Bahama Islands      | Bahamas               |
| Dominican Republic  | Dominican Rep.        |
| Congo               | Congo                 |
| South Africa        | South Africa          |

## Microstates not in 110m shapefile

Liechtenstein, Monaco, San Marino, Andorra, Malta, Vatican City — all too small for
the 110m resolution. Remove from country list. If needed, use 50m or 10m resolution
shapefiles (larger files, slower).

## When 110m chops narrow countries — use 50m

The 110m resolution simplifies narrow coastal countries into disconnected polygons.
Chile is the canonical example: at 110m it renders as 2 parts (mainland + southern tip)
with a visual gap between them. The `representative_point()` falls in the southern
fragment, placing the circle at the bottom of the map instead of the mainland side.

**Fix:** Download and use Natural Earth 50m cultural vectors:
```bash
cd ne_data
curl -LO https://nacisdns.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip
unzip -o ne_50m_admin_0_countries.zip "*.shp" "*.shx" "*.dbf" "*.prj"
```

50m Chile: 31 connected parts (vs 2 at 110m), rep_point naturally falls in central
Chile (~-71.5, -35.7). The 50m file is ~1.5MB — negligible performance difference.
Column names identical to 110m (drop-in replacement). South America benefits most;
other continents work fine at 110m but 50m gives better coastlines everywhere.

When a country appears fragmented or circles land in unexpected locations, try 50m
before changing marker placement logic.

## Font size scaling for country index (Typst page 1)

The bold country index below the map must fit ALL entries on page 1. A4 available
height (297mm - 18mm margins) = 279mm. Map + title + instructions consume 140-180mm,
leaving 99-139mm for the index. At default 1.2em leading:

| Countries | Font   | Leading | Fits on page? |
|-----------|--------|---------|---------------|
| 1-10      | 14pt   | 0.65em  | ✓ (plenty)    |
| 11-15     | 11-12pt| 0.5em   | ✓             |
| 16-20     | 10pt   | 0.45em  | ✓ (tight)     |
| 21+       | 9pt    | 0.45em  | ✓ (very tight)|

Always compile and verify the last index entry is visible. Entries silently overflow
off the bottom — Typst gives no warning.

## QC workflow — mandatory publisher-grade review

**Three-hat QC.** Before delivering any PDF, wear three hats:

1. **Compliance hat:** Count ALL entries. Verify index count matches map circles. Verify
   every numbered circle on the map has a corresponding index entry. Verify every index
   entry has a shaded country on the map. Page numbers correct throughout.

2. **QC hat:** Convert EVERY page to PNG via `pdftocairo` and run `vision_analyze` on
   each. Check: map visible (not blank), continent shape coherent (not floating blobs),
   circles perfectly round (not oval), no circles on borders, leader lines visible for
   tiny countries, no text cut-off, all languages present for every country, Chinese
   is Traditional (繁體) not Simplified, Japanese has furigana readings.

3. **Publisher hat:** Is it pleasant to read? Would you hand this to a classroom of
   students? Are font sizes consistent between map page and definition pages? Does the
   continent shape look natural (not squashed)? Do unshaded countries form a visible
   landmass or disconnected green patches? Would this look professional printed?

**Subagents are NOT reliable for QC.** `delegate_task` crashes with `'NoneType' object
is not iterable` for visual review. Use direct `vision_analyze` on `pdftocairo`-converted
PNGs. Convert every page — don't spot-check page 1 only. Asia had a blank page 1 issue
that only showed up on full-page review.

**Blank page detection:** Content pages from pdftocairo >50KB. Pages <10KB are blank
or nearly blank — investigate immediately. 100% white pixels = the map image failed
to render (likely corrupted Typst source from execute_code write_file bug).

1. **Unshaded land blending into background.** If unshaded countries are too close to the
   page background color (`#fdfaf3`), the continent looks like floating green blobs
   rather than a coherent landmass. Unshaded land must use a visibly distinct color:
   `#e8e0d0` (not `#f0ead6`). Borders between unshaded countries must be visible
   (`#b8af9a`, linewidth 0.4). During QC, ask: "Is the continent shape clearly visible
   as a unified landmass, or does it look like disconnected green patches?"

2. **Never pass read_file output to write_file in execute_code.** `read_file` returns
   content WITH line-number prefixes ("     1|content"). `write_file` writes it
   verbatim, corrupting Typst/source files. The file compiles with exit 0 but produces
   blank pages. Fix: use the `patch` tool for edits, or strip line-number prefixes
   before writing.

3. **pdftocairo for page conversion, not sips.** `sips` cannot extract specific PDF
   pages. Use `pdftocairo -png -f N -l N -singlefile -scale-to 1200`.

4. **Blank page detection.** Content pages from pdftocairo >50KB. Blank pages <10KB.
   Check file size before running vision QC.

5. **Country index silently overflows.** Entries that don't fit on page 1 disappear off
   the bottom with NO Typst warning. Always convert page 1 to PNG and vision-check that
   the LAST index entry is visible. Count them.

6. **`#text()` does NOT propagate into Typst list blocks.** Wrapping a `- list item`
   inside `#text(size: 14pt, weight: "bold")[...]` does NOT apply the formatting to the
   list entries. Lists have their own styling. Use per-line `#text()` calls instead:
   ```typst
   #text(size: 14pt, weight: "bold")[1. Kenya — 肯亞 — ケニア]
   #text(size: 14pt, weight: "bold")[2. Uganda — 烏干達 — ウガンダ]
   ```
   Do NOT use:
   ```typst
   #text(size: 14pt, weight: "bold")[
   - 1. Kenya — 肯亞 — ケニア
   - 2. Uganda — 烏干達 — ウガンダ
   ]
   ```
