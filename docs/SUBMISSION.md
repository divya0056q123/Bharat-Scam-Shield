# Submission write-up (copy into the form)

## Problem
First-time and retail investors in India are flooded with WhatsApp, Telegram, SMS, and social-media messages promising quick profit, guaranteed returns, or VIP access to investment groups. Many users are not trained to verify these claims and often act under urgency, pressure, or fear of missing out.

## Solution
Bharat Scan Shield helps retail investors pause, check, and understand suspicious financial content before they trust it. It is an educational investor-awareness tool for Indian users. A user can paste a message, speak it aloud, or upload a screenshot. The system highlights suspicious phrases, explains the warning signs in simple Hindi or English, and suggests safe next steps such as checking official SEBI sources, contacting trusted family members, and reporting fraud through 1930 or cybercrime.gov.in. Not financial advice; users should verify independently.

## Technology
Two-page HTML/CSS/JS interface (welcome and scanner, designed for low bandwidth) -> FastAPI backend -> transparent rule engine (guaranteed returns, unrealistic returns, urgency, payment/OTP requests, group invites, solicitation, authority claims, crypto/app pitches, suspicious links) -> optional LLM that only rewrites the explanation in plain words. OCR: Tesseract.js (English+Hindi) in the browser. Voice: Web Speech API. Third-party: Tesseract.js, Google Fonts, optional Anthropic API.

## Why it is trustworthy
Explainable (shows matched phrases), uncertainty-aware wording, messages are not stored by the app, screenshot files never leave the device, and scans are not financial advice. When optional AI explanations are enabled, message text is sent to Anthropic; the demo discloses this. The tool never asks for OTP/PIN, gives stock tips or predictions, or promotes brokers.

## Impact and scalability
Works for the many people who forward "tips" in family groups. Add Tamil, Bengali, Marathi, Telugu by translating the signal dictionary (rules are language-keyed). A WhatsApp bot or SMS-style interface can reuse the same API. Rules can be updated from SEBI/NSDL scam advisories. Public-good, no revenue from users.

## Limits (say this honestly)
Rule-based detection can miss new scam wording and can flag genuine messages. Current automated tests use synthetic regression cases; they are not a real-world accuracy benchmark. The tool supports a user's own checking and is not proof.

## Demo video (4 min)
0:00 problem (show sample scam) | 0:30 introduce tool | 0:45 paste sample, show result | 1:45 Hindi toggle + voice | 2:30 screenshot upload | 3:00 architecture | 3:30 privacy/guardrails and limits | 3:50 scaling.

## 8 slides
1 Title+tagline | 2 Problem | 3 Target users | 4 Solution flow | 5 Architecture | 6 Live demo | 7 Safety, privacy, guardrails | 8 Impact and scale.

## Final checklist
[ ] Runs locally and deployed link works  [ ] 3 samples tested in both languages  [ ] Demo video 3-5 min  [ ] Slides  [ ] GitHub repo public  [ ] Disclose Tesseract.js and any LLM API used  [ ] Only synthetic messages in demo
