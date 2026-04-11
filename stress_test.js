/**
 * k6 Stress Test — astrorattan.com
 * Simulates 100 concurrent users across 3 endpoint categories:
 *   1. Static frontend   (60% traffic)
 *   2. /health           (15% traffic)
 *   3. /api/panchang     (25% traffic) — DB + ephemeris computation
 *
 * Run: k6 run stress_test.js
 */
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// ── Custom metrics ────────────────────────────────────────────────
const errorRate    = new Rate('error_rate');
const p99Latency   = new Trend('p99_latency', true);
const failedReqs   = new Counter('failed_requests');
const timeoutReqs  = new Counter('timeout_requests');

// ── Test scenario: ramp to 100 VUs, hold 60s, ramp down ──────────
export const options = {
  stages: [
    { duration: '20s', target: 20  },   // warm up
    { duration: '30s', target: 100 },   // ramp to 100 users
    { duration: '60s', target: 100 },   // hold peak load
    { duration: '20s', target: 0   },   // ramp down
  ],
  thresholds: {
    http_req_failed:   ['rate<0.05'],    // <5% errors
    http_req_duration: ['p(95)<3000'],   // 95% of requests under 3s
    error_rate:        ['rate<0.05'],
  },
  summaryTrendStats: ['min', 'med', 'avg', 'p(90)', 'p(95)', 'p(99)', 'max'],
};

const BASE = 'https://astrorattan.com';

// Typical panchang params (Delhi)
const PANCHANG_URL = `${BASE}/api/panchang?lat=28.6139&lon=77.2090&date=2026-04-11`;

export default function () {
  const roll = Math.random();

  if (roll < 0.60) {
    // ── Scenario 1: Frontend static page ─────────────────────────
    const res = http.get(BASE + '/', { timeout: '10s' });
    const ok = check(res, {
      'frontend 200': (r) => r.status === 200,
      'frontend <2s':  (r) => r.timings.duration < 2000,
    });
    errorRate.add(!ok);
    if (!ok) {
      failedReqs.add(1);
      if (res.status === 0) timeoutReqs.add(1);
    }
    p99Latency.add(res.timings.duration);

  } else if (roll < 0.75) {
    // ── Scenario 2: Health check (lightweight, no DB) ─────────────
    const res = http.get(BASE + '/health', { timeout: '5s' });
    const ok = check(res, {
      'health 200':   (r) => r.status === 200,
      'health <500ms': (r) => r.timings.duration < 500,
      'db connected': (r) => {
        try { return JSON.parse(r.body).database === 'connected'; } catch { return false; }
      },
    });
    errorRate.add(!ok);
    if (!ok) failedReqs.add(1);
    p99Latency.add(res.timings.duration);

  } else {
    // ── Scenario 3: Panchang API (DB + Swiss Ephemeris math) ──────
    const res = http.get(PANCHANG_URL, { timeout: '15s' });
    const ok = check(res, {
      'panchang 200':  (r) => r.status === 200,
      'panchang <5s':  (r) => r.timings.duration < 5000,
      'has tithi':     (r) => {
        try { const b = JSON.parse(r.body); return !!b.tithi || !!b.data?.tithi; } catch { return false; }
      },
    });
    errorRate.add(!ok);
    if (!ok) {
      failedReqs.add(1);
      if (res.status === 0) timeoutReqs.add(1);
    }
    p99Latency.add(res.timings.duration);
  }

  // Realistic think time: 0.5–2s between requests per user
  sleep(0.5 + Math.random() * 1.5);
}
