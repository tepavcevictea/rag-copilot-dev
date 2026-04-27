### Product Guide: Creative Specifications
**Purpose:** Define accepted file formats and limits.  
**Scope:** Banner, native, and video creatives.  
**Specs:**  
- Banner max size: 250 KB (gzip not counted).  
- Video formats: MP4/H.264 up to 30 seconds for standard placements.  
- Native title max 80 chars, description max 140 chars.  
- Landing page must load in < 4 seconds on 4G benchmark.  
**Owner:** Creative QA  
**Last Updated:** 2026-03-07

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
