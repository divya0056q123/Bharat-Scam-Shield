import os
from pathlib import Path
from typing import Literal
import httpx
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from .rules import analyze

app = FastAPI(title="Bharat Scan Shield")  # no DB, message text is never logged or stored
FRONT = Path(__file__).resolve().parent.parent / "frontend"

class Req(BaseModel):
    text: str = Field(min_length=3, max_length=4000)
    lang: Literal["en", "hi"] = "en"

LABEL = {
 "en": {"high": "Several warning signs", "medium": "Potentially suspicious", "low": "No common warning signs found"},
 "hi": {"high": "कई चेतावनी संकेत", "medium": "संभावित रूप से संदिग्ध", "low": "आम चेतावनी संकेत नहीं मिले"},
}
SUMMARY = {
 "en": {"high": "This message shows several warning signs often seen in investment scams. We cannot be certain, so please verify it independently before sending money or details.",
        "medium": "This message has some warning signs. Please verify the sender and the claims independently before acting.",
        "low": "We did not find common warning signs, but this does not mean the message is safe. Always verify who is contacting you."},
 "hi": {"high": "इस संदेश में निवेश धोखाधड़ी में दिखने वाले कई संकेत हैं। हम पक्का नहीं कह सकते, इसलिए पैसे या जानकारी भेजने से पहले खुद जाँच करें।",
        "medium": "इस संदेश में कुछ चेतावनी संकेत हैं। कोई भी कदम उठाने से पहले भेजने वाले और दावों की स्वयं जाँच करें।",
        "low": "हमें आम चेतावनी संकेत नहीं मिले, पर इसका मतलब यह नहीं कि संदेश सुरक्षित है। संपर्क करने वाले की हमेशा जाँच करें।"},
}
STEPS = {
 "en": ["Do not send money, OTP, PIN or password.", "Check the sender in SEBI's official registered-intermediary list (sebi.gov.in).",
        "Do not click links. Open official websites yourself.", "Ask a family member before acting.",
        "If you lost money or suspect fraud: call 1930 or report at cybercrime.gov.in.", "For complaints about a registered entity: SEBI SCORES (scores.sebi.gov.in)."],
 "hi": ["पैसे, OTP, PIN या पासवर्ड न भेजें।", "भेजने वाले को सेबी की आधिकारिक पंजीकृत मध्यस्थ सूची (sebi.gov.in) में जाँचें।",
        "लिंक पर क्लिक न करें। आधिकारिक वेबसाइट खुद खोलें।", "कुछ करने से पहले परिवार के किसी सदस्य से पूछें।",
        "पैसे गए हों या धोखाधड़ी का शक हो तो 1930 पर कॉल करें या cybercrime.gov.in पर शिकायत करें।", "पंजीकृत संस्था की शिकायत: सेबी SCORES (scores.sebi.gov.in)।"],
}

async def llm_summary(text, result, lang):
    """Optional: plain-language rewrite. Rules decide the risk level; the LLM only explains."""
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return None
    sig = "; ".join(s["en"] for s in result["signals"]) or "none"
    system = ("You explain possible warning signs in an investment message to a first-time Indian investor. "
              "Use very simple words, max 70 words, in " + ("Hindi" if lang == "hi" else "English") + ". "
              "Never say the message is definitely a scam. Never give buy/sell/hold advice, price predictions, or name any product or broker. "
              "Say the user should verify independently.")
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post("https://api.anthropic.com/v1/messages",
                headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                json={"model": os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"), "max_tokens": 300, "system": system,
                      "messages": [{"role": "user", "content": f"Message:\n{text}\n\nSignals found: {sig}"}]})
        return r.json()["content"][0]["text"].strip()
    except Exception:
        return None  # always fall back to the rule-based summary

@app.post("/api/analyze")
async def analyze_ep(req: Req):
    r = analyze(req.text)
    L = req.lang
    summary = await llm_summary(req.text, r, L) or SUMMARY[L][r["level"]]
    return dict(level=r["level"], score=r["score"], categories=r["categories"], stats=r["stats"], label=LABEL[L][r["level"]], summary=summary, steps=STEPS[L],
        signals=[dict(title=s[L], why=s["why_" + L], matched=s["matched"]) for s in r["signals"]],
        disclaimer="Not financial advice. Not a guarantee. Always verify independently." if L == "en"
                   else "यह वित्तीय सलाह नहीं है। कोई गारंटी नहीं। हमेशा स्वयं जाँच करें।")

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/")
def index():
    return FileResponse(FRONT / "index.html")
