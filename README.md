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

## Technology Stack
- **Frontend**
    - HTML5, CSS3, and vanilla JavaScript; no frontend framework or build step.
    - Tesseract.js 5 for English/Hindi screenshot OCR in the browser.
    - Web Speech API for browser-based voice input; availability depends on the browser.
- **Backend**
    - Python with FastAPI for the web app and JSON API.
    - Uvicorn for the ASGI server.
    - Pydantic request validation through FastAPI.
    - `httpx` for the optional Anthropic API request.
- **Detection and tests**
    - A custom, explainable Python rule engine in `backend/rules.py`.
    - Python `unittest` regression tests using synthetic examples.
- **External services**
    - Optional Anthropic API for plain-language explanations. The rule engine, not the AI service, determines the score and risk level.
    - Tesseract.js is loaded from jsDelivr; Google Fonts provides the interface fonts.

## Project Architecture
1. **Page delivery:** FastAPI serves the welcome page at `/` and the scanner at `/scan`.
2. **Input capture:** The browser accepts pasted text, speech transcripts, or screenshots. Screenshot OCR runs in the browser; the image file itself is not uploaded.
3. **Analysis request:** The scanner sends the extracted or entered text and selected language to `POST /api/analyze`.
4. **Rule evaluation:** `backend.rules.analyze()` checks eight warning-signal families and suspicious links, then calculates the score, level, categories, and matched phrases.
5. **Explanation and guidance:** `backend.main` returns localized explanations and safety steps. If `ANTHROPIC_API_KEY` is configured, message text is also sent to Anthropic to rewrite the explanation; this does not change the rule-based score or level.
6. **Results:** The browser displays the score, warning signals, matched text, and next steps. Recent checks are kept in the current tab only.

The backend has no database and does not log scanned messages. Scanned text is sent to the analysis service but is not stored by the app. See [Privacy and limitations](#privacy-and-limitations) before enabling optional AI explanations.
