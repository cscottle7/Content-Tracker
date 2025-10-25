---
name: documentation-standards
description: Establishes consistent documentation structure, formatting, and templates for READMEs, API docs, user guides, and SOPs. Automatically applies to documentation creation, review, and update tasks across all technical writing including Markdown formatting conventions, code comments, and example patterns.
---

# Documentation Standards

## Purpose
Ensures consistency, completeness, and quality across all project documentation by providing standardized templates, formatting conventions, and best practices. Eliminates variation between documentation agents and reduces token overhead from repeated template definitions.

## Core Standards

### Markdown Formatting Conventions

**Headings**
- Use ATX-style headings (`#`) not underlined headings
- One H1 (`#`) per document (document title)
- Maintain heading hierarchy (no skipping levels)
- Add blank line before and after headings

**Code Blocks**
- Always specify language for syntax highlighting
- Use `bash` for shell commands, not `sh` or `shell`
- Use `console` for command output
- Keep code blocks under 50 lines (extract to files if longer)

**Lists**
- Use `-` for unordered lists (not `*` or `+`)
- Use `1.` for ordered lists (auto-numbering)
- Indent nested lists with 2 spaces
- Add blank line before/after lists

**Tables**
- Use header row with separator
- Align columns for readability in source
- Keep tables under 6 columns (split if needed)

**Links**
- Use reference-style links for repeated URLs
- Use relative paths for internal documentation
- Always include link text (no bare URLs)

**Emphasis**
- Use `**bold**` for important terms, UI elements
- Use `*italic*` for emphasis, variable names
- Use `` `backticks` `` for inline code, commands, file names

---

## README Structure

### Standard Template

```markdown
# [Project Name]

[One-sentence description of what this project does]

[![Build Status](badge-url)](link) [![License](badge-url)](link)

## Overview

[2-3 paragraph description covering:
- What the project does and why it exists
- Key features and capabilities
- Primary use cases]

## Features

- **[Feature 1]**: Brief description
- **[Feature 2]**: Brief description
- **[Feature 3]**: Brief description

## Installation

### Prerequisites

- [Requirement 1] (version X.X or higher)
- [Requirement 2]
- [Requirement 3]

### Quick Start

```bash
# Clone repository
git clone https://github.com/org/repo.git
cd repo

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Start development server
npm run dev
```

### Configuration

[Configuration instructions with examples]

```yaml
# Example configuration
setting1: value
setting2: value
```

## Usage

### Basic Example

```language
# Show simplest possible usage
code example
```

### Common Tasks

#### [Task 1]
```language
code example
```

#### [Task 2]
```language
code example
```

## API Reference

[Brief overview with link to detailed API documentation]

See [API Documentation](docs/API.md) for complete reference.

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code of conduct
- Development setup
- Pull request process
- Coding standards

## Testing

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test suite
npm test -- path/to/test
```

## License

This project is licensed under the [License Name] - see [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [docs link]
- **Issues**: [issue tracker link]
- **Discussions**: [discussion link]
- **Email**: [contact email]

## Acknowledgments

- [Credit 1]
- [Credit 2]
```

### README Best Practices

**DO:**
- Lead with clear value proposition
- Provide working code examples
- Include visual aids (screenshots, diagrams) for UI projects
- Link to detailed documentation
- Keep installation steps simple and tested
- Update badges and links regularly

**DON'T:**
- Assume prior knowledge of domain
- Use broken or outdated examples
- Include large code blocks (link to examples/)
- Forget prerequisites and version requirements
- Leave placeholder text like "TODO" or "Coming soon"

---

## API Documentation Format

### Endpoint Documentation Template

```markdown
## [HTTP Method] [Endpoint Path]

[One-sentence description of what this endpoint does]

### Endpoint
```
[METHOD] /api/v1/resource/{id}
```

### Description
[Detailed explanation of functionality, use cases, and behavior]

### Authentication
**Required**: Yes
**Type**: Bearer Token
**Scope**: `resource:read`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Unique identifier for the resource |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer | No | 20 | Number of results (1-100) |
| `offset` | integer | No | 0 | Pagination offset |
| `sort` | string | No | `created_at` | Sort field: `created_at`, `updated_at`, `name` |
| `order` | string | No | `desc` | Sort order: `asc` or `desc` |

### Request Headers

```
Content-Type: application/json
Authorization: Bearer {access_token}
```

### Request Body

```json
{
  "field1": "string",
  "field2": 123,
  "field3": {
    "nested": "object"
  }
}
```

**Schema:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `field1` | string | Yes | Max 255 chars | Description of field1 |
| `field2` | integer | No | Min 0, Max 1000 | Description of field2 |
| `field3` | object | No | - | Nested configuration object |

### Response

**Success Response (200 OK):**

```json
{
  "data": {
    "id": "abc123",
    "field1": "string",
    "field2": 123,
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  },
  "meta": {
    "request_id": "req_xyz789"
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `data.id` | string | Unique resource identifier |
| `data.field1` | string | Description |
| `data.created_at` | ISO 8601 datetime | Creation timestamp |
| `meta.request_id` | string | Request tracking ID |

### Error Responses

**400 Bad Request**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid field1 format",
    "details": {
      "field": "field1",
      "constraint": "Must be alphanumeric"
    }
  }
}
```

**401 Unauthorized**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired access token"
  }
}
```

**404 Not Found**
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Resource with id 'abc123' not found"
  }
}
```

**429 Too Many Requests**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Retry after 60 seconds.",
    "retry_after": 60
  }
}
```

### Rate Limiting
- **Rate**: 100 requests per minute per API key
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

### Example Request

```bash
curl -X POST https://api.example.com/api/v1/resource \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_access_token" \
  -d '{
    "field1": "example",
    "field2": 42
  }'
```

### Example Response

```json
{
  "data": {
    "id": "res_abc123",
    "field1": "example",
    "field2": 42,
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

### Notes
- [Additional implementation details]
- [Edge cases or special behavior]
- [Related endpoints or workflows]
```

### API Documentation Best Practices

**DO:**
- Document all parameters, including optional ones
- Show realistic request/response examples
- Include all possible error codes
- Specify data types and constraints
- Provide working curl examples
- Document rate limits and pagination
- Use consistent naming conventions

**DON'T:**
- Use placeholder data like "string" or "value"
- Omit error responses
- Forget authentication requirements
- Leave parameter descriptions vague
- Skip request/response schemas
- Use outdated API versions in examples

---

## Code Comment Standards

### When to Comment

**DO Comment:**
- Complex algorithms or business logic
- Non-obvious decisions or workarounds
- Public APIs and exported functions
- Regular expressions and magic numbers
- Performance-critical sections
- Security-sensitive code

**DON'T Comment:**
- Obvious code that explains itself
- What the code does (code shows that)
- Redundant information
- Commented-out code (use version control)

### Inline vs Block Comments

**Inline Comments** (sparingly)
```python
x = x + 1  # Compensate for border (off-by-one)
```

**Block Comments** (for context)
```python
# The data structure is optimized for lookup performance at the cost
# of insertion speed. We accept slower inserts because reads are 10x
# more common in production workloads.
```

### JavaScript/TypeScript (JSDoc)

```typescript
/**
 * Calculates the total price including tax and shipping
 *
 * @param subtotal - Pre-tax price in cents
 * @param taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @param shippingCost - Shipping cost in cents
 * @returns Total price in cents
 * @throws {ValidationError} If subtotal or shippingCost is negative
 *
 * @example
 * ```typescript
 * const total = calculateTotal(1000, 0.08, 500);
 * // Returns: 1580 (1000 + 80 tax + 500 shipping)
 * ```
 */
function calculateTotal(
  subtotal: number,
  taxRate: number,
  shippingCost: number
): number {
  if (subtotal < 0 || shippingCost < 0) {
    throw new ValidationError('Amounts cannot be negative');
  }

  const tax = Math.round(subtotal * taxRate);
  return subtotal + tax + shippingCost;
}
```

### Python (Docstrings)

```python
def process_payment(
    amount: int,
    payment_method: str,
    currency: str = "USD"
) -> PaymentResult:
    """
    Process a payment transaction through the payment gateway.

    Args:
        amount: Payment amount in smallest currency unit (e.g., cents)
        payment_method: Payment method identifier (e.g., 'card_123')
        currency: ISO 4217 currency code (default: 'USD')

    Returns:
        PaymentResult containing transaction_id and status

    Raises:
        PaymentError: If payment processing fails
        ValidationError: If amount <= 0 or invalid currency

    Example:
        >>> result = process_payment(1000, 'card_123', 'USD')
        >>> print(result.transaction_id)
        'txn_abc123'

    Note:
        This function is idempotent. Retrying with the same parameters
        will return the original transaction result.
    """
    pass
```

### Comment Style Guidelines

**Structure:**
- Start with what the code does (summary)
- Explain parameters and return values
- Document exceptions/errors
- Provide examples for complex functions
- Add notes for important behavior

**Language:**
- Use present tense ("Returns user data" not "Will return")
- Be concise but complete
- Use proper grammar and punctuation
- Avoid abbreviations unless standard (API, HTTP, etc.)

**Formatting:**
- Keep line length under 80 characters
- Use consistent capitalization
- Add blank lines between sections
- Align parameter descriptions

---

## User Guide Templates

### Getting Started Guide

```markdown
# Getting Started with [Product Name]

## Introduction

[Brief overview of what the product does and who it's for]

**Time to complete**: ~15 minutes

**What you'll learn:**
- [Learning objective 1]
- [Learning objective 2]
- [Learning objective 3]

## Prerequisites

Before you begin, ensure you have:
- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

## Step 1: [First Action]

[Clear instructions with screenshots if applicable]

```bash
# Command example
command here
```

**Expected result:**
[What users should see]

**Troubleshooting:**
- **Problem**: [Common issue]
  **Solution**: [How to fix]

## Step 2: [Next Action]

[Continue with clear, sequential steps]

## Step 3: [Final Action]

[Complete the tutorial]

## Verification

Verify your setup is working:

```bash
# Test command
test command here
```

You should see:
```
Expected output
```

## Next Steps

Now that you've completed setup, you can:
- [Next tutorial link]: Learn about [topic]
- [Feature guide link]: Explore [feature]
- [API reference link]: See all available options

## Common Issues

### [Issue 1]
**Symptoms**: [What user experiences]
**Cause**: [Why it happens]
**Solution**: [Step-by-step fix]

### [Issue 2]
**Symptoms**: [What user experiences]
**Cause**: [Why it happens]
**Solution**: [Step-by-step fix]

## Get Help

- [Documentation link]
- [Community forum link]
- [Support contact]
```

### Tutorial Template

```markdown
# [Tutorial Title]: [What User Will Accomplish]

## Overview

[2-3 sentences describing what users will build/learn]

**Difficulty**: [Beginner/Intermediate/Advanced]
**Time**: [Estimated time]
**Prerequisites**: [Link to prerequisite tutorials/knowledge]

## What You'll Build

[Description with screenshot/diagram of end result]

## What You'll Learn

- [Skill/concept 1]
- [Skill/concept 2]
- [Skill/concept 3]

## Architecture Overview

[Optional: Diagram or explanation of how pieces fit together]

## Step-by-Step Instructions

### Part 1: [Section Name]

#### 1. [Specific Action]

[Detailed instruction]

```language
code example
```

**Why this matters**: [Brief explanation of concept]

#### 2. [Next Action]

[Continue with numbered steps]

### Part 2: [Next Section]

[Continue with logical sections]

## Testing Your Work

[How to verify the tutorial worked]

```bash
# Test command
```

Expected output:
```
output example
```

## Complete Code

[Link to complete working example or repository]

## Extending This Tutorial

Try these modifications to reinforce learning:
- [Challenge 1]
- [Challenge 2]
- [Challenge 3]

## Review

You've learned how to:
- [Summarize key learning 1]
- [Summarize key learning 2]
- [Summarize key learning 3]

## Related Resources

- [Related tutorial 1]
- [Related tutorial 2]
- [Relevant documentation]
```

### Reference Guide Template

```markdown
# [Feature/Component] Reference

## Overview

[What this feature/component does and when to use it]

## Basic Usage

```language
# Minimal example showing most common use case
```

## Configuration Options

### Option: `option_name`

**Type**: `string | number`
**Required**: No
**Default**: `default_value`

[Description of what this option does]

**Example:**
```language
config_example
```

**Valid values:**
- `value1`: [Description]
- `value2`: [Description]

**Notes:**
- [Important note about this option]

[Repeat for all options]

## Methods/Functions

### `methodName(param1, param2)`

[Description of what method does]

**Parameters:**
- `param1` (type): [Description]
- `param2` (type): [Description]

**Returns:**
- type: [Description of return value]

**Throws:**
- `ErrorType`: [When this error occurs]

**Example:**
```language
example usage
```

[Repeat for all methods]

## Properties

### `propertyName`

**Type**: `type`
**Read-only**: Yes/No

[Description of property]

**Example:**
```language
example
```

## Events

### `eventName`

**Triggered**: [When this event fires]

**Event Data:**
```language
event data structure
```

**Example:**
```language
event handler example
```

## Advanced Usage

### [Advanced Topic 1]

[Explanation with example]

### [Advanced Topic 2]

[Explanation with example]

## Best Practices

- [Best practice 1]
- [Best practice 2]
- [Best practice 3]

## Performance Considerations

- [Performance tip 1]
- [Performance tip 2]

## Browser/Environment Support

[Compatibility information if relevant]

## See Also

- [Related feature]
- [Related guide]
```

### FAQ Template

```markdown
# Frequently Asked Questions

## General

### [Question in user's language]?

[Clear, complete answer with examples if helpful]

**See also**: [Link to related documentation]

### [Next question]?

[Answer]

## [Category 2]

### [Category-specific question]?

[Answer]

## Common Issues

### [Problem description as user would state it]?

**Cause**: [Why this happens]
**Solution**: [How to fix, with commands/screenshots]

```bash
# Solution command
```

### [Next common issue]?

[Solution]

## Still Need Help?

Can't find your answer? Try:
- [Search documentation]
- [Community forum]
- [Support contact]
```

---

## SOP (Standard Operating Procedure) Format

### SOP Template

```markdown
# SOP: [Action/Process Name]

**ID**: SOP-[Number]
**Version**: 1.0
**Last Updated**: YYYY-MM-DD
**Owner**: [Team/Person]
**Approver**: [Person/Role]

## Purpose

[1-2 sentences explaining why this procedure exists]

## Scope

**Applies to**: [Who should follow this]
**Frequency**: [When this is performed: daily, as-needed, etc.]
**Systems**: [What systems/tools are involved]

## Prerequisites

Before starting, ensure you have:
- [ ] [Access/permission requirement]
- [ ] [Tool or system requirement]
- [ ] [Knowledge requirement]
- [ ] [Approval requirement if applicable]

## Roles & Responsibilities

| Role | Responsibility |
|------|----------------|
| [Role 1] | [What they do] |
| [Role 2] | [What they do] |

## Procedure

### Preparation

1. [Preparation step 1]
2. [Preparation step 2]

### Execution

**Step 1: [Action Name]**

[Detailed instructions]

```bash
# Command or configuration example
```

**Verification**: [How to confirm step completed successfully]

**Step 2: [Next Action]**

[Continue with numbered steps]

**Decision Point**:
- **If [condition A]**: Proceed to Step X
- **If [condition B]**: Proceed to Step Y

[Continue through all steps]

### Post-Execution

1. [Cleanup or verification step]
2. [Documentation requirement]
3. [Notification requirement]

## Validation

Confirm the procedure was successful:

- [ ] [Check 1]: [Expected result]
- [ ] [Check 2]: [Expected result]
- [ ] [Check 3]: [Expected result]

## Rollback Procedure

If issues occur, follow these steps to revert:

1. [Rollback step 1]
2. [Rollback step 2]

## Troubleshooting

### Issue: [Problem Description]

**Symptoms**: [What you'll see]
**Diagnosis**: [How to confirm this is the issue]
**Resolution**:
1. [Fix step 1]
2. [Fix step 2]

**Escalation**: If unresolved after [timeframe], contact [person/team]

### Issue: [Next Problem]

[Resolution steps]

## Documentation Requirements

After completing this procedure, document:
- [What to record]
- [Where to record it]
- [Who to notify]

**Template**: [Link to documentation template if applicable]

## References

- [Related SOP]
- [System documentation]
- [Policy document]

## Compliance & Security

[Any compliance requirements, security considerations, or audit requirements]

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | [Name] | Initial version |
```

### SOP Best Practices

**DO:**
- Write for someone unfamiliar with the process
- Include exact commands, URLs, and file paths
- Add decision points with clear criteria
- Provide rollback procedures for risky operations
- Include verification steps
- Keep language imperative and precise
- Number steps sequentially
- Update regularly based on feedback

**DON'T:**
- Assume prior knowledge
- Use vague terms like "usually" or "might"
- Skip error handling procedures
- Forget to include prerequisite checks
- Leave out security or compliance notes
- Use screenshots that quickly become outdated (prefer text)

---

## Documentation Quality Checklist

Before finalizing any documentation:

### Accuracy
- [ ] All code examples tested and working
- [ ] Commands produce expected output
- [ ] Links resolve correctly
- [ ] Version numbers current
- [ ] Screenshots show current UI (if used)

### Completeness
- [ ] All required sections present
- [ ] Prerequisites clearly stated
- [ ] Error conditions documented
- [ ] Examples cover common use cases
- [ ] Edge cases addressed

### Clarity
- [ ] Written for target audience level
- [ ] Technical terms defined
- [ ] Steps in logical order
- [ ] No ambiguous instructions
- [ ] Consistent terminology throughout

### Formatting
- [ ] Headings follow hierarchy
- [ ] Code blocks have language specified
- [ ] Tables properly formatted
- [ ] Lists use consistent markers
- [ ] Proper emphasis (bold/italic/code)

### Usability
- [ ] TOC for documents >500 lines
- [ ] Cross-references linked
- [ ] Searchable section names
- [ ] Examples copy-paste ready
- [ ] Mobile-readable (if web-based)

---

## Before/After Examples

### Example 1: Poor vs. Good README

**POOR:**
```markdown
# MyApp

This is my app. It does stuff.

## Install
npm install

## Run
npm start
```

**GOOD:**
```markdown
# MyApp - Real-time Collaborative Task Manager

A lightweight task management system with real-time collaboration, built with React and WebSockets.

## Features

- **Real-time sync**: Changes appear instantly for all team members
- **Offline support**: Work without internet, sync when reconnected
- **Keyboard shortcuts**: Navigate and edit tasks without touching mouse

## Installation

### Prerequisites
- Node.js 18+ and npm 9+
- PostgreSQL 14+ (for data persistence)

### Quick Start
```bash
# Clone and install
git clone https://github.com/org/myapp.git
cd myapp
npm install

# Configure database
cp .env.example .env
# Edit .env with your database URL

# Run migrations
npm run migrate

# Start development server
npm run dev
```

Open http://localhost:3000

## Usage

### Creating Tasks
Click "New Task" or press `Ctrl+N`:
```typescript
// Or create programmatically
const task = await api.createTask({
  title: 'Review PR',
  priority: 'high',
  dueDate: '2025-01-20'
});
```
```

**Why Better:**
- Clear value proposition
- Complete setup instructions
- Working code examples
- Prerequisites specified
- Specific feature descriptions

### Example 2: Poor vs. Good API Documentation

**POOR:**
```markdown
## POST /users

Create user

Parameters:
- name
- email

Returns user object
```

**GOOD:**
```markdown
## POST /users

Creates a new user account and sends verification email.

### Endpoint
```
POST /api/v1/users
```

### Authentication
Not required (public endpoint)

### Request Body

```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "password": "securePass123!"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `name` | string | Yes | 2-100 characters |
| `email` | string | Yes | Valid email format, must be unique |
| `password` | string | Yes | Min 8 chars, must include number |

### Response (201 Created)

```json
{
  "data": {
    "id": "usr_abc123",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "created_at": "2025-01-15T10:30:00Z",
    "email_verified": false
  }
}
```

### Error Responses

**400 Bad Request** - Email already exists
```json
{
  "error": {
    "code": "EMAIL_EXISTS",
    "message": "An account with this email already exists"
  }
}
```

**422 Unprocessable Entity** - Validation failed
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Password must be at least 8 characters",
    "field": "password"
  }
}
```

### Example Request

```bash
curl -X POST https://api.example.com/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "password": "securePass123!"
  }'
```

### Rate Limiting
- 10 requests per hour per IP address
- Resets at the top of each hour
```

**Why Better:**
- Complete request/response examples
- All error codes documented
- Field constraints specified
- Working curl example
- Rate limiting noted
- Authentication requirements clear

### Example 3: Poor vs. Good Code Comments

**POOR:**
```python
def calc(a, b, c):
    # Calculate
    x = a + b
    # Multiply by c
    return x * c
```

**GOOD:**
```python
def calculate_total_with_tax(subtotal: float, shipping: float, tax_rate: float) -> float:
    """
    Calculates total price including shipping and tax.

    Tax is applied to subtotal only, not shipping (per IRS Publication 535).

    Args:
        subtotal: Item total in dollars
        shipping: Shipping cost in dollars
        tax_rate: Tax rate as decimal (0.08 for 8%)

    Returns:
        Total price in dollars, rounded to 2 decimal places

    Example:
        >>> calculate_total_with_tax(100.00, 15.00, 0.08)
        123.00
    """
    tax = round(subtotal * tax_rate, 2)
    total = subtotal + shipping + tax
    return round(total, 2)
```

**Why Better:**
- Descriptive function name
- Docstring explains business logic
- Type hints for clarity
- Example shows usage
- Explains non-obvious tax calculation rule

---

## Automated Triggers

This skill activates when agents:
- Create or update README files
- Document API endpoints or interfaces
- Write user guides, tutorials, or FAQs
- Develop SOPs or process documentation
- Review documentation for completeness
- Add code comments or docstrings
- Format Markdown documents
- Standardize documentation structure

**Task Keywords:** documentation, README, API docs, user guide, tutorial, SOP, procedure, comments, docstring, Markdown

---

## Integration

**Applies to Agents:**
- technical-readme-writer
- api-documenter
- user-guide-writer
- sop-steward
- code-reviewer (for comment standards)
- technical-writer (all types)

**Works with Skills:**
- code-quality-standards (for code comment validation)
- security-standards (for security documentation requirements)
- testing-standards (for test documentation)

**Token Reduction:**
- Eliminates ~1,800 tokens per documentation agent (4 agents)
- Total reduction: ~7,200 tokens across squad
- Templates loaded on-demand vs. always in prompt

**Maintenance:**
- Update templates here propagates to all documentation agents
- Single source of truth for formatting conventions
- Version control for documentation standard changes

---

**Source:** Consolidated from documentation agent best practices and industry standards (Google Developer Documentation Style Guide, Microsoft Writing Style Guide, GitLab Documentation Guidelines)