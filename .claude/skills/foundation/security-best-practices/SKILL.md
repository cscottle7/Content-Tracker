---
name: security-best-practices
description: Enforces OWASP Top 10 security standards including vulnerability detection patterns, secure coding practices, authentication/authorization standards, and data protection for security audits, threat modeling, vulnerability scanning, and penetration testing across all languages and frameworks.
---

# Security Best Practices

## Purpose
Centralized security knowledge base for all security-related agents. Provides actionable standards for vulnerability detection, secure coding patterns, and threat mitigation based on OWASP guidelines and industry best practices.

## OWASP Top 10 Vulnerabilities

### A01:2021 - Broken Access Control [CRITICAL]
**CWE-200, CWE-201, CWE-352**

**Vulnerable Pattern:**
```python
# Direct object reference without authorization
@app.get("/api/user/{user_id}/profile")
def get_profile(user_id: int):
    return db.query(User).filter(User.id == user_id).first()
```

**Secure Pattern:**
```python
# Verify user owns the resource
@app.get("/api/user/{user_id}/profile")
def get_profile(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return db.query(User).filter(User.id == user_id).first()
```

**Detection Patterns:**
- Direct database queries using user-supplied IDs without authorization checks
- Missing role/permission validation
- Horizontal privilege escalation (user accessing another user's data)
- Vertical privilege escalation (user accessing admin functions)

---

### A02:2021 - Cryptographic Failures [CRITICAL]
**CWE-259, CWE-327, CWE-328**

**Vulnerable Pattern:**
```javascript
// Weak encryption or plaintext storage
const password = req.body.password;
await db.users.create({ email, password }); // Stored in plaintext

// Weak hashing
const hash = crypto.createHash('md5').update(password).digest('hex');
```

**Secure Pattern:**
```javascript
// Use bcrypt/argon2 for passwords
const bcrypt = require('bcrypt');
const saltRounds = 12;
const hashedPassword = await bcrypt.hash(password, saltRounds);
await db.users.create({ email, password: hashedPassword });

// Use AES-256-GCM for data encryption
const crypto = require('crypto');
const algorithm = 'aes-256-gcm';
const key = crypto.scryptSync(secret, 'salt', 32);
const iv = crypto.randomBytes(16);
const cipher = crypto.createCipheriv(algorithm, key, iv);
```

**Detection Patterns:**
- Plaintext passwords in databases
- Use of MD5, SHA1 for password hashing
- Hardcoded encryption keys/secrets
- Transmission of sensitive data over HTTP (not HTTPS)
- Missing encryption for PII/sensitive data at rest
- Weak SSL/TLS configurations

**Data Protection Requirements:**
- Passwords: bcrypt (cost 12+), argon2id, or PBKDF2 (600k+ iterations)
- Sensitive data at rest: AES-256-GCM
- Sensitive data in transit: TLS 1.3 minimum
- PII: encrypt, minimize collection, implement data retention policies

---

### A03:2021 - Injection [CRITICAL]
**CWE-79, CWE-89, CWE-564**

#### SQL Injection

**Vulnerable Pattern:**
```python
# String concatenation in SQL
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)

# Payload: username = "admin'--" bypasses authentication
```

**Secure Pattern:**
```python
# Parameterized queries
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))

# ORM usage (preferred)
user = db.query(User).filter(User.username == username).first()
```

#### Cross-Site Scripting (XSS)

**Vulnerable Pattern:**
```javascript
// Direct HTML insertion
document.getElementById('welcome').innerHTML = "Hello " + username;
// Payload: username = "<img src=x onerror='alert(document.cookie)'>"
```

**Secure Pattern:**
```javascript
// Use textContent or sanitize
document.getElementById('welcome').textContent = "Hello " + username;

// React auto-escapes by default
<div>Hello {username}</div>

// For necessary HTML, use DOMPurify
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

#### Command Injection

**Vulnerable Pattern:**
```python
# Shell command with user input
import os
os.system(f"ping -c 1 {user_ip}")
# Payload: user_ip = "8.8.8.8; rm -rf /"
```

**Secure Pattern:**
```python
# Use subprocess with list arguments
import subprocess
subprocess.run(["ping", "-c", "1", user_ip], capture_output=True, timeout=5)

# Validate input format
import ipaddress
try:
    ipaddress.ip_address(user_ip)
    subprocess.run(["ping", "-c", "1", user_ip])
except ValueError:
    raise ValidationError("Invalid IP address")
```

**Detection Patterns:**
- String concatenation in SQL queries
- Direct HTML insertion (innerHTML, dangerouslySetInnerHTML without sanitization)
- User input in shell commands
- Unsanitized user input in eval(), exec()
- LDAP/XPath/NoSQL injection via unsanitized queries

---

### A04:2021 - Insecure Design [HIGH]
**CWE-209, CWE-256, CWE-501**

**Security Requirements:**
- Threat modeling during design phase
- Principle of least privilege
- Defense in depth (multiple security layers)
- Secure by default configurations
- Rate limiting and resource throttling

**Vulnerable Pattern:**
```python
# Unlimited password reset attempts
@app.post("/reset-password")
def reset_password(email: str):
    send_reset_email(email)
    return {"message": "If email exists, reset link sent"}
```

**Secure Pattern:**
```python
# Rate-limited with exponential backoff
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/reset-password")
@limiter.limit("3/hour")
def reset_password(email: str):
    # Add CAPTCHA after 2 failed attempts
    # Implement account lockout after 5 attempts
    send_reset_email(email)
    return {"message": "If email exists, reset link sent"}
```

**Detection Patterns:**
- Missing rate limiting on authentication endpoints
- No account lockout mechanisms
- Verbose error messages revealing system information
- Missing security controls in business logic
- No resource quotas or throttling

---

### A05:2021 - Security Misconfiguration [HIGH]
**CWE-16, CWE-611**

**Vulnerable Configurations:**
```yaml
# Debug mode in production
DEBUG = True
ALLOWED_HOSTS = ['*']

# Default credentials
admin:admin
root:password

# Unnecessary services enabled
- FTP on port 21
- Telnet on port 23
```

**Secure Configuration:**
```yaml
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')

# Strong, unique credentials
# Use secrets manager (AWS Secrets Manager, HashiCorp Vault)

# Minimal attack surface
- Disable unused services
- Remove default accounts
- Close unnecessary ports
```

**Detection Patterns:**
- Debug/verbose error modes in production
- Default credentials unchanged
- Unnecessary features enabled
- Missing security headers (CSP, HSTS, X-Frame-Options)
- Outdated software versions
- Exposed .git, .env, config files
- Directory listing enabled

**Required Security Headers:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

---

### A06:2021 - Vulnerable and Outdated Components [HIGH]
**CWE-1035, CWE-1104**

**Detection Patterns:**
- Dependencies with known CVEs
- Libraries >2 years old without updates
- Unmaintained packages (no commits in 1+ year)
- Using deprecated APIs/functions

**Mitigation Standards:**
```bash
# Automated scanning
npm audit
pip-audit
snyk test

# Dependency pinning
# package.json
"dependencies": {
  "express": "^4.18.2"  # Allows patch updates only
}

# requirements.txt
django==4.2.7  # Exact version pinning

# Regular update schedule
- Monthly: review security advisories
- Quarterly: update dependencies
- Before release: full dependency audit
```

**Severity Assessment:**
- **Critical CVE + Public Exploit:** Immediate patching required
- **High CVE:** Patch within 7 days
- **Medium CVE:** Patch within 30 days
- **Low CVE:** Patch in next release cycle

---

### A07:2021 - Identification and Authentication Failures [CRITICAL]
**CWE-287, CWE-306, CWE-798**

#### Password Security

**Vulnerable Pattern:**
```python
# Weak password requirements
if len(password) >= 6:
    create_account(username, password)

# Session without timeout
session.permanent = True
```

**Secure Pattern:**
```python
# Strong password policy
import re

def validate_password(password):
    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain uppercase")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain lowercase")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain digit")
    if not re.search(r"[!@#$%^&*]", password):
        raise ValueError("Password must contain special character")

    # Check against common passwords list
    if password in COMMON_PASSWORDS:
        raise ValueError("Password too common")

# Session timeout
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
```

#### Multi-Factor Authentication

**Required for:**
- Administrative accounts
- Access to sensitive data
- Financial transactions
- After suspicious activity detection

**Implementation:**
```python
from pyotp import TOTP

# TOTP setup
secret = pyotp.random_base32()
totp = TOTP(secret)

# Verify MFA token
def verify_mfa(user_token, secret):
    totp = TOTP(secret)
    return totp.verify(user_token, valid_window=1)
```

#### JWT Security

**Vulnerable Pattern:**
```javascript
// Weak secret, no expiration
const token = jwt.sign({ userId: user.id }, 'secret123');
```

**Secure Pattern:**
```javascript
// Strong secret, short expiration, include claims
const token = jwt.sign(
  {
    userId: user.id,
    role: user.role,
    iat: Math.floor(Date.now() / 1000)
  },
  process.env.JWT_SECRET, // 256-bit random key
  {
    expiresIn: '15m',
    issuer: 'yourapp.com',
    audience: 'yourapp.com'
  }
);

// Verify with strict options
jwt.verify(token, process.env.JWT_SECRET, {
  algorithms: ['HS256'],
  issuer: 'yourapp.com',
  audience: 'yourapp.com'
});

// Use refresh tokens for extended sessions
```

**Detection Patterns:**
- Weak password requirements (<12 chars)
- No MFA on admin accounts
- Predictable session IDs
- Session fixation vulnerabilities
- Missing session timeouts
- Credential stuffing vulnerabilities (no rate limiting)
- JWT with "none" algorithm
- Long-lived tokens without refresh mechanism

---

### A08:2021 - Software and Data Integrity Failures [HIGH]
**CWE-502, CWE-829**

**Vulnerable Pattern:**
```python
# Insecure deserialization
import pickle
data = pickle.loads(user_input)  # Remote code execution risk

# No integrity check on downloads
response = requests.get(plugin_url)
exec(response.text)
```

**Secure Pattern:**
```python
# Use safe serialization formats
import json
data = json.loads(user_input)  # Only deserializes basic types

# Verify integrity with signatures
import hashlib
import hmac

def verify_signature(data, signature, secret):
    expected = hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)

# CI/CD pipeline security
# Use signed commits
git config --global commit.gpgsign true

# Verify dependencies with checksums
pip install --require-hashes -r requirements.txt
```

**Detection Patterns:**
- Use of pickle, marshal, PyYAML.load (unsafe)
- Missing code signing
- No SRI (Subresource Integrity) for CDN resources
- Unsigned container images
- Auto-update without signature verification
- Missing integrity checks in CI/CD pipeline

---

### A09:2021 - Security Logging and Monitoring Failures [MEDIUM]
**CWE-778, CWE-223**

**Required Logging Events:**
- Authentication attempts (success/failure)
- Authorization failures
- Input validation failures
- Application errors/exceptions
- Administrative actions
- Data access (especially sensitive data)
- Security configuration changes

**Vulnerable Pattern:**
```python
# Generic error, no logging
try:
    process_payment(amount)
except Exception:
    return {"error": "Payment failed"}
```

**Secure Pattern:**
```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    logger.info(f"Payment initiated: user={user.id}, amount={amount}")
    process_payment(amount)
    logger.info(f"Payment successful: user={user.id}, transaction_id={txn.id}")
except PaymentError as e:
    logger.error(
        f"Payment failed: user={user.id}, amount={amount}, error={str(e)}",
        extra={
            'user_id': user.id,
            'ip_address': request.remote_addr,
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': 'payment_failure'
        }
    )
    # Don't expose internal error to user
    return {"error": "Payment could not be processed"}
```

**Detection Patterns:**
- No logging of authentication events
- Logs stored without integrity protection
- Missing alerts for suspicious patterns
- Logs contain sensitive data (passwords, tokens)
- No centralized log aggregation
- Insufficient log retention

**DO NOT LOG:**
- Passwords (plaintext or hashed)
- Session tokens/API keys
- Credit card numbers
- Personal health information
- Other PII without necessity

---

### A10:2021 - Server-Side Request Forgery (SSRF) [HIGH]
**CWE-918**

**Vulnerable Pattern:**
```python
# User-controlled URL without validation
@app.get("/fetch")
def fetch_url(url: str):
    response = requests.get(url)  # Can access internal services
    return response.text

# Payload: url = "http://169.254.169.254/latest/meta-data/"
# Accesses AWS metadata service, exposes credentials
```

**Secure Pattern:**
```python
from urllib.parse import urlparse
import ipaddress

ALLOWED_SCHEMES = ['http', 'https']
ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']

def is_safe_url(url):
    parsed = urlparse(url)

    # Check scheme
    if parsed.scheme not in ALLOWED_SCHEMES:
        return False

    # Check domain whitelist
    if parsed.hostname not in ALLOWED_DOMAINS:
        return False

    # Block private IP ranges
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
    except ValueError:
        pass  # Not an IP, hostname is OK if in whitelist

    return True

@app.get("/fetch")
def fetch_url(url: str):
    if not is_safe_url(url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    # Use timeout, disable redirects
    response = requests.get(url, timeout=5, allow_redirects=False)
    return response.text
```

**Detection Patterns:**
- User input directly used in HTTP requests
- No URL validation/whitelisting
- Access to metadata services (169.254.169.254, fd00:ec2::254)
- DNS rebinding vulnerabilities
- Missing network segmentation

**Blocked IP Ranges:**
- 127.0.0.0/8 (loopback)
- 10.0.0.0/8 (private)
- 172.16.0.0/12 (private)
- 192.168.0.0/16 (private)
- 169.254.0.0/16 (link-local)
- ::1/128 (IPv6 loopback)
- fc00::/7 (IPv6 private)

---

## Common Additional Vulnerabilities

### Cross-Site Request Forgery (CSRF)
**CWE-352**

**Vulnerable Pattern:**
```html
<!-- No CSRF protection -->
<form action="/transfer" method="POST">
  <input name="to_account" value="12345">
  <input name="amount" value="1000">
  <button>Transfer</button>
</form>
```

**Secure Pattern:**
```python
# Backend: Generate CSRF token
from secrets import token_urlsafe

@app.get("/form")
def get_form(session: Session):
    csrf_token = token_urlsafe(32)
    session['csrf_token'] = csrf_token
    return {"csrf_token": csrf_token}

@app.post("/transfer")
def transfer(csrf_token: str, session: Session):
    if csrf_token != session.get('csrf_token'):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    # Process transfer
```

```html
<!-- Frontend: Include token -->
<form action="/transfer" method="POST">
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
  <input name="to_account" value="12345">
  <input name="amount" value="1000">
  <button>Transfer</button>
</form>
```

**Alternative: SameSite Cookies**
```python
response.set_cookie(
    "session",
    session_id,
    httponly=True,
    secure=True,
    samesite='Strict'  # Prevents CSRF
)
```

### XML External Entity (XXE)
**CWE-611**

**Vulnerable Pattern:**
```python
import xml.etree.ElementTree as ET
tree = ET.parse(user_uploaded_file)  # XXE vulnerable
```

**Secure Pattern:**
```python
import defusedxml.ElementTree as ET
tree = ET.parse(user_uploaded_file)  # XXE protection

# Or disable external entities
from lxml import etree
parser = etree.XMLParser(resolve_entities=False)
tree = etree.parse(user_uploaded_file, parser)
```

### Insecure Direct Object References (IDOR)
**CWE-639**

**Vulnerable Pattern:**
```javascript
// URL: /api/invoice/1234
app.get('/api/invoice/:id', (req, res) => {
  const invoice = db.invoices.find(req.params.id);
  res.json(invoice);  // No ownership check
});
```

**Secure Pattern:**
```javascript
app.get('/api/invoice/:id', authenticate, (req, res) => {
  const invoice = db.invoices.findOne({
    id: req.params.id,
    user_id: req.user.id  // Verify ownership
  });

  if (!invoice) {
    return res.status(404).json({ error: 'Not found' });
  }

  res.json(invoice);
});
```

### Path Traversal
**CWE-22**

**Vulnerable Pattern:**
```python
@app.get("/download")
def download_file(filename: str):
    return send_file(f"/var/www/uploads/{filename}")
# Payload: filename = "../../etc/passwd"
```

**Secure Pattern:**
```python
import os
from pathlib import Path

@app.get("/download")
def download_file(filename: str):
    # Validate filename
    if '..' in filename or filename.startswith('/'):
        raise HTTPException(status_code=400, detail="Invalid filename")

    # Resolve to absolute path and verify it's within allowed directory
    base_dir = Path("/var/www/uploads").resolve()
    file_path = (base_dir / filename).resolve()

    if not file_path.is_relative_to(base_dir):
        raise HTTPException(status_code=400, detail="Invalid path")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return send_file(file_path)
```

---

## Input Validation & Sanitization Standards

### Validation Hierarchy
1. **Whitelist over Blacklist:** Define allowed inputs, reject everything else
2. **Type Validation:** Enforce expected data types
3. **Length Validation:** Enforce min/max lengths
4. **Format Validation:** Use regex for patterns (email, phone, etc.)
5. **Range Validation:** Numeric bounds, date ranges
6. **Business Logic Validation:** Valid state transitions, relationship constraints

### Validation Examples

```python
from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional

class UserRegistration(BaseModel):
    username: constr(min_length=3, max_length=30, regex=r'^[a-zA-Z0-9_]+$')
    email: EmailStr
    age: int
    password: constr(min_length=12)

    @validator('age')
    def validate_age(cls, v):
        if v < 13 or v > 120:
            raise ValueError('Age must be between 13 and 120')
        return v

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v
```

### Sanitization Patterns

```python
import html
import bleach
from markupsafe import escape

# HTML context
safe_output = html.escape(user_input)
safe_output = escape(user_input)  # Jinja2/Flask

# Allow limited HTML (e.g., blog comments)
allowed_tags = ['p', 'br', 'strong', 'em', 'a']
allowed_attrs = {'a': ['href', 'title']}
clean_html = bleach.clean(user_input, tags=allowed_tags, attributes=allowed_attrs)

# URL context
from urllib.parse import quote
safe_url = quote(user_input, safe='')

# JavaScript context (avoid if possible, use JSON)
import json
safe_json = json.dumps(user_input)
```

---

## Authentication & Authorization Standards

### Session Management

**Secure Session Configuration:**
```python
app.config.update(
    SESSION_COOKIE_SECURE=True,      # HTTPS only
    SESSION_COOKIE_HTTPONLY=True,    # No JavaScript access
    SESSION_COOKIE_SAMESITE='Lax',   # CSRF protection
    PERMANENT_SESSION_LIFETIME=1800, # 30 minutes
    SESSION_REFRESH_EACH_REQUEST=True
)

# Regenerate session ID after login
@app.post("/login")
def login(credentials):
    if verify_credentials(credentials):
        session.clear()  # Clear old session
        session.regenerate()  # New session ID
        session['user_id'] = user.id
        session['login_time'] = datetime.utcnow()
```

### OAuth 2.0 Security

**Required Implementations:**
- Use state parameter (CSRF protection)
- Validate redirect_uri against whitelist
- Use PKCE for public clients
- Short-lived access tokens (15 min)
- Refresh token rotation
- Revocation endpoint

```python
import secrets

# Generate state parameter
state = secrets.token_urlsafe(32)
session['oauth_state'] = state

# Redirect to OAuth provider
auth_url = f"{provider}/authorize?client_id={client_id}&redirect_uri={redirect_uri}&state={state}&response_type=code&code_challenge={code_challenge}&code_challenge_method=S256"

# Callback validation
@app.get("/oauth/callback")
def oauth_callback(code: str, state: str):
    if state != session.get('oauth_state'):
        raise HTTPException(status_code=403, detail="Invalid state")

    # Exchange code for token
    # Validate token
    # Create session
```

### Role-Based Access Control (RBAC)

```python
from enum import Enum
from functools import wraps

class Role(Enum):
    USER = 1
    MODERATOR = 2
    ADMIN = 3

def require_role(required_role: Role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role.value < required_role.value:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.delete("/user/{user_id}")
@require_role(Role.ADMIN)
def delete_user(user_id: int):
    # Only admins can delete users
    pass
```

---

## Data Protection Requirements

### PII Handling

**Classification:**
- **Tier 1 (Highly Sensitive):** SSN, financial accounts, health records, biometrics
- **Tier 2 (Sensitive):** Full name + DOB, email + password, precise location
- **Tier 3 (Personal):** Email alone, IP address, device ID

**Requirements by Tier:**

| Tier | Encryption at Rest | Encryption in Transit | Access Logging | Retention |
|------|-------------------|----------------------|----------------|-----------|
| 1    | AES-256-GCM       | TLS 1.3             | Required       | Minimal   |
| 2    | AES-256-GCM       | TLS 1.2+            | Required       | Limited   |
| 3    | Recommended       | TLS 1.2+            | Optional       | Business need |

### Encryption Standards

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# Encrypt sensitive data
def encrypt_data(plaintext: bytes, key: bytes) -> tuple:
    aesgcm = AESGCM(key)  # 256-bit key
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce, ciphertext

def decrypt_data(nonce: bytes, ciphertext: bytes, key: bytes) -> bytes:
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)

# Key management: Use AWS KMS, Azure Key Vault, or HashiCorp Vault
# NEVER hardcode encryption keys
```

### Secure Data Deletion

```python
# Soft delete for audit trail (non-sensitive data)
user.deleted_at = datetime.utcnow()
user.is_active = False

# Hard delete for PII (right to be forgotten)
db.session.delete(user)
db.session.commit()

# Crypto-shredding: Delete encryption key
key_vault.delete_key(user.key_id)
# Encrypted data becomes unrecoverable
```

---

## CVE/CWE Reference Patterns

### Standardized Vulnerability Reporting

**Report Format:**
```
[SEVERITY] Vulnerability Type - Location
CWE-XXX | CVE-YYYY-NNNNN (if applicable)

Description: [What the vulnerability is]
Impact: [What an attacker could do]
Location: [File:Line or Component]
Evidence: [Code snippet or proof]

Remediation:
1. [Step-by-step fix]
2. [Verification method]

References:
- [OWASP link]
- [CVE link]
```

### Common CWE Mappings

| Vulnerability Type | CWE | Severity |
|-------------------|-----|----------|
| SQL Injection | CWE-89 | Critical |
| XSS | CWE-79 | High |
| CSRF | CWE-352 | Medium |
| Broken Access Control | CWE-284 | Critical |
| Hardcoded Credentials | CWE-798 | Critical |
| Path Traversal | CWE-22 | High |
| Command Injection | CWE-78 | Critical |
| XXE | CWE-611 | High |
| SSRF | CWE-918 | High |
| Insecure Deserialization | CWE-502 | Critical |
| Weak Crypto | CWE-327 | High |
| Missing Authentication | CWE-286 | Critical |
| Insufficient Logging | CWE-778 | Medium |

### Severity Rating Criteria

**Critical:**
- Remote code execution
- Authentication bypass
- Direct data exposure (unencrypted PII)
- Privilege escalation to admin

**High:**
- SQL injection without RCE
- Stored XSS
- SSRF to internal resources
- Weak encryption of sensitive data

**Medium:**
- Reflected XSS
- CSRF on state-changing operations
- Information disclosure (non-sensitive)
- Missing security headers

**Low:**
- Information disclosure (minimal impact)
- Missing best practices (minimal risk)

---

## Automated Triggers

This skill activates when agents perform:
- Security audits or assessments
- Vulnerability scanning (SAST/DAST)
- Code review with security focus
- Threat modeling exercises
- Penetration testing strategy
- Security architecture design
- Incident response investigation
- Compliance validation (SOC 2, PCI-DSS, GDPR)

---

## Integration

**Inherits:** None (foundation skill)

**Works with:**
- code-quality-standards (for secure coding patterns)
- error-handling-patterns (for security error handling)
- testing-standards (for security test cases)

**Applied by:**
- security-auditor
- static-code-scanner
- threat-modeler
- pentest-strategist
- compliance-validator
- incident-responder

**Source:** OWASP Top 10 2021, CWE Top 25, NIST Secure Software Development Framework
