### Reporting Delay Runbook
**Purpose:** Handle delayed metrics in advertiser dashboard.  
**Scope:** Click, impression, conversion reporting pipelines.  
**Procedure:**  
- Validate ingestion lag in stream consumer dashboard.  
- If lag > 12 minutes, trigger `replay_window_15m`.  
- Notify support macro `reporting_delay_notice_v3`.  
- Mark dashboard banner if delay exceeds **30 minutes**.  
**Resolution target:** Under **60 minutes** for P2 incidents.  
**Owner:** Data Platform  
**Last Updated:** 2026-01-19

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
