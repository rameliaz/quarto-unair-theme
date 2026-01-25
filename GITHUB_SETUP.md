# GitHub Repository Setup Guide

Follow these steps to publish your Quarto UNAIR theme to GitHub.

## Prerequisites

- GitHub account
- Git installed on your computer
- The `quarto-unair-theme` folder ready

## Step 1: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. **Repository name**: `quarto-unair-theme`
3. **Description**: "Professional Quarto Revealjs presentation theme for Universitas Airlangga following official 2025 branding guidelines"
4. **Public** repository (so others can install it)
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

## Step 2: Add Your Logos

Before pushing to GitHub, add your official UNAIR logos:

```bash
cd quarto-unair-theme/img/
# Copy your logo files here
cp /path/to/your/logo.png .
cp /path/to/your/logo_white.png .
```

Or create placeholders for testing.

## Step 3: Initialize Git

```bash
cd quarto-unair-theme
git init
git add .
git commit -m "Initial commit: UNAIR Quarto theme v1.0.0"
```

## Step 4: Push to GitHub

Replace `yourusername` with your GitHub username:

```bash
git branch -M main
git remote add origin https://github.com/rameliaz/quarto-unair-theme.git
git push -u origin main
```

## Step 5: Configure Repository

### Add Topics

Go to your repository page and click "About" (gear icon), then add:

```
quarto
quarto-extension
revealjs
presentation-theme
universitas-airlangga
unair
indonesia
academic
```

### Enable Issues

Settings → Features → Check "Issues"

### Add Description

Use the description from Step 1 above.

## Step 6: Create a Release

1. Go to "Releases" → "Create a new release"
2. **Tag**: `v1.0.0`
3. **Title**: `v1.0.0 - Initial Release`
4. **Description**:
   ```markdown
   ## Initial Release
   
   First public release of the Universitas Airlangga Quarto presentation theme.
   
   ### Features
   - Official UNAIR 2025 branding
   - Automatic logo placement
   - Section dividers with blue background
   - Pre-styled components
   - Comprehensive documentation
   
   ### Installation
   ```bash
   quarto add yourusername/quarto-unair-theme
   ```
   
   See [README.md](README.md) for full documentation.
   ```
5. Click "Publish release"

## Step 7: Test Installation

Test that others can install it:

```bash
cd /tmp
mkdir test-install
cd test-install
quarto add yourusername/quarto-unair-theme
```

## Step 8: Update README

In your local repo, update all instances of `yourusername` in README.md:

```bash
# Replace yourusername with your actual GitHub username
sed -i 's/yourusername/YOUR_ACTUAL_USERNAME/g' README.md
sed -i 's/yourusername/YOUR_ACTUAL_USERNAME/g' QUICKSTART.md
sed -i 's/yourusername/YOUR_ACTUAL_USERNAME/g' example.qmd

git add .
git commit -m "Update username in documentation"
git push
```

## Step 9: Optional - GitHub Pages

To host example presentation:

1. Render example: `quarto render example.qmd`
2. Create `docs/` folder: `mkdir docs`
3. Move output: `mv example.html docs/index.html`
4. Move support files: `mv example_files docs/`
5. Commit and push
6. Settings → Pages → Source: "main branch /docs folder"

Your example will be live at: `https://yourusername.github.io/quarto-unair-theme/`

## Step 10: Promote Your Theme

### Quarto Community

Post on [Quarto Discussions](https://github.com/quarto-dev/quarto-cli/discussions):

```markdown
Title: [Theme] Universitas Airlangga Presentation Theme

I've created a professional Quarto Revealjs theme following Universitas 
Airlangga's official branding guidelines.

Features:
- Official brand colors and typography
- Smart logo placement
- Section dividers
- Pre-styled components

Installation:
```bash
quarto add yourusername/quarto-unair-theme
```

Repository: https://github.com/yourusername/quarto-unair-theme

Feedback welcome!
```

### Social Media

Tweet with #QuartoPub:

```
🎓 New #QuartoPub extension: Universitas Airlangga presentation theme!

✨ Official UNAIR branding
✨ Professional design

Install: quarto add rameliaz/quarto-unair-theme

#RStats #Python #DataScience
```

### UNAIR Community

Share within:
- UNAIR faculty mailing lists
- Internal communication channels
- Academic departments

## Maintenance

### Accepting Contributions

1. Review pull requests
2. Test changes thoroughly
3. Update CHANGELOG.md
4. Create new release for significant updates

### Version Updates

When releasing updates:

```bash
# Update version in _extension.yml
# Update CHANGELOG.md
git add .
git commit -m "Release v1.1.0"
git tag v1.1.0
git push origin main --tags
```

Then create GitHub release for the new tag.

## Troubleshooting

**Push rejected**: Make sure you have write access to the repository

**Installation fails**: Verify `_extensions/unair/_extension.yml` is correct

**Theme not found**: Wait a few minutes for GitHub to index, then try again

## Questions?

- Check [GitHub's documentation](https://docs.github.com)
- Ask in Quarto discussions
- Open an issue in your repository

---

**Congratulations!** Your theme is now public and others can use it! 🎉
