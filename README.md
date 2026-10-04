# Bharat Scan Shield — "Pause. Check. Understand."
**SANGYAN Hackathon · Track A**

Bharat Scan Shield is an educational investor-awareness tool for Indian retail investors. It helps people inspect suspicious investment messages before trusting them or sending money or personal information. The interface and explanations are available in English and Hindi.

## What it does
Users can paste a message, speak it, or upload a screenshot. The app highlights warning signs it recognizes, shows the phrases that triggered them, and suggests practical steps such as checking official sources or reporting suspected fraud. Screenshot OCR and speech capture run in the browser.

Signals include guaranteed or unusually high returns, pressure to act quickly, requests for money or sensitive details, investment groups, authority claims, crypto or trading-app pitches, and suspicious links.

## How to read a result
The rule engine assigns weights to detected signals and combines them into a score:

- **Low (0–2):** few common warning signals found
- **Medium (3–6):** some warning signals found
- **High (7+):** several warning signals found

The score is not a probability, and a low score does not mean a message is safe. The app shows matched phrases so users can understand why a warning appeared.

## Privacy and limitations
The app does not store or log scanned messages. Text is sent to the app's analysis service to produce a result. Screenshot image files stay on the user's device; OCR extracts text in the browser. Recent checks remain in the current browser tab only. If optional AI explanations are enabled, message text is also sent to Anthropic; the rule engine still determines the score and risk level.

This is not financial advice or proof that a message is fraudulent. Rule-based detection can miss new scam wording or flag genuine messages. Verify claims independently. The app does not provide stock tips, predictions, or buy/sell recommendations.

## Run locally (5 minutes)
    python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn backend.main:app --reload
    # open http://127.0.0.1:8000

Optional AI explanation (rules still decide the risk level):
    export ANTHROPIC_API_KEY=your_key      # Windows: set ANTHROPIC_API_KEY=your_key

Tests: `python -m unittest discover -s tests -t . -v`. Tests use synthetic examples and are not a real-world accuracy benchmark.

## Deploy free
Push to GitHub, create a Render/Railway web service. Build: `pip install -r requirements.txt`. Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`. Add ANTHROPIC_API_KEY as an env var (optional).

## Technology
FastAPI serves the two-page HTML/CSS/JavaScript interface and analysis API. A transparent Python rule engine checks eight signal families plus suspicious links, then returns a score, matched signals, bilingual explanation, and safety steps. Tesseract.js performs English/Hindi screenshot OCR in the browser; voice input uses the Web Speech API. Optional Anthropic API support rewrites the explanation in plain language without controlling the risk score.
