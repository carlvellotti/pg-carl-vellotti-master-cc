---
name: spin-up
description: Set up a project's CLAUDE.md with context management best practices — the subagent delegation pattern that keeps the main conversation clean.
user-invocable: true
---

# /spin-up — Context Management Setup

Set up a new project's CLAUDE.md with context management best practices — specifically, the subagent delegation pattern that keeps the main conversation clean.

## What This Does

When the user runs `/spin-up`, you help them configure a project's CLAUDE.md so that Claude Code automatically delegates exploration, research, and verbose operations to subagents instead of bloating the main context window.

## Workflow

### Step 1: Locate the target project

Ask the user: **"What project do you want to spin up? Give me the path or name."**

If they provide a path, use it. If they say "this one" or similar, use the current working directory.

### Step 2: Check for existing CLAUDE.md

Look for a `CLAUDE.md` file in the project root.

- **If it exists**: Read it and check whether it already has a `## Context Management` section.
  - If yes: Tell the user it's already set up. Offer to review/update it.
  - If no: Proceed to Step 3.
- **If it doesn't exist**: Create one. Proceed to Step 3.

### Step 3: Add the Context Management section

Add the following section to the CLAUDE.md. If the file already has content, append it in a logical location (after any existing overview/description sections, before any detailed reference sections).

```markdown
## Context Management

Context is your most important resource. Proactively use subagents (Task tool) to keep exploration, research, and verbose operations out of the main conversation.

**Default to spawning agents for:**
- Codebase exploration (reading 3+ files to answer a question)
- Research tasks (web searches, doc lookups, investigating how something works)
- Code review or analysis (produces verbose output)
- Any investigation where only the summary matters

**Stay in main context for:**
- Direct file edits the user requested
- Short, targeted reads (1-2 specific files)
- Conversations requiring iterative back-and-forth
- Tasks where the user needs to see intermediate steps

**Rule of thumb:** If a task will read more than ~3 files or produce output the user doesn't need to see verbatim, delegate it to a subagent and return a summary.
```

### Step 4: Confirm and educate

After adding the section, tell the user:

> Done — your CLAUDE.md now has the Context Management section.
>
> **How to verify it works:**
> Start a new session and ask Claude to investigate something in your codebase. You should see `Task` tool calls (spawning subagents) instead of a wall of individual `Read` calls. That means it's delegating.
>
> **What this saves you:**
> Without this, Claude reads every file directly into your conversation — burning 15,000+ tokens on content you'll never reference again. With this, exploration happens in isolated subagents and only the summary comes back. Your context stays clean.

## Important Notes

- **Never overwrite existing CLAUDE.md content.** Only add the Context Management section.
- If the user has a different structure preference, adapt the section to fit.
- This is a one-time setup per project. Once added, it persists across all sessions.
