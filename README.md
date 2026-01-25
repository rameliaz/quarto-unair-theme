# Universitas Airlangga Quarto Presentation Theme

A professional Quarto Revealjs presentation theme following Universitas Airlangga's official 2025 corporate branding guidelines.

[![Quarto](https://img.shields.io/badge/Made%20with-Quarto-blue)](https://quarto.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- ✅ **Official UNAIR Branding** - Colors, typography, and logo placement per 2025 brand guidelines
- ✅ **Professional Design** - Clean academic aesthetic for lectures and conferences
- ✅ **Smart Logo Management** - Automatic logo placement with white variant for dark backgrounds
- ✅ **Pre-styled Components** - Section headers, callouts, tables, and code blocks
- ✅ **Easy Customization** - Simple to adapt while maintaining brand consistency

## 📸 Preview

*[Screenshots will be added here]*

## 🚀 Installation

### Quick Install (Recommended)

```bash
quarto use template yourusername/quarto-unair-theme
```

This will create a new directory with the template and example presentation.

### Add to Existing Project

```bash
quarto add yourusername/quarto-unair-theme
```

## 📝 Usage

### Basic Setup

Create a `.qmd` file with this YAML header:

```yaml
---
title: "Your Presentation Title"
subtitle: "Your Subtitle"
author: "Your Name"
institute: "Universitas Airlangga"
date: today
format: unair-revealjs
---

## Your First Slide

Content here...
```

**Logo specifications:**
- Use official UNAIR horizontal logo (brandmark + wordmark)
- Format: PNG with transparent background
- Recommended size: 300-400px wide

### Section Dividers

Create blue section divider slides:

```markdown
# Section Title {background-color="#14497F"}

This is a section divider slide
```

The logo automatically switches to white on blue backgrounds!

## 🎨 Brand Colors

| Color | Hex | Usage |
|-------|-----|-------|
| **UNAIR Blue** | `#14497F` | Primary color, headings |
| **UNAIR Yellow** | `#FFCB05` | Accent color, highlights |
| **Red** | `#E6282B` | Alerts, important callouts |

### Using Brand Colors

```markdown
- [Blue text]{.unair-blue}
- [Text with yellow background]{.bg-unair-yellow}
```

## 📚 Component Examples

### Two-Column Layout

```markdown
:::: {.columns}
::: {.column}
Left column content
:::

::: {.column}
Right column content
:::
::::
```

### Callout Boxes

```markdown
::: {.callout-note}
**Note:** This is informative
:::

::: {.callout-warning}
**Warning:** Important notice
:::

::: {.callout-important}
**Important:** Critical information
:::
```

### Tables

Tables are automatically styled with UNAIR Blue headers:

```markdown
| Variable | Mean | SD |
|----------|------|-----|
| Age | 25.3 | 4.2 |
| Score | 78.5 | 12.1 |
```

### Code Blocks

```markdown
```r
library(ggplot2)

ggplot(data, aes(x, y)) +
  geom_point() +
  theme_minimal()
```
```

## ⚙️ Customization

### Adjust Logo Size

In `_extensions/unair/airlangga.scss`:

```scss
.reveal .slide-logo {
  max-height: 80px;  // Change this value
}
```

### Change Base Font Size

```scss
$presentation-font-size-root: 32px;  // Adjust as needed
```

### Modify Colors

```scss
$unair-blue: #14497F;    // Primary
$unair-yellow: #FFCB05;  // Accent
```

## 📋 Advanced Configuration

### Custom Reveal.js Options

```yaml
format:
  unair-revealjs:
    slide-number: true
    progress: true
    history: true
    center: false
    transition: slide
    chalkboard: true
```

### Incremental Lists

```yaml
format:
  unair-revealjs:
    incremental: true
```

Or per-slide:

```markdown
::: {.incremental}
- First item
- Second item
:::
```

## 🏗️ Project Structure

```
your-project/
├── _extensions/
│   └── unair/
│       ├── _extension.yml
│       ├── airlangga.scss
│       └── theme.html
├── img/
│   ├── logo.png
│   └── logo_white.png
└── presentation.qmd
```

## 🎯 Brand Compliance

This theme follows **Universitas Airlangga Logo Guidelines 2025**:

- ✅ Correct color usage (UNAIR Blue primary)
- ✅ Proper logo placement and spacing  
- ✅ Approved typography (Segoe UI/Inter)
- ✅ Professional academic aesthetic
- ✅ 15mm minimum clearance around logo

## 💡 Tips for Best Results

1. **Keep slides simple** - Aim for 3-5 bullet points per slide
2. **Use section headers** - Break presentation into logical sections
3. **Leverage callouts** - Highlight key information effectively
4. **Test your logos** - Ensure both regular and white versions look good
5. **Consistent formatting** - Use provided classes for uniform styling

## 🐛 Troubleshooting

### Styles not applying
- Confirm extension is installed: `quarto list extensions`
- Check YAML format: `format: unair-revealjs`
- Try: `quarto render --clean presentation.qmd`

### White logo not switching
- Verify `img/logo_white.png` exists
- Check section slide uses: `{background-color="#14497F"}`
- Case-sensitive hex code (lowercase preferred)

## 📖 Examples

See `example.qmd` in this repository for a complete demonstration of all features.

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

The UNAIR logo and brand elements remain property of Universitas Airlangga.

## 👏 Credits

**Theme created by:** Rizqy Amelia Zein with the help of Claude Sonnet 3.5
**Based on:** Universitas Airlangga Logo Guidelines 2025  
**Built with:** [Quarto](https://quarto.org)

## 📬 Contact

For questions or support:
- Open an [issue](https://github.com/rameliaz/quarto-unair-theme/issues)
- Contact me at [amelia.zein@psikologi.unair.ac.id](mailto:amelia.zein@psikologi.unair.ac.id)

---

**Keywords:** quarto, revealjs, presentation, theme, universitas-airlangga, unair, indonesia, academic, slides
