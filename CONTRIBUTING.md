# Contributing to Quarto UNAIR Theme

Thank you for considering contributing to this project! 🎉

## How to Contribute

### Reporting Issues

- Check if the issue already exists
- Use the issue template
- Include:
  - Quarto version (`quarto --version`)
  - Operating system
  - Steps to reproduce
  - Expected vs actual behavior
  - Screenshots if relevant

### Suggesting Enhancements

- Open an issue with the "enhancement" label
- Describe the feature clearly
- Explain why it would be useful
- Consider brand guideline compliance

### Pull Requests

1. **Fork the repository**

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Test thoroughly
   - Update documentation if needed

4. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- **SCSS**: Follow existing indentation (2 spaces)
- **JavaScript**: Use clear variable names, add comments
- **YAML**: Maintain consistent structure

### Testing Checklist

Before submitting PR, test:

- [ ] `quarto render example.qmd` finishes without warnings
- [ ] Logos appear on every slide except the agenda, quote and overview slides (centered cover logo on the title slide)
- [ ] White logo on dark slides (blue dividers, the closing slide)
- [ ] Brand sidebar and its slide number show on content slides only
- [ ] Section dividers, tables, code blocks and callouts look right
- [ ] No console errors, also on a phone-width window (Reveal's scroll view)
- [ ] Works when installed with `quarto add` into another project

### Brand Compliance

Changes must follow UNAIR 2025 Brand Guidelines:
- Primary color: #14497F (UNAIR Blue)
- Accent color: #FFCB05 (UNAIR Yellow)
- Complementary color: #E6282B (UNAIR Red), as an accent only, never for alerts or warnings
- Otherwise only black and white
- Typography: Segoe UI / Inter
- Logo placement: per guidelines

## Project Structure

```
quarto-unair-theme/
├── _extensions/unair/    # The extension
│   ├── _extension.yml    # Extension config
│   ├── airlangga.scss    # Styles
│   ├── theme.html        # Logo, sidebar and shrink-to-fit JavaScript
│   ├── unair.lua         # Embeds the logos, passes `short-title` to theme.html
│   ├── keygraphic.svg    # Source of the sidebar key graphic
│   ├── keypattern.svg    # Source of the batik strip
│   └── logo*.png         # Logos
├── pptx/                 # PowerPoint template and its build scripts
├── docs/                 # Rendered demo for GitHub Pages
├── img/snapshot.gif      # README preview
├── example.qmd           # Example presentation
└── README.md             # Documentation
```

## Questions?

Open an issue or reach out to the maintainers.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
