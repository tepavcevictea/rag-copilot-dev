### Product Guide: Conversion Tracking
**Purpose:** Configure pixel and server-side conversion events.  
**Scope:** Attribution setup and diagnostics.  
**Rules:**  
- Default attribution window: **7-day click, 1-day view**.  
- Dedup key required when using pixel + server events simultaneously.  
- Invalid timestamp skew beyond 5 minutes is dropped from real-time reporting.  
**Owner:** Measurement Team  
**Last Updated:** 2026-02-28

**Primary Users:**
- Self-serve advertisers, managed service teams, and support agents.

**Configuration Constraints:**
- Validate required fields before save/publish.
- Reject invalid combinations with user-readable reasons.

**Failure Modes to Watch:**
- Silent default values creating unexpected behavior.
- Misaligned timezone assumptions in scheduling/budget resets.

**Telemetry to Track:**
- Feature adoption rate
- Error frequency by configuration field
- Support tickets per feature area

**Related Documents:**
- `faq_data_export.md`
- `support_campaign_rejection_macro.md`

---
