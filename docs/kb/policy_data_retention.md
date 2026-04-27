### Data Retention Policy
**Purpose:** Define retention windows for operational and analytics data.  
**Scope:** Logs, support records, campaign metadata, billing docs.  
**Rules:**  
- Request logs retained for **90 days** in hot storage.  
- Billing records retained **7 years**.  
- Support tickets retained **24 months** unless legal hold is active.  
- User deletion requests must be executed within **30 days** where legally allowed.  
**Exceptions:** Security incidents can trigger temporary retention extension.  
**Owner:** Security and Legal  
**Last Updated:** 2026-02-01

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
