# UNAIR PowerPoint template

- `unair-template.potx` — the template. Double-click it to start a new deck, or
  use Design → Browse for Themes to apply it to an existing one. Layouts appear
  under Home → Layout.
- `unair-sample.pptx` — one example slide per layout.
- `src/` — scripts that rebuild both files from `../_extensions/unair`:
  `npm ci && pip install -r requirements.txt && npm run build`. Needs Node and
  Python; the build script calls `python`, so on systems where only `python3`
  exists run `node assets.js && python3 build.py` instead.

## Sidebar text and slide numbers

Content slides carry the blue sidebar. Its text is a **footer**, so one edit
covers the whole deck:

Insert → Header & Footer → tick *Footer* → type the short title → **Apply to All**.

The slide number in the yellow block updates by itself; nothing to switch on.
The title, section divider, agenda, quote and closing layouts have no sidebar,
and PowerPoint skips them when applying the footer.

## Layouts

Title · Section Divider · Content · Two Content · Title Only ·
Content (no sidebar) · Agenda · Text + Image · Image + Text ·
Text + Shaded Box · Three Columns · Overview Grid · Quote ·
Quote (Dark / Photo) · Closing

Use **Content (no sidebar)** for a slide that should go without the blue bar —
the bar comes from the slide master and can't be deleted slide by slide.

## Notes

- **Dark quote:** add the photo with Format Background → Picture. The blue tint
  sits on top of it.
- **Agenda:** one numbered list — add or delete items like any other list and
  the numbers renumber themselves.
- **Three Columns:** the columns are a borderless table. Right-click → Insert →
  Columns to add one; the new column inherits the formatting.
- **Tables** you insert come out borderless, which suits layout work. For a data
  table, pick a style under Table Design — the sample deck's "Tables" slide uses
  the branded blue one.
- **Quote slides** carry a title placeholder parked off the slide, so they have a
  name in Outline view and pass the Accessibility Checker without showing a
  heading. Type into it via Outline view or the Selection pane.
- Long text in a placeholder shrinks to fit as you type rather than spilling off
  the slide.
