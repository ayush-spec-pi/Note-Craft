# NoteCraft AI

**Adaptive Academic Companion for Engineering Students (MSRIT)**  
*Built by **Team NetRunners** for **wHACKiest 2026***

NoteCraft AI connects raw classroom lectures, teacher emphasis, messy typed/scanned PDF notes, and RIT Notebook Previous Year Questions (PYQs) into a single, exam-oriented study workspace.

---

## Why NoteCraft AI?

Engineering students juggle scattered slides, handwritten/scanned PDFs, unindexed PYQ archives, and verbal exam hints professors drop during lectures. NoteCraft AI bridges these inputs in one automated pipeline:

- **Catches what slides miss:** Extracts verbal exam traps, repeated derivations, and rubric warnings from classroom audio recordings.
- **Handles messy academic PDFs:** Reads both digital and scanned/photo-based PDFs using automatic OCR fallback and topic-level page filtering.
- **Zero-cost, resilient AI backend:** Uses a multi-model free-tier LLM fallback chain so note generation stays fast and reliable even under API rate limits.

---

## Core Features

### 1. Academic Context Onboarding
Personalizes the workspace by **Year**, **Cycle / Semester**, and **Branch** so Drive catalogs, PYQ searches, and analytics automatically scope to the student's curriculum.

### 2. Smart Study Pack (`ui_study.py`)
- **Flexible Inputs:** Works with PDFs only, lecture audio/transcripts only, or a combined multimodal pipeline.
- **Typed + Scanned PDF Engine (`processor.py`):** Extracts text via PyMuPDF (`fitz`) and automatically falls back to **RapidOCR** on image/scanned pages. Includes **Smart Topic Page Search** to isolate relevant pages inside combined unit PDFs.
- **Classroom Audio Transcription (`transcriber.py`):** Ultra-fast speech-to-text powered by **Groq Whisper (`whisper-large-v3-turbo`)**.
- **Exam-Focused Output (`llm_engine.py`):** Synthesizes four structured sections:
  1. **Teacher Spotlight** (emphasized topics, repeated derivations, and exam traps)
  2. **Structured Revision Notes**
  3. **Key Formulas, Derivations & Code** (with an automatic LaTeX sanitizer for clean KaTeX rendering)
  4. **60-Second Quick Recap**
- **Export:** One-click Markdown (`.md`) download for offline revision.

### 3. PYQ Vault (`ui_pyq.py`) *(Roadmap / Drive Integration)*
Scoped archive connected to the MSRIT RIT Notebook Google Drive catalog (`drive_catalog.json`) for topic-wise PYQ discovery and exam frequency trends.

### 4. Adaptive "Test Me" Quiz (`ui_test.py`) *(Roadmap)*
Subject, unit, and topic-scoped MCQ generator backed by historical PYQs and personal weakness memory.

### 5. Real-Time Weakness Analytics (`ui_dashboard.py`) *(Roadmap)*
Interactive Plotly dashboard tracking unit- and topic-wise weak spots that automatically updates after every quiz session.

---

## System Architecture

```text
  [1. INPUTS]                [2. EXTRACTION]             [3. CORE ENGINE]               [4. WORKSPACE UI]
+-------------------+     +--------------------+     +-----------------------+     +-------------------------+
| Lecture Audio     | --> | Groq Whisper API   | --+ | Multi-Model LLM       | --> | Smart Study Pack        |
| (MP3 / WAV / M4A) |     | (Speech-to-Text)   |   | | OpenRouter Fallback   |     | (Notes + Teacher Hints) |
+-------------------+     +--------------------+   | | + LaTeX Math Cleaner  |     +-------------------------+
                                                   +-------------------------+     +-------------------------+
+-------------------+     +--------------------+   | | Context & Storage     | --> | PYQ Vault & Trends      |
| Class Notes PDFs  | --> | PyMuPDF + RapidOCR | --+ | Drive Catalog DB &    |     +-------------------------+
| (Typed & Scanned) |     | + Topic Filtering  |   | | Weakness Memory JSON  | --> | Adaptive Test Me        |
+-------------------+     +--------------------+   | +-----------------------+     +-------------------------+
                                                   |                               +-------------------------+
+-------------------+                              |                               | Analytics Dashboard     |
| RIT Notebook PYQs | -----------------------------+                               | (Live Plotly Graphs)    |
| (Google Drive DB) |                                                              +-------------------------+
+-------------------+
```

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend & UI** | Streamlit (Custom Swiss / Notion-inspired CSS), Plotly |
| **PDF & OCR Pipeline** | PyMuPDF (`fitz`), RapidOCR (`rapidocr-onnxruntime`) |
| **Speech-to-Text** | Groq API (`whisper-large-v3-turbo`) |
| **LLM Synthesis** | OpenRouter API (Multi-model free-tier fallback chain) |
| **Environment & Config** | Python 3.10+, `python-dotenv`, `requests` |

---

## Project Structure

```text
notecraft-ai/
├── app.py                # Main Streamlit shell, onboarding, theme CSS & navigation
├── ui_study.py           # Smart Study Pack capture & workspace tab
├── ui_pyq.py             # PYQ Vault tab
├── ui_test.py            # Adaptive Test Me tab
├── ui_dashboard.py       # Real-Time Weakness Analytics tab
├── processor.py          # Typed + Scanned PDF reader (PyMuPDF + RapidOCR) & topic filter
├── transcriber.py        # Groq Whisper classroom audio transcription
├── llm_engine.py         # OpenRouter fallback engine & LaTeX math sanitizer
├── logo.png              # Application logo & favicon
├── requirements.txt      # Python dependencies
├── .env                  # Local API keys (git-ignored)
└── .gitignore
```

---

## Local Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Create and Activate a Virtual Environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root directory and add your API keys:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```
*(Never commit `.env` to version control.)*

### 5. Run the Application
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```
Or, with the virtual environment activated:
```bash
streamlit run app.py
```

Open **`http://localhost:8501`** in your browser. For an instant demo without uploading files, click **Load Sample** in the Study Pack tab and hit **Generate Smart Study Pack**.

---

## Team NetRunners

Built for **wHACKiest 2026** at **Ramaiah Institute of Technology (MSRIT)**, Bengaluru.
