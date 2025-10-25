---
name: code-quality-standards
description: Enforces code quality standards including style guidelines, naming conventions, comment requirements, and error handling patterns. Automatically validates during code review, quality assessment, and security audit tasks for Python, JavaScript, and TypeScript projects.
---

# Code Quality Standards

## Purpose
Establishes consistent code quality baselines across all development agents. Ensures maintainability, readability, and reliability through standardized style guidelines, naming conventions, documentation requirements, and error handling patterns.

---

## Core Standards

### 1. Style Guidelines

#### Python (PEP 8)
| Aspect | Standard | Example |
|--------|----------|---------|
| Line Length | Max 88 chars (Black formatter) | `def process_user_data(user_id: int, include_history: bool = False):` |
| Indentation | 4 spaces (no tabs) | `    return user_data` |
| Imports | Stdlib → Third-party → Local | `import os`<br>`import requests`<br>`from .models import User` |
| Blank Lines | 2 before classes/functions, 1 between methods | See examples below |
| Trailing Commas | Use in multi-line structures | `data = [1, 2, 3,]` |

**Python Example:**
```python
import os
from typing import List, Optional

import requests

from .models import User


class UserService:
    """Handles user-related operations."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "https://api.example.com"

    def get_user(self, user_id: int) -> Optional[User]:
        """Retrieve user by ID."""
        try:
            response = requests.get(
                f"{self.base_url}/users/{user_id}",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10,
            )
            response.raise_for_status()
            return User(**response.json())
        except requests.RequestException as e:
            logger.error(f"Failed to fetch user {user_id}: {e}")
            return None
```

#### JavaScript/TypeScript (ESLint + Prettier)
| Aspect | Standard | Example |
|--------|----------|---------|
| Line Length | Max 100 chars | `const processUserData = (userId: number, includeHistory = false) => {` |
| Indentation | 2 spaces | `  return userData;` |
| Quotes | Single quotes (strings), double (JSX) | `const name = 'John';` |
| Semicolons | Always required | `const x = 5;` |
| Trailing Commas | Use in multi-line (ES5+) | `const obj = { a: 1, b: 2, };` |

**TypeScript Example:**
```typescript
import { User, UserResponse } from './types';
import { ApiClient } from '../api/client';

interface UserServiceConfig {
  apiKey: string;
  baseUrl: string;
}

export class UserService {
  private apiClient: ApiClient;

  constructor(private config: UserServiceConfig) {
    this.apiClient = new ApiClient(config);
  }

  async getUser(userId: number): Promise<User | null> {
    try {
      const response = await this.apiClient.get<UserResponse>(
        `/users/${userId}`,
        { timeout: 10000 }
      );
      return this.mapResponseToUser(response);
    } catch (error) {
      console.error(`Failed to fetch user ${userId}:`, error);
      return null;
    }
  }

  private mapResponseToUser(response: UserResponse): User {
    return {
      id: response.id,
      name: response.name,
      email: response.email,
    };
  }
}
```

---

### 2. Naming Conventions

#### Language-Specific Rules

| Element | Python | JavaScript/TypeScript |
|---------|--------|----------------------|
| Variables | `snake_case` | `camelCase` |
| Functions/Methods | `snake_case` | `camelCase` |
| Classes | `PascalCase` | `PascalCase` |
| Constants | `UPPER_SNAKE_CASE` | `UPPER_SNAKE_CASE` |
| Private Members | `_leading_underscore` | `#privateField` or `_conventionOnly` |
| Type/Interface | `PascalCase` | `PascalCase` |
| Enums | `PascalCase` (name), `UPPER_CASE` (values) | `PascalCase` (name), `PascalCase` (values) |

#### Semantic Naming Guidelines

**DO:**
- Use descriptive, intention-revealing names: `calculate_monthly_revenue()` not `calc()`
- Boolean variables start with `is_`, `has_`, `should_`: `is_active`, `has_permission`
- Collections use plural nouns: `users`, `order_items`
- Functions use verb phrases: `get_user()`, `validate_email()`, `transform_data()`

**DON'T:**
- Use single letters except loop counters (`i`, `j`, `k`) or common math (`x`, `y`)
- Use abbreviations unless universally known (`http`, `api`, `url` are OK)
- Use type info in names: `user_dict`, `name_string` (type hints handle this)

**Examples:**
```python
# GOOD
def calculate_total_price(items: List[OrderItem], tax_rate: float) -> Decimal:
    is_discount_eligible = len(items) > 5
    has_premium_membership = user.membership_level == MembershipLevel.PREMIUM

    subtotal = sum(item.price for item in items)
    return apply_tax(subtotal, tax_rate) if not is_discount_eligible else subtotal

# BAD
def calc(i: List, t: float) -> Decimal:
    de = len(i) > 5
    pm = user.ml == ML.P

    st = sum(x.p for x in i)
    return at(st, t) if not de else st
```

---

### 3. Comment Requirements

#### When to Comment

**REQUIRED:**
- Module/file docstrings (purpose, usage)
- Public class docstrings (responsibility, usage)
- Public function/method docstrings (params, returns, raises)
- Complex algorithms (explain WHY, not WHAT)
- Non-obvious business logic
- Temporary workarounds (TODO, FIXME, HACK with ticket reference)

**AVOID:**
- Obvious code explanations: `# increment counter` before `counter += 1`
- Commented-out code (use version control)
- Redundant comments that repeat the code

#### Python Docstring Format (Google Style)

```python
def process_payment(
    order_id: int,
    amount: Decimal,
    payment_method: PaymentMethod,
    *,
    idempotency_key: Optional[str] = None
) -> PaymentResult:
    """Process a payment transaction for an order.

    Validates the payment method, processes the charge, and updates
    the order status. Supports idempotent operations via key.

    Args:
        order_id: Unique identifier for the order.
        amount: Payment amount in USD.
        payment_method: Payment method (credit_card, paypal, etc).
        idempotency_key: Optional key to prevent duplicate charges.

    Returns:
        PaymentResult containing transaction_id and status.

    Raises:
        InvalidPaymentMethodError: If payment method is not supported.
        InsufficientFundsError: If payment cannot be processed.
        DuplicateTransactionError: If idempotency_key already used.

    Example:
        >>> result = process_payment(
        ...     order_id=12345,
        ...     amount=Decimal("99.99"),
        ...     payment_method=PaymentMethod.CREDIT_CARD,
        ...     idempotency_key="order-12345-attempt-1"
        ... )
        >>> print(result.transaction_id)
        'txn_abc123'
    """
    # TODO(#456): Add support for cryptocurrency payments
    # HACK: Temporary retry logic until payment gateway fixes timeout issue
    pass
```

#### TypeScript JSDoc Format

```typescript
/**
 * Process a payment transaction for an order.
 *
 * Validates the payment method, processes the charge, and updates
 * the order status. Supports idempotent operations via key.
 *
 * @param orderId - Unique identifier for the order
 * @param amount - Payment amount in USD
 * @param paymentMethod - Payment method (credit_card, paypal, etc)
 * @param options - Optional configuration
 * @param options.idempotencyKey - Key to prevent duplicate charges
 *
 * @returns Promise resolving to PaymentResult with transaction_id and status
 *
 * @throws {InvalidPaymentMethodError} If payment method is not supported
 * @throws {InsufficientFundsError} If payment cannot be processed
 * @throws {DuplicateTransactionError} If idempotency key already used
 *
 * @example
 * ```typescript
 * const result = await processPayment(
 *   12345,
 *   99.99,
 *   PaymentMethod.CreditCard,
 *   { idempotencyKey: 'order-12345-attempt-1' }
 * );
 * console.log(result.transactionId); // 'txn_abc123'
 * ```
 */
async function processPayment(
  orderId: number,
  amount: number,
  paymentMethod: PaymentMethod,
  options?: { idempotencyKey?: string }
): Promise<PaymentResult> {
  // TODO(#456): Add support for cryptocurrency payments
  // Implementation...
}
```

#### Inline Comments for Complex Logic

```python
def calculate_shipping_cost(weight: float, distance: int, zone: str) -> Decimal:
    """Calculate shipping cost based on weight, distance, and zone."""
    base_rate = Decimal("5.00")

    # Apply tiered weight multiplier (non-linear pricing above 50 lbs)
    # Business rule: Encourage splitting heavy shipments
    if weight <= 10:
        weight_cost = Decimal(str(weight)) * Decimal("0.50")
    elif weight <= 50:
        weight_cost = Decimal(str(weight)) * Decimal("0.75")
    else:
        # Exponential increase to discourage single heavy shipments
        weight_cost = Decimal(str(weight)) * Decimal("1.25") * Decimal("1.5")

    # Zone multipliers based on carrier contracts (updated Q4 2024)
    zone_multipliers = {
        "local": Decimal("1.0"),
        "regional": Decimal("1.5"),
        "national": Decimal("2.0"),
        "international": Decimal("3.5"),
    }

    return (base_rate + weight_cost) * zone_multipliers.get(zone, Decimal("2.0"))
```

---

### 4. Error Handling Patterns

#### Python Exception Handling

**Best Practices:**
- Catch specific exceptions, not bare `except:`
- Use `try` blocks only around code that can raise
- Always log errors with context
- Re-raise after logging if caller should handle
- Clean up resources with `finally` or context managers

```python
import logging
from typing import Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# GOOD: Specific exception handling with context
def fetch_user_data(user_id: int) -> Optional[dict]:
    """Fetch user data from external API."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/users/{user_id}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        logger.error(
            f"Timeout fetching user {user_id}",
            extra={"user_id": user_id, "timeout": 10}
        )
        return None
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            logger.warning(f"User {user_id} not found")
            return None
        logger.error(
            f"HTTP error fetching user {user_id}: {e.response.status_code}",
            extra={"user_id": user_id, "status_code": e.response.status_code}
        )
        raise  # Re-raise for 5xx errors
    except requests.RequestException as e:
        logger.exception(f"Unexpected error fetching user {user_id}")
        raise

# BAD: Too broad, no context
def fetch_user_data_bad(user_id: int) -> Optional[dict]:
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
        return response.json()
    except:  # Never use bare except
        logger.error("Error occurred")
        return None

# GOOD: Resource cleanup with context manager
@contextmanager
def database_transaction(db_session):
    """Context manager for database transactions."""
    try:
        yield db_session
        db_session.commit()
        logger.info("Transaction committed successfully")
    except Exception as e:
        db_session.rollback()
        logger.error(f"Transaction failed, rolling back: {e}")
        raise
    finally:
        db_session.close()

# Usage
with database_transaction(session) as db:
    db.add(new_user)
```

#### TypeScript Error Handling

**Best Practices:**
- Use typed errors (extend `Error` class)
- Always type catch blocks (`unknown`, not `any`)
- Provide error context for debugging
- Use Result types for expected failures
- Handle promise rejections

```typescript
// GOOD: Custom typed errors
class ValidationError extends Error {
  constructor(
    message: string,
    public field: string,
    public value: unknown
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}

class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public endpoint: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// GOOD: Typed error handling with context
async function fetchUserData(userId: number): Promise<User | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      signal: AbortSignal.timeout(10000),
    });

    if (!response.ok) {
      if (response.status === 404) {
        console.warn(`User ${userId} not found`);
        return null;
      }
      throw new ApiError(
        `Failed to fetch user ${userId}`,
        response.status,
        `/users/${userId}`
      );
    }

    return await response.json();
  } catch (error) {
    // Always type as unknown, then narrow
    if (error instanceof ApiError) {
      console.error(`API error: ${error.message}`, {
        statusCode: error.statusCode,
        endpoint: error.endpoint,
      });
      throw error; // Re-throw for 5xx errors
    } else if (error instanceof DOMException && error.name === 'TimeoutError') {
      console.error(`Timeout fetching user ${userId}`, { userId, timeout: 10000 });
      return null;
    } else {
      console.error(`Unexpected error fetching user ${userId}:`, error);
      throw error;
    }
  }
}

// GOOD: Result type for expected failures
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

async function validateAndSaveUser(userData: unknown): Promise<Result<User>> {
  try {
    const validatedData = userSchema.parse(userData);
    const user = await saveUser(validatedData);
    return { success: true, data: user };
  } catch (error) {
    if (error instanceof ValidationError) {
      return {
        success: false,
        error: new Error(`Validation failed: ${error.message}`)
      };
    }
    throw error; // Unexpected errors still throw
  }
}

// Usage
const result = await validateAndSaveUser(formData);
if (result.success) {
  console.log('User saved:', result.data);
} else {
  console.error('Validation failed:', result.error.message);
}
```

---

### 5. Testing Requirements

#### Minimum Coverage Standards
- **Unit Tests:** 80% line coverage minimum
- **Integration Tests:** All API endpoints, critical paths
- **E2E Tests:** Core user journeys (signup, checkout, etc.)

#### Test File Naming
| Language | Convention | Example |
|----------|-----------|---------|
| Python | `test_<module>.py` | `test_user_service.py` |
| JavaScript/TypeScript | `<module>.test.ts` or `<module>.spec.ts` | `userService.test.ts` |

#### Test Structure (AAA Pattern)

**Python (pytest):**
```python
import pytest
from decimal import Decimal
from src.services.payment_service import PaymentService, InsufficientFundsError

class TestPaymentService:
    """Test suite for PaymentService."""

    @pytest.fixture
    def payment_service(self):
        """Create PaymentService instance for testing."""
        return PaymentService(api_key="test_key_123")

    def test_process_payment_success(self, payment_service):
        """Test successful payment processing."""
        # Arrange
        order_id = 12345
        amount = Decimal("99.99")

        # Act
        result = payment_service.process_payment(order_id, amount)

        # Assert
        assert result.success is True
        assert result.transaction_id is not None
        assert result.amount == amount

    def test_process_payment_insufficient_funds(self, payment_service):
        """Test payment processing with insufficient funds."""
        # Arrange
        order_id = 12345
        amount = Decimal("999999.99")

        # Act & Assert
        with pytest.raises(InsufficientFundsError) as exc_info:
            payment_service.process_payment(order_id, amount)

        assert "insufficient funds" in str(exc_info.value).lower()
        assert exc_info.value.order_id == order_id

    @pytest.mark.parametrize("amount,expected_fee", [
        (Decimal("10.00"), Decimal("0.30")),
        (Decimal("100.00"), Decimal("3.00")),
        (Decimal("1000.00"), Decimal("30.00")),
    ])
    def test_calculate_processing_fee(self, payment_service, amount, expected_fee):
        """Test processing fee calculation for various amounts."""
        # Act
        fee = payment_service.calculate_processing_fee(amount)

        # Assert
        assert fee == expected_fee
```

**TypeScript (Jest):**
```typescript
import { PaymentService } from './paymentService';
import { InsufficientFundsError } from './errors';

describe('PaymentService', () => {
  let paymentService: PaymentService;

  beforeEach(() => {
    paymentService = new PaymentService({ apiKey: 'test_key_123' });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('processPayment', () => {
    it('should successfully process a valid payment', async () => {
      // Arrange
      const orderId = 12345;
      const amount = 99.99;

      // Act
      const result = await paymentService.processPayment(orderId, amount);

      // Assert
      expect(result.success).toBe(true);
      expect(result.transactionId).toBeDefined();
      expect(result.amount).toBe(amount);
    });

    it('should throw InsufficientFundsError when funds are insufficient', async () => {
      // Arrange
      const orderId = 12345;
      const amount = 999999.99;

      // Act & Assert
      await expect(
        paymentService.processPayment(orderId, amount)
      ).rejects.toThrow(InsufficientFundsError);
    });
  });

  describe('calculateProcessingFee', () => {
    it.each([
      [10.00, 0.30],
      [100.00, 3.00],
      [1000.00, 30.00],
    ])('should calculate %p as %p fee', (amount, expectedFee) => {
      // Act
      const fee = paymentService.calculateProcessingFee(amount);

      // Assert
      expect(fee).toBe(expectedFee);
    });
  });

  describe('integration: full payment flow', () => {
    it('should process payment, update order, and send confirmation', async () => {
      // Arrange
      const orderId = 12345;
      const amount = 99.99;
      const mockUpdateOrder = jest.spyOn(paymentService, 'updateOrderStatus');
      const mockSendEmail = jest.spyOn(paymentService, 'sendConfirmationEmail');

      // Act
      await paymentService.processPayment(orderId, amount);

      // Assert
      expect(mockUpdateOrder).toHaveBeenCalledWith(orderId, 'paid');
      expect(mockSendEmail).toHaveBeenCalledWith(
        expect.objectContaining({ orderId, amount })
      );
    });
  });
});
```

#### Test Naming Convention
- Use descriptive names: `test_<function>_<scenario>_<expected_result>`
- Example: `test_process_payment_with_invalid_card_raises_error`
- Example: `should return null when user does not exist`

---

## Automated Triggers

This skill activates during:
- **Code Review:** Validating style, naming, documentation compliance
- **Quality Assessment:** Evaluating maintainability, readability scores
- **Security Audits:** Checking error handling, input validation patterns
- **Pre-commit Validation:** Enforcing standards before code submission
- **Refactoring Tasks:** Ensuring consistency after code changes
- **Documentation Generation:** Verifying docstring/JSDoc completeness

---

## Integration

**Inherits From:** None (foundation skill)

**Works With:**
- `security-best-practices` - Complements with security-specific standards
- `performance-optimization` - Aligns with performance patterns
- `testing-strategies` - Extends with testing methodologies

**Applied By:**
- `quality-assessor` - Primary enforcer of all standards
- `performance-tuner` - Validates code quality during optimizations
- `code-archaeologist` - Ensures standards during legacy code updates
- `security-auditor` - Checks compliance during security reviews
- `static-code-scanner` - Automates standard validation

**Token Efficiency:**
- Replaces ~400 lines per agent prompt
- Estimated reduction: 2,000 tokens × 5 agents = **10,000 tokens saved**
- Centralizes maintenance: Update once, applies to all agents

---

**Source:** Synthesized from PEP 8, Airbnb JavaScript Style Guide, Google Style Guides, and industry best practices.
