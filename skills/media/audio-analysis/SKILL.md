---
name: audio-analysis
description: "Audio analysis toolkit — genre, BPM, key, spectral features using Essentia. Use for track categorization, DJ set prep, and music projects."
version: 1.0.0
---

# Audio Analysis

Uses Essentia (installed in Hermes venv) to analyze audio files.

## Quick Analysis

```bash
/Users/lyndonarthurson/.hermes/hermes-agent/venv/bin/python3 -c "
import essentia.standard as es
audio = es.MonoLoader(filename='PATH', sampleRate=44100)()
# RhythmExtractor2013 returns a tuple: (bpm, beats, confidence, estimates, beats_intervals)
bpm, beats, conf, _, _ = es.RhythmExtractor2013(method='multifeature')(audio)
key, scale, strength = es.KeyExtractor()(audio)
# Use SpectralCentroidTime (not SpectralCentroid — that's the old API)
cents = es.SpectralCentroidTime()(audio)
print(f'BPM: {bpm:.0f} (conf={conf:.0%})  Key: {key} {scale} ({strength:.0%})  Centroid: {cents:.0f} Hz')
"
```

**NOTE:** Essentia v2.1 API uses `SpectralCentroidTime()` (returns float), not `SpectralCentroid()` (removed). `RhythmExtractor2013` returns 5-tuple, not a Pool.

## Genre Reference

| BPM Range | Genre |
|-----------|-------|
| 170-180 | Drum & Bass |
| 160-170 | Jungle / slower DnB / footwork |
| 130-150 | Dubstep / UK Bass / Halftime |
| 120-130 | House / Techno |
| 110-120 | Hip-hop / Breaks |
| 80-110 | Downtempo |

## Spectral Centroid hints
- < 600 Hz: Sub-heavy (dubstep, deep DnB)
- 600-1200 Hz: Balanced (jungle, UK bass)
- 1200-2000 Hz: Mid-forward (neurofunk, techstep)
- > 2000 Hz: Bright (liquid DnB, melodic house)
