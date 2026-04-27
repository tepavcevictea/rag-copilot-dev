### PII Handling Policy
**Purpose:** Protect personally identifiable information.  
**Scope:** Support workflows, exports, dashboards, logs.  
**Rules:**  
- Do not store raw IDs in general-purpose logs.  
- Mask emails in support screenshots before external sharing.  
- Access to full PII requires role `compliance_sensitive_read`.  
- Any accidental exposure must be reported within **1 hour**.  
**Exceptions:** Incident response can grant temporary emergency access with approval trail.  
**Owner:** Security Operations  
**Last Updated:** 2026-03-18

**Definitions:**
- **Request Window:** Time from invoice issuance during which a dispute/refund can be submitted.
- **Qualified Case:** Case type that satisfies policy and evidence requirements.

**Inputs Required:**
- Account ID and invoice reference
- Campaign IDs and date range
- Evidence artifacts (screenshots, logs, billing export)

**Operational Notes:**
- Support must not promise outcomes before Finance review.
- Any policy override requires documented approver and rationale.

**Audit and Controls:**
- Store all approval/denial decisions in ticket history.
- Monthly spot-check 5% of policy decisions for consistency.

**Related Documents:**
- `support_billing_disputes_macro.md`
- `security_access_control_matrix.md`

---
