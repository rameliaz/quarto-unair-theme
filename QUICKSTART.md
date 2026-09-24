# Quick Start Guide

Get started with the Universitas Airlangga Quarto theme in 5 minutes!

## Step 1: Install Quarto

If you haven't already:

- Download from [quarto.org](https://quarto.org/docs/get-started/)
- Or use: `brew install quarto` (macOS) / `choco install quarto` (Windows)

## Step 2: Install the Theme

### Option A: Start New Project (Recommended)

```bash
quarto use template rameliaz/quarto-unair-theme
```

This creates a new directory with everything set up.

### Option B: Add to Existing Project

```bash
cd your-project
quarto add rameliaz/quarto-unair-theme
```

> 📄 **Hosting on GitHub Pages:** if you publish your rendered slides from a `docs/` folder, add an empty `.nojekyll` file to it so GitHub Pages serves the output as-is instead of running it through Jekyll.
>
> To have Quarto copy it in on every render instead of doing it by hand, put the empty `.nojekyll` file in your project root and list it under `resources` in `_quarto.yml`:
> ```yaml
> project:
>   output-dir: docs
>   resources:
>     - .nojekyll
> ```

## Step 3: Create Your Presentation

Create `presentation.qmd`:

```yaml
---
title: "My Presentation"
author: "Your Name"
institute: "Universitas Airlangga"
format: unair-revealjs
---

## First Slide

Your content here!

## Second Slide

More content...

# Section Break {background-color="#14497F"}

New section!
```

## Step 4: Render

```bash
quarto render presentation.qmd
```

Or in RStudio: Click "Render" button

Your presentation will open in your browser.

## Tips

- **View example**: Open `example.qmd` to see all features
- **Customize**: Edit `_extensions/unair/airlangga.scss` for colors/fonts
- **Section slides**: Use `{background-color="#14497F"}` after headings
- **Callouts**: Try `::: {.callout-note}` for highlighted content

## Need Help?

- Check [README.md](README.md) for full documentation
- View [example.qmd](example.qmd) for working examples
- Open an [issue](https://github.com/rameliaz/quarto-unair-theme/issues) if stuck

## Next Steps

- Read the [full documentation](README.md)
- Explore the [example presentation](example.qmd)
- Customize colors and fonts
- Share your presentations!

---

**Questions?** Open an issue or see the Troubleshooting section of the [README](README.md).