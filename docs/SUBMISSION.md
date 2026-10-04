# Submission write-up (copy into the form)

## Problem
First-time, elderly and regional-language investors get WhatsApp/Telegram/SMS "guaranteed return" offers and cannot tell what is risky. English-heavy tools and complex jargon leave them alone at the moment they most need help.

## Solution
Bharat Scan Shield lets a user paste, speak or screenshot a suspicious message. It shows a cautious risk level (never "100% scam"), the exact phrases that triggered each warning, a simple explanation in Hindi or English, and safe verification steps (SEBI registered-intermediary list, 1930, cybercrime.gov.in, SEBI SCORES).

## Technology
React-free single-page front end (HTML/CSS/JS, loads fast on low bandwidth) -> FastAPI backend -> transparent rule engine (guaranteed returns, unrealistic returns, urgency, payment/OTP requests, group invites, solicitation, authority claims, crypto/app pitches, suspicious links) -> optional LLM that only rewrites the explanation in plain words. OCR: Tesseract.js (English+Hindi) in the browser. Voice: Web Speech API. Third-party: Tesseract.js, Google Fonts, optional Anthropic API.

## Why it is trustworthy
Explainable (shows matched phrases), uncertainty-aware wording, no storage of messages, screenshots never uploaded, never asks for OTP/PIN, no stock tips, predictions, brokers or monetisation.

## Impact and scalability
Works for the many people who forward "tips" in family groups. Add Tamil, Bengali, Marathi, Telugu by translating the signal dictionary (rules are language-keyed). A WhatsApp bot or SMS-style interface can reuse the same API. Rules can be updated from SEBI/NSDL scam advisories. Public-good, no revenue from users.

## Limits (say this honestly)
Rule-based detection can miss new scam wording and can flag genuine messages. It supports a user's own checking and is not proof.

## Demo video (4 min)
0:00 problem (show sample scam) | 0:30 introduce tool | 0:45 paste sample, show result | 1:45 Hindi toggle + voice | 2:30 screenshot upload | 3:00 architecture | 3:30 privacy/guardrails and limits | 3:50 scaling.

## 8 slides
1 Title+tagline | 2 Problem | 3 Target users | 4 Solution flow | 5 Architecture | 6 Live demo | 7 Safety, privacy, guardrails | 8 Impact and scale.

## Final checklist
[ ] Runs locally and deployed link works  [ ] 3 samples tested in both languages  [ ] Demo video 3-5 min  [ ] Slides  [ ] GitHub repo public  [ ] Disclose Tesseract.js and any LLM API used  [ ] Only synthetic messages in demo
