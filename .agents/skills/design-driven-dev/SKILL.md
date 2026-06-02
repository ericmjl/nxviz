---
name: design-driven-dev
description: Guide for design-driven development with prescribed folder structure. New features use full workflow (HLD → LLD → EARS). Bug fixes skip doc creation but verify intent coherence.
---

# Design-Driven Development

This skill guides a structured design-driven development workflow. The goal is to get alignment on what you're building *before* writing code, which dramatically reduces rework and misunderstandings.

## Critical Rule: Stop and Iterate

**STOP after completing each phase.** Present the document to the user for review. Incorporate their numbered feedback. Only proceed to the next phase when explicitly approved.

This is the most important part of the workflow. Don't rush through design to get to code.

## DOCS_DIR Discovery

Before starting any design work, determine the documentation directory:

1. **Check for user configuration** - Has the user specified a `DOCS_DIR` environment variable or project config?
2. **Default to `./docs/`** - This is the canonical location
3. **Discovery scan** - If not set, scan for `./docs/` or `./doc/` directories:
   - If exactly one found, confirm with user: "Found docs directory at `X`. Use this?"
   - If multiple found, ask: "Which docs directory should I use? Options: A, B"
4. **Create if needed** - If neither exists, ask: "Create `./docs/` for design documents?"

Once determined, use `DOCS_DIR` as the root for all design documents.

## Folder Structure

```
DOCS_DIR/
├── high-level-design.md           # Single HLD for entire project
└── designs/
    └── <feature-name>/
        ├── LLD.md                 # Low-level design for feature
        ├── <sub-feature-1>-EARS.md
        ├── <sub-feature-2>-EARS.md
        └── ...
```

**Example:**
```
docs/
├── high-level-design.md
└── designs/
    ├── authentication/
    │   ├── LLD.md
    │   ├── login-EARS.md
    │   ├── logout-EARS.md
    │   └── password-reset-EARS.md
    └── payments/
        ├── LLD.md
        ├── checkout-EARS.md
        └── refunds-EARS.md
```

## Workflow Overview

1. **High-Level Design (HLD)** - Project vision and architecture → `DOCS_DIR/high-level-design.md`
2. **Low-Level Design (LLD)** - Feature-specific technical design → `DOCS_DIR/designs/<feature>/LLD.md`
3. **EARS Specifications** - Sub-feature requirements → `DOCS_DIR/designs/<feature>/<subfeature>-EARS.md`

See [hld-template.md](references/hld-template.md) for HLD structure guidance.

## When to Use This Workflow

**Consult this skill for ALL code changes.**

**Full workflow (create new docs) for:**
- New features
- Major refactors
- Significant behavior changes

**Coherence check only (skip doc creation) for:**
- Bug fixes
- Quick changes (<30 minutes)
- Debugging sessions

Even when skipping doc creation, verify intent coherence: do existing specs, tests, and code align? If not, fix the docs before changing the code.

**If unsure, use the full workflow.** Over-designing is safer than under-designing.

## Phase 1: High-Level Design

**File:** `DOCS_DIR/high-level-design.md`

Check if an HLD exists first. For new projects or major features, create an HLD covering:
- Problem statement and goals
- Target users and personas
- System architecture overview
- Key design decisions and trade-offs
- Non-goals (what's explicitly out of scope)

**Required: Link to LLDs**
```markdown
## Related Designs

- [Authentication LLD](./designs/authentication/LLD.md)
- [Payments LLD](./designs/payments/LLD.md)
```

See [hld-template.md](references/hld-template.md) for full structure with examples.

**Stop and get user approval before proceeding.**

## Phase 2: Low-Level Design

**File:** `DOCS_DIR/designs/<feature>/LLD.md`

Create one LLD per major feature. Each LLD should include:
- Component overview and context
- Data models and interfaces
- API contracts (if applicable)
- Error handling and edge cases
- Dependencies

**Required: Link to HLD and EARS**
```markdown
## Related Documents

- [High-Level Design](../high-level-design.md)
- [Login EARS](./login-EARS.md)
- [Logout EARS](./logout-EARS.md)
```

See [lld-template.md](references/lld-template.md) for structure guidance, including when to use narrative vs. structured format.

**Stop and get user approval before proceeding.**

## Phase 3: EARS Specifications

**File:** `DOCS_DIR/designs/<feature>/<subfeature>-EARS.md`

Generate requirements using EARS (Easy Approach to Requirements Syntax). Create one EARS file per sub-feature.

**Required: Link to parent LLD**
```markdown
## Related Documents

- [Authentication LLD](./LLD.md)
```

See [ears-syntax.md](references/ears-syntax.md) for full EARS syntax, semantic ID format, and scope disambiguation guidance.

**Stop and get user approval before proceeding.**

## Cross-Document Linking Rules

### HLD → LLD
HLD **must** link to all LLDs:
```markdown
## Related Designs

- [Authentication LLD](./designs/authentication/LLD.md)
- [Payments LLD](./designs/payments/LLD.md)
```

### LLD → HLD
LLD **must** link back to HLD:
```markdown
## Related Documents

- [High-Level Design](../high-level-design.md)
```

### LLD → EARS
LLD **must** link to all its EARS files:
```markdown
## Requirements

- [Login Form EARS](./login-EARS.md)
- [Password Reset EARS](./password-reset-EARS.md)
```

### EARS → LLD
EARS **must** link back to parent LLD:
```markdown
## Related Documents

- [Authentication LLD](./LLD.md)
```

## Maintaining Intent Coherence

### The Arrow of Intent

There's a chain of documents that translates intent from vision to working code:

```
HLD → LLDs → EARS → Tests → Code
```

Each level translates the previous into more specific terms:
- **HLD** says *what* and *why*
- **LLDs** say *how* at a feature level
- **EARS** says *exactly what must be true* in testable terms
- **Tests** verify those truths
- **Code** makes them real

### The Principle: Coherence Over History

The arrow of intent must stay coherent. When one level changes, downstream levels must be reviewed and updated to match.

**Mutation, not accumulation.** Update docs in place. Delete what's wrong. The documentation should always reflect *current* intent.

### The Practice: Cascade Changes Downward

When requirements or understanding change:

1. **Identify the entry point** - Where in the chain does this change originate?
2. **Update at that level** - Mutate the doc directly
3. **Cascade downward** - Review and update each subsequent level:
   - HLD change → review LLDs → review EARS → review tests → review code
   - LLD change → review EARS → review tests → review code
   - EARS change → review tests → review code
4. **Delete what's obsolete** - Delete specs that no longer apply

### Before Implementation

Before implementing (or resuming implementation), verify coherence:
- Do the EARS specs trace to the current LLD?
- Does the LLD link to the current HLD?
- Do the tests trace to current EARS?
- If drift is detected, fix the docs first—then implement.

## Code Annotation Pattern

Annotate code with `@spec` comments linking to EARS IDs:

```typescript
// @spec AUTH-LOGIN-001, AUTH-LOGIN-002, AUTH-LOGIN-003
export function LoginForm({ ... }) {
  // Implementation
}
```

Test files also reference specs:

```typescript
// @spec AUTH-LOGIN-010
it('validates email format before submission', () => {
  expect(validateEmail('invalid')).toBe(false);
});
```

This creates traceability from requirements → code → tests.

## Why This Works

| Benefit | Why It Matters |
|---------|----------------|
| **Forced checkpoints** | Catches misunderstandings before you've built the wrong thing |
| **Progressive reveal** | Sparsity of files makes complex features manageable |
| **Cross-linking** | Always know where to find related context |
| **Traceability** | @spec annotations link code to requirements |
| **Survives session breaks** | Docs persist, context doesn't get lost |
| **Testable requirements** | EARS format ensures requirements are verifiable |
