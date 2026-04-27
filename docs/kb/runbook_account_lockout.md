### Account Lockout Runbook
**Purpose:** Recover legitimate users locked by risk controls.  
**Scope:** Login failures, suspicious session flags, MFA resets.  
**Procedure:**  
- Validate ownership via security challenge packet.  
- Force session revocation and password reset.  
- Re-enable account with `temp_high_monitoring` for 72 hours.  
- If repeated lockouts in 24 hours, escalate to Threat Detection.  
**Owner:** Identity Team  
**Last Updated:** 2026-02-09

**Trigger Conditions:**
- Alert breach, user report, or KPI degradation crossing threshold.

**Roles and Responsibilities:**
- **Primary On-call:** Owns triage and first mitigation.
- **Incident Commander:** Owns coordination and updates.
- **Comms Owner:** Publishes internal/external status messages.

**Decision Points:**
- If customer impact is broad, escalate incident severity.
- If root cause is uncertain, prioritize containment before optimization.

**Verification Checklist:**
- Metrics recovering toward baseline
- Error rate within normal operating range
- Backlog/retry queues drained

**Post-Incident Requirements:**
- Postmortem draft within 48 hours
- At least one prevention action item with owner and deadline

---
