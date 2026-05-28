# Continent Map Generation Pipeline

Full GeoPandas + Natural Earth map generation code. Proven on all 6 continents.

## Shapefile Data
- Prefer **50m** resolution for South America (Chile fragmentation fix) and any continent with narrow countries
- **110m** is sufficient for Africa, Asia, North America, Europe, Oceania
- Files: `ne_50m_admin_0_countries.shp` or `ne_110m_admin_0_countries.shp` from naciscdn.org

## Name Mappings (Natural Earth names differ from common names)
```python
NAME_FIX = {
    "United Kingdom": "United Kingdom", "Czech Republic": "Czechia",
    "Russia": "Russia", "Turkey": "Turkey", "South Korea": "South Korea",
    "United States": "United States of America", "Bahama Islands": "Bahamas",
    "Puerto Rico": "Puerto Rico", "Greenland": "Greenland", "Bolivia": "Bolivia",
    "Dominican Republic": "Dominican Rep.",
}
```

## Proven Map Generation Function

```python
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def generate_continent_map(continent_name, target_countries, bbox, figsize, output_path):
    """Generate a clean continent map with shaded target countries and numbered circles."""
    world = gpd.read_file("ne_data/ne_110m_admin_0_countries.shp")
    
    # Filter region
    region = world[world['CONTINENT'] == continent_name].copy()
    
    # Special: Greenland → Europe
    if continent_name == "Europe":
        gl = world[world['NAME'] == 'Greenland'].copy()
        if len(gl) > 0:
            region = gpd.GeoDataFrame(pd.concat([region, gl], ignore_index=True))
    
    # Special: Australia → Oceania
    if continent_name == "Oceania":
        au = world[world['NAME'] == 'Australia'].copy()
        if len(au) > 0:
            region = gpd.GeoDataFrame(pd.concat([region, au], ignore_index=True))
    
    # Map target names to Natural Earth names
    ne_targets = [NAME_FIX.get(n, n) for n in target_countries]
    region['target'] = region['NAME'].isin(ne_targets)
    
    # Mercator compensation
    xmin, xmax, ymin, ymax = bbox
    mid_lat = np.radians((ymin + ymax) / 2)
    aspect = 1.0 / np.cos(mid_lat)
    
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=200)
    fig.patch.set_facecolor('#fdfaf3')
    ax.set_facecolor('#fdfaf3')
    
    # Unshaded land — MUST be visibly different from background
    non = region[~region['target']]
    non.plot(ax=ax, facecolor='#e8e0d0', edgecolor='#b8af9a', linewidth=0.4)
    
    # Target countries
    tgt = region[region['target']]
    tgt.plot(ax=ax, facecolor='#7a9f58', edgecolor='#5a7a3a', linewidth=0.5)
    
    # Calculate circle size
    pixels_per_deg = figsize[0] * 200 / (xmax - xmin)
    circle_radius_deg = 20 / pixels_per_deg
    marker_diameter_pt = 40 * 72 / 200
    scatter_size = np.pi * (marker_diameter_pt / 2) ** 2
    
    # Place numbered markers
    for i, name in enumerate(ne_targets, 1):
        row = region[region['NAME'] == name]
        if len(row) == 0:
            continue
        
        geom = row.geometry.iloc[0]
        rp = geom.representative_point()  # Guaranteed inside polygon
        cx, cy = rp.x, rp.y
        
        # Tiny country detection (area < 2.0 deg²)
        is_tiny = geom.area < 2.0
        
        if is_tiny:
            # Leader line: small dot on country → line → external label
            ax.scatter(cx, cy, s=scatter_size * 0.3, c='white', edgecolors='none', zorder=10)
            cont_cx, cont_cy = (xmin + xmax) / 2, (ymin + ymax) / 2
            dx, dy = cx - cont_cx, cy - cont_cy
            dist = np.sqrt(dx**2 + dy**2)
            dx, dy = dx / dist, dy / dist
            offset = (xmax - xmin) * 0.04
            label_x, label_y = cx + dx * offset, cy + dy * offset
            ax.plot([cx, label_x], [cy, label_y], color='#444444', linewidth=1.2, zorder=9)
            ax.scatter(label_x, label_y, s=scatter_size, facecolors='white', edgecolors='none', zorder=10)
            ax.annotate(str(i), (label_x, label_y), fontsize=6.5, fontweight='bold',
                       color='#3a4f1f', ha='center', va='center', zorder=11)
        else:
            # Circle directly on country — use scatter (always round, unlike Circle patches)
            ax.scatter(cx, cy, s=scatter_size, c='white', edgecolors='none', zorder=10)
            ax.annotate(str(i), (cx, cy), fontsize=6.5, fontweight='bold',
                       color='#3a4f1f', ha='center', va='center', zorder=11)
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect(aspect)
    ax.axis('off')
    
    fig.savefig(output_path, dpi=200, bbox_inches='tight', pad_inches=0.1,
                facecolor='#fdfaf3', edgecolor='none')
    plt.close(fig)
```

## Continent Configurations

```python
CONFIG = {
    "Europe":       {"bbox": (-30, 45, 33, 82), "figsize": (8, 10)},
    "Asia":         {"bbox": (25, 150, -10, 60), "figsize": (12, 7)},
    "North America":{"bbox": (-170, -30, 5, 85), "figsize": (9, 10)},
    "South America":{"bbox": (-85, -33, -58, 15), "figsize": (6, 11)},
    "Oceania":      {"bbox": (110, 180, -52, -5), "figsize": (10, 8)},
}
```

## Typst Display Settings

```typst
#image("europe_map.png", width: 100%, height: 120mm, fit: "contain")
```
Adjust height per continent based on aspect ratio and index density.

## Font Sizing per Continent (for country index on page 1)

```python
INDEX_FONT = {
    "Europe": "11pt",       # 16 countries
    "Asia": "9pt",          # 21 countries
    "North America": "10pt",# 14 countries
    "South America": "14pt",# 5 countries
    "Oceania": "14pt",      # 2 countries
}
```
Smaller font for continents with more countries to fit all entries on page 1.
