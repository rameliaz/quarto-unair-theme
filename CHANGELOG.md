# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-09-11

### Fixed
- Title slide logo was small and off-center (appearing inline with the heading, top-right) because the theme's `.title-slide` CSS/JS selector actually matched Quarto's class for heading-only section-divider slides, not the real cover slide — which has `id="title-slide"` but class `quarto-title-block`, never class `title-slide`. Logo detection now matches on `id` and the logo is bigger (400×180px) and properly centered above the title block.
- Section divider slides (`# Heading {background-color="..."}`) showed the wrong (regular, not white) logo, for the same id/class collision — they were being treated as the cover slide.
- Logo on section dividers landed wherever the heading happened to be centered rather than staying close to it, and inconsistently between dividers: these slides' `<section>` shrink-wraps to its (short) content instead of filling the slide and is then centered as a unit, so viewport-relative positioning (`fixed`/`absolute`) had no reliable relationship to where the text actually landed. The logo is now a normal flow item stacked directly above the heading, so it always ends up close to the text.
- Logo position was inconsistent across regular content slides and some custom layouts (`.text-slide-bg`, `.columns-slide`): those sections set percentage padding directly on the `<section>`, which defaults to the `content-box` model with an explicitly-set width/height from reveal.js — so the padding added to that size instead of fitting inside it, overflowing the slide and shifting where the corner-anchored logo landed. Fixed with `box-sizing: border-box`.
- Logo on `.text-image` / `.image-text` slides was partially clipped (not appearing as a whole seal) because those layouts set `overflow: hidden` on the section, and the logo's default offset deliberately pokes slightly above the section's own top edge — cropping it. Removed the (unneeded) `overflow: hidden` there instead of moving the logo.
- Logo sat far above the heading on `.text-slide-bg` / `.columns-slide`: their own top padding pushes the heading down, but the logo stayed pinned near the slide's raw top edge. It now sits just above the heading's yellow rule, matching the gap on regular content slides.
- Slide numbers now consistently show on every slide except section dividers (previously inconsistent/always-on).
- Three-column layout (`.columns-slide`) text is now centered under each icon instead of left-aligned.
- Logo right edge now lines up flush with the tip of the heading's yellow rule on every slide, instead of undershooting it on regular content slides or overshooting it on `.text-slide-bg` / `.columns-slide`.
- Removed the logo from `.agenda-slide` — its own left-stripe label made the corner logo redundant.
- Several logo/footer/slide-number suppression rules (for `.section-slide`, `.quote-slide`, `.agenda-slide`, etc.) used `:has(.foo.present)`, which unintentionally matched reveal.js's parallel `.slide-background` div — that div copies the slide's classes plus a `.present` that lingers after navigating away, so the suppression leaked onto later, unrelated slides (e.g. the logo stayed hidden on "Introduction" after merely visiting the Agenda slide earlier). Qualified every such selector with the `section` tag so it only matches the live content slide.

### Added
- New opt-in slide layout formats, adapted from the CAIS Quarto template and restyled with UNAIR branding. Apply as a class on the heading that starts a slide:
  - `.agenda-slide` — numbered agenda/table of contents with a left grey stripe
  - `.section-slide` / `.section-slide-dark` — light and photo-background section dividers with a large background numeral
  - `.text-image` / `.image-text` — two-column slides with a full-bleed image on one side
  - `.text-slide-bg` — lead paragraph plus a shaded content box
  - `.columns-slide` — three-column icon/heading/text layout
  - `.overview-slide` — three-image grid with captions under a full-width title bar
  - `.quote-slide` / `.quote-slide-dark` — pull-quote layouts on light and photo backgrounds
  - `.closing-slide` — two-panel closing/contact slide
- `example.qmd` now demonstrates every new format under a "New Layout Formats" section
- Font Awesome 6 (via CDN) is now included with the theme, so `.qmd` files can use icon spans like `[ ]{.fa-solid .fa-envelope}` or `[ ]{.fa-brands .fa-github}`. Used in the closing slide's contact list (envelope, globe, Discord, Keybase, GitHub) in place of text labels.

## [1.0.1] - 2026-03-29

### Fixed
- Logo images (`logo.png`, `logo_white.png`) not appearing when rendering with `output-dir` set (e.g. to `docs/`)
- Root cause: `format-resources` is not a recognized Quarto extension key and was silently ignored; replaced with `resources` in `_quarto.yml` which correctly copies logos to the output directory preserving their path structure
- Removed non-functional `format-resources` key from `_extension.yml`
- Added `_quarto.yml` back to version control so users installing via `quarto use template` get the resources fix automatically

## [1.0.0] - 2025-01-25

### Added
- Initial release of Universitas Airlangga Quarto theme
- Official UNAIR branding (2025 guidelines)
- Automatic logo placement on all slides
- White logo variant for dark backgrounds
- Centered logo on title slides
- Section divider slides with blue background
- Pre-styled components:
  - Tables with UNAIR Blue headers
  - Code blocks with blue accent
  - Three callout box types (note, warning, important)
  - Two-column layouts
  - Custom color classes
- Professional typography (Segoe UI/Inter)
- Comprehensive documentation
- Example presentation
- MIT License

### Brand Compliance
- Primary color: UNAIR Blue (#14497F)
- Accent color: UNAIR Yellow (#FFCB05)
- Logo placement per brand guidelines
- Minimum clearance and sizing standards

## [Unreleased]

### Planned
- Additional callout styles
- More color theme variants
- Progress bar customization options
- Speaker notes styling
- Print CSS improvements

---

**Legend:**
- `Added` - New features
- `Changed` - Changes in existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security improvements
