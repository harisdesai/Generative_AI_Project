# Generative AI Project

Short description
-----------------

This repository contains a Generative AI project with a Streamlit-based frontend and associated backend components. It provides an interface for authentication and demoing generative-model features.

Key features
------------

- Streamlit frontend (login and demo UIs)
- Modular project layout suitable for extending models and services

Requirements
------------

- Python 3.8 or newer
- Recommended: virtual environment (venv or conda)

Quick start (Windows)
----------------------

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies (if a `requirements.txt` exists) or at least Streamlit:

```powershell
pip install -r requirements.txt
# or
pip install streamlit
```

3. Run the frontend (example):

```powershell
streamlit run .\FrontEnd\login.py
```

Project structure (high-level)
------------------------------

- `FrontEnd/` — Streamlit UI files (login, dashboards, demos)
- `BackEnd/` — API, model wrappers, services (may be present)
- `data/` — sample datasets or generated outputs
- `requirements.txt` — Python dependencies (if present)
- `README.md` — this file

Notes
-----

- If `requirements.txt` is not present, inspect the `FrontEnd` and `BackEnd` folders for specific dependency needs (commonly `streamlit`, `tensorflow`/`torch`, `transformers`, `fastapi`, etc.).
- Adjust run commands if your environment differs (PowerShell vs cmd vs WSL).

Contributing
------------

Contributions are welcome. Please open an issue or submit a pull request describing your changes.

Contact
-------

For questions, github - harisdesai
