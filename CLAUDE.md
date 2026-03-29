# CLAUDE.md — Quarto UNAIR Theme

This file documents project conventions and context for Claude Code assistance.

## Project Overview

A **Quarto Revealjs presentation theme** implementing Universitas Airlangga (UNAIR) official 2025 corporate branding guidelines. Published as a Quarto extension (`unair-revealjs` format).

- **Author**: Rizqy Amelia Zein
- **Version**: 1.0.0
- **License**: MIT (code); UNAIR logo is institutional property
- **Quarto requirement**: >= 1.4.0

## Key Files

| File | Purpose |
|------|---------|
| `_extensions/unair/_extension.yml` | Extension registration |
| `_extensions/unair/airlangga.scss` | All SCSS theme styles |
| `_extensions/unair/theme.html` | JavaScript logo management + inline styles |
| `example.qmd` | Working demo presentation |
| `README.md` | Full user documentation |
| `QUICKSTART.md` | 5-minute setup guide |
| `CHANGELOG.md` | Version history (Keep a Changelog format) |

## Brand Colors

```scss
$unair-blue:   #14497F;  // Primary — headings, links, table headers
$unair-yellow: #FFCB05;  // Accent — underlines, borders
$unair-red:    #E6282B;  // Alerts / warnings
```

## Architecture

- **SCSS** (`airlangga.scss`): All visual styling. Split into `scss:defaults` (variables) and `scss:rules` (component rules).
- **JavaScript** (`theme.html`): `manageLogos()` runs on `DOMContentLoaded` and `Reveal.slidechanged`. Inserts `logo.png` (regular) or `logo_white.png` (white variant) depending on slide background.
- **Logo switching logic**: white logo when `data-background-color="#14497F"` (section divider slides); regular logo all other slides; centered logo on title slide (index 0).

## GitHub Pages (`docs/`)

- Output goes to `docs/` via `project.output-dir` in `_quarto.yml`.
- `_quarto.yml` sets `format.unair-revealjs.output-file: index.html` so GitHub Pages serves the correct entry point.
- The supporting assets folder is named `example_files/` (based on source filename) — this is expected; `index.html` references it correctly via relative paths.
- Re-render with `quarto render example.qmd` after any changes.

## Development Conventions

- Keep all SCSS changes inside `_extensions/unair/airlangga.scss`.
- Keep all JavaScript/HTML changes inside `_extensions/unair/theme.html`.
- Logo assets live in both `_extensions/unair/` (for packaged extension) and `img/` (for local preview).
- Follow UNAIR 2025 brand guidelines — do not introduce colors outside the approved palette.
- Test changes using `example.qmd` before committing.
- Use semantic versioning; update `CHANGELOG.md` and `_extension.yml` version on releases.
- `output-file` in `_quarto.yml` must be under `format.unair-revealjs`, not `format.revealjs` — Quarto does not inherit project-level `revealjs` settings for custom extension formats.

## Custom CSS Classes (available in .qmd files)

- `.unair-blue`, `.unair-yellow`, `.unair-red` — text color
- `.bg-unair-blue`, `.bg-unair-yellow` — background color

## Installation (for users)

```bash
# New project
quarto use template rameliaz/quarto-unair-theme

# Add to existing project
quarto add rameliaz/quarto-unair-theme
```
