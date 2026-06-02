---
name: atomic-commits
description: "Break unstaged or mixed changes into small, atomic, logical git commits with Conventional Commit messages. Use when the user asks to commit, stage, or split changes — e.g. 'help me commit', 'commit my changes', 'break these into logical commits', 'what should I commit first', 'stage my changes', 'commit atomically', or 'make atomic commits'. Uses git diff, git add -p, and Conventional Commits (feat:/fix:/refactor:/chore:/docs:/test:/style:/perf:/build:/ci)."
license: MIT
---

# Atomic Commits

Guide the user from a dirty working tree to a clean commit history where each commit is one logical change with a clear Conventional Commit message.

## Workflow

### 1. Analyze changes

Run in parallel:

```
git status
git diff
git diff --cached
```

If there are too many files, also run `git diff --stat` for a summary.

### 2. Propose a commit plan

Group changes into atomic commits. Present the plan as an ordered table:

| # | Scope | Files | Commit message |
|---|-------|-------|----------------|
| 1 | ... | ... | `type(scope): description` |

**Grouping rules (priority order):**

1. **One concern per commit.** Separate refactorings from features from bug fixes. If a file has changes for two concerns, plan to use `git add -p` to split hunks within that file.
2. **Dependencies first.** If commit B depends on commit A, order A before B.
3. **Tests alongside or after.** Tests for a change go in the same commit or the immediately following one — never alone in a distant commit.
4. **Config/infra before features.** Build/config changes that features depend on come first.

**Commit message format** — Conventional Commits:

```
type(scope): imperative-mood summary

Optional body explaining why, not what.
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

Scope: optional but encouraged — the module, package, or area affected.

Rules:
- Imperative mood: "add feature" not "added feature"
- Lowercase summary, no period at end
- Under 72 characters for the summary line
- Body wraps at 72 characters

### 3. Execute — one commit at a time

For each proposed commit:

1. Stage exactly the right files/hunks: `git add <files>` or `git add -p <file>`
2. Show the user what will be committed: `git diff --cached --stat`
3. Create the commit: `git commit -m "type(scope): summary"`
4. If a pre-commit hook modifies files, handle the result (amend only if hook changes are expected and the user agrees)

**Within-file splitting:** When a single file contains changes for multiple commits, use `git add -p` interactively is not an option in this environment. Instead:
- Use `git add -p` equivalents by staging specific line ranges via patch mode, or
- Create a temporary stash, apply partial changes, commit, then repeat

Practical approach: use `git diff <file>` to identify hunk boundaries, then `git add -p` with scripted responses, or advise the user to run `git add -p <file>` manually for that specific file if the hunks are interleaved.

### 4. Verify

After all commits, run `git log --oneline -<N>` to show the resulting history and confirm with the user.

## Edge Cases

- **No changes to commit:** Say so. Do not create empty commits.
- **Only one logical change:** Skip the table; make a single commit directly.
- **Untracked files:** Include in the plan. Stage with `git add`.
- **Binary files:** Cannot split with `git add -p`. Assign to the most relevant commit.
- **Merge conflicts:** Do not attempt to resolve as part of this workflow. Alert the user.
