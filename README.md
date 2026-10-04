# Bharat Scan Shield — "Pause. Check. Understand."
SANGYAN Hackathon, Track A. Bharat Scan Shield helps retail investors pause, check, and understand suspicious financial content before they trust it. It is an educational investor-awareness tool for Indian users, available in Hindi and English.

Not financial advice. Verify independently.

Paste text, speak, or upload a screenshot; get explainable warning signs in Hindi/English and safe next steps. No stock tips or predictions. Scanned messages are not stored by the app. If optional AI explanations are enabled, message text is sent to Anthropic.

## Run locally (5 minutes)
    python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn backend.main:app --reload
    # open http://127.0.0.1:8000

Optional AI explanation (rules still decide the risk level):
    export ANTHROPIC_API_KEY=your_key      # Windows: set ANTHROPIC_API_KEY=your_key

Tests: `python -m unittest discover -s tests -t . -v`
These are synthetic regression cases, not a real-world accuracy benchmark.

## Deploy free
Push to GitHub, create a Render/Railway web service. Build: `pip install -r requirements.txt`. Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`. Add ANTHROPIC_API_KEY as an env var (optional).

## How it works
Text -> rule engine (8 signal families + link checks) -> score -> level -> bilingual explanation -> safe steps.
Screenshot OCR (Tesseract.js, eng+hin) and speech input run in the browser. Backend has no database and does not log messages.
