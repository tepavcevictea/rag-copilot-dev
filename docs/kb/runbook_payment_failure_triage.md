### Payment Failure Triage
**Purpose:** Resolve failed deposits and billing retries.  
**Scope:** Card, wire, and crypto top-ups.  
**Procedure:**  
- Verify provider status and error code family.  
- If `3DS_AUTH_REQUIRED`, trigger re-auth flow in customer portal.  
- If `RISK_DECLINE`, route case to Fraud Ops queue.  
- For duplicate holds, advise release window of **3-7 business days**.  
**SLA:** First response under **30 minutes** for enterprise accounts.  
**Owner:** Billing Platform  
**Last Updated:** 2026-02-22

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
