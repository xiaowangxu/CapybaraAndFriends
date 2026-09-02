# CardGrid Design QA

- Source visual truth: `C:\Users\XIAOWA~1\AppData\Local\Temp\codex-clipboard-65fb709f-6cd5-4dea-a74a-6b769ab90001.png`
- Source pixels: 2498 × 1193
- Implementation: `http://127.0.0.1:5173/CapybaraAndFriends/`
- Implementation screenshot: Codex in-app Browser capture emitted in the task evidence; the browser backend does not expose a filesystem path for captures.
- Combined comparison harness: `C:\Users\xiaowangxu\AppData\Local\Temp\cardgrid-qa\compare.html`
- Desktop viewport: 1440 × 900 CSS px at device pixel ratio 1
- Desktop grid capture: 1344 × 744 px for a 1344 × 744 CSS px grid region
- Responsive viewports: 900 × 900 and 390 × 844 CSS px
- State: default desktop, keyboard focus, tablet layout, and mobile layout

## Full-view comparison evidence

The source and implementation were rendered together in the combined comparison harness and captured in one Codex in-app Browser view. Both use a compact Bento composition with three equal cards on the first row, mixed spans on the second row, narrow gaps, large radii, neutral surfaces, image-led cards, and bottom-aligned actions. The implementation intentionally uses the site's existing monochrome illustration system and content instead of copying the source product imagery.

## Focused region comparison evidence

A separate crop was not required because the combined 1500 × 1900 comparison made card typography, 8px gaps, 24px radii, image crops, caption treatments, and link labels readable. Keyboard focus was checked separately at 1440 × 900.

## Required fidelity surfaces

- Fonts and typography: Existing Inter / Chinese system fallbacks are preserved. Heading weights, wrapping, hierarchy, line height, and small action labels remain readable at all tested sizes.
- Spacing and layout rhythm: Desktop uses six tracks with configured spans, 8px gaps, 180px row units, and 24px radii. Tablet resolves to three tracks without horizontal overflow. Mobile is a single content flow.
- Colors and visual tokens: Neutral white, warm gray, and black surfaces match the source's restrained palette and the existing site tokens. Focus uses the existing blue accent.
- Image quality and asset fidelity: All cards use existing project raster assets at natural quality with explicit `cover` or `contain` behavior. No placeholders, CSS drawings, generated substitutes, or stretched sprites are used.
- Copy and content: All example copy is derived from the current site and research articles. Links resolve under the VitePress base path.

## Findings

- No actionable P0, P1, or P2 differences remain.
- [P3] Image captions use translucent inset panels rather than the source's edge-aligned treatment. This is an acceptable readability adaptation for the project's high-contrast line art and avoids obscuring image content.

## Comparison history

1. Initial responsive pass found a P2 mobile density issue: `split` cards expanded to about 595px tall at 390px viewport width.
2. The mobile split template was changed from fractional implicit rows to a fixed 13rem media row plus a flexible content row.
3. Post-fix browser evidence measured the split cards at 400px and 384px, with an 8px inter-card gap and no horizontal overflow.

## Primary interactions and diagnostics

- Keyboard tab order reaches the first card after the brand and primary navigation.
- Focus outline is visible around the entire clickable card.
- Pressing Enter on the focused Cordis card navigates to the correct article route; browser back returns to the grid.
- Local image and link paths include `/CapybaraAndFriends/` through `withBase()`.
- Browser console: no warnings or errors after desktop, tablet, mobile, navigation, and HMR checks.

## Implementation checklist

- [x] Three registered templates: image, text, and split
- [x] Markdown-controlled grid settings and spans
- [x] Safe internal/external URL handling
- [x] Image failure and unknown-template fallback
- [x] Desktop, tablet, and mobile behavior
- [x] Keyboard focus and working navigation
- [x] Browser console clean

## Follow-up polish

- Consider adding a future media-only template when a card should have no visible text treatment.

final result: passed
