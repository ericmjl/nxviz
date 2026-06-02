# Low-Level Design Template

Low-Level Designs (LLDs) document feature-specific technical decisions. There is one LLD per major feature.

## File Location

`DOCS_DIR/designs/<feature-name>/LLD.md`

## Standard Structure

```markdown
# [Feature Name] - Low-Level Design

**Created**: YYYY-MM-DD
**HLD Link**: ../../high-level-design.md

## Overview

Brief description of this feature and its role.

## Data Models

### [Model Name]

| Field | Type | Description |
|-------|------|-------------|
| field1 | String | Description |

## API Contracts

| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| /api/feature | GET | - | FeatureResponse |

## Error Handling

| Code | Condition | Message |
|------|-----------|---------|
| 400 | Invalid input | "Error" |

## Edge Cases

- **Edge case 1**: How handled

## Dependencies

- Service: Purpose

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Sub-feature EARS](./subfeature-EARS.md)
```

## When to Use Narrative vs. Structured Format

### Use Narrative Format For:

**Complex constraint interactions** - When multiple requirements interact:

```markdown
## Offline Buffering Strategy

The offline buffer must balance three competing constraints: reliable
persistence across app crashes, efficient upload resumption, and minimal
battery impact during background sync. IndexedDB provides the persistence
foundation, storing metadata including uploadId and progress markers. When
network drops mid-upload, the multipart session preserves server-side state
while the client maintains enough context to resume without re-uploading
completed parts. The 5MB part size represents a deliberate trade-off between
retry cost (smaller parts mean less re-upload on failure) and request overhead
(larger parts mean fewer HTTP round-trips).
```

**Multi-service orchestration** - When showing flow between components:

```markdown
## Processing Pipeline

Order processing flows through three phases, each with distinct error handling
requirements. Phase 1 (validation) tolerates retry since it's idempotent - the
same input always produces the same result. Phase 2 (payment) requires careful
state tracking because payment gateway calls are expensive and partially-
completed transactions should be preserved. Phase 3 (fulfillment) uses database
transactions to ensure atomic updates across Orders, Inventory, and Shipping.
```

### Use Structured Format For:

**API contracts and interfaces**:

```markdown
## API Endpoints

| Endpoint              | Method | Request          | Response        |
| --------------------- | ------ | ---------------- | --------------- |
| `/orders`             | POST   | OrderCreateReq   | OrderConfirm    |
| `/orders/{id}`        | GET    | -                | Order           |
| `/orders/{id}/status` | GET    | -                | OrderStatus     |
```

**Configuration and thresholds**:

```markdown
## Rate Limiting Thresholds

**Per-user limits**:
- Standard tier: 100 requests/minute
- Premium tier: 1000 requests/minute

**Global limits**:
- Burst: 10,000 requests/second
- Sustained: 5,000 requests/second
```

**State enumerations**:

```markdown
## Order States

- `pending` - Created, awaiting payment
- `paid` - Payment confirmed
- `processing` - Being prepared
- `shipped` - In transit
- `delivered` - Complete
- `cancelled` - Order cancelled
```

## Example: Complete LLD

```markdown
# Authentication - Low-Level Design

**Created**: 2025-01-16
**HLD Link**: ../../high-level-design.md

## Overview

Authentication feature handles user registration, login, logout, and session management. Part of the core shopping app experience.

## Context

Per the HLD, we need secure authentication with offline capability. This LLD covers the authentication flow and token management.

## Authentication Flow

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Login   │───→│  Verify  │───→│  Issue   │
│   Form   │    │  Creds   │    │  Token   │
└──────────┘    └──────────┘    └──────────┘
      │                               │
      ▼                               ▼
┌──────────┐                   ┌──────────┐
│  Error   │                   │  Store   │
│  State   │                   │  Token   │
└──────────┘                   └──────────┘
```

## Data Models

### User

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| email | String | Unique, validated |
| passwordHash | String | bcrypt hash |
| createdAt | Timestamp | Account creation time |
| lastLogin | Timestamp | Most recent login |

### Session

| Field | Type | Description |
|-------|------|-------------|
| token | String | JWT, 24hr expiry |
| userId | UUID | Foreign key to User |
| refreshToken | String | Long-lived, 30 days |
| createdAt | Timestamp | Session start |

## API Contracts

### POST /auth/login

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response (200):**
```json
{
  "token": "eyJhbG...",
  "refreshToken": "rt_abc...",
  "user": {
    "id": "uuid",
    "email": "user@example.com"
  }
}
```

**Error Responses:**
- 401: Invalid credentials
- 429: Too many attempts

### POST /auth/refresh

**Request:**
```json
{
  "refreshToken": "rt_abc..."
}
```

**Response:**
```json
{
  "token": "eyJhbG...",
  "refreshToken": "rt_new..."
}
```

### POST /auth/logout

**Request:** (authenticated)
```json
{}
```

**Response:** 200 OK

## Error Handling

| Code | Condition | Message | Recovery |
|------|-----------|---------|----------|
| 401 | Invalid credentials | "Invalid email or password" | Show form |
| 401 | Token expired | (auto-refresh) | Refresh token |
| 401 | Refresh expired | "Session expired" | Redirect login |
| 429 | Rate limit | "Too many attempts" | Wait 15 min |

## Edge Cases

1. **Concurrent logins**: Last login wins, previous tokens remain valid until expiry
2. **Password change**: Invalidate all refresh tokens
3. **Offline login**: Not supported - show "connect to login" message
4. **Expired token during action**: Queue request, refresh, then replay

## Security Considerations

- Passwords: bcrypt with cost 12
- Tokens: JWT with short expiry (15 min access, 7 day refresh)
- HTTPS only in production
- CSRF protection via token in header

## Dependencies

- **Stripe**: No auth dependency
- **User service**: Internal, reads/writes User table
- **Redis**: Session storage for token blacklist

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Login EARS](./login-EARS.md)
- [Logout EARS](./logout-EARS.md)
- [Password Reset EARS](./password-reset-EARS.md)
```

## Key Principles

1. **One LLD per feature** - Don't split across multiple files
2. **Link to HLD** - Always reference the parent HLD
3. **Link to ALL EARS** - Every sub-feature should have an EARS file
4. **Decisions over descriptions** - Explain *why* for each choice
5. **Narrative for complexity** - Use prose for constraint interactions
6. **Structured for contracts** - Use tables for APIs and data models
