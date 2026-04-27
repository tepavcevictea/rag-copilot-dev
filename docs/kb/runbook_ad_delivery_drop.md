### Ad Delivery Drop Runbook
**Purpose:** Diagnose sudden campaign impression decline.  
**Scope:** Active campaigns with >40% drop in hourly impressions.  
**Procedure:**  
- Check targeting expansion toggles and budget pacing mode.  
- Confirm no recent policy enforcement actions.  
- Compare exchange partner fill rates for same period.  
- If exchange outage, apply traffic reroute profile `fallback_v2`.  
**Escalation:** If unresolved after **20 minutes**, escalate to exchange integration on-call.  
**Owner:** Ad Delivery Team  
**Last Updated:** 2026-03-02

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
