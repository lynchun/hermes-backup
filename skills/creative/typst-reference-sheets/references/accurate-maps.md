# Accurate Country Maps with Natural Earth + GeoPandas

AI image generation (GPT-5-image-mini, etc.) CANNOT produce accurate political maps.
It doesn't know country borders, names, or positions. For reference sheets that need
correct country highlighting, use this programmatic approach.

## Setup (one-time)

```bash
pip3 install geopandas matplotlib
```

Natural Earth shapefile download (110m resolution, ~5MB):
```bash
mkdir -p ne_data && cd ne_data
curl -O https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip
unzip ne_110m_admin_0_countries.zip
```

## Generate a continent map with shaded targets + numbered circles

```python
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

SHP = "ne_data/ne_110m_admin_0_countries.shp"
world = gpd.read_file(SHP)
region = world[world['CONTINENT'] == 'Africa'].copy()

target_names = ['Kenya', 'Uganda', 'Congo', 'Tanzania', 'South Africa',
                'Namibia', 'Angola', 'Gabon', 'Madagascar', 'Libya']
region['target'] = region['NAME'].isin(target_names)

fig, ax = plt.subplots(1, 1, figsize=(8, 10), dpi=200)
fig.patch.set_facecolor('#fdfaf3')
ax.set_facecolor('#fdfaf3')

# Non-target: pale beige
region[~region['target']].plot(ax=ax, facecolor='#f0ead6', edgecolor='#c4b998', linewidth=0.3)

# Target: olive green
region[region['target']].plot(ax=ax, facecolor='#7a9f58', edgecolor='#5a7a3a', linewidth=0.5)

# Numbered circles — NO border (Lyndon prefers borderless)
CIRCLE_RADIUS = 0.8
for i, name in enumerate(target_names, 1):
    row = region[region['NAME'] == name]
    if len(row) == 0:
        continue
    centroid = row.geometry.centroid.iloc[0]
    x, y = centroid.x, centroid.y
    circle = mpatches.Circle((x, y), CIRCLE_RADIUS, facecolor='white',
                              edgecolor='none', zorder=10)
    ax.add_patch(circle)
    ax.annotate(str(i), (x, y), fontsize=6.5, fontweight='bold',
                color='#3a4f1f', ha='center', va='center', zorder=11)

ax.set_xlim(-25, 60)   # Africa bounds
ax.set_ylim(-40, 42)
ax.axis('off')

fig.savefig('africa_map.png', dpi=200, bbox_inches='tight', pad_inches=0.1,
            facecolor='#fdfaf3', edgecolor='none')
```

## All-continents batch generation

See the reference script at `gen_all_maps.py` in the Country_Reference project for a single-pass script that generates all 5 continent maps. Key patterns:

- **Continent bounding boxes** (for `ax.set_xlim/ylim`):
  - Europe: (-25, 45, 33, 72)
  - Asia: (25, 150, -10, 60)
  - North America: (-170, -30, 5, 85)
  - South America: (-85, -30, -60, 15)
  - Oceania: (160, 180, -50, -25)

- **Figure sizes** (for proportional maps):
  - Europe: (10, 8), Asia: (12, 8), N. America: (10, 9), S. America: (6, 10), Oceania: (6, 8)

- **Natural Earth continent names**: 'Africa', 'Europe', 'Asia', 'North America', 'South America', 'Oceania'

## Natural Earth name mapping

Some country names in user lists differ from Natural Earth. Common mappings:

| User name | Natural Earth `NAME` |
|---|---|
| United Kingdom | United Kingdom |
| Czech Republic | Czechia |
| United States | United States of America |
| Bahama Islands | Bahamas |
| South Korea | South Korea |
| Republic of South Africa | South Africa |

Use `region['NAME'].unique()` to list all available names in a continent and find matches.

## Map sizing for Typst/A4 portrait

In Typst: `image("africa_map.png", width: "100%", height: Nmm, fit: "contain")`

Proven heights from 6-continent delivery (A4, 10mm/8mm/14mm margins):
- **Africa**: 155mm (10 countries, 14pt index)
- **Europe**: 140mm (15 countries, 11pt index)
- **Asia**: 125mm (21 countries, 9pt index — less height to leave room for the long index)
- **North America**: 140mm (15 countries, 10pt index)
- **South America**: 155mm (5 countries, 14pt index — tall/narrow continent)
- **Oceania**: 155mm (1 country, 14pt index — fill the page)

The map height must leave enough room for the country index below. Rule of thumb: allocate ~65mm for title+instructions+footer, then subtract index height (font_size × count × leading × ~0.35 mm/pt) from the remainder. Test by compiling and verifying the last index entry is visible.

Always save with `facecolor='#fdfaf3'` (warm beige) to match the Typst page background — no white rectangle edge.

## Key facts
- **Use borderless circles** (`edgecolor='none'`) — Lyndon prefers these over black-bordered circles
- Country names must match Natural Earth `NAME` field EXACTLY
- Natural Earth field names: `'NAME'` (country), `'CONTINENT'` (e.g., 'Africa')
- The old `gpd.datasets.get_path('naturalearth_lowres')` is deprecated — use downloaded shapefiles
- Centroids work with geographic CRS (warning is harmless for visual placement)
- DPI 200+ for clean print output
- Save with `bbox_inches='tight'` + `pad_inches=0.1`
