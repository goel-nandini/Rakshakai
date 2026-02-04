# RakshakAI – Product Requirements Document (PRD)

## 1. Product Overview

**Product Name:** RakshakAI
**Type:** Agentic Honeypot for Scam Detection & Intelligence Extraction
**Version:** v1.0 (Hackathon Scope)

RakshakAI is an AI-powered agentic honeypot system designed to detect scam intent, autonomously engage scammers in multi-turn conversations, extract actionable intelligence, and report consolidated results to the evaluation platform without revealing detection.

---

## 2. Problem Statement

Online scams such as bank fraud, UPI scams, phishing, fake government calls, and impersonation are increasingly adaptive. Scammers dynamically modify their tactics based on victim responses, rendering traditional static detection systems ineffective.

The challenge is to build an **Agentic Honey-Pot** that can:

* Detect scam intent
* Engage scammers autonomously
* Extract intelligence covertly
* Report results in a structured and evaluable format

---

## 3. Objectives

RakshakAI must:

1. Detect scam or fraudulent messages
2. Activate an autonomous AI agent
3. Maintain a believable human-like persona
4. Handle multi-turn conversations
5. Extract scam-related intelligence
6. Return structured API responses
7. Secure access using API key authentication
8. Send a mandatory final result callback

---

## 4. High-Level Architecture

## 4.1 AI / Reasoning Architecture

RakshakAI uses a **single Large Language Model (LLM)** as its core reasoning engine to support scam detection, agentic conversation, and adaptive response generation.

The system follows a **prompt-driven reasoning approach**, where carefully designed prompts guide the LLM’s behavior for:

* Human-like conversational replies
* Context-aware follow-up questions
* Adaptive engagement strategies based on scam type and extracted intelligence

RakshakAI **does not rely on graph-based orchestration frameworks (such as LangGraph)**. Instead, all agent lifecycle steps are coordinated using **deterministic orchestration in backend code**.

In this design:

* The LLM acts purely as a **reasoning and language generation component**
* All control flow decisions (scam detection, authority validation, continuation, termination, and callback triggering) are handled explicitly in application logic

This approach ensures:

* Predictable and debuggable behavior
* Low latency and reduced operational overhead
* Clear lifecycle control required for evaluation and scoring
* Safe, auditable multi-turn interactions

```
┌──────────────┐
│ GUVI Platform│
│ (Scam Input) │
└──────┬───────┘
       ↓
┌──────────────────────────┐
│ RakshakAI Public API     │
│ POST /honeypot/message  │
└──────┬──────────────────┘
       ↓
┌──────────────────────────┐
│ Phase 1: Detection       │
│ - Scam Classification   │
│ - Rule Validation       │
│ - Confidence Scoring    │
└──────┬──────────────────┘
       ↓
┌──────────────────────────┐
│ Phase 2: Agentic Flow    │
│ - Persona Response      │
│ - Multi-turn Memory     │
│ - Intelligence Capture  │
└──────┬──────────────────┘
       ↓
┌──────────────────────────┐
│ Phase 3: Final Callback  │
│ - Aggregate Intelligence│
│ - Send to GUVI          │
└──────────────────────────┘
```

---

## 5. Phase 1 – Scam Detection & Trigger Decision

### Purpose

Determine whether an incoming message is a scam, classify its type, and decide whether to activate honeypot engagement.

### Inputs

```json
{
  "sessionId": "string",
  "message": {
    "sender": "scammer",
    "text": "string",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

### Scam Categories Supported

* Bank / KYC / OTP Scam
* Fake Government / Police Scam
* UPI Refund / Collect Scam
* Job / Internship Scam
* Investment / Crypto Scam
* Phishing Link Scam
* Delivery / Courier Scam
* Romance Scam
* Lottery / Prize Scam
* Remote Access Scam
* Fake Customer Care Scam
* Missed Call Scam
* Fake Course / Certificate Scam

### Detection Mechanism

* Keyword and intent analysis
* Scam pattern templates
* Claim extraction (bank, authority, payment requests)
* Bank / Government rule validation
* Scam confidence scoring

### Bank & Government Rules Validation

Static rule registry representing official behaviors.

```python
BANK_RULES = {
  "SBI": {
    "never_asks": ["OTP", "PIN", "CVV"],
    "never_requests": ["UPI collect", "remote access"]
  }
}

GOVT_RULES = {
  "POLICE": {
    "never": ["arrest threats on call", "UPI fine payment"]
  }
}
```

If scammer claims violate these rules, scam confidence is increased.

### Outputs (Internal)

```json
{
  "scamDetected": true,
  "scamType": "Bank / KYC Scam",
  "scamScore": 85
}
```

---

## 6. Phase 1.5 – Authority Intelligence Fetch (Real-Time Bank/Government Context)

### Purpose

Enhance scam detection and agentic engagement by dynamically fetching and validating **real-time authoritative information** about banks and government bodies when scammers impersonate them.

This phase bridges static rule-based detection and fully agentic behavior by grounding the agent’s decisions in **live, publicly verifiable reference data**.

---

### Scope & Constraints

**In Scope (Allowed):**

* Fetching public-facing bank/government metadata
* Validating official domains and communication channels
* Referencing known fraud-prevention rules published by authorities
* Cached, periodically refreshed data

**Out of Scope (Explicitly Not Done):**

* Accessing internal bank systems or customer data
* Real-time account verification
* Impersonating banks or government bodies
* Legal or enforcement actions

---

### Authority Identification

From scammer messages, RakshakAI extracts claims of authority impersonation:

```json
{
  "claimedAuthority": "SBI | HDFC | RBI | POLICE | NONE"
}
```

This extraction uses lightweight keyword and entity matching.

---

### Authority Profile Model

Each authority is represented internally using a dynamic profile:

```python
AuthorityProfile {
  name: string
  type: "BANK" | "GOVT"
  official_domains: [string]
  official_channels: ["SMS" | "EMAIL" | "APP" | "NOTICE"]
  never_asks: [string]
  never_requests: [string]
  last_refreshed: timestamp
}
```

---

### Real-Time Data Fetching Strategy

RakshakAI maintains a **hybrid live-cache model**:

1. Seed authority profiles are bootstrapped from verified sources
2. Profiles are cached in-memory with TTL (6–24 hours)
3. On detection of authority impersonation:

   * Cache is checked
   * If stale or missing, a refresh is triggered

Sources include:

* Official bank websites (fraud awareness pages)
* RBI public advisories
* Government cyber safety portals

---

### Rule Validation Engine (Dynamic)

Scammer claims are validated against the fetched authority profile:

```python
if "OTP" in scammer_request and "OTP" in profile.never_asks:
    scam_score += 30

if "UPI" in scammer_request and "UPI collect" in profile.never_requests:
    scam_score += 25
```

Violations:

* Increase scam confidence
* Lock scam category
* Influence agent questioning strategy

---

### Integration with Agentic Flow

This phase **does not speak to the scammer directly**.

Instead, it informs Phase 2 by providing contextual constraints:

* What the authority would *never* ask
* What channels are legitimate
* What procedural inconsistencies to probe

---

### Updated Flow Integration

```
PHASE 1: Scam Detection
      ↓
PHASE 1.5: Authority Intelligence Fetch
      ↓
Rule Violation Validation
      ↓
PHASE 2: Agentic Honeypot Engagement
```

---

## 7. Phase 2 – Agentic Honeypot Engagement

### Purpose

Engage scammers autonomously using a believable human persona while extracting intelligence over multi-turn conversations.

### Agent Persona

* Confused but cooperative
* Non-technical
* Slightly anxious
* Never accusatory
* Never reveals detection

### Agentic Flow

```
Scammer Message
      ↓
Load Session Context
      ↓
Persona-Guided Prompt
      ↓
Adaptive Reply Generation
      ↓
Reply Sent
```

### Session Memory Model

```python
Session {
  sessionId: string
  messages: [Message]
  scamDetected: bool
  scamType: string
  scamScore: int
  intel: Intelligence
  intelYield: int
  totalMessages: int
  closed: bool
}
```

### Message Object

```json
{
  "sender": "scammer | user",
  "text": "string",
  "timestamp": 1770005528731
}
```

### Intelligence Object

```json
{
  "upiIds": [],
  "phoneNumbers": [],
  "phishingLinks": [],
  "bankAccounts": [],
  "suspiciousKeywords": []
}
```

### Intelligence Extraction

* Regex-based extraction (UPI IDs, phone numbers, URLs)
* Pattern heuristics
* Optional LLM-assisted parsing

### Intelligence Yield Scoring

Used to determine continuation vs termination.

* Initial yield: 100
* No new intel: -10
* Repetition: -20
* High-value intel found: +40

---

## 7. Phase 3 – Final Intelligence Handover

### Purpose

Send consolidated scam intelligence to the GUVI evaluation endpoint.

### Termination Conditions

Trigger Phase 3 when:

* Scam is confirmed AND
* High-value intelligence is extracted OR
* Intelligence yield is exhausted

### Mandatory Callback Endpoint

```
POST https://hackathon.guvi.in/api/updateHoneyPotFinalResult
```

### Callback Payload

```json
{
  "sessionId": "abc123",
  "scamDetected": true,
  "totalMessagesExchanged": 18,
  "extractedIntelligence": {
    "bankAccounts": [],
    "upiIds": ["fraud@upi"],
    "phishingLinks": [],
    "phoneNumbers": [],
    "suspiciousKeywords": ["urgent", "verify"]
  },
  "agentNotes": "Impersonated bank, used urgency and UPI redirection"
}
```

### Callback Rules

* Called exactly once per session
* Only after engagement completion
* Mandatory for evaluation

---

## 8. Data Flow Diagram

```
Incoming Request
      ↓
Validate API Key
      ↓
Load/Create Session
      ↓
Phase 1: Scam Detection
      ↓
Is Scam?
  ┌───────────┬───────────┐
  │ Yes       │ No        │
  ↓           ↓           ↓
Phase 2       Normal Reply
Agentic Flow
      ↓
Extract Intelligence
      ↓
Check Termination
  ┌───────────┬───────────┐
  │ Yes       │ No        │
  ↓           ↓           ↓
Phase 3       Continue Loop
Callback
```

---

## 9. Public API Specification

### Endpoint

```
POST /honeypot/message
```

### Headers

```
x-api-key: YOUR_SECRET_API_KEY
Content-Type: application/json
```

### Response

```json
{
  "status": "success",
  "reply": "Why will my account be blocked?"
}
```

---

## 10. Non-Functional Requirements

* Stateless public API
* Internal stateful session memory
* Sub-second response time
* Ethical compliance (no impersonation, no harassment)
* Secure API key validation

---

## 11. Out of Scope

* Real user alerts
* Blocking or reporting to law enforcement
* Real bank or government API integrations
* Voice/audio analysis
* Persistent databases (hackathon scope)

---

## 12. One-Line Summary

RakshakAI is an AI-powered agentic honeypot that detects scam intent, autonomously engages scammers using a human-like persona, extracts actionable intelligence through multi-turn conversations, and reports consolidated scam data via a mandatory evaluation callback.
