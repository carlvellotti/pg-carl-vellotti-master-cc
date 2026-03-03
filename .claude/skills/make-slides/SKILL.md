---
name: make-slides
description: "Build presentation slides as HTML/CSS with Puppeteer screenshot loop. Use when the user mentions 'make slides,' 'create slides,' 'presentation,' 'slide deck,' or 'make-slides.'"
user-invocable: true
allowed-tools: "Read,Write,Edit,Bash,Glob,Grep"
---

# Make Slides

Build polished presentation slides as HTML/CSS, with a Puppeteer measure → screenshot → iterate loop to ensure pixel-perfect output.

## Dimensions

All slides are **1920×1080px** (16:9 standard presentation).

## Required Inputs

Before starting, confirm you have:
1. **Content** — what the slides should cover (outline, notes, transcript, bullet points)
2. **Slide count** (optional) — how many slides. Default: let the content dictate.
3. **Style direction** (optional) — dark/light, brand colors, mood. Default: dark background, clean type.

If content is missing or unclear, ask before proceeding.

## Design Rules

### Layout Principles
- **One idea per slide.** If you're cramming, split it.
- **Visual hierarchy matters more than decoration.** Title > key point > supporting detail.
- **Generous whitespace.** Slides are projected large — breathing room is a feature.
- **Left-align text by default.** Center-alignment only for single-line titles or hero statements.

### Typography
- Title: 72-96px, weight 700-800
- Subtitle/key point: 48-60px, weight 600
- Body text: 36-44px, weight 400-500
- Caption/source: 24-28px, weight 400
- **Never go below 24px** — if the audience can't read it from the back of the room, cut words instead
- Use a clean sans-serif: `'Inter', 'Outfit', system-ui, sans-serif`

### Color
- **Dark theme default:** `#0f172a` background, `#f8fafc` text, one accent color
- **Light theme:** `#ffffff` background, `#1e293b` text, one accent color
- **Accent color usage:** headlines, key numbers, underlines, highlight boxes — never more than 30% of the slide
- High contrast always. Test: squint at it. If you can't read it, fix it.

### Visual Elements
- **Charts/diagrams:** Simple, large labels, 3-4 data points max per slide
- **Icons:** Optional. If used, keep consistent style (outline OR filled, not mixed)
- **Images:** Full-bleed or contained with rounded corners. Never stretched.
- **Code blocks:** Dark background, large monospace font (28px+), syntax highlighting

### What NOT to Do
- No clip art or stock photo placeholders
- No bullet point walls (3 bullets max, or use a different layout)
- No gradients unless intentional and subtle
- No drop shadows on text
- No logo on every slide (title + closing only)
- No transition animations (this is static HTML)

## Build Process

### Step 1: Plan the Deck

From the content, outline:
```
Slide 1: [Title slide — topic + speaker]
Slide 2: [Key question or hook]
Slide 3: [First main point]
...
Slide N: [Closing / CTA]
```

Present the outline to the user for approval before building.

### Step 2: Build the HTML

Create one HTML file per slide in the project folder. Structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .slide {
      width: 1920px;
      height: 1080px;
      overflow: hidden;
      position: relative;
      font-family: 'Inter', system-ui, sans-serif;
      padding: 80px 100px;
      /* colors as CSS variables */
      --bg: #0f172a;
      --text: #f8fafc;
      --accent: #3b82f6;
      background: var(--bg);
      color: var(--text);
    }
  </style>
</head>
<body style="background:#1e1e1e; display:flex; justify-content:center; align-items:center; min-height:100vh;">
  <div class="slide">
    <!-- Slide content -->
  </div>
</body>
</html>
```

### Step 3: Serve and Measure (MANDATORY)

Start the local server and verify with Puppeteer:

```bash
cd PROJECT_DIR && python3 -m http.server 8765 &
```

**Measure overflow:**
```bash
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });
  await page.goto('http://localhost:8765/SLIDE_FILE.html', { waitUntil: 'networkidle0' });
  const m = await page.evaluate(() => {
    const el = document.querySelector('.slide');
    return {
      containerH: el.offsetHeight,
      contentH: el.scrollHeight,
      overflow: el.scrollHeight - el.offsetHeight,
      containerW: el.offsetWidth,
      contentW: el.scrollWidth,
      overflowW: el.scrollWidth - el.offsetWidth
    };
  });
  console.log(JSON.stringify(m, null, 2));
  await browser.close();
})();
"
```

**Target:** overflow = 0 in both dimensions.

### Step 4: Screenshot Each Slide

```bash
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });
  await page.goto('http://localhost:8765/SLIDE_FILE.html', { waitUntil: 'networkidle0' });
  const el = await page.\$('.slide');
  await el.screenshot({ path: 'slide-NN.png' });
  console.log('Screenshot saved');
  await browser.close();
})();
"
```

### Step 5: Iterate (3-5 rounds per slide)

Each round: measure → screenshot → evaluate → edit → measure again.

Check each slide for:
- [ ] No overflow or clipping
- [ ] Text readable at presentation size
- [ ] Visual hierarchy is clear
- [ ] Accent color used intentionally, not everywhere
- [ ] Whitespace is generous, not cramped

### Step 6: Present to User

Show all slide screenshots in order. Ask for feedback. Iterate as needed.

## Cleanup

When done:
```bash
pkill -f "python3 -m http.server" 2>/dev/null
```
