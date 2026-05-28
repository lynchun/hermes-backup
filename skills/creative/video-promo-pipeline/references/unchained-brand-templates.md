# Unchained Recordings Brand Templates

Label-specific design language and template library for Unchained Recordings promos.

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

**Every video must hit the drop** — the moment the main energy climax of the track section enters. Not just any beat, but the primary energy peak.

### Implementation
1. Analyse the track before building (RMS energy over time, see umbrella audio analysis section)
2. Offset the audio start so the video's climax moment aligns with the drop
3. Structure: build-up during low energy → climax ON the drop → fade out after

## Template 1: Face-Left / Name-Right

Reference videos: Cesco, OAKK, Groves

### Structure

| Scene | Time | Content |
|-------|------|---------|
| Logo intro | During build-up | Unchained logo fades in centre. Label name below. |
| Face reveal | ON the drop | Artist face (bg removed) slides in from left. Text appears right-aligned. |
| Outro | After drop | Logo returns + "OUT NOW" |

### Layout
- **Left side:** Artist face, isolated from cover art, positioned at ~25% from top, 80px from left. 350-400px wide. No circular crop — raw silhouette.
- **Right side:** Three text elements, right-aligned, 60px from right edge:
  - Artist name: 96px, blue (#2266cc), letter-spacing 6px
  - Track title: 82px, purple (#8844aa), letter-spacing 4px
  - EP label: 48px, red (#ff3355), letter-spacing 5px
- All text uses Unchained custom font (blocky, all-caps)
- Text sizes must be uniform across all videos for the same element type

## Template 2: Zoom-Out Reveal

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

### Critical: Static HTML Only
Do NOT generate ASCII data dynamically via JS then animate with GSAP. HyperFrames frame capture reads `window.__timelines` synchronously on page load. If JS runs too long building DOM, capture starts before content exists — blank frames.

**Correct approach:** Pre-generate all rows of ASCII text as static `<div>` elements. Assign each row a CSS animation class. Use `@keyframes` for all motion — GSAP only for overlay effects.

### Timing Sequence (15-second promo)

| Time | Event |
|------|-------|
| 0-2s | Fade in from black, chaotic ASCII flickers |
| 2-4s | Fragment rows begin pulsing — UNCHAINED, catalogue number visible |
| 4-7s | Artist name emerges, glitches, fades, reappears |
| 7-10s | EP title decodes from data |
| 10-12s | Track names appear as remix nodes |
| 12-14s | Release date emerges as deployment date |
| 14-15s | Final decoded message peaks, then collapses |

## Beat-Sync Rules
- Edits (cuts, reveals, text entrances) land ON the kick or snare, never between
- Slow motion / gentle moves during low-energy sections
- Fast dynamic moves on the drop
- Energy of visuals follows energy of music — always

## Project Location

`~/Unchained/unchained-promos/` — HyperFrames project
`assets/audio/` — track WAVs
`assets/covers/` — cover art and extracted face images
`assets/logo/` — Unchained logo PNGs
`assets/fonts/` — Unchained font TTF
