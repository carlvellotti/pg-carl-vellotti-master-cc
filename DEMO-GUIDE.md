# Episode 3 Demo Guide

Run-of-show for the entire episode. Bullet talking points + exact commands. Have this open on the side.

---

## Prerequisites (do before recording)

1. Claude Code installed and logged in
2. Status line configured (see Act 1 below)
3. Browser tabs open:
   - `https://www.claudecodeschool.com/` (without frontend design skill)
   - `https://www.claudecodeschool.com/advanced-cc` (with frontend design skill)
   - `https://skills.sh/vercel-labs/skills/find-skills`
4. Separate terminal window ready for skills.sh installs
5. Python 3 with pandas, matplotlib, seaborn installed
6. Puppeteer installed (`npm install puppeteer` in the demo repo)
7. Tavily and Firecrawl API keys in `.env` (for web research demo)

---

## Overall Frame (~3 min)

- Since the last episode, I've gone from watching Claude Code work to actually collaborating with it
- I've gotten way better — have a lot to show
- Today we're answering the two biggest PM questions:
  - **"How can I trust the work?"** → Jupyter notebooks (Act 3)
  - **"What does the actual operating system look like?"** → The OS (Act 4)
- But first — the two things that made the biggest difference in my day-to-day: context management and skills
- "I want to show you the four things that changed everything"

---

## Act 1: Context Management (~12 min)

- One of the first things I realized is just how important context is
- The worst thing about Claude Code is how the context window fills up
- Context rot — your later messages get worse outputs, not because Claude got dumber but because the context got crowded
- Context poisoning — bad info early in the conversation compounds
- The unlock: building your intuition around context. If you can SEE it filling up, everything changes
- That starts with the status line

### Status Line Setup

After running `/statusline`, paste this:

```
show model name, folder name (not full path), and context usage as a 10-character block progress bar with the scaled percentage number next to it. Use pipe separators between items. Scale the percentage so that 80% real usage shows as 100% (since Claude compacts at 80%). Color the bar green under 50%, yellow 50-65%, orange 65-95%, and blinking red with a skull emoji at 95%+. Keep it compact — dim the model and folder name, bright colors only on the bar.
```

- Result: `Claude 4 Opus | pg-ep-3-demo | ██░░░░░░░░ 19%`
- This bar is why I started taking context management seriously
- When you can SEE it filling up, you stop treating every conversation like it's infinite
- Smart zone model: 0-40% = sharp, 40-60% = degrading, 80%+ = hallucinations

### Sub-Agent Comparison

- We've covered subagents before, but now it's helpful to look at them in the context of context.
- When you ask Claude Code to do a task, it will just sometimes it will be smart about using its sub-agents, but oftentimes if it's just a straight task, it will do it on its own.
- The biggest technique for managing context: sub-agents
- The framework: "Does the main session need all the details, or just the output?"

**Round 1 — the bad way (don't delegate):**

```
Research the top 5 Claude Code tips from Reddit this week
```

- Watch the status bar jump — point it out
- Claude does web searches in the main session, raw results dump into context

**Round 2 — the good way (delegate):**

```
Spin up an agent to research the top 5 Claude Code tips from Reddit this week and just give me the summary
```

- Status bar barely moves — point at the difference
- Agent does the work in its own context, returns a paragraph

### AskUserQuestion — Two-Way Collaboration

- "Here's one that surprised me — Claude Code can ask YOU questions"
- You direct Claude's work with sub-agents. But Claude can also direct yours.
- It presents options, asks for your preference, checks assumptions — the same things a good junior PM would do
- Show a live example — give it something ambiguous:

```
Help me figure out the right pricing tier structure for this product
```

- Watch it ask clarifying questions: who's the target customer? what's the current model? what are the goals?
- It doesn't just guess — it asks before building
- "This is what makes it feel like a thinking partner instead of a text generator"

### Bridge to Skills: /spin-up

- "I actually built a custom skill that instructs Claude Code to use sub-agents intelligently"
- You can add the instructions to your CLAUDE.md, which kind of helps, but the better way is a skill
- Show the actual skill:

```
/spin-up
```

- Walk through what it does — sets up context management rules in any project's CLAUDE.md
- "This is a skill. It's just a markdown file with instructions. And that's a perfect segue..."

---

## Act 2: Skills (~15 min)

- Skills are the absolute key to making Claude Code closer to AGI
- So many of the things people think Claude Code is bad at — if you just give it the right tools, it can actually overcome those weaknesses
- The pattern: find a gap in Claude's default behavior, write instructions that close it
- Three levels of power — I'll show all three

### 1. Prompt Only — Frontend Design Skill

- "People say AI makes generic designs. Here's what Claude Code builds by default..."

Show two tabs side by side:
- **Without skill:** `https://www.claudecodeschool.com/`
- **With skill:** `https://www.claudecodeschool.com/advanced-cc`

- Without: light blue, plain card, basic form, default fonts — looks like a template
- With: dark theme, orange accents, terminal-style input, stats row, topic chips — completely different
- Same tool, same prompt style, dramatically different output

Open the actual SKILL.md on screen:

```bash
open ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/frontend-design/skills/frontend-design/SKILL.md
```

- It's 42 lines of markdown. No code. No dependencies. No build step.
- It explicitly bans "AI slop" — Inter font, purple gradients, cookie-cutter layouts
- It forces a design process before coding — pick a bold aesthetic direction first
- Last line: "Claude is capable of extraordinary creative work. Don't hold back."
- "A skill is just a markdown file that makes Claude better at one specific thing."

### Auto-Triggering Hook — Making Skills Fire Automatically

- "Last episode, skills were flaky — they didn't auto-trigger. That's fixed now."
- I built a hook — a 59ms Python script that runs every time you send a message
- No AI call, just keyword matching against your installed skills
- When it matches, it nudges Claude to evaluate whether to activate the skill

Demo it live — type a natural prompt (don't use the slash command):

```
make me a slide for the title of this talk
```

- Watch the make-slides skill fire automatically — audience sees the magic
- This also sets up the puppeteer demo coming next
- Then demystify it:

```
/hooks
```

- Show the config, show where it lives
- "And if it's ever in the way — `/hooks`, delete, done"
- The mechanism: scans all your skills in 59ms, matches trigger phrases, injects context. That's it.

### 2. Prompt + Tools — Web Research Skill

- "Skills get more powerful when you give them actual tools"
- This skill connects Claude Code to Tavily (search API) and Firecrawl (web scraper) — external tools it can't access natively
- Both have free tiers. You don't need to pay for this.

Run live:

```
Research what PMs are saying about using AI for data analysis — what's working, what's not, and what tools are they reaching for
```

- Watch it search multiple sources, scrape pages, synthesize findings
- Callback from Act 1: "Remember the sub-agent research demo? This is the skill that powers that kind of work — but with real web access instead of just Reddit"

### 3. Prompt + Tools + Self-Validation — Make Slides Skill

- "And even more powerful when they can see their own output"
- This skill uses Puppeteer — Claude can screenshot what it built, measure it, see problems, and fix them
- "This is the closest thing to Claude Code having eyes"

Run live (single slide, show the iteration loop):

```
Make a single title slide for a presentation called "From Watching to Collaborating" — my talk on how to get good at Claude Code. Make it bold and distinctive. Use the make-slides skill and show me each iteration.
```

- What to point out: the measure → screenshot → evaluate → edit cycle
- It measures overflow, takes a screenshot, evaluates its own design, makes changes
- Show 3 iterations — each one gets better
- "It's not just following instructions. It's checking its own work."

### Where to Get Skills — skills.sh

- "Now — where do you get these skills? There's a marketplace."
- Show the tab: `skills.sh/vercel-labs/skills/find-skills`
- skills.sh by Vercel — a marketplace for skills across agents

**Step 1: Install find-skills** (in separate terminal)

```bash
npx skills add https://github.com/vercel-labs/skills --skill find-skills -y
```

**Step 2: Restart Claude Code** (new session picks up the skill)

**Step 3: Use it**

```
/find-skills for data analysis
```

- It searches the ecosystem, returns results with install counts

**Step 4: Install data-analysis-jupyter from the results** (in separate terminal)

```bash
npx skills add mindrally/skills --skill data-analysis-jupyter -y
```

**Step 5: Restart Claude Code**

**Step 6: Open the skill**

- It's at `.claude/skills/data-analysis-jupyter/SKILL.md` — just pandas/matplotlib/seaborn best practices in markdown
- "I just gave Claude Code a data analysis specialty in under a minute."

**Bridge to Act 3:** "And now that Claude Code knows how to do data analysis with Jupyter notebooks... let me show you what that actually looks like."

---

## Act 3: Jupyter Notebooks (~8 min)

- The biggest question PMs have about AI outputs: **"How can I trust this?"**
- Especially with data — if you're making a recommendation based on numbers Claude gave you, you need to know those numbers are real
- This is the trust problem. Jupyter notebooks solve it.

**What Jupyter notebooks are (quick):**
- Code cells + text cells + output cells — all in one document
- Think of it as a spreadsheet where you can see all the formulas AND the reasoning
- The code that produced every number is right there, visible, runnable

The data is at `data/survey-responses.csv` — 212 TaskFlow user survey responses.

### Prompt 1: See the data

```
Open data/survey-responses.csv in a Jupyter notebook and show me what we're working with — columns, data types, and a few sample rows
```

- 212 responses, 14 columns — satisfaction, NPS, feature importance scores, enterprise interest
- Point out: Claude wrote the code, ran it, showed the output, all in one document

### Prompt 2: Distribution chart

```
Show me the distribution of enterprise interest scores as a chart
```

- Reveals: 68% scored 4-5 ("interested" or "very interested")
- Looks great for enterprise. Setup for the twist.

### Prompt 3: The insight

```
Show me a correlation heatmap of all the numeric columns — satisfaction, feature importance scores, enterprise interest, and NPS. What patterns jump out?
```

- Seaborn heatmap — visually dense, looks like real data science
- Key findings:
  - Satisfaction ↔ NPS: 0.80 (strong, obvious)
  - Enterprise Interest ↔ Satisfaction: **0.08** (nearly uncorrelated!)
  - Enterprise Interest ↔ NPS: **0.09** (the people who want enterprise are NOT your happiest users)
- "The people demanding enterprise features aren't your promoters. They're a completely different population. If you built enterprise to make your best customers happy, you'd be solving for the wrong people."

**The trust point:**
- "I didn't write any of this code. But I can see every step — the markdown explaining what we're doing, the code cell, the chart right below it."
- "That's the audit trail. You're not trusting Claude's answer. You're trusting the code that produced the answer."
- "Send this notebook to your data team. They can verify every number in 5 minutes."

---

## Act 4: The Operating System (~12 min)

- One of the biggest questions people have: they learn Claude Code features, but they don't understand how to actually work within it day-to-day
- Everything I just showed — context management, skills, notebooks — they're powerful on their own
- But they compound when you put them into a system
- A Personal OS = folder structure + instructions + skills. That's it.

### Show the structure

You're already in it. This repo IS the OS.

Open the file explorer / `ls` — walk through:

- `CLAUDE.md` — "This is the entry point. Claude reads it automatically every conversation."
- `GOALS.md` — "Identity, ownership areas, quarterly goals. Claude always knows what you're working toward."
- `.claude/skills/` — "Seven slash commands." (`/standup`, `/meeting-prep`, `/spin-up`, `/make-slides`, `/synthesize-research`, `/draft-prd-section`, `/weekly-update`)
- `Tasks/` — "Backlog, active, archive. Simplest possible task system."
- `Projects/` — "Three real projects. Each one has its own brief, research, outputs."
- `Workflows/` — "Repeatable processes. The weekly stakeholder update is 4 steps."
- `Knowledge/People/` — "Before my 1:1 with David Chen, Claude already knows who he is."

### Run skills live

```
/standup
```

- Pulls from Tasks/active.md, GOALS.md, recent activity
- Synthesizes a morning briefing in seconds
- "This takes 2 minutes. Without the OS, this is a fresh 15-minute prompt."

```
/meeting-prep david chen
```

- Reads David Chen's People/ profile (communication style, what he cares about, preferences)
- Pulls from recent 1:1 notes and active tasks
- Generates talking points tailored to this specific person
- "It already knows who David is, what you talked about last time, and what's on your plate"

### The compounding point

- Every file I add makes every future interaction smarter
- Every skill I build makes the next one easier
- The more you use it, the less you have to explain
- "Six months ago I was prompting Claude Code from scratch every time. Now I walk in, say two words, and the system knows what I need."

### Share with the audience

- This repo: `github.com/carlvellotti/pg-ep-3-demo`
- Blank template to fork: `github.com/carlvellotti/carls-product-os`
- "Fork the blank one, fill in your CLAUDE.md, and you're running."

---

## Wrap (~3 min)

Quick summary:
- "Context management — learn to direct the work, not just watch it"
- "Skills — teach Claude Code to do things your way, from just a prompt to tools that check their own work"
- "Jupyter notebooks — trust the output by seeing the work"
- "The OS — make it all compound"

Where to start:
- "CLAUDE.md. Spend 30 minutes writing down who you are, what you own, and how you work. Everything else builds on that."
