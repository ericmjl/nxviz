# EARS Syntax Reference

EARS (Easy Approach to Requirements Syntax) provides structured patterns for writing unambiguous, testable requirements.

**Source**: https://alistairmavin.com/ears/

## File Location

`DOCS_DIR/designs/<feature>/<subfeature>-EARS.md`

## Spec File Format

Each EARS file contains requirements with status markers:

```markdown
## [Sub-Feature Name]

- [x] **{ID}**: {Requirement statement}
- [ ] **{ID}**: {Requirement statement}
- [D] **{ID}**: {Requirement statement}
```

### Status Markers

- `[x]` — **Implemented**: Code and tests exist that realize this spec
- `[ ]` — **Active gap**: Should be implemented, work to do
- `[D]` — **Deferred**: Correct intent, not needed yet

### Removing Specs

**Delete specs that are no longer wanted.** Do not mark them — just remove the line. Git preserves history.

## Example File Structure

```markdown
# Login - EARS

**Parent LLD**: ./LLD.md

## Login Form

- [x] **AUTH-LOGIN-001**: The system shall display email and password fields.
- [x] **AUTH-LOGIN-002**: The system shall validate email format before submission.
- [ ] **AUTH-LOGIN-003**: The system shall offer "remember me" option.

## Error Handling

- [x] **AUTH-LOGIN-010**: If credentials are invalid, the system shall display an error message.
- [ ] **AUTH-LOGIN-011**: If account is locked, the system shall display lockout duration.

## Related Documents

- [Authentication LLD](./LLD.md)
```

## Semantic ID Format

`{FEATURE}-{SUBFEATURE}-{NNN}`

- **FEATURE**: 2-4 letter prefix (e.g., `AUTH`, `CART`, `PAY`)
- **SUBFEATURE**: Short feature code (e.g., `LOGIN`, `CHECKOUT`, `REFUND`)
- **NNN**: Sequential number, zero-padded (001, 002, ...)

**Example IDs:**
- `AUTH-LOGIN-001` - Auth feature, login sub-feature, requirement 1
- `PAY-CHECKOUT-010` - Payments feature, checkout sub-feature, requirement 10
- `CART-EDIT-005` - Cart feature, edit sub-feature, requirement 5

## EARS Requirement Patterns

### 1. Ubiquitous (always true)

**Pattern**: "The system shall..."

```
- **AUTH-LOGIN-001**: The system shall display a login form with email and password fields.
```

### 2. Event-Driven (triggered by action)

**Pattern**: "When [trigger], the system shall..."

```
- **AUTH-LOGIN-002**: When the user taps the login button, the system shall validate credentials.
```

### 3. State-Driven (while condition is true)

**Pattern**: "While [state], the system shall..."

```
- **CART-UI-003**: While the cart is empty, the system shall display an empty state message.
```

### 4. Optional (feature-dependent)

**Pattern**: "Where [feature enabled], the system shall..."

```
- **AUTH-LOGIN-005**: Where biometric auth is enabled, the system shall prompt for Face ID.
```

### 5. Unwanted (error handling)

**Pattern**: "If [unwanted condition], then the system shall..."

```
- **AUTH-LOGIN-010**: If credentials are invalid, then the system shall display an error message.
```

## Scope Disambiguation

A spec should be interpretable correctly even if found via grep without surrounding context.

### Checklist

1. **Name the scope in the WHEN clause** - If scoped to a specific mode, state it explicitly
2. **Litmus test**: "If a second variant existed, would this be unambiguous?"
3. **Cross-file concepts**: Include brief parenthetical when referencing concepts from other files

### Examples

**Bad** — sounds universal, actually scoped to one notification channel:
```
- **NOTIF-BE-003**: Notifications shall use a 30-second delivery timeout.
```

**Good** — scope is explicit:
```
- **NOTIF-BE-003**: Both email and push notifications shall use a 30-second delivery timeout.
```

### Watch Ubiquitous Specs

"The system shall..." specs are most vulnerable — they have no WHEN clause to carry scope.

## Code Annotations

Reference specs in implementation:

```typescript
// @spec AUTH-LOGIN-001, AUTH-LOGIN-002, AUTH-LOGIN-003
export function LoginForm({ ... }) {
  // Implementation
}
```

In tests:

```typescript
// @spec AUTH-LOGIN-002
it('validates email format before submission', () => {
  expect(validateEmail('invalid')).toBe(false);
});
```

## Traceability

### From LLD to EARS

In your LLD, link to all EARS files:

```markdown
## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Login EARS](./login-EARS.md)
- [Logout EARS](./logout-EARS.md)
```

### From EARS to LLD

In each EARS file, link back to parent LLD:

```markdown
**Parent LLD**: ./LLD.md
```

### From Plan to EARS

In implementation plans, map specs to phases:

```markdown
## Phase 1: Login Feature

**Specs**: AUTH-LOGIN-001 through AUTH-LOGIN-015

- Login form (AUTH-LOGIN-001 to AUTH-LOGIN-005)
- Validation (AUTH-LOGIN-010 to AUTH-LOGIN-012)
- Error handling (AUTH-LOGIN-020 to AUTH-LOGIN-022)
```

## Complete Example

```markdown
# Login - EARS

**Parent LLD**: ./LLD.md

## Form UI

- [x] **AUTH-LOGIN-001**: The system shall display email input field.
- [x] **AUTH-LOGIN-002**: The system shall display password input field.
- [x] **AUTH-LOGIN-003**: The system shall display a login button.
- [ ] **AUTH-LOGIN-004**: Where biometric auth is enabled, the system shall display biometric button.

## Form Validation

- [x] **AUTH-LOGIN-010**: The system shall validate email format before submission.
- [x] **AUTH-LOGIN-011**: The system shall validate password is not empty.
- [ ] **AUTH-LOGIN-012**: The system shall show inline validation errors.

## Authentication

- [x] **AUTH-LOGIN-020**: When credentials are valid, the system shall issue a session token.
- [x] **AUTH-LOGIN-021**: When credentials are invalid, the system shall display error message.
- [ ] **AUTH-LOGIN-022**: When account is locked, the system shall display lockout message with duration.

## Session Management

- [x] **AUTH-LOGIN-030**: The system shall store session token securely.
- [ ] **AUTH-LOGIN-031**: Where "remember me" is checked, the system shall issue extended-lived token.
- [D] **AUTH-LOGIN-032**: The system shall support concurrent sessions (limited to 3).

## Related Documents

- [Authentication LLD](./LLD.md)
```

## Key Principles

1. **One EARS file per sub-feature** - Don't combine unrelated requirements
2. **Always link to parent LLD** - Bidirectional traceability
3. **Semantic IDs** - Use consistent `{FEATURE}-{SUBFEATURE}-{NNN}` format
4. **Testable requirements** - Can you write a test that verifies this?
5. **Delete, don't deprecate** - Remove obsolete specs entirely
6. **Scope explicitly** - Avoid implicit assumptions
