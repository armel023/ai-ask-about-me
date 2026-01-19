AI Ask About Me
================

Small Gradio chat app that answers questions “as” Armel Ardael using a summary and LinkedIn PDF. It can also record contact details or unanswered questions through Pushover.

Requirements
------------
- Python 3.12+
- OpenAI API key in the environment
- Pushover app token and user key
- `me/linkedin.pdf` and `me/summary.txt` present

Setup
-----
1) Clone the repo and enter the folder.
2) Create `.env` (values are required for tool calls):
```
OPENAI_API_KEY=sk-...
PUSHOVER_TOKEN=your-pushover-app-token
PUSHOVER_USER=your-pushover-user-key
```
3) Install dependencies:
```
pip install -r requirements.txt
```
   or with `uv`:
```
uv sync
```

Run
---
```
python app.py
```
Gradio will print a local URL to open the chat UI.

Notes
-----
- PDF text is extracted at startup; if the file is missing or unreadable, the app will error.
- Outbound notifications use Pushover via HTTPS; ensure network access.
- History from Gradio is normalized before calling the OpenAI Chat Completions API (`gpt-4o-mini` by default).