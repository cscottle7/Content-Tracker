---
name: testing-frameworks
description: Standardizes testing approaches including AAA pattern, naming conventions, coverage requirements, mocking strategies, and test organization. Activates during test writing, test strategy design, quality assessment, and test automation for Jest, pytest, Mocha, JUnit, and other frameworks.
---

# Testing Frameworks

## Purpose
Provides universal testing standards and framework-specific implementations to ensure consistent, maintainable, and effective test suites across all projects. Eliminates redundancy in testing agent prompts while maintaining quality standards.

## Core Testing Principles

### AAA Pattern (Arrange-Act-Assert)
All tests must follow this three-phase structure:

1. **Arrange**: Set up test data, mocks, and preconditions
2. **Act**: Execute the function/method under test
3. **Assert**: Verify the expected outcome

**Unit Test Example (Jest/TypeScript)**:
```typescript
describe('UserService', () => {
  it('should create user with hashed password', async () => {
    // Arrange
    const userData = { email: 'test@example.com', password: 'plaintext123' };
    const mockHasher = jest.fn().mockResolvedValue('hashed_password');
    const userService = new UserService(mockHasher);

    // Act
    const result = await userService.createUser(userData);

    // Assert
    expect(result.password).toBe('hashed_password');
    expect(mockHasher).toHaveBeenCalledWith('plaintext123');
  });
});
```

**Unit Test Example (pytest/Python)**:
```python
def test_create_user_with_hashed_password():
    # Arrange
    user_data = {"email": "test@example.com", "password": "plaintext123"}
    mock_hasher = Mock(return_value="hashed_password")
    user_service = UserService(hasher=mock_hasher)

    # Act
    result = user_service.create_user(user_data)

    # Assert
    assert result.password == "hashed_password"
    mock_hasher.assert_called_once_with("plaintext123")
```

**Integration Test Example (Jest)**:
```typescript
describe('API Integration: POST /users', () => {
  it('should persist user to database and return 201', async () => {
    // Arrange
    const payload = { email: 'new@example.com', password: 'secure123' };
    await cleanDatabase();

    // Act
    const response = await request(app).post('/users').send(payload);

    // Assert
    expect(response.status).toBe(201);
    const dbUser = await db.users.findOne({ email: 'new@example.com' });
    expect(dbUser).toBeDefined();
    expect(dbUser.password).not.toBe('secure123'); // should be hashed
  });
});
```

**E2E Test Example (Playwright)**:
```typescript
test('complete user registration flow', async ({ page }) => {
  // Arrange
  await page.goto('/register');

  // Act
  await page.fill('[data-testid="email"]', 'user@example.com');
  await page.fill('[data-testid="password"]', 'SecurePass123!');
  await page.click('[data-testid="submit"]');

  // Assert
  await expect(page.locator('[data-testid="welcome-message"]')).toBeVisible();
  await expect(page).toHaveURL('/dashboard');
});
```

## Test Naming Conventions

### JavaScript/TypeScript (Jest, Mocha, Vitest)
Use `describe` for grouping and `it`/`test` for individual tests:

```typescript
describe('ComponentName or ClassName', () => {
  describe('methodName', () => {
    it('should [expected behavior] when [condition]', () => {});
    it('should throw error when [invalid condition]', () => {});
  });

  describe('edge cases', () => {
    it('should handle null input gracefully', () => {});
    it('should handle empty array', () => {});
  });
});
```

**Naming Pattern**: `should [action/outcome] when/if [condition]`

### Python (pytest, unittest)
Use `test_` prefix with descriptive snake_case names:

```python
class TestUserService:
    def test_create_user_with_valid_data(self):
        pass

    def test_create_user_raises_error_when_email_exists(self):
        pass

    def test_create_user_handles_database_connection_failure(self):
        pass

class TestEdgeCases:
    def test_handles_none_input(self):
        pass

    def test_handles_empty_string(self):
        pass
```

**Naming Pattern**: `test_[method]_[expected_outcome]_[condition]`

### Java (JUnit)
Use `@Test` annotation with camelCase or underscores:

```java
@Test
public void createUser_WithValidData_ReturnsUser() {
    // Arrange, Act, Assert
}

@Test
public void createUser_WhenEmailExists_ThrowsException() {
    // Arrange, Act, Assert
}
```

## Test Organization

### Directory Structure

**JavaScript/TypeScript Projects**:
```
src/
  components/
    UserCard.tsx
    __tests__/
      UserCard.test.tsx
      UserCard.integration.test.tsx
  services/
    UserService.ts
    __tests__/
      UserService.test.ts
tests/
  e2e/
    user-registration.spec.ts
    user-login.spec.ts
  integration/
    api/
      users.test.ts
  fixtures/
    users.json
  helpers/
    database.ts
```

**Python Projects**:
```
src/
  services/
    user_service.py
tests/
  unit/
    services/
      test_user_service.py
  integration/
    test_api_users.py
  e2e/
    test_user_workflows.py
  fixtures/
    users.py
    factories.py
  conftest.py  # pytest fixtures
```

### File Naming Conventions

| Test Type | JavaScript/TypeScript | Python | Java |
|-----------|----------------------|---------|------|
| Unit | `*.test.ts` or `*.spec.ts` | `test_*.py` | `*Test.java` |
| Integration | `*.integration.test.ts` | `test_*_integration.py` | `*IntegrationTest.java` |
| E2E | `*.e2e.test.ts` or `*.spec.ts` | `test_*_e2e.py` | `*E2ETest.java` |

## Coverage Requirements

### Minimum Thresholds
- **Overall Coverage**: 80% minimum
- **Critical Paths**: 100% (authentication, payment, data loss scenarios)
- **Branch Coverage**: 75% minimum
- **New Code**: 90% minimum (enforce in CI/CD)

### Coverage Measurement Tools

**Jest (JavaScript/TypeScript)**:
```json
{
  "jest": {
    "collectCoverage": true,
    "coverageThreshold": {
      "global": {
        "branches": 75,
        "functions": 80,
        "lines": 80,
        "statements": 80
      },
      "./src/critical/**/*.ts": {
        "branches": 100,
        "functions": 100,
        "lines": 100,
        "statements": 100
      }
    }
  }
}
```

**pytest (Python)**:
```ini
# pytest.ini
[tool:pytest]
addopts = --cov=src --cov-report=html --cov-report=term --cov-fail-under=80

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

**JaCoCo (Java)**:
```xml
<execution>
  <id>check</id>
  <goals><goal>check</goal></goals>
  <configuration>
    <rules>
      <rule>
        <element>BUNDLE</element>
        <limits>
          <limit>
            <counter>LINE</counter>
            <value>COVEREDRATIO</value>
            <minimum>0.80</minimum>
          </limit>
        </limits>
      </rule>
    </rules>
  </configuration>
</execution>
```

### Coverage Strategy
1. **Focus on business logic**: Prioritize testing complex algorithms and decision trees
2. **Skip trivial code**: Getters, setters, simple DTOs may not need explicit tests
3. **Test edge cases**: Null, empty, boundary values, error conditions
4. **Monitor trends**: Coverage should increase over time, not decrease

## Mocking Patterns

### When to Mock
- **External APIs/Services**: Always mock to avoid network calls and flakiness
- **Database Calls**: Mock in unit tests, use real/test DB in integration tests
- **Time-Dependent Code**: Mock `Date.now()`, `time.time()` for predictability
- **File System**: Mock in unit tests to avoid I/O overhead
- **Random Values**: Mock randomness for deterministic tests

### When NOT to Mock
- **Pure functions**: No external dependencies, no need to mock
- **Integration tests**: Test real interactions between components
- **Simple utility functions**: Actual implementation is faster than mock setup

### Mock Types

**Stub**: Returns predetermined values
```typescript
// Jest
const stub = jest.fn().mockReturnValue(42);

// Python
stub = Mock(return_value=42)
```

**Spy**: Records calls while preserving original behavior
```typescript
// Jest
const spy = jest.spyOn(object, 'method');

// Python (pytest)
spy = mocker.spy(object, 'method')
```

**Mock**: Replaces entire implementation
```typescript
// Jest
const mock = jest.fn().mockImplementation((x) => x * 2);

// Python
mock = Mock(side_effect=lambda x: x * 2)
```

### Framework-Specific Mocking

**Jest (JavaScript/TypeScript)**:
```typescript
// Mock module
jest.mock('./UserService');
const mockUserService = UserService as jest.MockedClass<typeof UserService>;

// Mock function
const mockFetch = jest.fn().mockResolvedValue({ json: () => ({ id: 1 }) });
global.fetch = mockFetch;

// Mock partial object
const mockConfig = {
  apiUrl: 'http://test.com',
  timeout: 5000
} as Config;

// Verify calls
expect(mockFetch).toHaveBeenCalledTimes(1);
expect(mockFetch).toHaveBeenCalledWith('http://test.com/users', expect.objectContaining({
  method: 'POST'
}));
```

**pytest (Python)**:
```python
# Mock with pytest-mock
def test_api_call(mocker):
    mock_requests = mocker.patch('requests.get')
    mock_requests.return_value.json.return_value = {'id': 1}

    result = fetch_user(1)

    mock_requests.assert_called_once_with('http://api.com/users/1')
    assert result['id'] == 1

# Mock with unittest.mock
from unittest.mock import Mock, patch

@patch('module.external_service')
def test_service_call(mock_service):
    mock_service.get_data.return_value = {'status': 'ok'}
    # test code
```

**Mocha with Sinon (JavaScript)**:
```javascript
const sinon = require('sinon');

describe('UserService', () => {
  let fetchStub;

  beforeEach(() => {
    fetchStub = sinon.stub(global, 'fetch').resolves({
      json: () => Promise.resolve({ id: 1 })
    });
  });

  afterEach(() => {
    fetchStub.restore();
  });

  it('should fetch user data', async () => {
    const result = await userService.getUser(1);
    expect(fetchStub.calledOnce).to.be.true;
    expect(result.id).to.equal(1);
  });
});
```

## Test Data Management

### Fixtures (Static Data)

**Jest**:
```typescript
// tests/fixtures/users.ts
export const mockUsers = [
  { id: 1, email: 'user1@example.com', role: 'admin' },
  { id: 2, email: 'user2@example.com', role: 'user' }
];

// usage in test
import { mockUsers } from '../fixtures/users';
```

**pytest**:
```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_users():
    return [
        {"id": 1, "email": "user1@example.com", "role": "admin"},
        {"id": 2, "email": "user2@example.com", "role": "user"}
    ]

# usage in test
def test_user_list(sample_users):
    assert len(sample_users) == 2
```

### Factories (Dynamic Data)

**JavaScript (Fishery)**:
```typescript
import { Factory } from 'fishery';

const userFactory = Factory.define<User>(({ sequence }) => ({
  id: sequence,
  email: `user${sequence}@example.com`,
  createdAt: new Date()
}));

// usage
const user = userFactory.build();
const users = userFactory.buildList(5);
const adminUser = userFactory.build({ role: 'admin' });
```

**Python (Factory Boy)**:
```python
import factory

class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    created_at = factory.LazyFunction(datetime.now)

# usage
user = UserFactory()
users = UserFactory.build_batch(5)
admin = UserFactory(role='admin')
```

### Database Seeders (Integration/E2E Tests)

**JavaScript/TypeScript**:
```typescript
// tests/helpers/database.ts
export async function seedDatabase() {
  await db.users.insertMany([
    { email: 'test1@example.com', password: 'hashed' },
    { email: 'test2@example.com', password: 'hashed' }
  ]);
}

export async function cleanDatabase() {
  await db.users.deleteMany({});
  await db.posts.deleteMany({});
}

// usage
beforeEach(async () => {
  await cleanDatabase();
  await seedDatabase();
});
```

**Python**:
```python
# tests/conftest.py
@pytest.fixture
def db_session():
    """Creates a fresh database session for testing."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(engine)
```

### Cleanup Strategies

**Transactional Tests (Rollback after each test)**:
```python
# pytest with SQLAlchemy
@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

**Truncate Strategy (Fast cleanup)**:
```typescript
afterEach(async () => {
  await db.raw('TRUNCATE users, posts CASCADE');
});
```

**Delete Strategy (Safest for isolated tests)**:
```typescript
afterEach(async () => {
  await db.users.deleteMany({ email: { $regex: /test/ } });
});
```

## Framework-Specific Examples

### Jest (JavaScript/TypeScript)

**Setup**:
```json
{
  "jest": {
    "preset": "ts-jest",
    "testEnvironment": "node",
    "setupFilesAfterEnv": ["<rootDir>/tests/setup.ts"],
    "testMatch": ["**/__tests__/**/*.test.ts"]
  }
}
```

**Async Testing**:
```typescript
it('should resolve user data', async () => {
  const user = await userService.getUser(1);
  expect(user.email).toBe('test@example.com');
});

it('should reject with error', async () => {
  await expect(userService.getUser(999)).rejects.toThrow('User not found');
});
```

**Snapshot Testing**:
```typescript
it('should match component snapshot', () => {
  const tree = renderer.create(<UserCard user={mockUser} />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

### pytest (Python)

**Setup**:
```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

**Parametrized Tests**:
```python
@pytest.mark.parametrize("email,expected", [
    ("valid@example.com", True),
    ("invalid-email", False),
    ("", False),
])
def test_email_validation(email, expected):
    assert validate_email(email) == expected
```

**Fixtures with Scope**:
```python
@pytest.fixture(scope="module")
def database():
    """Shared database connection for entire test module."""
    db = create_connection()
    yield db
    db.close()
```

### Mocha (JavaScript)

**Setup**:
```json
{
  "scripts": {
    "test": "mocha --require ts-node/register 'tests/**/*.test.ts'"
  }
}
```

**Hooks**:
```javascript
describe('UserService', () => {
  before(() => {
    // runs once before all tests
  });

  beforeEach(() => {
    // runs before each test
  });

  afterEach(() => {
    // runs after each test
  });

  after(() => {
    // runs once after all tests
  });
});
```

### JUnit (Java)

**Setup**:
```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class UserServiceTest {
    private UserService userService;

    @BeforeAll
    void setupAll() {
        // runs once before all tests
    }

    @BeforeEach
    void setup() {
        userService = new UserService();
    }

    @Test
    void createUser_WithValidData_ReturnsUser() {
        // Arrange
        UserDTO dto = new UserDTO("test@example.com", "password");

        // Act
        User result = userService.createUser(dto);

        // Assert
        assertNotNull(result);
        assertEquals("test@example.com", result.getEmail());
    }

    @Test
    void createUser_WhenEmailExists_ThrowsException() {
        // Arrange
        UserDTO dto = new UserDTO("existing@example.com", "password");

        // Act & Assert
        assertThrows(DuplicateEmailException.class, () -> {
            userService.createUser(dto);
        });
    }
}
```

## Automated Triggers
This skill activates during:
- Test file creation or modification
- Test strategy design and planning
- Code review with test quality assessment
- Test coverage analysis and reporting
- Test automation setup and configuration
- CI/CD pipeline test integration
- Quality assessment tasks

## Integration
- **Works with**: code-quality-standards (enforces testing in code reviews)
- **Works with**: error-handling (validates error testing coverage)
- **Applied by**: qa-automation, test-strategist, quality-assessor, any agent writing tests

**Token Efficiency**: Replaces ~1,500 tokens per testing agent (3 agents × 1,500 = 4,500 total tokens saved)

**Source**: Industry best practices, Jest documentation, pytest documentation, JUnit 5 documentation, Kent C. Dodds testing principles