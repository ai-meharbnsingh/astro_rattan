# 10 — Benchmarks

## Performance
| Metric | Target | Measurement | Test Scenario | Breaks At |
|--------|--------|-------------|---------------|-----------|
| Kundli generation (p95) | < 2s | Timing middleware | Single chart, 9 planets | N/A (computation-bound) |
| Panchang calculation (p95) | < 500ms | Timing middleware | Single date/location | N/A |
| AI response (p95) | < 10s | Timing middleware | Single question + kundli context | OpenAI rate limit |
| API response (non-AI, p95) | < 200ms | Timing middleware | 50 concurrent requests | 200 concurrent |
| Product catalog (p95) | < 100ms | Timing middleware | 100 products, paginated | 10K products |
| WebSocket latency | < 100ms | Client timestamp diff | Chat message round-trip | 50 concurrent sessions |
| Database query (p95) | < 50ms | EXPLAIN timing | Most complex join | 100K rows per table |
| io-gita atom vector build | < 1s | Python timeit | 16 atoms, D=10000 | N/A (deterministic) |
| Panchang cached response | < 5ms | Timing middleware | Repeat query same date/location (vs 200ms uncached) | N/A |
| Order confirmation email | < 5s | End-to-end timing | Single order placed with email notification | Email provider rate limit |

## Scalability Ceilings
| Component | Handles | Breaks At | Bottleneck | Upgrade Path | Fix Cost |
|-----------|---------|-----------|-----------|--------------|----------|
| SQLite WAL | 100 concurrent reads | 10 concurrent writes | Single-writer lock | PostgreSQL migration | Medium |
| Swiss Ephemeris | Unlimited calculations | Ephemeris file range (~6000 years) | Data file limits | Extended ephemeris | Low |
| OpenAI API | 3500 RPM (gpt-4) | Rate limit | API quota | Increase tier or cache | Low |
| io-gita engine | D=10000 in ~0.5s | Memory at D>100000 | numpy array allocation | Reduce D or chunk | Low |
| File uploads (products) | Local disk | Disk space | Storage | S3/Cloudinary | Medium |
| WebSocket | 100 concurrent | 500+ concurrent | Python async limits | Redis pub/sub | Medium |

## Cost Budget
| Service | Monthly Est. | Alert At | Hard Limit |
|---------|-------------|----------|------------|
| OpenAI API (GPT-4) | $50-200 | $150 | $300 |
| Hosting (VPS/Cloud) | $20-50 | $40 | $100 |
| Razorpay fees | 2% of transactions | N/A | N/A |
| Stripe fees | 2.9% + $0.30 per tx | N/A | N/A |
| Domain + SSL | $15/year | N/A | N/A |

## Project Metrics (v2.0)
| Metric | Value |
|--------|-------|
| app/ source files | 45 |
| Total API routes | 88 |
| Test count target | 300+ |
| IN-SCOPE features | 36 (6 waves) |

## Quality Gates
| Gate | Target | Tool | Frequency |
|------|--------|------|-----------|
| Test Coverage | > 80% | pytest --cov | Every wave |
| API Contract Match | 100% | Contract tests | Every wave |
| Security Audit | 0 CRITICAL | Gemini sec_gate | Phase 7, 9 |
| Blueprint Delta | 0 missing features | Blueprint diff | Phase 7 |
| Dead Code | 0 unused public functions | grep check | Phase 6, 8 |
| Response Format | 100% match | Pydantic validation | Every route |
