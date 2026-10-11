# Simple PDF RAG App

A Streamlit app for asking questions about a PDF. It uses OpenAI embeddings to find relevant passages and GPT-4o mini to generate answers.

## Features

- Upload a PDF through a simple web interface.
- Split PDF text into overlapping chunks.
- Search relevant passages using a FAISS vector index.
- Generate answers with GPT-4o mini.

## Requirements

- Python 3.10 or newer
- An OpenAI API key

## Setup

Clone the repository and open a terminal in its directory:

```bash
git clone <your-repository-url>
cd <repository-directory>
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS or Linux:**

```bash
source .venv/bin/activate
```

Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Configure your API key

Create a `.env` file in the project directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Keep your API key private. Make sure `.env` is listed in `.gitignore` so it isn’t committed to GitHub.

## Run the app

```bash
streamlit run main.py
```

Open the local URL printed by Streamlit in your browser.

## Use the app

1. Upload a PDF.
2. Wait for the app to process and index it.
3. Enter a question about the PDF.
4. Read the answer displayed below the question box.

The app processes one PDF per session. The vector index is held in Streamlit session state and isn’t saved between sessions.

## How it works

The app extracts text from the PDF and splits it into 1,000-character chunks with 200 characters of overlap. It creates embeddings using OpenAI’s `text-embedding-3-small` model and stores them in a FAISS vector index. When you ask a question, the app retrieves relevant chunks and uses `gpt-4o-mini` to generate an answer.

## Limitations

- Requires an internet connection and a valid OpenAI API key.
- Scanned PDFs may need OCR, which the app does not currently provide.
- Answers can be incomplete or incorrect; check important details against the original PDF.
- The app writes the uploaded PDF to `temp.pdf` while processing it.

> **Note:** The `requirements.txt` shared earlier lists Google Gemini packages, while this version of `main.py` imports OpenAI packages. The requirements file may need matching OpenAI dependencies for the app to install and run.
