"""Rule engine: finds observable warning signals. Never claims certainty."""
import re

F = re.I | re.U
SIGNALS = [
 dict(id="guaranteed", w=3,
  en="Guaranteed or risk-free returns",
  hi="गारंटीड या बिना जोखिम का मुनाफ़ा",
  why_en="All real investments carry risk. Nobody can honestly promise a fixed profit.",
  why_hi="हर निवेश में जोखिम होता है। कोई भी पक्के मुनाफ़े का सच्चा वादा नहीं कर सकता।",
  pats=[r"guarantee\w*", r"assured\s+(return|profit|income)", r"sure[\s-]?shot", r"100\s?%\s*(safe|profit|return)", r"risk[\s-]?free", r"no\s+risk", r"गारंटी", r"पक्का\s+(मुनाफ़ा|मुनाफा)", r"बिना\s+जोखिम"]),
 dict(id="highreturn", w=3,
  en="Very high returns in a short time",
  hi="कम समय में बहुत ज़्यादा रिटर्न",
  why_en="Returns far above normal bank or market levels, in days or weeks, are a classic scam pattern.",
  why_hi="कुछ दिनों या हफ़्तों में बैंक या बाज़ार से कहीं ज़्यादा रिटर्न धोखाधड़ी का आम तरीका है।",
  pats=[r"(double|triple)\s+(your\s+)?(money|investment)", r"\b\d{2,4}\s?%\s*(daily|per\s+day|weekly|a\s+week|monthly|per\s+month|in\s+\d+\s+days?)", r"\b\d+\s?x\s+(return|profit)", r"दोगुना", r"तिगुना", r"daily\s+income"]),
 dict(id="urgency", w=2,
  en="Urgency or pressure to act fast",
  hi="जल्दी करने का दबाव",
  why_en="Scammers rush you so you do not stop to think or ask someone.",
  why_hi="ठग जल्दी मचाते हैं ताकि आप रुककर सोच या किसी से पूछ न सकें।",
  pats=[r"limited\s+(seats|slots|period|time|offer)", r"hurry", r"act\s+now", r"last\s+chance", r"today\s+only", r"contact\s+immediately", r"only\s+\d+\s+(seats|slots|spots)", r"जल्दी", r"तुरंत", r"आखिरी\s+मौका", r"सीमित\s+सीट"]),
 dict(id="payment", w=3,
  en="Asks for money, OTP or private details",
  hi="पैसे, OTP या निजी जानकारी माँगना",
  why_en="Genuine advisors never ask for OTP, PIN or password. Be careful of 'fees' paid to individuals.",
  why_hi="सच्चे सलाहकार OTP, PIN या पासवर्ड नहीं माँगते। किसी व्यक्ति को 'फीस' देने से सावधान रहें।",
  pats=[r"(pay|deposit|transfer|send)\s+(₹|rs\.?|money|fee|amount)", r"(registration|processing|joining)\s+fee", r"\bupi\b", r"\botp\b", r"\bpin\b", r"password", r"पैसे\s+भेज", r"जमा\s+करें"]),
 dict(id="group", w=2,
  en="Pushes you into a WhatsApp/Telegram group",
  hi="WhatsApp/Telegram ग्रुप में जुड़ने का दबाव",
  why_en="Fake 'VIP' groups are a common way to build false trust with many people at once.",
  why_hi="नकली 'VIP' ग्रुप एक साथ कई लोगों का झूठा भरोसा जीतने का आम तरीका हैं।",
  pats=[r"chat\.whatsapp\.com", r"t\.me/", r"telegram", r"join\s+(our|my)\s+(vip|group|channel)", r"(vip|premium)\s+(group|channel)", r"ग्रुप\s+में\s+जुड़"]),
 dict(id="tips", w=2,
  en="Investment solicitation or 'tips'",
  hi="निवेश के लिए बुलावा या 'टिप्स'",
  why_en="Unsolicited tips are not advice from a registered professional. Verify who is sending them.",
  why_hi="बिन माँगे टिप्स किसी पंजीकृत सलाहकार की सलाह नहीं होते। भेजने वाले की जाँच करें।",
  pats=[r"stock\s+tips?", r"hot\s+tips?", r"target\s+price", r"multibagger", r"jackpot", r"insider", r"\binvest\b.{0,40}\btoday\b", r"आज\s+ही\s+निवेश"]),
 dict(id="authority", w=2,
  en="Claims of approval or authority",
  hi="मान्यता या अधिकार का दावा",
  why_en="Claims like 'SEBI approved' are easy to fake. Check the official SEBI registered-intermediary list yourself.",
  why_hi="'सेबी मान्य' जैसे दावे नकली हो सकते हैं। सेबी की आधिकारिक सूची में खुद जाँचें।",
  pats=[r"sebi\s+(registered|approved|certified)", r"rbi\s+approved", r"government\s+(approved|scheme)", r"(nse|bse)\s+(partner|member)", r"सेबी\s+(से\s+)?(पंजीकृत|मान्य)", r"सेबी\s+पंजीकृत"]),
 dict(id="crypto", w=2,
  en="Crypto, forex or 'AI trading app' pitch",
  hi="क्रिप्टो, फॉरेक्स या 'AI ट्रेडिंग ऐप' का प्रचार",
  why_en="These are often used in fake investment platforms. Treat unknown apps with caution.",
  why_hi="नकली निवेश प्लेटफ़ॉर्म में इनका अक्सर इस्तेमाल होता है। अनजान ऐप से सावधान रहें।",
  pats=[r"usdt", r"crypto", r"bitcoin", r"ai\s+trading", r"arbitrage", r"forex", r"binary\s+option"]),
]
URL_RE = re.compile(r"(?:https?://|www\.)[^\s]+|\b[\w-]+\.(?:xyz|top|vip|click|icu|site|online|buzz|live)\b[^\s]*", F)
SHORT = ("bit.ly", "tinyurl", "cutt.ly", "rb.gy", "is.gd", "shorturl")
BAD_TLD = (".xyz", ".top", ".vip", ".click", ".icu", ".site", ".buzz")
PERIOD = re.compile(r"\b(day|days|week|weeks|hours?)\b|दिन|हफ़्ते|हफ्ते", F)
MONEY = re.compile(r"(?:₹|rs\.?|inr|rupees)\s*([\d,]+)|([\d,]+)\s*(?:₹|rs\b|rupees)", F)

def _money(text):
    vals = []
    for a, b in MONEY.findall(text):
        s = (a or b).replace(",", "")
        if s.isdigit():
            vals.append(int(s))
    return vals

def _host(u):
    return re.sub(r"^https?://", "", u.lower()).split("/")[0]

def _url_flags(text):
    out = []
    for u in URL_RE.findall(text):
        l, h = u.lower(), _host(u)
        if any(s in l for s in SHORT):
            out.append((u, "shortened link hides the real site"))
        elif re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}(:\d+)?", h):
            out.append((u, "link uses a raw IP address"))
        elif "sebi" in h and not h.endswith("sebi.gov.in"):
            out.append((u, "looks like SEBI but is not sebi.gov.in"))
        elif any(h.rstrip(".,)").endswith(t) for t in BAD_TLD):
            out.append((u, "unusual website ending"))
    return out

def analyze(text: str):
    found, score = [], 0
    for s in SIGNALS:
        hits = []
        for p in s["pats"]:
            m = re.search(p, text, F)
            if m:
                hits.append(m.group(0).strip())
        if s["id"] == "highreturn" and not hits:
            m = _money(text)
            if len(m) >= 2 and m[0] > 0 and m[1] / m[0] >= 1.5 and PERIOD.search(text):
                hits.append(f"₹{m[0]:,} → ₹{m[1]:,}")
        if hits:
            found.append(dict(id=s["id"], en=s["en"], hi=s["hi"], why_en=s["why_en"], why_hi=s["why_hi"], matched=hits[:3]))
            score += s["w"]
    urls = _url_flags(text)
    if urls:
        score += 2
        found.append(dict(id="url", en="Suspicious link", hi="संदिग्ध लिंक",
            why_en="Never log in or pay through a link you did not open yourself from an official site.",
            why_hi="जो लिंक आपने आधिकारिक साइट से खुद नहीं खोला, उससे लॉगिन या भुगतान न करें।",
            matched=[f"{u} ({r})" for u, r in urls[:2]]))
    level = "high" if score >= 7 else "medium" if score >= 3 else "low"
    signal_count = len(found)
    link_count = sum(1 for s in found if s["id"] == "url")
    categories = [s["id"] for s in found]
    return dict(level=level, score=score, categories=categories,
               stats={"risk_score": score, "signal_count": signal_count, "link_count": link_count},
               signals=found)
