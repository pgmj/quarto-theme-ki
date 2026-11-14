# quarto-theme-ki

A portable Karolinska Institutet theme for Quarto slides, as reveal.js (HTML)
and PowerPoint, plus a matching ggplot2 theme. **Copy this whole folder into a
project root** and point a `.qmd` at it.

For an example presentation, see my presentation at the <a href="https://pgmj.github.io/SAMC2026/" target="_blank">Scandinavian Applied Measurement Conference 2026</a>.

## Contents

```
quarto-theme-ki/
├── ki_embed.scss        # reveal.js slide theme, logo embedded: use this one
├── ki.scss              # same theme with the logo linked (source copy, not for decks)
├── ki.R                 # ggplot2 theme + KI colour palette
├── template.qmd         # starter deck — copy to project root and edit
├── ki-reference.pptx    # pandoc reference doc for PowerPoint output
├── make-reference-pptx.py  # rebuilds ki-reference.pptx from the .potx
├── assets/              # KI logos (neg = white, pos = black, rgb = colour)
│                        # + ki-template.potx (official KI PowerPoint template)
└── fonts/DM_Sans/       # optional: drop DM Sans .ttf files here for offline use
```

## Quick start

1. Copy the whole `quarto-theme-ki/` folder into your project root.
2. Copy `quarto-theme-ki/template.qmd` to the project root, rename it, and edit.
3. Render with `quarto render deck.qmd`. This builds both `deck.html` and
   `deck.pptx`; add `--to revealjs` or `--to pptx` for one of them. (The theme
   paths in the front matter are relative to the project root.)

## Use in slides

In your root `.qmd` front matter:

```yaml
format:
  revealjs:
    theme: [default, quarto-theme-ki/ki_embed.scss]
    embed-resources: true
    slide-number: true
    footer: "Karolinska Institutet – ett medicinskt universitet"
    title-slide-attributes:
      data-background-color: "#4F0433"
```

Always render reveal.js decks as standalone HTML: use `ki_embed.scss` together
with `embed-resources: true` (as in `template.qmd`). The result is one `.html` file
with fonts, images and the logo inside it, so it can be emailed, uploaded or opened
without the project folder. Quarto sets `embed-resources` per document, so the
theme cannot switch it on by itself; keep it in the front matter.

`ki.scss` is the same theme with the title-slide logo linked from `assets/`
instead of embedded. It is kept as the readable source of the theme, not for
rendering decks. If you change `ki.scss`, make the same change in `ki_embed.scss`.

## Slide types

| Style | Markdown | Look |
|-------|----------|------|
| Title | from YAML `title`/`subtitle`/`author` | dark plum, white text, KI logo |
| Content | `## Heading` | white, plum heading, plum bullets |
| Pale section | `## Heading {.ljusbla}` | pale-blue background |
| Pale section | `## Heading {.ljusorange}` | pale-orange background |
| Divider | `## Heading {.plum}` | dark plum, white text |
| Divider | `## Heading {.blue}` | deep blue, white text |
| Centred | `## Heading {.centered}` | title and body centred (lists stay left-aligned) |

These classes apply to reveal.js only (see PowerPoint output below).

## PowerPoint output

Add a `pptx` format next to `revealjs` (already in `template.qmd`):

```yaml
format:
  revealjs:
    ...
  pptx:
    reference-doc: quarto-theme-ki/ki-reference.pptx
    slide-level: 2
```

`quarto render` then builds both the .html and the .pptx; `quarto render deck.qmd --to pptx`
builds only the .pptx. Slides use the KI PowerPoint layouts:

| Markdown | KI layout |
|----------|-----------|
| title slide | Startbild |
| `# Heading` | Avsnittsbild (section header) |
| `## Heading` | Rubrik och innehåll |
| `## Heading` + `.columns` | Rubrik + 2 innehållsdelar |

Things that do not carry over from reveal.js:

- The slide classes (`.plum`, `.ljusbla`, …), `.smaller`, inline `style=` and raw HTML
  such as `<br>`. Set a pptx-only subtitle under `format: pptx:` if the main one uses `<br>`.
- Text directly under a `# Heading` becomes its own untitled slide, and text after
  `.columns` likewise. Text above a table or image switches to pandoc's plain
  "Content with Caption" layout. Wrap such text so it shows on the slide in reveal.js and in
  speaker notes in pptx:

  ```markdown
  :::: {.content-visible when-format="revealjs"}
  Text
  ::::

  :::: {.content-visible when-format="pptx"}
  ::: notes
  Text
  :::
  ::::
  ```

- The render warns that "Comparison", "Content with Caption" and "Blank" layouts are
  missing. That is harmless unless a slide uses one, in which case it gets pandoc's
  unbranded layout.

`ki-reference.pptx` only needs rebuilding if the KI template changes. Replace
`assets/ki-template.potx` and run `python3 quarto-theme-ki/make-reference-pptx.py`. The
script renames the Swedish layouts to the English names pandoc looks for and removes the
handout master and SharePoint metadata, whose dangling links otherwise make PowerPoint
offer to repair the file.

## Use in plots (R)

```r
source("quarto-theme-ki/ki.R")
ggplot(...) +
  theme_ki() +
  scale_color_manual(aesthetics = c("fill", "color"), values = ki_color_palette)
```

`ki.R` uses local DM Sans TTFs from `fonts/DM_Sans/` if present, otherwise
falls back to the Google Fonts web copy.

## KI palette

`#4F0433` plum · `#870052` logo plum · `#FF876F` orange · `#B84145` dark
orange · `#FEEEEB` light orange · `#4DB5BC` blue · `#002C34` dark blue ·
`#EDF4F4` light blue.
