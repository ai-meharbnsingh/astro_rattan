# 05 — Security

## Authentication
- **Method:** JWT HS256
- **Token lifetime:** 24 hours
- **Password hashing:** bcrypt (12 rounds)
- **Token storage:** Frontend localStorage (SPA)

## Authorization (RBAC)
| Role | Access |
|------|--------|
| user | Own kundlis, cart, orders, consultations, AI chat, library, prashnavali |
| astrologer | All user + own dashboard, consultation management, availability toggle |
| admin | All + user management, order management, content CMS, astrologer approval, AI logs |

## Threat Model
| Threat | Mitigation |
|--------|------------|
| SQL Injection | Parameterized queries (? placeholders), Pydantic validation |
| XSS | React auto-escapes, no dangerouslySetInnerHTML for user input |
| CSRF | JWT in headers (not cookies), SameSite policy |
| Brute force login | Rate limiting (5 attempts/minute per IP) |
| Payment tampering | Server-side price calculation, webhook signature verification |
| Unauthorized access | JWT middleware on protected routes, role checks |
| CORS abuse | Whitelist frontend origin only |
| OpenAI API key leak | Server-side only, never sent to frontend |
| Razorpay/Stripe secrets | Server-side only, webhook signature verification |

## Rate Limiting
- **Middleware:** slowapi (FastAPI-compatible rate limiting)
- **Global limit:** 60 requests/minute per IP
- **Login endpoint:** 5 attempts/minute per IP (brute force protection)
- **AI endpoints:** 10 requests/minute per user (cost protection)
- **Registration:** 3 attempts/minute per IP (spam protection)
- **Response on limit:** 429 Too Many Requests with `Retry-After` header

## Input Sanitization
- **Library:** bleach (HTML sanitization for all user text inputs)
- **Sanitized fields:** name, phone, city, question text, consultation notes, review text, content submissions
- **Strategy:** Strip all HTML tags, allow no markup in user inputs
- **Applied at:** Pydantic validator level (before DB write)

## Account Deactivation
- **Flag:** `is_active` column on users table (INTEGER, default 1)
- **Login check:** Auth middleware rejects deactivated users with 403 "Account deactivated"
- **Admin deactivation:** `PATCH /api/admin/users/{id}/deactivate` sets `is_active=0`
- **Admin activation:** `PATCH /api/admin/users/{id}/activate` sets `is_active=1`
- **Self-deactivation guard:** Admin cannot deactivate their own account (400 error)
- **Cascading:** Deactivated users' active consultations are cancelled, cart is preserved

## Password Change
- **Endpoint:** `POST /api/auth/change-password`
- **Flow:** Verify current password (bcrypt compare) → Validate new password strength → Hash new password → Update DB
- **Validation:** New password must be >= 8 characters, different from current
- **Response:** 200 on success, 400 if current password wrong, 422 if new password invalid

## Payment Security
- **Razorpay:** Verify webhook signature using `razorpay_signature` header
- **Stripe:** Verify webhook using `stripe.webhooks.constructEvent()`
- **Price:** Always calculated server-side from product DB, never trusted from client
- **Idempotency:** Payment webhook handlers are idempotent (check payment_status before updating)
