# HyperFrames Rendering Pitfalls

Collected from real composition failures. These supplement the main SKILL.md rules.

## Canvas-based Compositions Fail

Canvas rendering (even with `window.__timelines` registered synchronously) is detected as "async" by the HyperFrames capture engine. The engine waits up to 45 seconds for the timeline to register, then captures blank frames.

**Fix:** Use static HTML + CSS animations instead. All content must be in the initial DOM — no JS data generation at render time.

## JS-heavy DOM Generation

If JS code builds hundreds of DOM elements before registering `window.__timelines`, the capture engine may time out or start before content exists.

**Fix:** Pre-generate all HTML statically. If dynamic content is required, keep it minimal (< 50 elements) and register the timeline immediately after DOM generation, not after a setTimeout or callback.

## Minification Breaks Compositions

If a composition works in `preview` but renders blank in `render`, the minifier may have broken a script. Symptoms:
- Console shows "Unexpected token" or "Invalid or unexpected token"
- The minifier collapses comments into executable code

**Fix:** Remove or simplify complex template literals. Avoid `//` comments inside template literals. Use `/* */` block comments instead inside JS template strings.

## Seeded PRNG Required

`Math.random()` causes `non_deterministic_code` lint errors. Use mulberry32:

```javascript
function mulberry32(a) {
  return function() {
    let t = a += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
const rng = mulberry32(20260610); // seed to release date
```
