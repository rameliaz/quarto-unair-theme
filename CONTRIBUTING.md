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

- [ ] Theme renders correctly with example.qmd
- [ ] Logos appear on all slides (except title)
- [ ] White logo switches on blue background
- [ ] Section dividers display correctly
- [ ] Tables, code blocks, callouts styled properly
- [ ] No console errors
- [ ] Works with `quarto install extension`

### Brand Compliance

Changes must follow UNAIR 2025 Brand Guidelines:
- Primary color: #14497F (UNAIR Blue)
- Accent color: #FFCB05 (UNAIR Yellow)
- Typography: Segoe UI / Inter
- Logo placement: per guidelines

## Project Structure

```
quarto-unair-theme/
├── _extensions/unair/    # Core theme files
│   ├── _extension.yml    # Extension config
│   ├── airlangga.scss    # Styles
│   └── theme.html        # JavaScript
├── img/                  # Logo files
├── example.qmd           # Example presentation
└── README.md             # Documentation
```

## Questions?

Open an issue or reach out to the maintainers.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
