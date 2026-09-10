# STYLEGUIDE.md — Visual & Implementation Specification

> **Source of truth:** a full static capture of `iwell.eu` (Dutch homepage, HubSpot CMS + React islands, build `iwell-project/476`).
> All values below were read directly from the reference's compiled CSS, DOM and island props, or systematically derived from them.
>
> **Legend**
> `[OBSERVED]` — literally present in the reference source.
> `[INFERRED]` — not literally present; derived from surrounding values, or from behaviour that must exist for the observed markup to work. Stay internally consistent with these; do not replace them with personal taste.
>
> **This document is written for an AI coding agent.** It is a build spec, not a mood board. Read section 14 (Implementation rules) before writing any code.

---

## Table of contents

1. [Design direction](#1-design-direction)
2. [Design tokens](#2-design-tokens)
3. [Typography](#3-typography)
4. [Grid and layout system](#4-grid-and-layout-system)
5. [Responsive behavior](#5-responsive-behavior)
6. [Components](#6-components)
7. [Images and media](#7-images-and-media)
8. [Iconography](#8-iconography)
9. [Animations and transitions](#9-animations-and-transitions)
10. [Grid animations](#10-grid-animations)
11. [Interaction behavior](#11-interaction-behavior)
12. [Desktop implementation](#12-desktop-implementation)
13. [Mobile implementation](#13-mobile-implementation)
14. [Implementation rules for Claude](#14-implementation-rules-for-claude)

---

## 1. Design direction

### 1.1 One-line characterisation

Swiss-grotesk industrial minimalism: a **hard-edged, zero-radius, full-bleed panel system** in a near-monochrome plum/grey/white palette, punctuated by a single high-voltage lime accent, with a **light-weight display typeface at large sizes** and motion restricted to hover and horizontal transport.

### 1.2 Concrete design rules

These rules are what make the style recognisable. Break any one of them and the result stops looking like the reference.

| # | Rule | Basis |
|---|---|---|
| DR-1 | **Corners are square.** Cards, images, sections, buttons, inputs and panels all have `border-radius: 0`. The *only* rounded things are circular icon buttons (`border-radius: 100px`) and the video-modal frame (`8px`). | `[OBSERVED]` |
| DR-2 | **No shadows on layout.** Elevation is expressed by background-colour change (white ↔ `#f1f1f1` ↔ plum), never by a drop shadow. Shadows exist only on floating overlays (language popup, video modal). | `[OBSERVED]` |
| DR-3 | **No borders as decoration.** There is essentially one hairline in the whole page: a 1px rule above the carousel attribution, and the 1px footer divider. Separation is achieved by alternating background colours of adjacent full-width bands. | `[OBSERVED]` |
| DR-4 | **Sections are full-bleed colour bands, not floating cards.** A section = a container (max 1800px) filled edge-to-edge with white / `#f1f1f1` / plum / an image, with padding *inside* it. Nothing is inset with a gap around it. | `[OBSERVED]` |
| DR-5 | **The lime accent is rationed.** `#cfff00` appears at most 2–4 times per viewport: primary buttons, the highlighted nav item, hover states. It is never a background for large areas of body copy. | `[OBSERVED]` |
| DR-6 | **Headings are LIGHT, not bold.** All `h1`–`h6` use the *light* weight (300) at large sizes. Weight increases only as size decreases: labels and buttons at 11–12px are medium/semibold. This inversion is the typographic signature. | `[OBSERVED]` |
| DR-7 | **Uppercase + 2.2px letter-spacing is the label idiom.** Every small text element (button, nav link, eyebrow, footer heading, meta tag) is uppercase, 11–14px, letter-spacing `2.2px` (≈`0.2em`). Body copy is never uppercase. | `[OBSERVED]` |
| DR-8 | **Generous but asymmetric whitespace.** Vertical section padding is 96px desktop; horizontal is 48px. Copy blocks are constrained (437–664px) while the panel around them runs full width — text sits left, air sits right. | `[OBSERVED]` |
| DR-9 | **Left alignment, always.** Headings, body, meta and buttons align to the left edge of their column. `text-align: center` appears only for the certificate strip and mobile CTA buttons; `text-md-end` only for a single section-header action button. | `[OBSERVED]` |
| DR-10 | **Density is medium-low.** Long-form paragraphs are truncated (`-webkit-line-clamp: 4`) rather than allowed to make a row dense. One idea per panel. | `[OBSERVED]` |
| DR-11 | **Contrast is high and binary.** Text is plum `#2e103b` on light, pure white on dark. There is no mid-grey body text and no opacity-dimmed copy, except the mobile sub-menu links (`opacity: .65`). | `[OBSERVED]` |
| DR-12 | **Rhythm comes from alternating bands.** The case list alternates `#f1f1f1` / `#fff` per row; the page alternates image-bleed sections with flat colour sections. This alternation *is* the vertical rhythm. | `[OBSERVED]` |
| DR-13 | **One motion vocabulary: reveal-by-clip and slide.** Circles expand via `clip-path`, arrows slide out/in, images scale 1.05, menus translate. Nothing bounces, fades-up-on-scroll, or springs. | `[OBSERVED]` |
| DR-14 | **Imagery is always cropped to fill, never letterboxed.** `object-fit: cover` everywhere except logos (`contain`). | `[OBSERVED]` |
| DR-15 | **Interactive surfaces invert on hover.** The dominant hover pattern is background↔foreground swap (white→plum, grey→lime), not opacity or scale on the container. | `[OBSERVED]` |

### 1.3 Composition principles

- **Editorial 4/8 split.** The signature desktop layout is a narrow text column (`col-lg-4`, 33%) against a wide visual (`col-lg-8`, 67%) that is allowed to bleed *past* the right viewport edge (`right: -10vw`). `[OBSERVED]`
- **Half-and-half card pairs.** Feature CTAs sit as two `col-lg-6` cards with `g-0` — no gutter — so they read as one two-cell band. `[OBSERVED]`
- **Full-width list rows.** Cases are not a card grid; they are stacked full-width rows, each split 50/50 text|image, alternating background. `[OBSERVED]`
- **Header floats over the hero.** The fixed header is transparent above the hero (white logo, white tagline) and switches to a light palette (dark logo, dark tagline) once scrolled or when a dropdown opens. `[OBSERVED]`

---

## 2. Design tokens

Copy this block verbatim into the template's global stylesheet. Everything downstream references these names.

```css
:root {
  /* ---------- Brand colours ---------- */
  --color-volt:              #cfff00;  /* primary accent / CTA */
  --color-volt-hover:        #bbee04;  /* accent hover */
  --color-plum:              #2e103b;  /* primary dark / body text */
  --color-plum-deep:         #1b0020;  /* darkest UI ink, dark card bg */
  --color-ink:               #030104;  /* near-black, dropdown links */
  --color-black:             #000000;  /* button label on volt */
  --color-white:             #ffffff;
  --color-grey:              #f1f1f1;  /* surface grey / alternating band */
  --color-grey-placeholder:  #ededed;  /* skeleton / empty media */
  --color-focus:             #631f82;  /* focus ring + dropdown link hover */
  --color-navy:              #17154a;  /* gradient scrim base only */

  /* ---------- Semantic ---------- */
  --color-background:            #f8f7f7; /* <body> */
  --color-surface:               var(--color-white);
  --color-surface-alt:           var(--color-grey);
  --color-surface-inverse:       var(--color-plum);
  --color-text-primary:          var(--color-plum);
  --color-text-inverse:          var(--color-white);
  --color-text-on-accent:        var(--color-black);
  --color-heading:               var(--color-plum);
  --color-accent:                var(--color-volt);
  --color-accent-hover:          var(--color-volt-hover);
  --color-border-hairline:       var(--color-plum-deep); /* 1px rules */
  --color-divider:               var(--color-grey);      /* footer line */

  /* ---------- Overlays & gradients ---------- */
  --overlay-card-backdrop:  rgba(27, 0, 32, 0.35);   /* #1b002059 on CTA banners */
  --overlay-panel:          rgba(0, 0, 0, 0.40);     /* mobile menu scrim */
  --overlay-slide-in:       rgba(0, 0, 0, 0.75);     /* body.mobile-slide-in scrim */
  --overlay-modal:          rgba(0, 0, 0, 0.80);     /* video modal backdrop */
  --gradient-black-fade:    linear-gradient(0deg, rgba(0,0,0,0.30) 0%, rgba(0,0,0,0) 100%);
  --gradient-navy-fade:     linear-gradient(0deg, rgba(23,21,74,0.60) 0%, rgba(23,21,74,0) 100%);
  --gradient-nav-card:      linear-gradient(180deg, #030104 0%, #2e103b 14.21%, rgba(0,0,0,0) 62.32%),
                            linear-gradient(0deg, rgba(0,0,0,0.5), rgba(0,0,0,0.5));

  /* ---------- Opacity ---------- */
  --opacity-muted-link:  0.65;  /* mobile sub-menu links */
  --opacity-hidden:      0;
  --opacity-scrim:       0.75;

  /* ---------- Radius (mostly zero — see DR-1) ---------- */
  --radius-none:  0;
  --radius-pill:  100px;   /* icon buttons only */
  --radius-modal: 8px;     /* video modal frame only */
  --radius-chip:  12px;    /* highlighted <span> inside a heading */
  /* Utility scale present in the theme but UNUSED on the reference homepage.
     Do not introduce these unless the reference page you are rebuilding uses them. */
  --radius-sm: 1rem;  --radius-md: 1.5rem;  --radius-lg: 2rem;  --radius-xl: 2.5rem;

  /* ---------- Shadows (floating overlays only) ---------- */
  --shadow-popup:  0 8px 80px rgba(0, 0, 0, 0.15);
  --shadow-modal:  0 0 30px rgba(0, 0, 0, 0.60);
  --shadow-button: 0 2px 6px rgba(0, 0, 0, 0.30);
  --shadow-none:   none;   /* the default for every layout element */

  /* ---------- Blur ---------- */
  /* No backdrop-filter / blur anywhere in the reference. Do not add any. */

  /* ---------- Spacing scale (px, exact from the reference token file) ---------- */
  --space-0:    0px;
  --space-100:  4px;
  --space-200:  8px;
  --space-300:  12px;
  --space-400:  16px;
  --space-500:  24px;
  --space-600:  32px;
  --space-650:  40px;
  --space-700:  48px;
  --space-800:  64px;
  --space-900:  72px;
  --space-1000: 96px;
  --space-1100: 128px;
  --space-1200: 256px;   /* "extra-large" utility only */

  /* ---------- Layout spacing (semantic) ---------- */
  --space-section-y:            96px;  /* desktop vertical padding inside a band */
  --space-section-y-mobile:     32px;  /* ≤576px, default band */
  --space-section-y-mobile-lg:  64px;  /* ≤991px for header rows / streamers */
  --space-section-x:            48px;  /* desktop horizontal padding inside a band */
  --space-section-x-mobile:     16px;
  --space-panel:                48px;  /* card / article inner padding, desktop */
  --space-panel-md:             32px;  /* ≤991px */
  --space-panel-sm:             24px;  /* ≤576px vertical */
  --space-stack:                48px;  /* gap in a text stack */
  --space-stack-tight:          32px;  /* gap inside a card body */
  --space-gutter:               24px;  /* bootstrap --bs-gutter-x = 1.5rem */

  /* ---------- Container ---------- */
  --container-max:      1800px;
  --content-max-quarter: 437px;  /* narrow body column */
  --content-max-half:    664px;  /* case-row body copy */
  --content-max-box:     480px;  /* .box--inner */
  --content-max-hero:    640px;  /* hero content block */
  --content-max-carousel: 460px; /* testimonial copy */

  /* ---------- Motion ---------- */
  --ease-standard:   cubic-bezier(0.25, 0.1, 0.25, 1);    /* menus, colours, panels */
  --ease-emphasized: cubic-bezier(0.4, 0, 0.2, 1);        /* header hide/show */
  --ease-clip:       cubic-bezier(0.785, 0.135, 0.15, 0.86); /* icon-button clip-path */
  --ease-image:      cubic-bezier(0.65, 0, 0.35, 1);      /* image scale, row bg */
  --ease-legacy:     ease;                                /* the .cubic-ease utility */
  --ease-rotate:     ease-in-out;                         /* chevron rotation */

  --duration-instant: 150ms;
  --duration-fast:    200ms;
  --duration-quick:   250ms;
  --duration-base:    300ms;
  --duration-medium:  350ms;
  --duration-slow:    400ms;
  --duration-legacy:  500ms;   /* .cubic-ease */
  --duration-image:   600ms;
  --duration-clip:    650ms;
  --duration-panel:   750ms;   /* body slide-in */

  --stagger-menu-item: 60ms;

  /* ---------- Z-index layers ---------- */
  --z-behind:            -1;   /* background-image figures */
  --z-base:               0;
  --z-content:            1;
  --z-main:               2;   /* <main> */
  --z-nav-inner:         20;
  --z-nav-branding:     200;   /* logo + submenu container */
  --z-mobile-header:   1000;
  --z-header-dropdown:  998;
  --z-header:           999;
  --z-hero-modal:      9999;
  --z-lang-fixed:      9999;   /* fixed language switcher ≤991px */
  --z-panel-overlay:  10000;
  --z-panel:          10001;
  --z-lang-popup:     10002;
}
```

### 2.1 Colour usage matrix `[OBSERVED]`

| Surface | Background | Heading | Body | Accent element |
|---|---|---|---|---|
| Default band | `--color-white` | `--color-plum` | `--color-plum` | volt button |
| Alt band | `--color-grey` | `--color-plum` | `--color-plum` | volt button |
| Inverse band | `--color-plum` | `--color-white` (forced `!important`) | `--color-white` | volt button |
| Accent band | `--color-volt` | `--color-plum` | `--color-plum` | plum icon button |
| Over image | image + `--overlay-card-backdrop` or `--gradient-nav-card` | `--color-white` | `--color-white` | volt button |

### 2.2 Body defaults `[OBSERVED]`

```css
*, *::before, *::after { box-sizing: border-box; }
html { text-size-adjust: none; overflow-x: hidden; }
body {
  margin: 0; padding: 0;
  min-height: 100vh;
  overflow-x: hidden;
  background-color: var(--color-background);
  color: var(--color-text-primary);
  line-height: 1.5;
  font-optical-sizing: auto;
}
main { position: relative; z-index: var(--z-main); }
img, picture { display: block; max-width: 100%; }
h1, h2, h3, h4 { text-wrap: balance; line-height: 1.1; }
button, input, label { line-height: 1.1; }
ol[role="list"], ul[role="list"] { list-style: none; }
a:not([class]) { color: currentColor; text-decoration-skip-ink: auto; }
:target { scroll-margin-block: 5ex; }
```

---

## 3. Typography

### 3.1 Typeface `[OBSERVED]` / substitution `[INFERRED]`

The reference uses **Haffer** (Displaay Type Foundry), a neo-grotesk, loaded as **four separate `@font-face` families** rather than four weights of one family:

| CSS family name | File | Nominal weight |
|---|---|---|
| `hafferlight` | `haffer-light.woff2` | 300 |
| `hafferregular` | `haffer-regular.woff2` | 400 |
| `haffermedium` | `haffer-medium.woff2` | 500 |
| `haffersemibold` | `haffer-semibold.woff2` | 600 |

`font-display: swap` on all four. Headings declare `font-weight: inherit` — weight comes entirely from the family name. `font-feature-settings: "ss02" 1, "ss03" 1, "ss04" 1, "ss05" 1, "ss06" 1` is applied to headings and card copy (stylistic alternates). `[OBSERVED]`

**Substitution ladder** `[INFERRED]` — if Haffer is not licensed for the template, use, in order of preference:

1. **Instrument Sans** (Google Fonts) — closest grotesk proportions and tall x-height.
2. **Inter Tight** (Google Fonts) — tighter than Inter, acceptable at display sizes.
3. `Helvetica Neue, Arial, sans-serif` as the final fallback.

Whichever you pick, **normalise the API to the reference's four-family model** so the rest of this spec applies unchanged:

```css
:root {
  --font-sans: "Instrument Sans", "Inter Tight", "Helvetica Neue", Arial, sans-serif;
  --font-light:    var(--font-sans);   --weight-light: 300;
  --font-regular:  var(--font-sans);   --weight-regular: 400;
  --font-medium:   var(--font-sans);   --weight-medium: 500;
  --font-semibold: var(--font-sans);   --weight-semibold: 600;
  --font-features: "ss02" 1, "ss03" 1, "ss04" 1, "ss05" 1, "ss06" 1; /* no-op on substitutes */
}
```

> When substituting, **drop 25–50 to the heading weight rather than raise it** — a substitute grotesk at 300 usually reads heavier than Haffer Light at display sizes. Never let a heading render at 400+ above 32px. `[INFERRED]`

### 3.2 Type scale `[OBSERVED]`

| Token / class | Size | rem | Family | Line-height | Letter-spacing | Transform |
|---|---|---|---|---|---|---|
| `.font-size--xxl` | 80px | 5rem | light | 1.1 | 0 | none |
| `.font-size--xl` | 56px | 3.5rem | light | 1.1 | 0 | none |
| `.font-size--lg` | 32px | 2rem | light | 1.1 | 0 | none |
| `.font-size--md` | 24px | 1.5rem | light | 1.1 | 0 | none |
| `.font-size--sm` | 14px | 0.875rem | light | 1.35 | 0 | none |
| `.font-size--xs` | 11px | 0.6875rem | medium | 1.1 | 2.2px | uppercase |
| `.subtitle` (eyebrow) | 11.2px | 0.7rem | medium | 1.1 | 2.2px | uppercase |
| `p` (body) | 16px | 1rem | light | 135% | 0 | none |
| `.button` | 11px | 0.6875rem | medium/semibold | 1.5rem | 2.2px | uppercase |
| `.button--link` | 14.4px | 0.9rem | semibold | 1.5rem | 2.2px | uppercase |
| `.submenu--link` (nav) | 11px | 0.6875rem | semibold | 1.1 | 2.2px | uppercase |
| dropdown menu link | 14px | 0.875rem | regular (430) | 1.35 | 0 | none |
| footer `h4` | 14.4px | 0.9rem | medium | 1.1 | 2.2px | uppercase |
| footer link | 14px | 0.875rem | regular | 1.35 | 0 | uppercase |
| case meta item | 12px | 0.75rem | medium | 1.1 | 0.2em | uppercase |
| header tagline | 10.8px | 0.675rem | regular | 1.1 | 2.2px | uppercase |
| hamburger label | 11px | 0.6875rem | regular | 1.1 | 2.2px | none |

> **Note on `.button` letter-spacing:** the module CSS declares the invalid value `letter-spacing: 20%`, which browsers discard; the effective value inherited from the theme bundle is `2.2px`. Implement `2.2px`. `[OBSERVED]`

### 3.3 Fluid heading sizes `[OBSERVED]`

```css
.hero--title            { font-size: clamp(24px, 8vw, 80px); }        /* ≤576px: fixed 40px */
.section-heading        { font-size: clamp(2rem, 1.25rem + 3vw, 3.5rem); }   /* cases-grid heading */
.card-title--lg         { font-size: clamp(1.5rem, 1.25rem + 1.5vw, 2.5rem); } /* CTA card title */
.card-title--md         { font-size: clamp(1.5rem, 1.25rem + 1vw, 2rem); }     /* case row title */
```

### 3.4 Heading hierarchy

| Level | Desktop | Mobile (≤576px) | Family | Colour | Margin-bottom |
|---|---|---|---|---|---|
| H1 (hero only) | `clamp(24px, 8vw, 80px)` | 40px | light | white (on media) | 0 |
| H2 section heading | `clamp(32px, 1.25rem+3vw, 56px)` | 32px | light | plum | 0 (header uses flex gap) |
| H2 card title | `clamp(24px, 1.25rem+1.5vw, 40px)` | 24px | light | plum / white on plum | 0 |
| H3 block title | 32px (`--xl` → 56px when used as a section head) | 32px (`--xl` collapses to 32px + mb 32px) | light | plum | 64px inside `content-text-side-cta`; 48px for `--xl` |
| H3 row title | `clamp(24px, 1.25rem+1vw, 32px)` | 24px | regular | plum | 0 |
| H4 footer heading | 14.4px uppercase | same | medium | plum | 32px |

Rules:
- `h1–h6 { margin-top: 0; line-height: 1.1; color: var(--color-heading); font-family: var(--font-light); font-weight: var(--weight-light); }` `[OBSERVED]`
- A `<span>` inside a heading is a *highlight chip*: `padding: 0 1rem 0.25rem; border-radius: 12px;` (give it `background: var(--color-volt)`). `[OBSERVED]` / background `[INFERRED]`
- `.font-size--xl` carries its own `margin-bottom: 48px`, dropping to `32px` at ≤576px. `[OBSERVED]`

### 3.5 Body & long-form

```css
p {
  font-family: var(--font-light); font-weight: var(--weight-light);
  font-size: 1rem; line-height: 135%; margin: 0 0 1.5rem;
}
li { font-family: var(--font-light); font-size: 1rem; line-height: 135%; }
strong { font-size: 2rem; line-height: 140%; }  /* inside .content-block only */
```

Two competing body settings exist in the reference; the **module-level rule wins** (loaded last): `hafferlight, 1rem, 135%`. The theme-bundle fallback is `hafferregular, 0.9rem, 135%` — use it only for legal/utility pages. `[OBSERVED]`

Card and rich-text body copy uses a *different* setting — heavier and looser:
```css
.card-body, .rte-body { font-family: var(--font-regular); font-size: 1rem; line-height: 1.5; }
.article-body         { font-family: var(--font-regular); font-size: 1rem; line-height: 1.6; }
.article-body p + p   { margin-top: 1.6em; }  /* paragraph rhythm without bottom margins */
```
`[OBSERVED]`

### 3.6 Responsive typography summary

| Element | ≥1200px | 992–1199 | 768–991 | 577–767 | ≤576px |
|---|---|---|---|---|---|
| Hero H1 | up to 80px (8vw) | 8vw | 8vw | 8vw | **40px fixed** |
| `.font-size--xl` | 56px | 56px | 56px | 56px | **32px**, mb 32px |
| Section H2 (clamp 3vw) | 56px | ~46px | ~40px | ~34px | 32px |
| CTA card title | 40px | ~36px | ~32px | ~28px | 24px |
| `content-text-side-cta` lead `p` | 32px | 32px | 32px | 32px | **20px** |
| Mobile menu primary link | — | 41px | 41px | 41px | **28px** |
| Streamer employee name | 32px | 32px | **24px** | 24px | **20px** |
| Body `p` | 16px | 16px | 16px | 16px | 16px (unchanged) |
| Labels / buttons | 11px | 11px | 11px | 11px | 11px (unchanged) |

**Rule:** body copy and labels never scale down. Only display sizes scale. `[OBSERVED]`

---

## 4. Grid and layout system

### 4.1 Foundation `[OBSERVED]`

The reference uses **Bootstrap 5.2.3 grid-only** (no components), plus a small custom utility layer.

| Property | Value |
|---|---|
| Columns | 12 |
| Container max-width | `1800px` |
| Container margins | `margin-left/right: auto` (centred), `width: 100%` |
| Container horizontal padding | **`0`** — Bootstrap's container padding is stripped in this build |
| Default gutter | `--bs-gutter-x: 1.5rem` (24px) → 12px padding per column side |
| Row negative margin | `calc(var(--bs-gutter-x) * -0.5)` = −12px |

> **Critical:** because `.container` has no padding, the *page edge padding lives inside each section's inner wrapper* (`48px` desktop / `16px` mobile). Reproduce this exactly — it is why full-bleed images can reach the viewport edge while text stays inset.

### 4.2 Breakpoints `[OBSERVED]`

| Name | Min-width | Bootstrap prefix | Used for |
|---|---|---|---|
| xs | 0 | (none) | base / mobile |
| sm | 576px | `col-sm-*` | small-phone → large-phone boundary; most `max-width: 576px` overrides |
| md | 768px | `col-md-*` | tablet portrait; `max-width: 768px` header overrides |
| lg | 992px | `col-lg-*` | tablet landscape / small laptop; `max-width: 991px` layout stacking |
| xl | 1200px | `col-xl-*` | **navigation switch point** (`d-none d-xl-block` / `d-xl-none`) |
| xxl | 1400px | `col-xxl-*` | wide desktop column refinements |

**Max-width query values actually used:** `576px`, `768px`, `767px` (once), `991px`, `1199px`. Use these exact values, not `575.98px` style Bootstrap-internal ones, for your own overrides. `[OBSERVED]`

### 4.3 Column allocations used on the homepage `[OBSERVED]`

| Section | xxl (≥1400) | lg (≥992) | md (≥768) | base |
|---|---|---|---|---|
| Header logo | `col-xl-3` | — | — | flex |
| Header nav | `col-lg-9` (justify-end) | `col-lg-9` | — | hidden <1200 |
| Lead statement | `col-xxl-9` | `col-lg-8` | `col-md-10` | `col-12` |
| Text + visual | text `col-xxl-4` / visual `col-xxl-8` | `col-lg-4` / `col-lg-8` | visual `col-md-6` | `col-12` |
| CTA card pair | — | `col-lg-6` ×2 | — | `col-12` |
| Content block | — | — | `col-md-8` + `col-md-4` | `col-12` |
| Footer widgets | — | `col-lg-2` ×6 | `col-md-4` | `col-12` |

Gutters: the CTA pair and the text+visual row use **`g-0` / `gx-0`** (zero gutter) so panels touch. The footer uses default gutters plus `row-gap: 48px`. `[OBSERVED]`

### 4.4 Layout utilities to port `[OBSERVED]`

```css
.container { width: 100%; max-width: var(--container-max); margin-inline: auto; }
.row { display: flex; flex-wrap: wrap;
       margin-inline: calc(var(--space-gutter) * -0.5); }
.row > * { flex-shrink: 0; width: 100%; max-width: 100%;
           padding-inline: calc(var(--space-gutter) * 0.5); }
.g-0, .gx-0 { --bs-gutter-x: 0; }

.gap-sm { gap: 8px; } .gap-md { gap: 16px; } .gap-lg { gap: 24px; } .gap-xl { gap: 32px; }

/* Section rhythm utilities (with built-in responsive collapse) */
.pt--small  { padding-top: 32px; }  .pb--small  { padding-bottom: 32px; }
.pt--medium { padding-top: 64px; }  .pb--medium { padding-bottom: 64px; }
.pt--large  { padding-top: 128px; } .pb--large  { padding-bottom: 128px; }
.pt--extra-large { padding-top: 256px; } .pb--extra-large { padding-bottom: 256px; }
@media (max-width: 991px) {
  .pt--small { padding-top: 24px; } .pb--small { padding-bottom: 24px; }
  .pt--large { padding-top: 56px; } .pb--large { padding-bottom: 56px; }
  .pt--extra-large { padding-top: 80px; } .pb--extra-large { padding-bottom: 80px; }
}
@media (max-width: 768px) { .pt--small { padding-top: 20px; } .pb--small { padding-bottom: 20px; } }
/* mt--*/mb--* mirror these exactly */

.radius--sm { border-radius: 1rem; } /* unused on home — see DR-1 */
.ratio-1x1 { aspect-ratio: 1/1; display: flex; align-items: center; justify-content: center; width: 100%; }
.ratio-16x9 { aspect-ratio: 16/9; display: flex; align-items: center; justify-content: center; width: 100%; }
.image--cover img { width: 100%; height: 100%; object-fit: cover; }
.cubic-ease { transition: all 500ms ease; }
```

Note the **128px → 56px** collapse for `--large`: the reference compresses aggressively below 992px, it does not scale proportionally. `[OBSERVED]`

### 4.5 Section spacing reference table `[OBSERVED]`

| Section | ≥992px padding | ≤991px | ≤576px |
|---|---|---|---|
| `content-block` | `96px 48px` | `96px 48px` | `32px 16px` |
| `cases-grid__header` | `96px 48px` | `64px 16px` | `64px 16px` |
| `streamer--inner` | `96px 48px` | `96px 48px` | `64px 16px` |
| `content-text-side-cta` | `64px 48px` | `64px 48px` | `48px 16px` |
| `content-text-side-visual article` | `48px` | `48px 16px` | `32px 16px` |
| CTA card body (vertical) | `48px` | `32px` | `24px 16px` |
| CTA card body (horizontal) | `64px 121px 64px 48px` | `48px` | `48px` |
| Case row body | `48px` | `32px 16px` | `32px 16px` |
| Footer widgets | `64px 48px` | `64px 48px` | `32px 16px` |
| Footer certificates | `32px 48px` | `32px 48px` | `32px 16px` |
| Footer copyright | `48px` | `48px` | `32px 16px` |
| Header container | `32px 48px` | `32px 48px` (`16px` ≤768) | `16px` |
| Carousel container | `0 48px` | `0 48px` | `0 48px` |

**Derived rule:** desktop horizontal inset is **48px**, mobile is **16px**. Desktop vertical is **96px** for major bands, **64px** for supporting bands, **48px** for card interiors. `[OBSERVED]`

### 4.6 Vertical rhythm

There is no `margin` between sections — sections butt directly against each other and their internal padding creates the rhythm. Two adjacent 96px paddings produce the visual 96px gap, not 192px, because the reference sets one side to `--pt-none` / `--pb-none` where sections should touch (e.g. hero → lead statement → text+visual run with zero interstitial space). `[OBSERVED]`

**Rule:** never add `margin-top` / `margin-bottom` to a section. Control rhythm with the section's own `padding-top` / `padding-bottom` modifier classes. `[OBSERVED]`

---

## 5. Responsive behavior

### 5.1 The four structural switch points

| Breakpoint | What changes |
|---|---|
| **≤1199px** | Desktop nav + desktop language switcher hide. Hamburger + `myiwell` chip appear. Language switcher becomes a fixed bottom-right button. |
| **≤991px** | All two-column layouts stack. Case rows become `column-reverse` (image above text). Horizontal CTA cards become `column-reverse`. The bleeding visual (`added-distance`) becomes static full-width. Card body padding 48→32. Mobile panel is still 50vw. |
| **≤768px** | Header container padding 48→16. Mobile menu bar height 96→84. Mobile panel becomes 100vw. Mobile primary nav link 41→28px. Hero video buttons shrink to 32px. |
| **≤576px** | Section padding collapses to `16px` horizontal / `32–64px` vertical. Display type drops to fixed small sizes. Hero becomes a fixed 460px band. Carousel profile 300×400 → 200×300. |

### 5.2 Element-by-element responsive matrix `[OBSERVED]`

| Element | Desktop | Change | At |
|---|---|---|---|
| Desktop submenu | visible | `display: none` | <1200px |
| Hamburger bar | hidden | `display: flex` | <1200px |
| Language switcher | inline in header | `position: fixed; bottom:16px; right:16px; z-index:9999` | ≤991px |
| Language popup | opens downward | opens upward (`bottom: 100%`) | ≤768px |
| Header container padding | `32px 48px` | `16px` | ≤768px |
| Header logo height | 32px | **52px** | ≤768px |
| Mobile bar height | 96px | 84px | ≤768px |
| Mobile bar width | `calc(100% − 200px)` | `calc(100% − 120px)` | ≤480px |
| Mobile panel width | `50vw` | `100vw` | ≤768px **or** portrait |
| Mobile panel topbar padding | `28px 42px 28px 76px` | `20px 24px` | ≤768px |
| Mobile panel nav | `margin-top:200px; padding:0 42px 80px 76px` | `margin-top:120px; padding:0 40px 80px` | ≤768px |
| Hero | `min-height:720px; height:80vh; max-height:90vh` | `min-height:460px; height:460px; max-height:600px` | ≤576px |
| Hero content offset | `left:40px; bottom:40px` | `left:16px; bottom:24px` | ≤576px |
| Hero video buttons | `padding:40px; gap:16px` | `padding:16px; gap:8px`, icons 48→32px | ≤768px |
| Hero video buttons axis | row | **column** | ≤576px |
| Text+visual visual | `position:absolute; right:−10vw; width:max(940px, 60%+10vw)` | `position:static; width:100%` | ≤991px |
| Text+visual article | `col-lg-4` | `col-12`, order unchanged (text first) | ≤991px |
| CTA card pair | `col-lg-6` side by side | `col-12` stacked | <992px |
| CTA card banner | 192px tall | 160px tall | ≤576px |
| CTA horizontal card | `flex-direction: row-reverse` | `column-reverse` (image on top) | ≤991px |
| CTA wrapper grid | `5fr 1fr` | `1fr` (icon drops below, still right-aligned) | ≤991px |
| Case row | `flex-direction: row` (text \| image) | `column-reverse` → **image above text** | ≤991px |
| Case image | `flex:1 1 0; min-height:320px` | `width:100%; aspect-ratio:16/9` | ≤991px |
| Case body spacing | `> * + * { margin-top: 32px }` | `24px` | ≤991px |
| Case wrapper gap | 48px | 24px | ≤767px |
| Carousel content | `width: 460px` | `width:100%; padding: 0 24px` | ≤768px |
| Carousel logo | 80×80 inline | absolute `bottom:24px; right:24px`, white bg | ≤768px |
| Carousel profile img | 300×400 | 200×300 | ≤576px |
| Carousel arrows | in-flow 80px | `left:−54px` / `right:−54px` | ≤768px |
| Footer widget | `col-lg-2` | `col-md-4` → `col-12`, `margin-bottom: 48px` | ≤576px |
| Buttons in `.button__mobile-width` | auto width | `width:100%; text-align:center` | ≤768px |
| `.spacing__left-right--*` | n/a | 1rem / 1.5rem / 2rem / 3rem | ≤991px |

### 5.3 Order changes `[OBSERVED]`

- Case rows and horizontal CTA cards use `flex-direction: column-reverse` on mobile so the **image moves above the text** — do not achieve this with `order:` on the source elements; the reference reverses the flex axis.
- The text+visual section keeps DOM order (text first) — the visual is absolutely positioned on desktop and simply returns to flow on mobile.

### 5.4 Overflow behaviour `[OBSERVED]`

- `html, body { overflow-x: hidden }` — required, because the desktop visual deliberately extends to `right: -10vw`.
- `.content-text-side-visual { overflow: clip }` on the section itself.
- `.marquee-streamer--container { overflow: hidden }`, inner `.wrapper { width: calc(100% + 200px); overflow: hidden }`.
- `.carousel--container { overflow: hidden }` but `.carousel--swiper { overflow: visible !important }` — slides bleed past the container edge and are clipped by the parent.
- Mobile panel: `overflow-y:auto; overflow-x:hidden; overscroll-behavior:contain; -webkit-overflow-scrolling:touch;` plus `data-lenis-prevent` so smooth-scroll does not hijack it.

---

## 6. Components

### 6.1 Header (fixed, theme-switching)

```css
.header {
  position: fixed; top: 0; width: 100%; z-index: var(--z-header);
  box-sizing: border-box;
  transition: background-color var(--duration-base) var(--ease-standard),
              transform        var(--duration-base) var(--ease-emphasized);
}
.header--container { padding: 32px 48px; }
@media (max-width: 768px) { .header--container { padding: 16px; } }
```

| Property | Value |
|---|---|
| Position | fixed, full width, over content |
| Height (desktop) | 32 + 52 + 32 ≈ **116px** `[INFERRED from padding + 52px nav item]` |
| Height (≤768px) | 16 + 52 + 16 = **84px** (matches `mobile-menu--container` 84px) `[OBSERVED]` |
| Default state | transparent background, **white** logo (`.header--logo-primary`), white tagline |
| `.header--scrolled` | dark logo (`.header--logo-dark` opacity 1), tagline `#1b0020`, primary logo opacity 0 |
| `.header.dropdown-is-open` | `background-color: #f1f1f1` + dark logo palette |
| `.header.mobile-is-open` | dark palette, logo `opacity:0; visibility:hidden`, `transform: none !important` |
| `.header--scroll-hidden` | `transform: translateY(-100%)` |
| `.header--up` / `.header--down` | `translateY(0)` / `translateY(-100%)` |
| Logo | height 32px (≤768px: 52px), `max-height:32px`, `margin-right:40px`, opacity transition 300ms `--ease-standard` |
| Tagline | `0.675rem`, uppercase, `letter-spacing: 2.2px`, `--font-regular`, hidden below xl (`d-none d-xl-block`) |
| Focus | `outline: 2px solid var(--color-focus); outline-offset: 2px` |

**Dark-header default** `[OBSERVED]` — pages whose first module is *not* the hero start on the dark palette:
```css
html:not(.has-light-header) .header--logo-primary { display: none; }
html:not(.has-light-header) .header--logo-dark    { opacity: 1 !important; }
html:not(.has-light-header) .header--tagline      { color: var(--color-plum-deep); }
```
The hero adds `has-light-header` to `<html>`; an IntersectionObserver on `[data-header-theme="light"]` then owns the palette by toggling `.header--scrolled`. `[OBSERVED]`

### 6.2 Primary navigation (≥1200px)

```css
.submenu--link {
  display: flex; align-items: center; gap: 8px;
  height: 52px; padding: 12px 16px;
  font-family: var(--font-semibold); font-size: 0.6875rem; line-height: 1.1;
  letter-spacing: 2.2px; text-transform: uppercase; white-space: nowrap;
  color: var(--color-plum); background-color: var(--color-white);
  border: none; border-radius: 0; cursor: pointer;
  transition: all 500ms ease;               /* .cubic-ease */
}
.submenu--link:not(.highlight):hover { background-color: var(--color-plum); color: var(--color-white); }
.submenu--link.highlight             { background-color: var(--color-volt); color: var(--color-plum); }
.submenu--link.highlight:hover       { background-color: var(--color-plum); color: var(--color-white); }
.submenu--item.active .submenu--link { background-color: var(--color-plum) !important; color: #fff !important; }
```

| State | Appearance |
|---|---|
| Default | white pill-less block, plum text |
| Hover | plum block, white text |
| Highlight (`myiwell`) | volt block, plum text |
| Highlight hover | plum block, white text |
| Active/open | plum block, white text (forced) |
| Chevron | `transform: rotate(180deg)` closed → `rotate(0)` open, `transition: all 500ms ease-in-out`, `margin-left: 6px` |

Nav items sit in a flex row, right-aligned, **no gap between them** — they read as one continuous white bar. `[OBSERVED]`

There is a hidden **ghost copy** of the nav (`.submenu--ghost-section`, `visibility:hidden; width:max-content; white-space:nowrap`) used to measure natural nav width; when it exceeds the available space the header gets `.nav-is-wrapped` and hides the language switcher. Reproduce this only if the template has a variable-length nav. `[OBSERVED]`

### 6.3 Mega-dropdown

```css
.header--dropdown {
  position: absolute; top: 100%; left: 0; right: 0;
  height: 0; opacity: 0; overflow: hidden;
  z-index: var(--z-header-dropdown);
  background-color: var(--color-grey);
}
.header--dropdown--inner { background-color: #fff; display: flex; width: 100%; }
.header--dropdown--links { flex: 1; display: flex; flex-direction: column; gap: 32px; padding: 40px; }
.header--dropdown--card  { flex: 0 0 30%; min-width: 280px; aspect-ratio: 1/1;
                           padding: 32px; background-color: var(--color-plum-deep);
                           display: flex; flex-direction: column; overflow: hidden; position: relative; }
```

| Part | Spec |
|---|---|
| Panel open | `height: 0 → auto` and `opacity: 0 → 1`, JS-driven `[OBSERVED markup]` / duration `~300ms` with `--ease-standard` `[INFERRED]` |
| Section title | `--font-regular`, `1.5rem`, `line-height:1.5`, colour `#1b0020` |
| Menu link | `14px`, `font-weight:430`, `line-height:1.35`, colour `#030104`, `padding:12px 0`, no transform |
| Menu link hover | colour `var(--color-focus)` (`#631f82`) |
| Two-column list | `column-count: 2; column-gap: 64px;` list items `break-inside: avoid` |
| Card background | `<img>` absolutely filling, `object-fit: cover`, `z-index: 0` |
| Card overlay | `--gradient-nav-card`, `z-index: 1` |
| Card body | `z-index: 2`, flex column, `justify-content: space-between`, inner text gap `32px` |
| Card title / description | `1.5rem / 1.5` and `1rem / 1.6`, both `--font-regular`, white |
| Card button | volt bg, plum text, `height: 52px`, `padding: 12px 16px`, `gap: 8px`, `0.6875rem` uppercase `ls 2.2px`, `align-self: flex-start`; hover → plum bg, white text, `300ms --ease-standard` |
| Header while open | `.header.dropdown-is-open { background-color: #f1f1f1 }` |

### 6.4 Mobile menu bar (<1200px)

```css
.mobile-menu--container {
  position: fixed; top: 0; right: 0;
  width: calc(100% - 200px); height: 96px; padding: 0 48px;
  display: flex; align-items: center; justify-content: flex-end;
}
@media (max-width: 768px) { .mobile-menu--container { height: 84px; padding: 0 16px; } }
@media (max-width: 480px) { .mobile-menu--container { width: calc(100% - 120px); } }

.hamburger {
  display: flex; align-items: center; gap: 8px;
  height: 45px; padding: 8px 12px; border: none; cursor: pointer;
  background-color: var(--color-grey); color: var(--color-plum-deep);
  font-size: 0.6875rem; line-height: 1.1; letter-spacing: 2.2px; text-transform: none;
  transition: opacity 150ms linear, filter 150ms linear;
}
.hamburger:hover { background-color: var(--color-volt); }
```

The bar also carries a `myiwell` chip: same 45px height, `padding: 8px 12px`, grey bg → volt on hover/`.highlight`. `[OBSERVED]`

### 6.5 Mobile slide-in panel

| Property | Value |
|---|---|
| Position | `fixed; top:0; right:0; bottom:0`, `width: 50vw`, `max-width: 100vw` |
| Width ≤768px or portrait | `100vw !important` |
| Background / z-index | `#fff` / `10001` |
| Closed | `transform: translateX(100%); visibility: hidden` |
| Open (`.is-open`) | `transform: translateX(0); visibility: visible` |
| Scroll | `overflow-y:auto; overscroll-behavior:contain; data-lenis-prevent` |
| Overlay | `.mobile-panel--overlay` fixed inset 0, `rgba(0,0,0,0.4)`, `z:10000`, `opacity 0 → 1` over `300ms --ease-standard` |
| Page scrim | `body.mobile-slide-in header::before { opacity: .75 }` on a full-viewport black layer; `#main-content` transitions `all 750ms --ease-standard` |

Panel internals:

| Part | Spec |
|---|---|
| Topbar | `padding: 28px 42px 28px 76px` (≤768: `20px 24px`), starts `opacity:0; translateY(-10px)`, animates in `300ms --ease-standard` with **150ms delay** |
| Login chip | grey bg, plum text, `height:52px`, `padding:12px 16px`, gap 8, semibold 11px uppercase ls 2.2; hover → plum/white `200ms ease` |
| Close chip | **volt bg**, plum text, same metrics; hover → plum/white |
| Nav wrapper | `padding: 0 42px 80px 76px; margin-top: 200px` (≤768: `margin-top:120px; padding:0 40px 80px`) |
| Nav label | semibold `0.6875rem`, uppercase, ls 2.2px, `margin-bottom: 32px` |
| Primary list gap | `16px`; secondary list gap `0` |
| Primary link | `--font-regular`, `2.5625rem` (41px) / `1.75rem` (28px) ≤768, `line-height: 1.1`, colour plum |
| Secondary link | `1.375rem` (22px) |
| Item enter | `opacity:0; translateY(20px)` → `opacity:1; translateY(0)`, `400ms --ease-standard`, inline `transition-delay` **0, 60, 120, 180, 240ms** |
| Text roll-up hover | link contains two identical `<span>`s in `.mobile-panel--text-slide-inner`; hover → `translateY(-50%)` over `300ms --ease-standard`. Slide window heights: primary `58px` (≤768 `40px`), secondary `45px` |
| Sub-items | `height:0; opacity:0` → auto/1 (JS); first child `margin-top:16px`; link `1.25rem`, `padding:16px 0`, `opacity:.65` → `1` on hover over `200ms ease` |
| Nav arrow | rotates `90deg` when `.is-selected`, `300ms --ease-standard` |
| Secondary column | `opacity:0; translateX(40px)` → `0`, `400ms --ease-standard`; its items `translateX(20px)` → `0`, `350ms` |
| CTA block | `padding: 0 76px 48px` (≤768 `0 40px 48px`), `margin-top:auto`; items `margin-bottom:12px` |
| Focus | `outline: 2px solid #631F82; outline-offset: 2px` |

### 6.6 Buttons

#### 6.6.1 Text button

```css
.button {
  display: inline-block; position: relative; width: auto;
  padding: 12px 16px; border: none; border-radius: 0; text-decoration: none;
  font-family: var(--font-medium); font-size: 0.6875rem; line-height: 1.5rem;
  letter-spacing: 2.2px; text-transform: uppercase;
}
.button--primary   { background-color: var(--color-volt);  color: var(--color-black); }
.button--secondary { background-color: var(--color-white); color: var(--color-black); }
.button:hover      { background-color: var(--color-volt-hover); }
.button:has(.button--icon) { padding-left: 0; }
.button--link { padding: 0; font-size: 0.9rem; letter-spacing: 2.2px;
                text-transform: uppercase; color: var(--color-black); }
```

| State | Primary | Secondary | Link |
|---|---|---|---|
| Default | volt / black | white / black | transparent / black |
| Hover | `#bbee04` | `#bbee04` | inherits icon-swap only |
| Focus-visible | `outline: 2px solid #631F82; outline-offset: 2px` `[OBSERVED in header/panel]`, apply globally `[INFERRED]` | same | same |
| Disabled | not present in the reference — if needed: `opacity:.4; pointer-events:none` `[INFERRED]` | | |
| Mobile (`.button__mobile-width > *`) | `width:100%; text-align:center` at ≤768px | | |

Buttons carrying an icon nest the icon *inside*: `<a class="button button--primary"><div class="d-flex"><div class="button--icon">…</div>Label</div></a>`, and the left padding is removed so the circle sits flush. `[OBSERVED]`

#### 6.6.2 Circular icon button — the signature interaction

```css
.button--icon {
  position: relative; display: inline-block; overflow: hidden;
  width: 48px; height: 48px; padding: 0; border: none; border-radius: 100px;
  text-decoration: none;
}
.button--icon .button--circle {
  position: absolute; inset: -1px;
  clip-path: inset(8px 8px 8px calc(100% - 50px) round 100px);
  transition: clip-path 650ms var(--ease-clip), transform 650ms var(--ease-clip);
}
.button--icon .button--circle .circle-container {
  position: absolute; right: 0; width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.button--icon:hover .button--circle,
.hover--icon:hover .button--circle { clip-path: inset(0 round 4.25rem); }

/* two stacked arrows that swap */
.arrow--animation.is-1 { opacity: 1; transform: translateZ(0); }
.arrow--animation.is-2 { position: absolute; opacity: 0; transform: translate3d(-165%, 0, 0); }
.button--icon:hover .arrow--animation.is-1,
.hover--icon:hover  .arrow--animation.is-1 { opacity: 0; transform: translate3d(165%, 0, 0); }
.button--icon:hover .arrow--animation.is-2,
.hover--icon:hover  .arrow--animation.is-2 { opacity: 1; transform: translateZ(0); }

.button--icon.button--plum  { background-color: var(--color-plum); }
.button--icon.button--plum svg { fill: #fff; }
.button--icon.button--plum i   { color: #fff; }
.button--icon.button--volt  { background-color: var(--color-volt); }
.button--icon.button--white { background-color: #fff; }
.button--icon.button--grey  { background-color: var(--color-grey); } /* carousel arrows [INFERRED] */
```

**Behaviour:** at rest the coloured fill is clipped to a small pill on the right edge; on hover the clip expands to the full circle while arrow #1 exits right and arrow #2 enters from the left. `[OBSERVED]`

**Crucial:** `.hover--icon` on an ancestor (card, row) triggers the same animation — the icon button is *never* hovered directly on cards; the whole card drives it. `[OBSERVED]`

| Context | Size |
|---|---|
| Base / hero video controls | 48px (32px at ≤768px in the hero) |
| Case-grid row | 54px |
| CTA-block card | 56px |
| Carousel prev/next | 80px, inner svg `1.5rem` |

### 6.7 Hero

```css
.hero { position: relative; min-height: 720px; height: 80vh; max-height: 90vh; }
@media (max-width: 576px) { .hero { min-height: 460px; height: 460px; max-height: 600px; } }
.hero--content { position: absolute; left: 40px; bottom: 40px; z-index: 1; max-width: 640px; }
@media (max-width: 576px) { .hero--content { left: 16px; bottom: 24px; } }
.hero--title { margin: 0; color: #fff; font-size: clamp(24px, 8vw, 80px); }
@media (max-width: 576px) { .hero--title { font-size: 40px; } }
.hero--image, .hero--video { position: absolute; top: 0; width: 100%; height: 100%; overflow: hidden; }
.hero--video video { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                     min-width: 100%; min-height: 100%; width: auto; height: auto; }
.hero--video-buttons { position: absolute; right: 0; bottom: 0; z-index: 1;
                       display: flex; gap: 16px; padding: 40px; }
@media (max-width: 768px) { .hero--video-buttons { padding: 16px; gap: 8px; }
                            .hero--video-buttons .button--icon { width: 32px; height: 32px; } }
@media (max-width: 576px) { .hero--video-buttons { flex-direction: column; gap: 8px; } }
```

- Content structure: `<section class="hero" data-header-theme="light"> > .container.h-100 > .hero--container.h-100 > .hero--content > h1.hero--title`. `[OBSERVED]`
- `data-header-theme="light"` marks the element the header IntersectionObserver watches. `[OBSERVED]`
- The video is client-hydrated; a centred SVG spinner occupies the space until it loads. `[OBSERVED]`
- Video modal: `position:fixed; inset:0; z-index:9999; display:flex; center`; backdrop `rgba(0,0,0,.8)`; content starts `opacity:0; transform:scale(.9)` and animates in; video `border-radius:8px; box-shadow:0 0 30px rgba(0,0,0,.6)`; close button white circle at `top:-20px; right:-20px`; `body.modal-open header { opacity: 0; pointer-events: none }`. `[OBSERVED]`

### 6.8 CTA blocks (paired feature cards)

```css
.cta-blocks-advanced__grid { /* .row.g-0 */ }
.cta-blocks-advanced__card { display: flex; flex-direction: column; width: 100%;
                             overflow: hidden; color: inherit; text-decoration: none; }
.cta-blocks-advanced__banner { position: relative; margin: 0; width: 100%; height: 192px;
                               overflow: hidden; background: var(--color-plum); flex-shrink: 0; }
.cta-blocks-advanced__banner img { width: 100%; height: 100%; object-fit: cover; display: block;
                                   transition: transform 600ms var(--ease-image); }
.cta-blocks-advanced__card--linked:hover .cta-blocks-advanced__banner img { transform: scale(1.05); }
.cta-blocks-advanced__backdrop { position: absolute; inset: 0;
                                 background: var(--overlay-card-backdrop); pointer-events: none; }
.cta-blocks-advanced__body { flex: 1 1 auto; display: flex; flex-direction: column;
                             gap: 32px; padding: 48px; }
.cta-blocks-advanced__wrapper { flex: 1 1 auto; display: grid;
                                grid-template-columns: 5fr 1fr; gap: 24px; width: 100%; }
.cta-blocks-advanced__icon-button { justify-self: end; align-self: end; }
@media (max-width: 991px) { .cta-blocks-advanced__body { padding: 32px; gap: 24px; }
                            .cta-blocks-advanced__wrapper { grid-template-columns: 1fr; gap: 24px; } }
@media (max-width: 576px) { .cta-blocks-advanced__banner { height: 160px; }
                            .cta-blocks-advanced__body { padding: 24px 16px; } }
```

| Property | Value |
|---|---|
| Grid | `.row.g-0` with `col-lg-6 col-12 d-flex`; cards `height: 100%` |
| Card element | the whole card is a single `<a>` (`--linked`), `aria-label` = title |
| Banner image position variants | `--position-top/bottom/left/right/center` → `object-position` |
| Body background variants | `--bg-grey`, `--bg-white`, `--bg-plum` (forces white text), `--bg-volt` |
| Title | `clamp(1.5rem, 1.25rem + 1.5vw, 2.5rem)`, `--font-light`, `line-height:1.1`, plum |
| Content | `--font-regular`, `1rem`, `line-height:1.5`, `#000`; `p + p { margin-top: 1em }` |
| Icon button | 56px, bottom-right of the 5fr/1fr grid |
| Hover | image `scale(1.05)` + icon circle expands (via `.hover--icon`) |
| Focus | `outline: 2px solid #2E103B; outline-offset: 2px` |
| Horizontal variant | `--grid--horizontal`: card `row-reverse`, banner/body `flex: 1 1 50%`, body `padding: 64px 121px 64px 48px`, `gap: 64px`, `justify-content: center`; `--card--image-side-left` → `row`; ≤1199 `padding-right: 64px`; ≤991 `column-reverse` + `padding: 48px; gap: 32px`, banner back to 192px |
| Mobile image size modifiers | `--mobile-image-large` (320px), `--mobile-image-square` (`aspect-ratio: 1/1`), `--mobile-image-full` (`height:auto; object-fit: contain`) — all ≤991px |

### 6.9 Case grid (full-width alternating rows)

```css
.cases-grid__header { display: flex; align-items: center; justify-content: space-between;
                      gap: 32px; padding: 96px 48px; }
@media (max-width: 991px) { .cases-grid__header { padding: 64px 16px; } }
.cases-grid__heading { margin: 0; font-family: var(--font-light);
                       font-size: clamp(2rem, 1.25rem + 3vw, 3.5rem); line-height: 1.1; color: var(--color-plum); }
.cases-grid__list { display: flex; flex-direction: column; }
.cases-grid__row  { display: flex; align-items: stretch; text-decoration: none; color: inherit;
                    transition: background-color 300ms var(--ease-image); }
.cases-grid__row--grey  { background-color: var(--color-grey); }
.cases-grid__row--white { background-color: var(--color-white); }
.cases-grid__body { flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; padding: 48px; }
.cases-grid__body > * + * { margin-top: 32px; }
.cases-grid__body > .cases-grid__meta + .cases-grid__title { margin-top: 16px; }
.cases-grid__meta { display: flex; gap: 16px; flex-wrap: wrap; }
.cases-grid__meta-item { font-family: var(--font-medium); font-size: 12px;
                         letter-spacing: 0.2em; text-transform: uppercase; color: var(--color-plum); }
.cases-grid__title { margin: 0; font-family: var(--font-regular);
                     font-size: clamp(1.5rem, 1.25rem + 1vw, 2rem); line-height: 1.1; color: var(--color-plum); }
.cases-grid__wrapper { display: flex; flex-direction: column; align-items: flex-start; gap: 48px; }
.cases-grid__text { max-width: 664px; font-family: var(--font-regular); font-size: 1rem;
                    line-height: 1.5; color: var(--color-plum);
                    display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical;
                    overflow: hidden; text-overflow: ellipsis; min-height: 6em; }
.cases-grid__image { flex: 1 1 0; margin: 0; min-width: 0; min-height: 320px;
                     overflow: hidden; position: relative; }
.cases-grid__image img { position: absolute; inset: 0; width: 100%; height: 100%;
                         object-fit: cover; display: block;
                         transition: transform 600ms var(--ease-image); }
.cases-grid__row.hover--icon:hover .cases-grid__image img { transform: scale(1.05); }
.cases-grid__row:focus-visible { outline: 2px solid #2E103B; outline-offset: -2px; }
@media (max-width: 991px) {
  .cases-grid__row  { flex-direction: column-reverse; }
  .cases-grid__body { padding: 32px 16px; }
  .cases-grid__body > * + * { margin-top: 24px; }
  .cases-grid__image { flex: 0 0 auto; width: 100%; height: auto; min-height: 0; aspect-ratio: 16/9; }
}
@media (max-width: 767px) { .cases-grid__wrapper { gap: 24px; } }
```

Row order: **meta chips → title → (copy + icon button)**. The icon button is 54px, `align-items: flex-start` in the wrapper. Rows alternate `--grey` / `--white` starting with grey. `[OBSERVED]`

### 6.10 Text + bleeding visual

```css
.content-text-side-visual { position: relative; overflow: clip; }
.content-text-side-visual article { position: relative; z-index: 1; padding: 48px; min-height: 0; }
.content-text-side-visual--stack { display: flex; flex-direction: column; gap: 48px; align-items: flex-start; }
.content-text-side-visual--article h3 { margin: 0; font-family: var(--font-light);
                                        font-size: 2rem; line-height: 1.4; color: var(--color-plum); }
.content-text-side-visual--body { margin: 0; font-family: var(--font-regular);
                                  font-size: 1rem; line-height: 1.6; color: var(--color-plum); }
.content-text-side-visual--body.content-fit--quarter { max-width: 437px; }
.content-text-side-visual--body p { margin: 0; }
.content-text-side-visual--body p + p { margin-top: 1.6em; }

.content-text-side-visual--visual { position: absolute; top: 0; right: 0; width: 60%; z-index: 0; }
.content-text-side-visual--visual.content-fit--half { width: 48%; }
@media (min-width: 992px) {
  .content-text-side-visual--visual.added-distance {
    width: max(940px, calc(60% + 10vw)); right: -10vw; left: auto; max-width: none;
  }
  .content-text-side-visual--visual.added-distance.content-fit--half { width: max(780px, calc(48% + 10vw)); }
}
@media (max-width: 991px) {
  .content-text-side-visual--visual,
  .content-text-side-visual--visual.added-distance { position: relative; right: 0; width: 100%; }
  .content-text-side-visual article { padding: 48px 16px; }
}
@media (max-width: 576px) { .content-text-side-visual article { padding: 32px 16px; } }
```

Padding modifiers: `--pt-sm/md/lg` = 32/64/96px, `--pb-sm/md/lg` identical; at ≤576px `md` → 48 and `lg` → 64. `--pt-none` / `--pb-none` for touching sections. `[OBSERVED]`

`--match-height` variant makes the visual a flex sibling (`flex: 1 1 0`) with `min-width: max(940px, 60% + 10vw)`, `margin-right: -10vw`, `padding-right: 10vw` — the image fills the row height with `object-fit: cover`; at ≤991px it goes `object-fit: contain`, full width. `[OBSERVED]`

### 6.11 Lead statement block (`content-text-side-cta`)

```css
.content-text-side-cta--container { background-color: #fff; padding: 64px 48px; }
.content-text-side-cta--container.background--grey { background-color: var(--color-grey); }
@media (max-width: 576px) { .content-text-side-cta--container { padding: 48px 16px; } }
.content-text-side-cta--body   { font-size: 2rem; margin: 0; }
.content-text-side-cta--body p { font-size: 2rem; margin-bottom: 48px; }
@media (max-width: 576px) { .content-text-side-cta--body p { font-size: 1.25rem; margin-bottom: 48px; } }
```
Column: `col-xxl-9 col-lg-8 col-md-10 col-sm-12 col-12`, `.row.justify-content-start.gx-0`. The copy is `--font-light` with `mb-0`. The optional side article has `h3 { font-size: 2rem; margin-bottom: 64px }` and a full-width, centred button. `[OBSERVED]`

### 6.12 Section header block (`content-block`)

```css
.content-block--container { padding: 96px 48px; }
@media (max-width: 576px) { .content-block--container { padding: 32px 16px; } }
.content-block--container.background--plum { color: #fff; }
.content-block--container.background--plum :is(h1,h2,h3,h4,h5,h6,p) { color: #fff !important; }
.content-block .box--inner { max-width: 480px; }
.content-block--content strong { font-size: 2rem; line-height: 140%; }
@media (min-width: 768px) { .content-block .text-md-end { text-align: right; } }
```
Layout: `.row > .col-md-8` (heading, `.font-size--xl`) + `.col-md-4.text-md-end` (primary button). `[OBSERVED]`

### 6.13 Testimonial carousel (Swiper)

```css
.carousel--container { background-color: #fff; padding: 0 48px; overflow: hidden; }
.carousel--swiper { display: flex; overflow: visible !important; }
.carousel--slide { width: auto !important; flex-shrink: 0; }
.carousel--card  { display: flex; }
.carousel--block-large  { display: flex; gap: 64px; }
.carousel--block-medium { display: flex; gap: 32px; }
.carousel--block-small  { display: flex; gap: 16px; }
.carousel figure { margin: 0; width: auto; height: 400px; }
.carousel--image { width: 100%; height: 100%; object-fit: cover; }
.carousel--profile { width: 300px !important; height: 400px !important; }
.carousel--profile img { width: 100%; height: 100%; object-fit: cover; }
.carousel--logo { width: 80px; height: 80px; }
.carousel--content { width: 460px; }
.carousel--name { position: relative; padding-top: 3rem; }
.carousel--name::after { content: ""; position: absolute; left: 0; top: 24px;
                         width: 54px; height: 1px; border-top: 1px solid #1B0020; }
.carousel--pagination-block .carousel--prev,
.carousel--pagination-block .carousel--next { width: 80px !important; height: 80px !important; }
.carousel--pagination-block :is(.carousel--prev, .carousel--next) svg { width: 1.5rem; }
.carousel--pagination-block :is(.carousel--prev, .carousel--next)::after { display: none; } /* kill Swiper glyphs */
@media (max-width: 768px) {
  .carousel figure { position: relative; }
  .carousel--content { width: 100%; padding: 0 24px; }
  .carousel--logo { width: auto; height: 80px; position: absolute;
                    background: #fff; bottom: 24px; right: 24px; }
  .carousel--prev { left: -54px; } .carousel--next { right: -54px; }
}
@media (max-width: 576px) {
  .carousel--profile { width: 200px !important; height: 300px !important; }
  .profile-mobile-width { width: calc(100vw - 94px); }
  .carousel--block-medium { gap: 32px; }
}
```

Slide anatomy `[OBSERVED]`: `logo (80×80) + portrait (300×400)` → `quote (font-size--md, light, 460px) + attribution (font-size--sm with the 54px rule)` → `three supporting images (400px tall, auto width)`, joined by `--block-large` (64px) / `--block-medium` (32px) / `--block-small` (16px) flex groups.

Swiper options from the island props: `{ type: "slider", display_limit: 5, navigation: "show", card_color: "white" }`. Slides are free-width (`width:auto`), so this is a **drag/arrow horizontal transport, not a fixed-slide-per-view carousel**. `[OBSERVED]`

### 6.14 Logo marquee

```css
.marquee-streamer--container { background-color: #fff; overflow: hidden; }
.marquee-streamer .wrapper { position: relative; display: flex; align-items: center;
                             width: calc(100% + 200px); height: auto; overflow: hidden; }
.marquee-streamer--box { position: relative; display: flex; align-items: center; justify-content: center;
                         height: 100%; margin: 0; padding: 0; flex-shrink: 0; overflow: hidden; }
.marquee-streamer--box .box--inner { padding: 50px 0; width: 100%; height: 100%; }
.marquee-streamer--box.type--images .box--inner { padding: 0; }
.marquee-streamer--box.box--image { width: 400px; overflow: hidden; }
.marquee-streamer--box.box--image.type--logos { width: 180px; height: 180px; margin: 0 1.5rem; }
.marquee-streamer--box.box--image.type--logos .box--inner { padding: 0; }
.marquee-streamer--box.box--image img { width: 100%; height: 100%; object-fit: cover; }
.marquee-streamer--box .box--logos { display: flex; }
.marquee-streamer--box .box--logos img { margin: auto; max-width: 100%; max-height: 100%; object-fit: contain; }
```

- 17 logo tiles at 180×180 with `24px` side margins (`1.5rem`), images `object-fit: contain`. `[OBSERVED]`
- Continuous right-to-left translation, JS-driven (the `calc(100% + 200px)` over-width exists to hide the wrap seam). `[OBSERVED — mechanism]`
- **Speed:** not present in the source. Use `≈ 40s` for one full loop, `linear`, infinite, no pause on hover. `[INFERRED]`

Implementation `[INFERRED]`:
```css
@keyframes marquee-x { from { transform: translate3d(0,0,0); }
                       to   { transform: translate3d(-50%,0,0); } }
.marquee-streamer .wrapper { animation: marquee-x 40s linear infinite; }
@media (prefers-reduced-motion: reduce) { .marquee-streamer .wrapper { animation: none; } }
```
Duplicate the tile list twice in the DOM for a seamless `-50%` loop.

### 6.15 CTA streamer (image-backed band)

```css
.streamer--inner { position: relative; z-index: 0; padding: 96px 48px; color: #fff; }
@media (max-width: 576px) { .streamer--inner { padding: 64px 16px; } }
.streamer--inner-custom-padding { padding: 48px; }
@media (max-width: 991px) { .streamer--inner-custom-padding { padding: 48px 16px; } }
@media (max-width: 576px) { .streamer--inner-custom-padding { padding: 32px 16px; } }
.streamer .background-image { position: absolute; inset: 0; z-index: -1; margin: 0;
                              width: 100%; height: 100%; }
.streamer .background-image img { width: 100%; height: 100%; object-fit: cover; }
.streamer .title { color: #fff; max-width: 100%; min-width: 0;
                   text-wrap: balance; hyphens: auto; overflow-wrap: anywhere; }
.call-to-action-streamer { overflow: hidden; }
.call-to-action-streamer--header { margin-bottom: 80px; }
.call-to-action-streamer .box--inner { max-width: 480px; }
```
Content sits in `col-md-6`: `h3.title.font-size--xl` (white, 56px) → body `p` → `.button.button--primary`. `[OBSERVED]`

**Employee variant** (`.streamer--employee`) `[OBSERVED]`: at ≥992px the row is absolutely positioned to `inset: 0` with `align-items: stretch`, the portrait's `ratio-1x1` is neutralised (`aspect-ratio: auto`) so the image fills the band height; the info panel has `padding: 32px` (24 ≤991, 16 ≤576); name `.font-size--lg` steps 32 → 24 → 20px; contact links are `--font-light`, sentence case, colour plum, `text-decoration: none`; at ≤576px contact gap 8px and icons 20×20.

### 6.16 Footer

```css
.footer { width: 100%; }
.footer--gap { row-gap: 48px; }
.footer--widgets { padding: 64px 48px; background-color: var(--color-grey); }
@media (max-width: 576px) { .footer--widgets { padding: 32px 16px; }
                            .footer .widget { margin-bottom: 48px; } }
.footer h4 { font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2.2px;
             margin-bottom: 32px; font-family: var(--font-medium); }
.footer ul { list-style: none; margin: 0; padding: 0; }
.footer ul li a { color: var(--color-plum); font-size: 0.875rem; }
.footer a { text-decoration: none; font-family: var(--font-regular); text-transform: uppercase; }
.footer p { color: var(--color-plum); }

.footer--certificates { padding: 32px 48px; background-color: #fff; }
@media (max-width: 576px) { .footer--certificates { padding: 32px 16px; } }
.footer--certificates .certificates--image { position: relative; width: 72px; height: 72px;
                                             padding: 0; margin: 0 0.5rem; }
.footer--line { width: 100%; height: 1px; background-color: var(--color-grey); }
.footer--copyright { padding: 48px; background-color: #fff; }
@media (max-width: 576px) { .footer--copyright { padding: 32px 16px; } }
.footer--copyright :is(span, a) { margin: 0 1rem; color: var(--color-plum);
                                  text-transform: none !important; font-family: var(--font-light) !important; }
```

Structure: **widgets band (grey) → certificates band (white, centred) → 1px line → copyright band (white)**. Widget columns `col-lg-2 col-md-4` × 6 (menu, social, then one per country office). `[OBSERVED]`

### 6.17 Language switcher

| State | Spec |
|---|---|
| Trigger (desktop, in header) | grey bg, plum text, `height: 52px`, `padding: 12px 16px`, gap 8, `--font-medium` `0.6875rem` uppercase ls 2.2px; hover → plum/white `200ms ease` |
| Trigger (legacy `.language__switcher--selected`) | grey bg, `height: 46px`, `padding: 8px 12px`, `0.75rem`, `line-height: 2.5`; hover → **volt** bg; `transition: all 500ms var(--ease-standard)` |
| Position ≤991px | `position: fixed; bottom: 16px; right: 16px; z-index: 9999` |
| Popup | `position: absolute; top: 100%; right: 0`, white, `padding: 8px`, `gap: 2px`, `box-shadow: 0 8px 80px rgba(0,0,0,.15)`, `z-index: 10002`, `max-width: calc(100vw - 48px)` |
| Popup ≤768px | opens upward: `top: auto; bottom: 100%` |
| Popup arrow (legacy) | 8px CSS triangle in `#F1F1F1`, top `-8px`, right `12px`; flips below at ≤768px |
| Country label | semibold `0.6875rem`, uppercase, ls 2.2px, `padding: 6px 14px 2px` |
| Language row | `--font-regular` `1rem`, `min-height: 40px` (44px inside the mobile panel), `padding: 8px 14px`; hover/focus bg `#f1f1f1`; focus outline `2px solid #2E103B` offset 2px |
| Flags | 16×16 `background-size: contain`, `margin-right: 8px` |

### 6.18 Spinner (loading placeholder)

```css
.spinner { width: 100%; height: 100%; display: flex; }
.spinner svg { margin: auto; }
.panel__content--light .spinner svg { stroke: #fff; }
@keyframes spinner_rotate { to { transform: rotate(360deg); } }
@keyframes spinner_dash {
  0%        { stroke-dasharray: 0 150;  stroke-dashoffset: 0; }
  47.5%     { stroke-dasharray: 42 150; stroke-dashoffset: -16; }
  95%, 100% { stroke-dasharray: 42 150; stroke-dashoffset: -59; }
}
.spinner__ring { transform-origin: center; animation: spinner_rotate 2s linear infinite; }
.spinner__ring circle { stroke-linecap: round; animation: spinner_dash 1.5s ease-in-out infinite; }
```
SVG: `24×24`, `viewBox 0 0 24 24`, `circle r=9.5`, `fill:none`, `stroke-width:3`, `stroke:#000`. `[OBSERVED]`

### 6.19 Accordion (present in the theme, used on inner pages)

| Property | Value `[OBSERVED]` |
|---|---|
| Item | `display:flex; flex-direction:column; padding: 12px 0` |
| Header | `display:flex; gap:2rem; align-items:center; cursor:pointer; transition: all 300ms ease-in-out` |
| Number | `1.25rem`, muted |
| Title | `3rem`, `--font-regular`, plum, `flex: 1` |
| Suffix (toggle) | `40×40`, `border-radius:100px`, `padding:12px` (≤768: `32×32`, `padding:10px`) |
| Icon | 16×16 plus-sign built from two `::before/::after` bars (2px), `transition: transform 250ms ease-out`; open → `rotate(90deg)` / `rotate(180deg)` (plus → minus) |
| Details | `height: 0; overflow: hidden` → `height: auto` when `.open` |
| Accordion title label | `--font-regular`, uppercase, `ls 2.2px`, `0.75rem`, `line-height: 2.5` |

> The reference's accordion sets placeholder colours (`gray`, `red`, `blue`) that are clearly unfinished. **Use the palette instead:** suffix background `var(--color-grey)` → `var(--color-volt)` on hover/open, icon bars `var(--color-plum)`. `[INFERRED]`

### 6.20 Components NOT present in the reference

Do **not** invent these; if the template needs them, derive them from the rules above and mark them clearly:

badges/chips (other than the `.cases-grid__meta-item` text label and heading `<span>` chip), tabs, tooltips, pagination dots, breadcrumbs (a HubSpot default exists but is unstyled), data tables, toasts, avatars, progress bars, form inputs (the homepage has **no form**; forms are HubSpot-rendered elsewhere).

**Form field derivation** `[INFERRED]`, if you must build one:
```css
.field { height: 52px; padding: 12px 16px; border: none; border-radius: 0;
         background: var(--color-white); color: var(--color-plum);
         font-family: var(--font-regular); font-size: 1rem; }
.field:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
.field__label { font-family: var(--font-medium); font-size: 0.6875rem;
                letter-spacing: 2.2px; text-transform: uppercase; margin-bottom: 8px; display: block; }
textarea.field { height: auto; min-height: 10em; }
```
(52px, zero radius, no border, 12/16 padding and the uppercase 11px label all match the nav/button/language-trigger system.)

---

## 7. Images and media

| Rule | Spec | Basis |
|---|---|---|
| Default fit | `object-fit: cover` with `width:100%; height:100%` | `[OBSERVED]` |
| Logos only | `object-fit: contain; max-width:100%; max-height:100%; margin:auto` | `[OBSERVED]` |
| Background image pattern | `figure.background-image { position:absolute; inset:0; margin:0; width:100%; height:100%; z-index:0 }` — in streamers `z-index: -1` | `[OBSERVED]` |
| `.image` | `width:100%; overflow:hidden` | `[OBSERVED]` |
| `.image--full` | `width:100%; display:inline-flex`, img `object-fit: cover` | `[OBSERVED]` |
| Border radius on media | **0**, always | `[OBSERVED]` |
| Aspect ratios in use | `1/1` (nav card, CTA mobile-square, employee portrait), `16/9` (case image ≤991px), `3/4` (carousel portrait 300×400 / 200×300), fixed `192px` / `160px` / `320px` / `400px` heights | `[OBSERVED]` |
| Utility ratios | `.ratio-1x1`, `.ratio-16x9` — both `display:flex; align-items:center; justify-content:center; width:100%` | `[OBSERVED]` |
| Hover zoom | `transform: scale(1.05)` over `600ms var(--ease-image)` — only on linked cards and case rows | `[OBSERVED]` |
| Overlay on CTA banner | flat `rgba(27,0,32,0.35)` full-cover `<span>`, `pointer-events:none` | `[OBSERVED]` |
| Overlay on nav card | double gradient `--gradient-nav-card` (dark at top, transparent from 62%) | `[OBSERVED]` |
| Scrim utilities | `.background-gradients--black-fade::before` and `.background--fade::after` (navy) — bottom-to-top fades | `[OBSERVED]` |
| Filters | **none** — no grayscale, blur, or brightness filters anywhere | `[OBSERVED]` |
| Responsive images | native `srcset` + `sizes="(max-width: 1440px) 100vw, 1440px"`; widths served at 400 / 640 / 720 / 1440 / 2160 / 2880 / 3600 / 4320 | `[OBSERVED]` |
| Loading | first CTA banner and first case image `loading="eager" fetchpriority="high"`; everything below `loading="lazy" fetchpriority="auto" decoding="async"` | `[OBSERVED]` |
| Video (hero) | `<video>` absolutely centred with `translate(-50%,-50%)`, `min-width/min-height: 100%`, `width/height: auto` — cover-crop without `object-fit` | `[OBSERVED]` |
| Video (inline visual) | `.visual--video video { display:block; width:100%; height:auto }` | `[OBSERVED]` |
| Poster / fallback | still image + centred SVG spinner until the island hydrates | `[OBSERVED]` |

---

## 8. Iconography

| Property | Spec | Basis |
|---|---|---|
| Format | inline SVG, no icon font | `[OBSERVED]` |
| Style | geometric, monoline; arrows are the dominant glyph | `[OBSERVED]` |
| Fill vs stroke | UI glyphs (arrows, chevrons, close, user, globe) are **filled paths**; only the loading spinner uses stroke | `[OBSERVED]` |
| Stroke width where stroked | `3` on the 24px spinner ring; use `1.5–2px` for any line icon you add at 24px | `[OBSERVED]` / `[INFERRED]` |
| Sizes | 16×16 (flags, accordion plus), 20×20 (contact icons ≤576px), 24×24 (spinner, carousel arrow `1.5rem`), inside 48/54/56/80px circular buttons | `[OBSERVED]` |
| Colour | inherits: `fill: #fff` on plum buttons; plum on volt/white/grey buttons; `currentColor` for inline label icons | `[OBSERVED]` |
| Icon↔label gap | **8px** everywhere (`gap: 8px` on nav links, chips, hamburger, language rows) | `[OBSERVED]` |
| Chevron placement | `margin-left: 6px; margin-bottom: 1px`, rotated `180deg` closed → `0` open | `[OBSERVED]` |
| Arrow pairing | every circular button holds **two** arrow SVGs (`.arrow--animation.is-1` / `.is-2`) for the slide-swap | `[OBSERVED]` |
| Logo | 57×24 SVG, `fill="white"` (primary) and `fill="#1B0020"` (dark) variants of the same paths | `[OBSERVED]` |

---

## 9. Animations and transitions

### 9.1 Global motion tokens

| Token | Value | Where used |
|---|---|---|
| `--ease-standard` | `cubic-bezier(0.25, 0.1, 0.25, 1)` | header background, dropdown, mobile panel, language rows, page slide-in |
| `--ease-emphasized` | `cubic-bezier(0.4, 0, 0.2, 1)` | header hide/show transform |
| `--ease-clip` | `cubic-bezier(0.785, 0.135, 0.15, 0.86)` | icon-button `clip-path` |
| `--ease-image` | `cubic-bezier(0.65, 0, 0.35, 1)` | image `scale`, case-row background |
| `ease` | — | the `.cubic-ease` utility (`transition: all 500ms ease`) |
| `ease-in-out` | — | chevron rotation |
| `linear` | — | hamburger opacity/filter, spinner rotation, marquee |

`.cubic-ease` is applied liberally in the markup (logos, buttons, images, figures, nav links) as a catch-all `all 500ms ease`. Port it as a utility class and keep applying it to the same elements. `[OBSERVED]`

### 9.2 Complete motion inventory

| # | Animation | Trigger | Duration | Easing | Delay | From → To | Basis |
|---|---|---|---|---|---|---|---|
| A1 | **Smooth scroll** (Lenis, `lerp: 0.1`, vertical) | page scroll | — | interpolated | — | native scroll → eased scroll | `[OBSERVED]` |
| A2 | **Header hide on scroll down** | scroll direction change (`layout.hide_on_scroll: true`) | 300ms | `--ease-emphasized` | 0 | `translateY(0)` → `translateY(-100%)`; reverses on scroll up | `[OBSERVED]` |
| A3 | **Header palette switch** | hero leaves viewport / dropdown opens | 300ms | `--ease-standard` | 0 | transparent bg → `#f1f1f1`; logo/tagline crossfade opacity `0↔1` | `[OBSERVED]` |
| A4 | **Logo crossfade** | same as A3 | 300ms | `--ease-standard` | 0 | white logo `opacity 1→0`, dark logo `0→1` (stacked absolutely) | `[OBSERVED]` |
| A5 | **Nav chevron rotate** | dropdown open | 500ms | `ease-in-out` | 0 | `rotate(180deg)` → `rotate(0)` | `[OBSERVED]` |
| A6 | **Mega-dropdown open** | click / hover nav item | ~300ms `[INFERRED]` | `--ease-standard` `[INFERRED]` | 0 | `height:0; opacity:0` → measured height, `opacity:1` (JS-driven) | `[OBSERVED markup]` |
| A7 | **Dropdown panel crossfade** | switching between nav items | ~200ms `[INFERRED]` | `--ease-standard` | 0 | inactive `opacity:0; pointer-events:none` → active `opacity:1; pointer-events:all`, both absolutely stacked | `[OBSERVED]` |
| A8 | **Dropdown link hover** | hover | 500ms (`.cubic-ease`) | `ease` | 0 | colour `#030104` → `#631f82` | `[OBSERVED]` |
| A9 | **Dropdown card button hover** | hover | 300ms | `--ease-standard` | 0 | volt/plum → plum/white | `[OBSERVED]` |
| A10 | **Icon-button circle reveal** | hover on button **or** on `.hover--icon` ancestor | **650ms** | `--ease-clip` | 0 | `clip-path: inset(8px 8px 8px calc(100% - 50px) round 100px)` → `inset(0 round 4.25rem)` | `[OBSERVED]` |
| A11 | **Arrow slide-swap** | same trigger as A10 | 650ms (shares the transition) `[INFERRED]` | `--ease-clip` `[INFERRED]` | 0 | arrow1 `translateZ(0)/op 1` → `translate3d(165%,0,0)/op 0`; arrow2 `translate3d(-165%,0,0)/op 0` → `translateZ(0)/op 1` | `[OBSERVED transforms]` |
| A12 | **Card image zoom** | hover on `.cta-blocks-advanced__card--linked` or `.cases-grid__row` | 600ms | `--ease-image` | 0 | `scale(1)` → `scale(1.05)` | `[OBSERVED]` |
| A13 | **Case row background** | hover | 300ms | `--ease-image` | 0 | background-color transition (no colour change declared — reserved for a hover tint) | `[OBSERVED]` |
| A14 | **Button background** | hover | 500ms (`.cubic-ease`) | `ease` | 0 | volt `#cfff00` → `#bbee04` | `[OBSERVED]` |
| A15 | **Nav item invert** | hover | 500ms (`.cubic-ease`) | `ease` | 0 | white/plum → plum/white | `[OBSERVED]` |
| A16 | **Hamburger** | hover | 150ms | `linear` | 0 | grey → volt background (`transition-property: opacity, filter`) | `[OBSERVED]` |
| A17 | **Mobile panel slide-in** | hamburger click | ~400ms `[INFERRED]` | `--ease-standard` `[INFERRED]` | 0 | `translateX(100%)` → `translateX(0)`, `visibility hidden→visible` | `[OBSERVED states]` |
| A18 | **Panel overlay fade** | same | 300ms | `--ease-standard` | 0 | `opacity 0 → 1`, `pointer-events none → auto` | `[OBSERVED]` |
| A19 | **Panel topbar enter** | panel `.is-open` | 300ms | `--ease-standard` | **150ms** | `opacity 0, translateY(-10px)` → `opacity 1, translateY(0)` | `[OBSERVED]` |
| A20 | **Panel nav item stagger** | panel `.is-open` | 400ms | `--ease-standard` | **0/60/120/180/240ms** (inline `transition-delay`) | `opacity 0, translateY(20px)` → `opacity 1, translateY(0)` | `[OBSERVED]` |
| A21 | **Panel secondary column** | sub-menu selected | 400ms | `--ease-standard` | 0 | `opacity 0, translateX(40px)` → `opacity 1, translateX(0)`, `pointer-events none → auto` | `[OBSERVED]` |
| A22 | **Panel secondary items** | same | 350ms | `--ease-standard` | 0 | `opacity 0, translateX(20px)` → `opacity 1, translateX(0)` | `[OBSERVED]` |
| A23 | **Panel link text roll-up** | hover on `.mobile-panel--nav-link` | 300ms | `--ease-standard` | 0 | `.mobile-panel--text-slide-inner: translateY(0)` → `translateY(-50%)`, revealing the duplicate span. Window heights: 58px / 40px (≤768) primary, 45px secondary | `[OBSERVED]` |
| A24 | **Panel sub-item expand** | click a parent link | JS height animation `[OBSERVED markup: height:0; opacity:0]`; use **300ms `--ease-standard`** | `--ease-standard` | 0 | `height 0 → auto`, `opacity 0 → 1` | `[OBSERVED]` / duration `[INFERRED]` |
| A25 | **Panel arrow rotate** | parent `.is-selected` | 300ms | `--ease-standard` | 0 | `rotate(0)` → `rotate(90deg)` | `[OBSERVED]` |
| A26 | **Sub-item link opacity** | hover | 200ms | `ease` | 0 | `opacity .65` → `1` | `[OBSERVED]` |
| A27 | **Page slide-in (legacy accordion menu)** | `body.mobile-slide-in` | **750ms** | `--ease-standard` | 0 | `#main-content` shifts; `header::before` black scrim `opacity 0 → .75` | `[OBSERVED]` |
| A28 | **Accordion toggle** | click | 250ms | `ease-out` | 0 | plus icon bars `rotate(90deg)` / `rotate(180deg)`; details `height 0 → auto` | `[OBSERVED]` |
| A29 | **Accordion header** | hover | 300ms | `ease-in-out` | 0 | suffix background change | `[OBSERVED]` |
| A30 | **Marquee transport** | always on | ~40s loop `[INFERRED]` | `linear` | 0 | `translate3d(0,0,0)` → `translate3d(-50%,0,0)`, infinite | mechanism `[OBSERVED]`, speed `[INFERRED]` |
| A31 | **Carousel slide** | arrow click / drag | Swiper default 300ms `[INFERRED]` | Swiper default `ease` `[INFERRED]` | 0 | `translate3d` on `.swiper-wrapper` | `[OBSERVED lib]` |
| A32 | **Hero video modal open** | click play | ~300ms `[INFERRED]` | `--ease-standard` `[INFERRED]` | 0 | content `opacity 0, scale(.9)` → `opacity 1, scale(1)`; header `opacity → 0` | `[OBSERVED start state]` |
| A33 | **Spinner** | while an island hydrates | 2s rotate + 1.5s dash | `linear` / `ease-in-out` | 0 | infinite | `[OBSERVED]` |
| A34 | **Language trigger hover** | hover | 200ms / 500ms (legacy) | `ease` / `--ease-standard` | 0 | grey → plum-white, or grey → volt | `[OBSERVED]` |

### 9.3 Motion that does NOT exist — do not add it

`[OBSERVED absence — verified across every stylesheet in the capture]`

- ❌ No scroll-triggered fade-in / slide-up reveals for sections, headings, or paragraphs.
- ❌ No parallax on any background image.
- ❌ No page-transition / route-transition animation.
- ❌ No text-splitting or per-character/per-word reveals.
- ❌ No counters, number tickers, or progress animations.
- ❌ No sticky-scroll pinning or scroll-scrubbed timelines.
- ❌ No cursor follower or custom cursor (only `cursor: pointer`).
- ❌ No 3D transforms, perspective, or rotation on content.
- ❌ No spring/bounce easing anywhere.

The page is **static on scroll**; all motion is either hover-triggered, menu-triggered, or continuous transport (marquee/carousel). Preserve this restraint — adding scroll reveals is the single easiest way to make the rebuild stop looking like the reference.

### 9.4 Reduced motion `[INFERRED]`

Not handled in the reference. Add it — it costs nothing and cannot alter the static appearance:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important; animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important; scroll-behavior: auto !important;
  }
  .marquee-streamer .wrapper { animation: none; }
}
```
Also disable Lenis smooth scrolling when the query matches.

---

## 10. Grid animations

**Explicit finding: the reference contains no true grid animation.** `[OBSERVED absence]`

Verified against every stylesheet in the capture — there is **no**:

- staggered card/grid-cell reveal on scroll or on load;
- animated grid resizing, column-count transition, or `grid-template` animation;
- masonry layout or masonry reflow animation;
- FLIP / layout-shift animation when a grid re-orders at a breakpoint;
- scroll-driven vertical or horizontal offset of grid columns;
- filter/sort transition on any collection.

The grids (`.row.g-0` card pair, `.cases-grid__list`, footer widget row) are **static flex/grid layouts**. Breakpoint changes happen instantly via media queries, with no transition on the layout properties.

### What *is* grid-adjacent motion, and must be reproduced

| Motion | What actually moves | Spec |
|---|---|---|
| **Marquee horizontal transport** | the whole `.wrapper` flex track of 17 logo tiles | continuous `translate3d(-50%)` loop, `linear`, ~40s `[INFERRED speed]`, over-width `calc(100% + 200px)`, parent `overflow: hidden` |
| **Carousel horizontal transport** | the Swiper `.swiper-wrapper` track of auto-width slides | drag + arrow-driven `translate3d`, slides `overflow: visible` so neighbours bleed past the 48px-padded container |
| **Per-cell hover** | *inside* a cell, never the cell itself | image `scale(1.05)` 600ms `--ease-image` + icon `clip-path` 650ms `--ease-clip` |
| **Stagger** | mobile menu items only — **not** any content grid | `transition-delay: 0/60/120/180/240ms` |

**Rule:** if the template you are modifying already animates grids on scroll, **remove that behaviour** for sections rebuilt from this spec. A cell may animate its own contents on hover; the grid itself never moves.

---

## 11. Interaction behavior

### 11.1 Hover

| Target | Effect |
|---|---|
| Primary/secondary button | background → `#bbee04` |
| Nav link | white/plum → plum/white (invert) |
| Nav link `.highlight` | volt/plum → plum/white |
| Dropdown menu link | colour → `#631f82` |
| Dropdown card button | volt/plum → plum/white |
| Hamburger, `myiwell` chip, language option | grey → volt |
| Login/close/lang chips in panel | grey/volt → plum/white |
| Linked card (whole card is the hover target) | banner image `scale(1.05)` **and** icon-button circle expands **and** arrows swap |
| Case row | image `scale(1.05)` + icon circle expands; row background transitions |
| Mobile panel primary link | text rolls up 50% to the duplicate span |
| Mobile panel sub-item | `opacity .65 → 1` |
| Video modal close | `#fff` → `#eee` |
| Circular icon button (direct) | clip-path expand + arrow swap |

**Pattern rule:** a card's icon button is decorative and marked `aria-hidden="true" inert` — it never receives its own hover. Drive it from `.hover--icon` on the parent `<a>`. `[OBSERVED]`

### 11.2 Click

- Nav parent items are `<button aria-expanded aria-haspopup aria-controls>` toggling `.header--dropdown--content.open`. `[OBSERVED]`
- Hamburger is `<button id="hamburger" aria-expanded aria-controls="mobile-panel">`. `[OBSERVED]`
- Mobile parent items are `<button aria-expanded aria-controls="mobile-submenu-N">`. `[OBSERVED]`
- Whole cards and case rows are single `<a>` elements with `aria-label`. `[OBSERVED]`
- The hero play button opens the fullscreen video modal; `body` gets `.modal-open`. `[OBSERVED]`
- A "scroll to section" pattern exists: `lenis.scrollTo(target, { duration: 2, offset: -200 })`. `[OBSERVED]`

### 11.3 Scroll

- Lenis smooth scroll: `new Lenis({ lerp: 0.1, smooth: true, direction: "vertical" })` driven by `requestAnimationFrame`. `[OBSERVED]`
- IntersectionObserver watches `[data-header-theme="light"]` to toggle the header palette. `[OBSERVED]`
- Scroll direction toggles `.header--up` / `.header--down` / `.header--scroll-hidden`. `[OBSERVED]`
- Scrollable overlays opt out with `data-lenis-prevent`. `[OBSERVED]`
- **No other scroll-linked behaviour exists.** `[OBSERVED absence]`

### 11.4 Drag / swipe

Only the Swiper carousel is draggable/swipeable. The marquee is not interactive. `[OBSERVED]`

### 11.5 Sticky

`position: fixed` header only. There are no `position: sticky` elements. `[OBSERVED]`

### 11.6 Modals & overlays

| Overlay | z-index | Scrim | Scroll lock |
|---|---|---|---|
| Mega-dropdown | 998 | none (header turns `#f1f1f1`) | no |
| Mobile panel | 10001 | `rgba(0,0,0,.4)` at 10000 | `overscroll-behavior: contain` + `data-lenis-prevent` |
| Language popup | 10002 | none | no |
| Video modal | 9999 | `rgba(0,0,0,.8)` | header hidden via `body.modal-open` |

### 11.7 Focus & accessibility `[OBSERVED]`

```css
.header a:focus-visible, .header button:focus-visible,
.mobile-panel a:focus-visible, .mobile-panel button:focus-visible,
#hamburger:focus-visible { outline: 2px solid #631F82; outline-offset: 2px; }

.cases-grid__row:focus-visible { outline: 2px solid #2E103B; outline-offset: -2px; }
.cta-blocks-advanced__card--linked:focus-visible { outline: 2px solid #2E103B; outline-offset: 2px; }
.language-popup--lang:focus-visible { outline: 2px solid #2E103B; outline-offset: 2px; }
```
Rule: **purple `#631F82` ring in the header/panel chrome, plum `#2E103B` ring in content.** Offset is `2px`, except `-2px` on case rows so the ring stays inside the full-bleed row.

Also present: `role="dialog" aria-modal="true"`, `aria-current="true"` on the active language, `inert` + `aria-hidden="true"` on decorative icon buttons, `role="list"` on stripped lists, `aria-label` on every icon-only control. Reproduce all of it. `[OBSERVED]`

### 11.8 Cursor

`cursor: pointer` on all interactive elements; `cursor: default` on the current language. No custom cursor. `[OBSERVED]`

---

## 12. Desktop implementation

Build order, top to bottom, at ≥1200px. Every section is `<section> > .container > [module wrapper]`. `.container` is `max-width: 1800px`, centred, **no horizontal padding**.

### 12.1 Header (fixed overlay)

```
header.header.cubic-ease
└ .container
  └ .header--content.header--container            padding: 32px 48px
    └ .d-flex.align-items-center.justify-content-between
      ├ .col-xl-3.d-flex.header--logo--container   z-index: 200
      │ └ .header--logo.my-auto                    height: 32px; margin-right: 40px
      │   ├ a > img.header--logo-primary           white logo, 57×24
      │   ├      img.header--logo-dark             absolutely stacked, opacity 0, margin-top 4px
      │   └ span.header--tagline.d-none.d-xl-block "Established in the EU"
      └ .col-lg-9.d-flex.justify-content-end
        └ .header--navigation                      height:100%; z-index:20; justify-content:center
          └ section.header--submenu.d-none.d-xl-block
            └ .submenu--container.d-flex.justify-content-end   z-index: 200
              └ nav.submenu > ul.submenu--list > li.submenu--item × N
                 (button.submenu--link or a.submenu--link; last item .highlight)
            └ .header--dropdown                    absolute top:100%; height:0; opacity:0; z-index:998
```

- Nav items: 52px tall, `padding: 12px 16px`, white background, **no gap** — they form one continuous bar flush right.
- Dropdown inner: white flex row — links column `flex:1; padding:40px; gap:32px`, feature card `flex:0 0 30%; min-width:280px; aspect-ratio:1/1; padding:32px`.
- Language switcher sits in `.langauge-switcher--container.d-none.d-xl-block`, right of the nav.
- Header sits *over* the hero: transparent, white logo/tagline. On scroll past the hero it hides on scroll-down and shows the dark palette on scroll-up.

### 12.2 Hero — full-bleed video band

| Property | Value |
|---|---|
| Container | `.container.h-100 > .hero--container.h-100` |
| Height | `min-height: 720px; height: 80vh; max-height: 90vh` |
| Media | `<video>` filling the section, centred cover-crop; no overlay by default |
| Content | absolute `left: 40px; bottom: 40px`, `max-width: 640px` |
| Title | `h1.hero--title`, white, `clamp(24px, 8vw, 80px)`, `line-height: 1.1`, `margin: 0`, `<br>` for the intended line break |
| Controls | absolute bottom-right, `padding: 40px`, `gap: 16px`, 48px circular icon buttons (play / mute) |
| Header hook | `data-header-theme="light"` on `<section>` |

**Responsive note:** the title's `8vw` means it hits 80px at 1000px viewport width and stays there; do not let it exceed 80px.

### 12.3 Lead statement band

```
section.content-text-side-cta > .container
└ .content-text-side-cta--container.background--grey      padding: 64px 48px
  └ .row.justify-content-start.gx-0
    └ .col-xxl-9.col-lg-8.col-md-10.col-12
      └ .mx-auto > .content-text-side-cta--body
        └ p.font-weight--light.mb-0                        font-size: 2rem; line-height: 135%
```
A single 32px light paragraph on grey, occupying 66–75% of the width. No heading, no button. This is the page's "manifesto" beat.

### 12.4 Text + bleeding visual

```
section.content-text-side-visual.--stretch.--pt-none.--pb-none > .container
└ .content-text-side-visual--container
  └ .row.justify-content-start.gx-0
    ├ article.col-xxl-4.col-lg-4.col-12                      padding: 48px
    │ └ .content-text-side-visual--stack                     gap: 48px; align-items: flex-start
    │   ├ h3.content--dark                                   2rem / 1.4, light
    │   ├ .content-text-side-visual--body.content-fit--quarter  max-width: 437px; 1rem/1.6, regular
    │   └ .content-text-side-visual--footer.d-flex
    │     └ a.button.button--primary.ps-0                    icon-in-button variant
    └ .content-text-side-visual--visual.--match-height.added-distance.content-fit--quarter
      .col-xxl-8.col-lg-8.col-md-6.col-12.order-2.d-flex
      └ figure.background-image > img.image                  fills row height, object-fit: cover
```
The visual is `min-width: max(940px, 60% + 10vw)` with `margin-right: -10vw; padding-right: 10vw`, so it runs **past the right viewport edge**. The section is `overflow: clip`; `body` is `overflow-x: hidden`. This deliberate bleed is a signature move — reproduce it exactly.

### 12.5 Paired CTA cards

```
section.cta-blocks-advanced > .container
└ .row.g-0.cta-blocks-advanced__grid.--vertical
  └ .col-lg-6.col-12.d-flex   × 2
    └ a.cta-blocks-advanced__card.--position-center.--linked.hover--icon
      ├ figure.cta-blocks-advanced__banner        height: 192px, cover, data-header-theme="light"
      │ ├ img (1440×1440 source, srcset)
      │ └ span.cta-blocks-advanced__backdrop      rgba(27,0,32,.35)
      └ .cta-blocks-advanced__body.--bg-grey      padding: 48px; gap: 32px
        ├ h2.cta-blocks-advanced__title           clamp(1.5rem,1.25rem+1.5vw,2.5rem), light
        └ .cta-blocks-advanced__wrapper           grid 5fr 1fr; gap 24px
          ├ .cta-blocks-advanced__content         1rem/1.5, regular, #000
          └ span.cta-blocks-advanced__icon-button (aria-hidden, inert)
            └ button.button--icon.button--plum    56px
```
Two equal cards butt together with zero gutter. Cards stretch to equal height (`.cta-blocks-advanced__grid .card { height: 100% }`), the icon button pinned bottom-right by the 5fr/1fr grid.

### 12.6 Case list

```
section.cases-grid > .container
├ .cases-grid__header                    flex; space-between; gap 32px; padding 96px 48px
│ ├ h2.cases-grid__heading               clamp(2rem,1.25rem+3vw,3.5rem), light
│ └ .cases-grid__header-cta > a.button.button--primary
└ .cases-grid__list                      flex column
  └ a.cases-grid__row.--grey|--white.hover--icon   × 4, alternating
    ├ .cases-grid__body                  flex 1 1 0; padding 48px
    │ ├ .cases-grid__meta                flex; gap 16px  → span.cases-grid__meta-item × 2
    │ ├ h3.cases-grid__title             (16px below meta)
    │ └ .cases-grid__wrapper             flex column; align-items flex-start; gap 48px
    │   ├ .cases-grid__text              max-width 664px; line-clamp 4; min-height 6em
    │   └ span.cases-grid__icon > button.button--icon.button--plum   54px
    └ figure.cases-grid__image           flex 1 1 0; min-height 320px; img absolute cover
```
Text left, image right, 50/50. Backgrounds alternate grey → white → grey → white. The whole row is one link.

### 12.7 Section header + action (`content-block`)

```
section.content-block > .container
└ .content-block--container.blog.background--white    padding: 96px 48px
  └ .row
    ├ .col-md-8  > h3.font-size--xl                   56px light, mb 48px
    └ .col-md-4.text-md-end > a.button.button--primary
```

### 12.8 Testimonial carousel

```
section.carousel > .container
└ .carousel--container                     background #fff; padding 0 48px; overflow hidden
  └ .row.justify-content-center
    └ section.slider > .col-12
      └ .swiper.carousel--swiper           display flex; overflow visible !important
        └ .swiper-wrapper
          └ .swiper-slide.carousel--slide  width auto
            └ .carousel--card.carousel--block-large      gap 64px
              ├ .carousel--block-medium.profile-mobile-width   gap 32px
              │ ├ .carousel--logo.d-flex                 80×80 partner logo
              │ └ figure.carousel--profile               300×400 portrait, cover
              ├ .carousel--block-medium > .carousel--block-small
              │ └ .carousel--content                     width 460px
              │   ├ p.font-weight--light.font-size--md   24px quote
              │   └ .carousel--name.font-size--sm        14px, 3rem top padding + 54px rule
              └ .carousel--block-medium                  gap 32px, 3 supporting images 400px tall
      └ .carousel--pagination-block                      80px prev/next icon buttons
```

### 12.9 Logo marquee

```
section.marquee-streamer > .container
└ .marquee-streamer--container            background #fff; overflow hidden
  └ .row.justify-content-center
    └ #wrapper-NNNN.wrapper               width calc(100% + 200px); flex; align-items center
      └ .marquee-streamer--box.box--image.type--logos  × 17 (duplicate the set for the loop)
        180×180, margin 0 1.5rem
        └ .box--inner > .box--logos.d-flex.h-100 > figure.background-image > img (contain)
```

### 12.10 Closing CTA streamer

```
section.streamer > .container
└ .row.h-100.g-0
  ├ .col-12.streamer--inner                padding 96px 48px; color #fff; z-index 0
  │ └ .row.my-auto > .col-md-6
  │   ├ h3.title.font-size--xl.font-weight--light   56px white
  │   ├ .call-to-action-streamer--body > p
  │   └ a.button.button--primary
  └ figure.background-image > img          absolute inset 0; z-index -1; cover
```

### 12.11 Footer

```
footer.footer > .container
├ .footer--widgets            padding 64px 48px; background #f1f1f1
│ └ .row.justify-content-start > .row.footer--gap (row-gap 48px)
│   └ .col-lg-2.col-md-4.widget × 6
│     ├ h4.font-weight--medium         0.9rem uppercase ls 2.2px, mb 32px
│     └ ul > li > a  (0.875rem, uppercase, regular, plum)  |  address <p>
├ .footer--certificates       padding 32px 48px; background #fff
│ └ .row.justify-content-center > .certificates--image × 3   72×72, margin 0 .5rem
├ .footer--line               height 1px; background #f1f1f1
└ .footer--copyright          padding 48px; background #fff
  └ .row > p + legal links    sentence case, light, plum, margin 0 1rem
```

---

## 13. Mobile implementation

At ≤576px this is **not** the desktop layout stacked — several compositional decisions change. Build in this order.

### 13.1 Header → a two-part fixed chrome

The desktop single header bar splits into **two independently positioned fixed elements**:

1. `header.header` keeps only the logo (left), `padding: 16px`, logo `height: 52px` (larger than desktop — it is the only branding left).
2. `.mobile-menu--container` is a **separate fixed element**, `top: 0; right: 0`, `height: 84px`, `padding: 0 16px`, `width: calc(100% − 200px)` (`calc(100% − 120px)` ≤480px), right-aligned, containing the `myiwell` chip and the hamburger.

Both chips are **45px tall** (not 52px) with `padding: 8px 12px` — the mobile chrome is denser than desktop.

The desktop nav and desktop language switcher are `display: none`. The language switcher reappears as a **fixed bottom-right button** (`bottom:16px; right:16px; z-index:9999`) whose popup opens **upward**.

### 13.2 Navigation → full-screen right panel

- Panel is `100vw` at ≤768px or in portrait, sliding from `translateX(100%)`.
- Topbar: `myiwell` (grey) + language + **Close (volt)**, `padding: 20px 24px`, entering with a 150ms delay.
- Nav starts **120px from the top** (`margin-top: 120px`) with `padding: 0 40px 80px` — a deliberately large empty zone above the links.
- Primary links are **28px** (vs 41px on tablet, vs 11px in the desktop bar) — the mobile menu is the only place the nav becomes display typography.
- Items enter staggered 60ms apart.
- Tapping a parent expands sub-items inline (`height: 0 → auto`) and rotates its arrow 90°; sub-links are 20px at `opacity: .65`.
- CTA block pinned to the bottom (`margin-top: auto`, `padding: 0 40px 48px`).

### 13.3 Hero → fixed-height band, not a viewport hero

**Composition change:** the hero stops being viewport-relative. `height: 460px` fixed (min 460, max 600). The title drops to a **fixed 40px** — it stops scaling with `8vw`. Content moves to `left: 16px; bottom: 24px`.

Video controls stack **vertically** (`flex-direction: column`, `gap: 8px`) in the bottom-right corner at 32px each, so they occupy a narrow strip rather than a horizontal row that would collide with the title.

**Visual priority on mobile:** headline > video > controls. The controls shrink and stack precisely so the 40px headline keeps the bottom-left quadrant.

### 13.4 Lead statement

`padding: 48px 16px`; the paragraph drops **32px → 20px** and keeps its 48px bottom margin. It is now the loudest text on the screen after the hero — do not shrink it further.

### 13.5 Text + visual → order preserved, bleed removed

The visual stops being absolute: `position: relative; width: 100%; right: 0`, and switches from `object-fit: cover` to **`object-fit: contain`** so the illustration is never cropped. Article padding `32px 16px`. DOM order is preserved (text above image) — this is the one section where the image does **not** move above the text.

### 13.6 CTA cards → stacked, image on top

`col-12` each. Banner 160px tall. Body `padding: 24px 16px`, `gap: 24px`. The `5fr 1fr` grid collapses to `1fr`, so the icon button drops **below** the copy but stays `justify-self: end` (bottom-right). Title lands at 24px.

Optional per-card mobile image treatments if the design calls for it: `--mobile-image-large` (320px), `--mobile-image-square` (1:1), `--mobile-image-full` (`height:auto; contain`).

### 13.7 Case rows → image above text (reversed)

**Composition change:** `flex-direction: column-reverse`. The image moves to the top at `aspect-ratio: 16/9` full-width; the text block follows at `padding: 32px 16px` with 24px internal rhythm. The 4-line clamp is kept, so every card stays the same height regardless of copy length. The 54px icon button stays bottom-left-aligned within the wrapper (`align-items: flex-start`), 24px below the copy.

Alternating grey/white backgrounds are retained — they are the only separator between stacked rows.

### 13.8 Section header + action

`content-block` collapses to `padding: 32px 16px`; `col-md-8`/`col-md-4` become full width, so the heading (32px) sits above a left-aligned button (`text-md-end` no longer applies below 768px).

### 13.9 Carousel → partial-slide peek

**Composition change:** the slide keeps `width: auto` and the container keeps `overflow: hidden` while the track is `overflow: visible`, so the **next slide peeks in from the right** — this is the mobile affordance for swipe. Reproduce it; do not switch to a one-slide-per-view carousel.

- Portrait shrinks to **200×300**; `.profile-mobile-width` sets `calc(100vw − 94px)`.
- The partner logo becomes an **absolute overlay** on the portrait: `bottom: 24px; right: 24px`, white background, `height: 80px`, auto width.
- Quote block goes full width with `padding: 0 24px`.
- Prev/next buttons move outside the container (`left: -54px` / `right: -54px`) so they don't cover the slide.

### 13.10 Marquee

Unchanged structurally: 180×180 tiles, 24px margins, same speed. On a 375px viewport roughly two tiles are visible — that is intended.

### 13.11 Closing CTA streamer

`padding: 64px 16px` (this band keeps 64px vertical, more than the 32px default — it is the conversion moment). The background image stays a full cover crop behind white text; `col-md-6` becomes full width. The button is left-aligned; if the template uses `.button__mobile-width`, it goes `width: 100%; text-align: center`.

### 13.12 Footer

- Widgets band `padding: 32px 16px`, each `.widget` gets `margin-bottom: 48px`, columns stack full width.
- Certificates: `padding: 32px 16px`, three 72×72 marks stay on one centred row.
- Copyright: `padding: 32px 16px`; links keep `margin: 0 1rem` and wrap.

### 13.13 Mobile spacing summary

| Zone | Value |
|---|---|
| Page side padding | **16px** (everywhere, no exceptions) |
| Band vertical padding | 32px default, 48px for the lead statement, 64px for case header and closing CTA |
| Card interior | `24px 16px` (CTA), `32px 16px` (case, article) |
| Stack gap inside a card | 24px |
| Fixed chrome height | 84px |
| Bottom-fixed language button | 16px from both edges |

---

## 14. Implementation rules for Claude

Follow these literally while adapting an existing template to this spec.

### 14.1 Scope and architecture

1. **Preserve the existing project architecture.** Do not introduce a framework, build step, CSS-in-JS layer, or component library that is not already in the template. Adapt the template's own components.
2. **Do not redesign the reference.** Your job is fidelity, not improvement. If something in the reference looks unbalanced or unconventional (the `-10vw` image bleed, the light-weight headings, the missing `border-radius`), that is the style — reproduce it.
3. **Reuse existing components before creating new ones.** Restyle the template's button/card/header rather than adding parallel implementations.
4. **Do not port the reference's HubSpot scaffolding.** `dnd-section`, `row-fluid`, `hs_cos_wrapper`, `widget-span`, `span12` and the island `<script>` blocks are CMS plumbing. Keep only the semantic layer: `section > .container > module wrapper > .row > .col-*`.

### 14.2 Tokens and values

5. **Introduce no arbitrary values.** Every colour, spacing, radius, duration and font size you write must come from section 2 or 3, or be derived from the scale there. If you need 20px of spacing, ask whether 16 or 24 is right — there is no 20 in the scale (except the `pt--small` ≤768px override).
6. **Use the CSS custom properties**, not raw hex/px, everywhere except inside the token definition block itself.
7. **Radius is 0 unless the element is a circular icon button.** Do not soften corners.
8. **Do not add shadows** to cards, sections, headers, or buttons. Only the three overlay shadows in section 2 exist.
9. **Do not add blur, backdrop-filter, glassmorphism, or gradients** beyond the four gradient tokens defined.
10. **Letter-spacing on any uppercase label is `2.2px` (or `0.2em` at 12px).** Never leave an uppercase label at default tracking.

### 14.3 Typography

11. **Headings use the light weight.** If your substitute font makes 300 look too heavy at 56px, reduce optical weight — never increase it.
12. **Never scale body copy or labels responsively.** Only display sizes change across breakpoints (section 3.6).
13. **Use the exact `clamp()` expressions** in section 3.3 rather than inventing new fluid formulas.

### 14.4 Layout and responsive

14. **`.container` has no horizontal padding.** Page inset comes from the module wrapper (`48px` / `16px`). Do not move it.
15. **Preserve responsive behaviour exactly** as tabulated in section 5.2. Match the *breakpoint values* too (`576 / 768 / 991 / 1199 / 1200 / 1400`).
16. **Stack with `column-reverse` where the reference does** (case rows, horizontal CTA cards) — do not reorder with `order:` and do not leave the image below the text.
17. **Sections never carry margin.** Rhythm comes from their own padding; adjacent sections touch.
18. **Match proportions before adding detail.** Get the 4/8 split, the 50/50 case row, the 5fr/1fr card grid, the 192px banner, the 320px case image and the 48/96px paddings right first. Decorative refinements come after.

### 14.5 Motion

19. **Do not invent interactions.** Implement only the animations in section 9.2. Explicitly do not add scroll reveals, parallax, page transitions, text-splitting, counters, or spring easing (section 9.3).
20. **The grid itself never animates** (section 10). Cells may animate their own contents on hover.
21. **Use the four easing tokens.** Do not substitute `ease-out`, `ease-in-out`, or a spring where the reference specifies a cubic-bezier.
22. **Card hover is driven from the parent**, via `.hover--icon` — never bind hover to the decorative icon button itself, and keep it `aria-hidden="true" inert`.
23. **Add `prefers-reduced-motion` handling** (section 9.4). This is the one addition to the reference that is always correct.

### 14.6 Fidelity of detail

24. **Do not simplify distinctive details.** Specifically preserve: the two-arrow slide-swap, the `clip-path` circle reveal, the `-10vw` image bleed, the alternating grey/white case rows, the 4-line clamp with `min-height: 6em`, the 54px hairline above the carousel attribution, the mobile text roll-up on menu links, the dual logo crossfade, and the peeking carousel slide on mobile.
25. **Keep the accessibility affordances**: `aria-expanded`/`aria-controls` on toggles, `aria-label` on icon-only controls, `role="dialog" aria-modal="true"` on the panel, `inert` on decorative buttons, `role="list"` on stripped lists, and the two focus-ring colours (`#631F82` chrome, `#2E103B` content).
26. **Keep desktop and mobile equally faithful.** Mobile is specified in section 13 as its own composition; do not ship "desktop, stacked".

### 14.7 When a value is unknown

27. **If an exact value cannot be determined, derive it systematically** from the nearest documented element — same component family, same size tier, same spacing step — and stay internally consistent across the whole build. Prefer an existing token over a new number.
28. **Mark such choices in code comments** as `/* INFERRED: … */` so they can be reviewed, exactly as `[INFERRED]` is used in this document.
29. **Never invent a colour.** If a state needs a colour that is not in section 2, use the closest documented state (usually the plum/white invert or the volt hover).

### 14.8 Verification checklist

Before declaring a section done, confirm:

- [ ] No `border-radius` other than `0`, `100px` (icon buttons), `8px` (video modal), `12px` (heading chip).
- [ ] No `box-shadow` on any layout element.
- [ ] Every uppercase label is 11–14px with `letter-spacing: 2.2px`.
- [ ] Every heading above 24px uses the light weight.
- [ ] Desktop section padding is `96px 48px` (or the documented exception); mobile is `… 16px`.
- [ ] `.container` is `max-width: 1800px`, centred, unpadded.
- [ ] Card hovers scale the image `1.05` over `600ms cubic-bezier(0.65,0,0.35,1)` **and** expand the icon circle over `650ms cubic-bezier(0.785,0.135,0.15,0.86)`.
- [ ] No scroll-triggered animation exists anywhere.
- [ ] Case rows and horizontal cards reverse to image-on-top at ≤991px.
- [ ] The bleeding visual reaches `right: -10vw` at ≥992px and `body` has `overflow-x: hidden`.
- [ ] The header hides on scroll-down, shows on scroll-up, and swaps logo/tagline palette past the hero.
- [ ] Mobile nav links are 28px, stagger 60ms, and roll up on hover; the panel is 100vw at ≤768px.
- [ ] Focus rings are present and use the correct colour per zone.
