# SHADDOWS — LON3LY EP: Data-Transmission Fragment Seed Data

Session: 24 May 2026 — First successful data-transmission template build.

## Seeded Release Data to Embed

### Layer 1 — Core Release Fragments (amber/yellow highlights)

```
UNCHAINED
UNCHAINED_RECORDINGS
UNCH053
SHADDOWS
SH4DD0WS
LON3LY_EP
LON3LY
PENRYN
SWEETPEA
10_JUNE_2026
PENRYN_REMIX
SWEETPEA_REMIX
```

### Layer 2 — System Metadata (blue/white)

```
BASS_SIGNAL
SIGNAL_LOCKED
TRANSMISSION_ACTIVE
NEW_RELEASE
EP_DEPLOYED
RELEASE_DEPLOYED
STREAM_BUY_SUPPORT
LOW_FREQUENCY
DNB
HALFTIME
BASS_MUSIC
PRE_SAVE
OUT_NOW
OUT_N0W
```

### Layer 3 — Filler Terminal Code Lines (decorative only)

```
0x77A//91x4b..r3l++s1gnal::0dB///001101..x..
/r3l3ase_packet##??----OUT_N0W----//err_404
bpm_174//low_frequency//xXx__str3am__xXx
DEPLOY_DATE//confirmed//0101///UNCH053--
++s1gnal.locked::0dB///001101//BASS_SIGNAL..
----REMIX_NODE----OUT_N0W----//err_905--
xXx__str3am_buy_support__xXx//LOW_FREQUENCY
0101///UNCH053--R3L3ASE//DEPLOYED--0110
..?.?.? SIGNAL LOCK BASS//LOW_FREQ//UNCH053
1 0 _ J U N E _ 2 0 2 6 //// corrupted////
O U T _ N O W //// decoded////TRANSMISSION
0xFF//d3pl0y_c0nf1rm3d//914b..r3l++s1gnal
bpm_174//low_frequency//xXx__catalogue__xXx
PRE_SAVE//DEPLOY_DATE//confirmed//0101//xXx
HALFTIME//BASS_SIGNAL//LOW_FREQ//UNCH053//
err_404//str3am_buy_support//DEPLOYED--0110
xXx__DNB__xXx//low_frequency//TRANSMISSION
0101///SIGNAL_LOCKED--0110..?.?.? BASS SIGNAL
##??----TRANSMISSION_ACTIVE----//err_404----
0xDE//AD//BEEF//c0rrupt3d//s1gnal//l0st//
```

## Row Assignment (75 rows, 55 chars wide)

| Row | Fragment | Colour |
|-----|----------|--------|
| 3 | LOW_FREQUENCY | dim |
| 5 | BASS_SIGNAL | blue |
| 7 | DNB | white |
| 8 | UNCHAINED | amber |
| 10 | SIGNAL_LOCKED | white |
| 12 | UNCHAINED_RECORDINGS | amber |
| 14 | HALFTIME | dim |
| 15 | UNCH053 | yellow |
| 17 | BASS_MUSIC | blue |
| 18 | TRANSMISSION_ACTIVE | blue |
| 20 | NEW_RELEASE | white |
| 22 | SHADDOWS | amber |
| 25 | SH4DD0WS | amber |
| 28 | EP_DEPLOYED | blue |
| 30 | LON3LY_EP | yellow |
| 33 | LON3LY | yellow |
| 35 | RELEASE_DEPLOYED | white |
| 38 | PENRYN | cyan |
| 40 | SWEETPEA | cyan |
| 42 | PENRYN_REMIX | cyan |
| 44 | SWEETPEA_REMIX | cyan |
| 45 | PRE_SAVE | white |
| 48 | 10_JUNE_2026 | yellow |
| 50 | STREAM_BUY_SUPPORT | blue |
| 52 | OUT_NOW | amber |
| 54 | OUT_N0W | amber |

Filler code lines at rows: 2, 6, 16, 26, 36, 46, 56, 65

## Seeded PRNG

Use mulberry32 seeded to `20260610` (release date) for deterministic rendering:
```js
function mulberry32(a) {
  return function() {
    let t = a += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
const rng = mulberry32(20260610);
```

## CSS Animation Classes for Row Movement

```css
.scroll-right { animation: scrollRight 8s linear infinite; }
.scroll-left { animation: scrollLeft 6s linear infinite; }
.jitter { animation: jitter 0.3s infinite alternate; }
.drift-slow { animation: driftSlow 12s ease-in-out infinite alternate; }
.drift-fast { animation: driftFast 4s ease-in-out infinite alternate; }
```

Assign classes cyclically: row%5=jitter, row%7=scroll-right, row%9=scroll-left, row%11=drift-slow, remainder=jitter.

## Background Layers (z-order)

| z-index | Layer |
|---------|-------|
| 1 | Blue glow pulse (CSS animation breathe 4s) |
| 2 | Data field (text content) |
| 97 | Glitch flash overlay (GSAP-driven) |
| 98 | Vignette |
| 99 | Scanlines |
| 100 | CRT flicker (CSS animation 0.08s) |
| 101 | Static noise (CSS animation 0.5s) |

## Known Issues / Pitfalls

- **CPU-heavy**: 75 rows x 55 cols = 4125 spans with individual colour/opacity. Render took ~4 minutes on Mac. Consider reducing to ~50 rows for faster renders.
- **Font rendering**: Use `Courier New` — the Unchained font doesn't work for variable-width ASCII. Reserve custom font for title overlays only.
- **Audio offset**: This template is visual-only driven. Audio should be analysed separately for drop-sync if adding music bed.
