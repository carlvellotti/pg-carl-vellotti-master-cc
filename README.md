# Product Growth Podcast — Episode 3 Demo

**"From Watching to Collaborating"** — Carl Vellotti's third appearance on the Product Growth podcast.

This repo is the live demo environment from the episode. It's a working **PM Operating System** built for a fictional PM (Alex Chen, Senior PM at GradeFlow) that shows how Claude Code becomes a daily thinking partner — not just a code generator.

## What's Inside

This repo is a fully functional Claude Code workspace. Open it in Claude Code and everything works — skills, commands, context, all of it.

| Folder | What It Is |
|--------|-----------|
| `CLAUDE.md` | The entry point. Claude reads this automatically every conversation. |
| `GOALS.md` | Alex's identity, ownership areas, and quarterly goals. |
| `.claude/skills/` | 5 slash commands: `/standup`, `/meeting-prep`, `/synthesize-research`, `/draft-prd-section`, `/weekly-update` |
| `Tasks/` | Simple backlog → active → archive task pipeline |
| `Projects/` | 3 real projects with briefs, research, and outputs |
| `Workflows/` | Multi-step repeatable processes (weekly stakeholder update, quarterly planning, research synthesis) |
| `Meetings/` | 1:1 notes, standups, one-off meeting notes |
| `Knowledge/` | People profiles, company reference, research library |
| `Templates/` | Document structures (PRD, brief, interview notes, weekly update) |
| `data/` | Survey dataset (212 responses) for the Jupyter notebook demo |

## Follow Along

**See [`DEMO-GUIDE.md`](DEMO-GUIDE.md) for the exact prompts and commands from each section of the episode.**

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Max plan recommended (Pro works for most demos)
- Python 3 + pandas + matplotlib + seaborn (for Jupyter demo)
- Node.js / npx (for skills.sh installs)

### Quick Start

```bash
git clone https://github.com/carlvellotti/pg-ep-3-demo.git
cd pg-ep-3-demo
claude
```

That's it. Claude reads `CLAUDE.md` automatically and knows the full workspace.

## Episode Topics

1. **Context Management** — Status line, sub-agents, delegating work
2. **Skills** — Frontend design, web research, skills.sh marketplace, auto-triggering hooks
3. **Jupyter Notebooks** — Data analysis with visible audit trails
4. **The Operating System** — How it all compounds into a daily workflow

## Resources

- [Carl's Product OS](https://github.com/carlvellotti/carls-product-os) — Blank template you can fork and customize
- [skills.sh](https://skills.sh) — Vercel's skills marketplace
- [Claude Code for PMs](https://ccforpms.com) — Full course
- [@carlvellotti](https://twitter.com/carlvellotti) on X
