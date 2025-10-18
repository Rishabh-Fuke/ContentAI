# ContentAI / Autogram — Quick start

This repository contains the Autogram crew project. Follow these steps to run locally.

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. Copy the example env and add your OpenAI key:

```bash
cp .env.example .env
# edit .env and set OPENAI_API_KEY=<your_key>
```

3. Run the app (from project root):

```bash
PYTHONPATH=autogram/src python -m autogram.main
```

If the app complains about missing `OPENAI_API_KEY`, make sure you added it to `.env` and activated your virtualenv.
