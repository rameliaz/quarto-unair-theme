# Universitas Airlangga Quarto Presentation Theme

A reproducible Quarto Revealjs presentation theme following Universitas Airlangga's official 2025 corporate branding guidelines.

[![Quarto](https://img.shields.io/badge/Made%20with-Quarto-blue)](https://quarto.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- ✅ **Official UNAIR Branding** - Colors, typography, and logo placement per 2025 brand guidelines
- ✅ **Professional Design** - Clean academic aesthetic for lectures and conferences
- ✅ **Smart Logo Management** - Automatic logo placement with white variant for dark backgrounds
- ✅ **Pre-styled Components** - Section headers, callouts, tables, and code blocks
- ✅ **11 Slide Layout Formats** - Agenda, section dividers, image bleeds, 3-columns, quotes, and more
- ✅ **Easy Customization** - Simple to adapt while maintaining brand consistency

## 📸 Preview

<video src="./img/snapshot.mp4" controls width="100%">
  Your browser does not support the video tag. Watch the preview at ./img/snapshot.mp4.
</video>

See [`example.qmd`](example.qmd) for a live demonstration of every slide layout.

## 🚀 Installation

### Quick Install (Recommended)

```bash
quarto use template rameliaz/quarto-unair-theme
```

This will create a new directory with the template and example presentation.

### Add to Existing Project

```bash
quarto add rameliaz/quarto-unair-theme
```

Then add `format: unair-revealjs` to your `.qmd` file's YAML header. See [`QUICKSTART.md`](QUICKSTART.md) for a 5-minute setup walkthrough.

## 🏗️ Project Structure

```
quarto-unair-theme/
├── _extensions/
│   └── unair/
│       ├── _extension.yml      # Extension registration
│       ├── airlangga.scss      # Theme styles (SCSS)
│       ├── theme.html          # Logo management JS + inline styles
│       ├── logo.png            # Regular logo
│       └── logo_white.png      # White logo (dark backgrounds)
├── img/
│   ├── logo.png                # Logo for local preview
│   ├── logo_white.png          # White logo for local preview
│   └── snapshot.mp4            # Preview video
├── docs/                       # Rendered GitHub Pages output
├── example.qmd                 # Working demo presentation
├── _quarto.yml                 # Project configuration
├── README.md
├── QUICKSTART.md                # 5-minute setup guide
├── CHANGELOG.md                 # Version history
└── LICENSE
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details. The UNAIR logo and brand elements remain property of Universitas Airlangga. I prompted Claude Sonnet 5 to improve the theme.