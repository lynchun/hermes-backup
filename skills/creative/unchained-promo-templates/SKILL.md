---
name: unchained-promo-templates
description: Promo video templates for Unchained Recordings — drop-synced editing, face-left/name-right layout, template patterns, and brand guidelines. Use when building any promo video for this DnB label.
---

# Unchained Promo Video Templates

Brand guidelines and template system for Unchained Recordings promotional videos.

## Brand Identity

**Logo:** Unchained Recordings — two clenched fists facing each other at top, broken chain at bottom, text in industrial blocky sans-serif. Monochrome (white on black).

**Font:** Custom "Unchained" font (blocky, angular, all-caps). Can use similar fallback: bold sans-serif with sharp angles.

**Colour Palette:**
- Primary: Black (#000) background, white text
- Accent blue: #2266cc (artist names)
- Accent purple: #8844aa (track titles)
- Accent red: #ff3355 (EP labels, important text)

**Cover Art Style:** Graphic novel / cel-shaded / comic-book aesthetic. Heavy black ink outlines, high-contrast, bold colours. Darker/neon-noir mood.

## The Core Principle: Drop-Synced Editing

The single most important rule: **every video must hit the drop.**

### What "the drop" means
The drop = the moment the big beat/energy enters. Not just any beat, but the **main energy climax** of the track section being used.

### How to implement drop sync
1. **Analyse the track** before building. Find the drop time(s) using energy analysis (RMS loudness over time).
2. **Offset the audio start** so that the video's climax moment aligns with the drop.
3. Structure: build-up during low energy → climax ON the drop → fade out after.

### Example: Shaddows Deep Blue
- Audio starts at ~0:25-0:30 during build-up
- First drop hits at 0:45
- Second drop hits at 3:06-3:07
- Video climax (face reveal, text entrance) lands EXACTLY on the drop

## Template 1: Face-Left / Name-Right

Reference videos: Cesco, OAKK, Groves

### Structure
| Scene | Time | Content |
|-------|------|---------|
| Logo intro | During build-up | Unchained logo fades in centre. Label name below. |
| Face reveal | ON the drop | Artist face (bg removed) slides in from left. Text appears right-aligned. |
| Outro | After drop | Logo returns + "OUT NOW" |

### Layout
- **Left side:** Artist face, isolated from cover art (background removed), positioned at ~25% from top, 80px from left. 350-400px wide.
- **Right side:** Three text elements, right-aligned, 60px from right edge:
  - Artist name: 96px, blue (#2266cc), letter-spacing 6px
  - Track title: 82px, purple (#8844aa), letter-spacing 4px
  - EP label: 48px, red (#ff3355), letter-spacing 5px
- **All text uses Unchained custom font** (blocky, all-caps)
- **Text sizes must be uniform** (same size for same element type across all videos)
- **Text should be 100% bigger** than initial drafts — be generous with font sizes

### Beat-Sync Rules
- Edits (cuts, reveals, text entrances) should land **ON the kick or snare**, never between
- Slow motion / gentle moves during low-energy sections
- Fast dynamic moves on the drop
- Energy of visuals follows energy of music — always

### Face Extraction
- Crop the face from the cover art (just head, beanie/hat, glasses — NO background or jacket)
- Use precise pixel coordinates from vision analysis
- Remove background so it sits on pure black
- Position as standalone figure, no circular crop needed — raw silhouette

## Template 2: Zoom-Out Reveal (overused but keep as option)

Artist name starts MICRO (tiny) → zooms OUT to MACRO revealing full name + EP title on the drop. The reveal is an expansion — tension builds as the name enlarges.

## Template 3: Cover Slide-Through

Quick slides through cover art images build tension before artist/EP reveal. Cuts land on kick/snare. Reference: Lost Sirens style.

## Template 4: TV Test Pattern Intro

Test pattern image + artist name + catalogue number. Retro, suspense-building before the drop.

## Template 5: Dripping Numbers Intro

Dripping numbers animate around Unchained logo. Creates suspension before drop, raises brand profile.

## Template 6: Marvel-Style 3D (external commission)

3D graphics with covers flowing dynamically through text. Commissioned from Fiverr. Reference only — not for automated generation.

## Template 7: Data-Transmission / Chaotic ASCII Terminal

Reference: Promo for SHADDOWS — LON3LY EP (May 2026)

### Concept
The release info is embedded inside a dense field of scrolling, corrupted ASCII characters — like an intercepted bass transmission. The viewer feels chaos first, then slowly realises the chaos contains the release data.

### Ratio
- 70% random chaotic ASCII characters (dim blue/grey)
- 15% corrupted label/release fragments (semi-readable)
- 10% semi-readable release metadata
- 5% clear final decoded message

### Colour Palette (terminal mode)
- Background: deep navy/blue-black (#050a18), radial glow (#0a1a3a at centre)
- Primary text: dim blue (#2a4a7a, #4a6a9a)
- Readable fragments: pale blue (#6a9fd8), cyan (#40c4e0), white-blue (#b8d4f0)
- Highlights (sparing): amber (#e8a030), yellow (#f0d050)
- Background effects: scanlines, CRT flicker, vignette, blue glow pulse, static noise

### How to Build (HyperFrames)

**CRITICAL PITFALL: Do NOT generate the ASCII data dynamically via JS then animate with GSAP.** The HyperFrames frame capture engine reads `window.__timelines` synchronously on page load — if JS runs too long building DOM before registering the timeline, capture starts before any content exists, producing blank frames.

**Correct approach: Static HTML with CSS animations.**

1. Pre-generate all rows of ASCII text as static `<div>` elements
2. Assign each row a CSS animation class for movement (jitter, scroll-left, scroll-right, drift-slow, drift-fast)
3. Use `@keyframes` for all motion — GSAP only for overlay effects (glitch flashes, screen pulses)
4. Embed release fragments at specific row indices, not randomly
5. Use seeded PRNG (mulberry32 seeded to release date) so renders are deterministic
6. Fragment rows get `frag-pulse` CSS animation for pulsing glow visibility
7. GSAP timeline should be minimal and register synchronously after DOM

### Fragment Embedding Strategy
- Assign each fragment a fixed row number
- Centre the text in the row with slight horizontal offset
- Corrupt ~12% of characters within fragments
- Three layers of fragment visibility:
  - Layer 1 (amber/yellow): core release data (SHADDOWS, LON3LY_EP, UNCH053, 10_JUNE_2026, PENRYN, SWEETPEA)
  - Layer 2 (blue/white): system metadata (SIGNAL_LOCKED, BASS_SIGNAL, TRANSMISSION_ACTIVE, EP_DEPLOYED)
  - Layer 3 (dim): filler terminal code lines (look like code but are just decorative)

### How to Build (HyperFrames) — CRITICAL

**PITFALL — Do NOT generate the ASCII data dynamically via JS then animate with GSAP.** The HyperFrames frame capture engine reads `window.__timelines` synchronously on page load. If JS runs too long building DOM before registering the timeline, capture starts before any content exists — blank frames.

**Correct approach: Static HTML with CSS animations.**

1. Pre-generate ALL rows of ASCII text as static `<div>` elements in the HTML
2. Assign each row a CSS animation class for movement (jitter, scroll-left, scroll-right, drift)
3. Use `@keyframes` for all motion — GSAP only for overlay effects (glitch flashes, screen pulses)
4. Embed release fragments at specific row indices (not randomly)
5. Use seeded PRNG (mulberry32 seeded to release date) for deterministic renders
6. Fragment rows get a `frag-pulse` CSS animation for pulsing glow visibility
7. GSAP timeline should be minimal and register synchronously after the DOM

**Canvas approach also fails** — even if `window.__timelines` is registered synchronously, HyperFrames detects canvas-based compositions as "async" and waits before capturing, often causing timeout issues.

### Timing Sequence (15-second promo)

| Time | Event |
|------|-------|
| 0-2s | Fade in from black, chaotic ASCII flickers, mostly unreadable |
| 2-4s | Fragment rows begin pulsing — UNCHAINED, UNCH053 visible briefly |
| 4-7s | SHADDOWS emerges, glitches, fades, reappears (glitch flash at 4s) |
| 7-10s | LON3LY_EP decodes from data (bass-hit glitch at 7s) |
| 10-12s | PENRYN / SWEETPEA appear as remix nodes (glitch at 10s) |
| 12-14s | 10_JUNE_2026 emerges as deployment date (screen flash at 12s) |
| 14-15s | Final decoded message peaks, then collapses (pulse at 14s) |

### Core Principles (Apply to ALL templates)

1. **Every cut, reveal, and transition must land ON the kick or snare** where it creates emotive effect
2. **Visual energy follows music energy** — slow during build-up, dynamic on the drop
3. **Unchained logo** appears at various points: sometimes on beat, sometimes start/end, sometimes throughout
4. **Tension and anticipation** before any reveal is a core theme — build first, release on the drop
5. **Face must be isolated from cover art background** — sits alone on black
6. **Text sizes are uniform** across all videos for the same element type
7. **Text must be large** — 100% bigger than what feels natural for print/web
8. **Drops:** First drop is primary, second drop can be used as alternative

## Audio Analysis Reference

Always analyse the track's structure before building:
- Use RMS energy analysis (100ms windows) over first 90s
- Drop = sustained section above 80dB threshold
- Build-up = section ramp from ~75dB to 80dB
- Note both first and second drop times

## Project Location

`~/Unchained/unchained-promos/` — HyperFrames project
`assets/audio/` — track WAVs
`assets/covers/` — cover art and extracted face images
`assets/logo/` — Unchained logo PNGs
`assets/fonts/` — Unchained font TTF
