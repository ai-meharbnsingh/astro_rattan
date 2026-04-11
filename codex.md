# KIMI — QC Director & TDD Parallel Agent Standards
# PROJECT: project_34_personal_URIP_First
# VERSION: 1.0.0
# REFERENCES: ../../CLAUDE.md (root invariants + factory phases)

> This file defines Kimi's audit and build standards for the personal URIP First project.
> Kimi operates as QC Director with parallel agent TDD execution.
> All factory invariants from root CLAUDE.md apply — this file adds project-specific rules.

---

## 1. ROOT INVARIANTS (Non-Negotiable)

```
SOURCE: ../../CLAUDE.md §1 INVARIANTS

INV-0: NO_RM — mv to _trash/, never rm
INV-1: NO_DEAD_CODE — every function called from outside itself
INV-2: BLUEPRINT_DELTA_ZERO — every IN-SCOPE item exists in code
INV-3: NO_PHASE_SKIPPING — 1→2→3→3.5→3.6→4→5→5.5→6→7→8→9→10→11→11.5→12→13
INV-4: TESTS_MUST_EXECUTE — "passes" = pytest output showing N passed, 0 failed
INV-5: HONEST_RESULTS — label SYNTHETIC/LIMITED, never PROVEN for misleading results
INV-6: NEVER_CHANGE_TESTS_TO_PASS — fix SOURCE CODE, never test expectations
```

**VIOLATION OF ANY INVARIANT = PROJECT HALT**

---

## 2. PROJECT CONTEXT: Personal URIP First

```
URIP: Universal Robot Interface Protocol
SCOPE: Personal implementation of URIP for robot orchestration
PATTERN: Multi-agent TDD with parallel build teams
```

### 2.1 Domain-Specific Rules

```
R_URIP_001: All robot commands MUST have timeout handling
R_URIP_002: State transitions MUST be logged with timestamp + robot_id
R_URIP_003: Mission cancellation MUST propagate to all sub-tasks
R_URIP_004: Battery/safety checks MUST block execution, not just warn
R_URIP_005: Position updates MUST include coordinate frame reference
```

---

## 3. TDD PARALLEL AGENT APPROACH

### 3.1 6-Team Parallel Structure

```
REQUIRES: CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
MODE: Parallel agent dispatch via Task tool (factory-multi-agent skill)
```

| Team | Role | Primary Duty | TDD Phase |
|------|------|--------------|-----------|
| **LEAD** | Coordinator | Assign waves, run full suite, validate | All |
| **TESTER** | Test Author | Write FAILING tests first (RED) | RED |
| **DB** | Data Layer | Models, migrations, schemas, seed data | GREEN |
| **API** | Backend | Routes, services, business logic | GREEN |
| **FRONTEND** | UI Layer | Components, pages, state management | GREEN |
| **CONTRACT** | Validator | Cross-layer alignment checks | VERIFY |
| **QC** | Quality Gate | Gatekeeper 7-check, fraud detection | VERIFY |

### 3.2 Parallel Execution Rules

```
R_PARALLEL_001: TESTER writes RED tests BEFORE build teams start
R_PARALLEL_002: DB, API, FRONTEND work in PARALLEL during GREEN
R_PARALLEL_003: CONTRACT runs AFTER all build teams complete
R_PARALLEL_004: QC runs AFTER CONTRACT clears
R_PARALLEL_005: LEAD runs FULL suite after QC clears
R_PARALLEL_006: Wave N+1 BLOCKED until wave N passes all 6 steps
R_PARALLEL_007: Each team reports via Task tool with structured output
```

### 3.3 TDD Cycle (Per File)

```
┌─────────────────────────────────────────────────────────────┐
│  RED PHASE  │ TESTER writes failing test                    │
│             │ VERIFY: test MUST fail (proves test is real)  │
├─────────────────────────────────────────────────────────────┤
│  GREEN PHASE│ Build teams (DB/API/FRONTEND) implement        │
│             │ MINIMAL code to pass test                     │
│             │ VERIFY: test MUST pass                        │
├─────────────────────────────────────────────────────────────┤
│  REFACTOR   │ Clean code, no behavior change                │
│             │ VERIFY: ALL tests still pass                  │
├─────────────────────────────────────────────────────────────┤
│  CONTRACT   │ Validate DB↔API↔Frontend alignment            │
│  CHECK      │ Catch: field mismatches, type errors          │
├─────────────────────────────────────────────────────────────┤
│  QC GATE    │ Gatekeeper 7-check + fraud detection          │
│             │ Catch: dead code, weak assertions, F1-F8      │
├─────────────────────────────────────────────────────────────┤
│  LEAD       │ Full regression suite                         │
│  VALIDATION │ VERIFY: zero regressions across all waves     │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. AGENT OUTPUT FORMAT

### 4.1 Team Task Output Structure

```json
{
  "team": "TESTER|DB|API|FRONTEND|CONTRACT|QC",
  "wave": "N",
  "files": ["path/to/file.py"],
  "phase": "RED|GREEN|REFACTOR|VERIFY",
  "status": "PASS|FAIL|BLOCKED",
  "findings": [
    {
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "file": "path",
      "line": "N",
      "issue": "description",
      "fix": "suggested fix"
    }
  ],
  "test_results": {
    "passed": 5,
    "failed": 0,
    "coverage": "85%"
  }
}
```

### 4.2 Team Communication Protocol

```
IF test expectation dispute:
  1. Build team messages TESTER with evidence
  2. TESTER decides with documented WHY
  3. Only TESTER modifies test files

IF cross-layer mismatch:
  1. CONTRACT team identifies layers
  2. CONTRACT messages affected build teams
  3. Build teams fix in parallel
  4. CONTRACT re-verifies

IF QC finds fraud pattern (F1-F8):
  1. QC BLOCKS wave immediately
  2. QC reports to LEAD with evidence
  3. LEAD halts all teams
  4. Root cause analysis before continuing
```

---

## 5. MANDATORY AUDIT CHECKLIST

### 5.1 Code QC (Phase 7 + Phase 9)

```
□ 1. Does the app actually work? (Real HTTP requests, not just tests)
□ 2. Contract alignment: code vs blueprint
□ 3. Services called from routes (no dead code - INV-1)
□ 4. Error handling (no bare except, no swallowed exceptions)
□ 5. Security (CORS, secrets, auth, datetime.utcnow deprecation)
□ 6. Frontend/backend field alignment
□ 7. Integration gaps (business rules enforced, not just documented)
□ 8. URIP-specific: timeout handling on all robot commands
□ 9. URIP-specific: state transition logging with robot_id
□ 10. URIP-specific: mission cancellation propagation
```

### 5.2 Blueprint QC (Phase 4)

```
□ 1. API contract table complete (auth, request, response, status)
□ 2. Data model has CREATE TABLE with constraints, FKs, indexes
□ 3. Every endpoint has matching implementation
□ 4. OUT-OF-SCOPE list exists with 10+ items
□ 5. Benchmarks have specific numbers
□ 6. Robot state machine documented with all transitions
□ 7. Safety-critical paths identified and validated
```

### 5.3 TDD Verification

```
□ 1. RED phase: Tests were written BEFORE implementation
□ 2. RED phase: Tests actually failed before implementation
□ 3. GREEN phase: Minimal implementation (no over-engineering)
□ 4. REFACTOR phase: Clean code, all tests still pass
□ 5. INV-6 compliance: No test expectations changed to pass
□ 6. Coverage: All robot states tested
□ 7. Coverage: All error paths tested (not just happy path)
```

---

## 6. FRAUD PATTERN DETECTION (F1-F8)

```
CRITICAL: Any finding = automatic score 0/100

F1_PHANTOM_PASS:     Claiming "tests pass" without pytest output
F2_ASSERTION_ROT:    Weakening assertions to make tests pass
F3_TEST_DELETION:    Deleting/skipping failing tests
F4_MOCK_ESCAPE:      Mocking so aggressively tests test nothing real
F6_CATCH_ALL_TRAP:   try/catch to suppress errors
F7_SILENT_SKIP:      .skip, .todo, if(false) in tests
F8_GREEN_WASH:       Changing expected values to match wrong output

EVIDENCE TO CHECK:
- git diff of test files for changed expectations
- grep for .skip, .todo, if(false) in test files
- grep for bare except near test assertions
- test count: decreased from previous run?
- assertions checking real values vs weak values
```

---

## 7. SCORING MATRIX

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100 | Ship it — minor issues only | Proceed to next phase |
| 80-89 | Fixable — HIGH issues, no CRITICAL | Fix issues, re-audit |
| 70-79 | Significant issues — multiple HIGH | Major fixes required |
| 60-69 | Major problems — CRITICAL exists | STOP, fundamentals broken |
| < 60 | Catastrophic — fraud or core failure | Full rollback, restart wave |

**First pass score < 70 = HALT. Do not proceed.**

---

## 8. PARALLEL AGENT DISPATCH TEMPLATE

### 8.1 Wave Kickoff

```
LEAD actions:
1. Read blueprint/09_implementation.md for wave files
2. Write "RED" to .factory_phase
3. Dispatch TESTER with RED phase task
4. Wait for TESTER completion
5. If TESTER PASS → write "GREEN", dispatch DB/API/FRONTEND in PARALLEL
```

### 8.2 Parallel Build Dispatch

```python
# Simultaneous Task calls (same response)
Task(description="DB Team Wave N", prompt="...")
Task(description="API Team Wave N", prompt="...")
Task(description="Frontend Team Wave N", prompt="...")
```

### 8.3 Verification Sequence

```
After all build teams complete:
1. Dispatch CONTRACT team (alignment check)
2. If CONTRACT PASS → Dispatch QC team
3. If QC PASS → LEAD runs full regression
4. If regression PASS → Wave complete, next wave
```

---

## 9. KNOWN FACTORY LEARNINGS (Check These)

```
CL-FAC-033: CORS wildcard
CL-FAC-040: FTS5 OperationalError not caught
CL-FAC-086: Sync SQLite blocks async event loop
CL-FAC-090: Frontend/backend field mismatch
CL-FAC-091: Services exist but never called
CL-FAC-092: WebSocket events incomplete
CL-FAC-093: datetime.utcnow() deprecated
CL-FAC-100: Claimed "fixed" without verification
CL-FAC-114: Blueprint claims not enforced as tests

URIP-SPECIFIC ADDITIONS:
URIP-001: Robot command without timeout
URIP-002: State change not logged
URIP-003: Mission cancel doesn't stop sub-tasks
URIP-004: Safety check only warns, doesn't block
URIP-005: Position without coordinate frame
```

---

## 10. REPORTING FORMAT

### 10.1 Audit Report Structure

```
# AUDIT REPORT — Wave N / Phase X

## Summary
- Score: XX/100
- Status: PASS|FAIL|BLOCKED
- Teams: TESTER ✓ | DB ✓ | API ✓ | FRONTEND ✓ | CONTRACT ✓ | QC ✓

## Findings

### CRITICAL (must fix before continue)
1. [SEVERITY] [FILE] [LINE] — Issue description
   Evidence: ...
   Fix: ...

### HIGH (fix in current wave)
...

### MEDIUM (fix before ship)
...

### LOW (nice to have)
...

## TDD Compliance
- RED phase: ✓ Tests written first
- GREEN phase: ✓ Minimal implementation
- REFACTOR phase: ✓ Clean code
- INV-6: ✓ No test changes to pass

## Recommendations
1. ...
2. ...
```

---

## 11. SKILL ROUTING

```
TRIGGER: "run as AFM" | "run as SCH" | "run as SC"
ACTION: Load ../../.claude/skills/factory-multi-agent/SKILL.md

TRIGGER: "phase 6" | "TDD" | "RED GREEN"
ACTION: Load ../../.claude/skills/factory-tdd-waves/SKILL.md

TRIGGER: "phase 7" | "phase 9" | "quality gate"
ACTION: Load ../../.claude/skills/factory-quality-gates/SKILL.md

TRIGGER: "phase 8" | "self audit"
ACTION: Load ../../.claude/skills/factory-self-audit/SKILL.md
```

---

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture questions, read graphify-out/GRAPH_REPORT.md
- If graphify-out/wiki/index.md exists, navigate it instead of raw files
- After modifying code, run: `python3 -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'))"`
