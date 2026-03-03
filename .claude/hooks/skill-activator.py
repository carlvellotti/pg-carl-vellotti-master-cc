#!/usr/bin/env python3
"""
Skill Activator Hook — UserPromptSubmit
Matches the user's prompt against available skills via trigger phrases.
If matches found, injects additionalContext forcing Claude to evaluate YES/NO.
If no matches, exits silently (zero overhead).
"""

import json
import os
import re
import sys


def extract_frontmatter(filepath):
    """Extract name and description from SKILL.md YAML frontmatter."""
    with open(filepath, "r") as f:
        lines = f.readlines()

    if not lines or lines[0].strip() != "---":
        return None, None

    name = None
    desc_parts = []
    in_frontmatter = False
    in_multiline_desc = False

    for line in lines:
        stripped = line.strip()

        if stripped == "---":
            if in_frontmatter:
                break  # end of frontmatter
            in_frontmatter = True
            continue

        if not in_frontmatter:
            continue

        if in_multiline_desc:
            # continuation lines are indented
            if line.startswith("  ") or line.startswith("\t"):
                desc_parts.append(line.strip())
            else:
                in_multiline_desc = False
                # fall through to check if this is another key

        if not in_multiline_desc:
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("description:"):
                value = line.split(":", 1)[1].strip()
                if value in (">", "|", ">-", "|-"):
                    in_multiline_desc = True
                else:
                    desc_parts.append(value.strip('"').strip("'"))

    description = " ".join(desc_parts).strip()
    return name, description


def extract_triggers(description):
    """Pull trigger phrases from single-quoted and double-quoted strings in the description."""
    single = re.findall(r"'([^']+)'", description)
    double = re.findall(r'"([^"]+)"', description)
    triggers = [t.lower() for t in single + double if len(t) >= 4]
    return triggers


def trigger_matches(trigger, prompt_lower):
    """Check if a trigger phrase matches the prompt.

    Uses word-presence matching: all significant words in the trigger
    must appear in the prompt, but not necessarily adjacent.
    'create graphic' matches 'create a graphic for my post'
    'SEO audit' matches 'can you audit my SEO'
    """
    words = [re.sub(r'[^a-z0-9]', '', w) for w in trigger.split()]
    words = [w for w in words if len(w) >= 3]
    if not words:
        return False
    return all(w in prompt_lower for w in words)


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = data.get("prompt", "")
    cwd = data.get("cwd", "")

    if not prompt:
        sys.exit(0)

    prompt_lower = prompt.lower()
    skills_dir = os.path.join(cwd, ".claude", "skills")

    if not os.path.isdir(skills_dir):
        sys.exit(0)

    matches = []

    for entry in sorted(os.listdir(skills_dir)):
        skill_path = os.path.join(skills_dir, entry, "SKILL.md")
        if not os.path.isfile(skill_path):
            continue

        name, description = extract_frontmatter(skill_path)
        if not name or not description:
            continue

        matched = False

        # Strategy 1: skill name in prompt (hyphenated or spaced)
        name_lower = name.lower()
        if name_lower in prompt_lower:
            matched = True
        elif "-" in name_lower and name_lower.replace("-", " ") in prompt_lower:
            matched = True

        # Strategy 2: trigger phrases from description
        if not matched:
            triggers = extract_triggers(description)
            for trigger in triggers:
                if trigger_matches(trigger, prompt_lower):
                    matched = True
                    break

        if matched:
            short_desc = description[:150]
            matches.append(f"  - /{name}: {short_desc}")

        if len(matches) >= 5:
            break

    if not matches:
        sys.exit(0)

    skill_list = "\n".join(matches)
    context = (
        f"SKILL CHECK: {len(matches)} skill(s) may apply to this prompt:\n\n"
        f"{skill_list}\n\n"
        "For each: YES or NO (one-line reason). If YES, activate with the Skill tool before proceeding."
    )

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }
    json.dump(output, sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
