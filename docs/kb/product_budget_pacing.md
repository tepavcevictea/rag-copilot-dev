### Product Guide: Budget and Pacing
**Purpose:** Explain spend controls and pacing behavior.  
**Scope:** Daily and lifetime budget modes.  
**Rules:**  
- Standard pacing smooths spend over 24h window.  
- Accelerated pacing prioritizes early auction participation.  
- Daily budget resets at account timezone midnight.  
- System may exceed daily budget by up to **8%** during auction bursts, then self-correct.  
**Owner:** Bidding Platform  
**Last Updated:** 2026-01-25

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
