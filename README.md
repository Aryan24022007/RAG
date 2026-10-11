Simple PDF RAG App

A lightweight Retrieval-Augmented Generation (RAG) app that lets you ask questions about a PDF. Upload a document, let the app index its text, and ask questions in plain language. Answers are generated with Google Gemini using relevant passages retrieved from the uploaded PDF.

## Features

- Upload a PDF through a simple Streamlit interface.
- Extract and split PDF text into overlapping chunks.
- Create an in-memory FAISS vector index using Google Generative AI embeddings.
- Retrieve relevant passages and generate answers with Gemini 2.5 Flash.
- Instruct the model to say when the answer is not present in the document.

## How it works

1. The app loads your Google API key from `.env`.
2. You upload a PDF, which is temporarily saved so LangChain can read it.
3. The PDF text is split into chunks of 1,000 characters with 200 characters of overlap.
4. Google embeddings are generated and stored in a FAISS index for the current session.
5. For each question, the app retrieves relevant chunks and sends them with the question to Gemini 2.5 Flash.

The uploaded PDF and vector index are not configured for persistent storage; the index lives in Streamlit session state.

## Requirements

- Python 3.10 or newer
- A Google AI API key with access to the Gemini and embedding models used by the app

## Setup

Clone the repository and open a terminal in the project directory:

```bash
git clone <your-repository-url>
cd <repository-directory>
```

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Configure your API key

Create a file named `.env` in the project directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Replace the example value with your key. Keep `.env` private: do not commit API keys to GitHub. If `.env` is not already excluded, add it to `.gitignore`.

## Run the app

```bash
streamlit run main.py
```

Streamlit will print a local URL to open in your browser.

## Use the app

1. Upload a PDF using **Upload PDF**.
2. Wait for the vector database to finish building.
3. Enter a question about the PDF in **Ask something about your PDF**.
4. Read the generated answer below the input.

Upload a different PDF to replace the current session's index. The app currently handles one PDF at a time and does not retain the index between sessions.

## Dependencies

The exact package constraints are listed in [`requirements.txt`](requirements.txt). The app uses:

- [Streamlit](https://streamlit.io/) for the web interface
- [LangChain](https://www.langchain.com/) for document processing and model orchestration
- [Google Gemini](https://ai.google.dev/) for embeddings and answer generation
- [FAISS](https://github.com/facebookresearch/faiss) for vector search
- [pypdf](https://pypdf.readthedocs.io/) for PDF loading

## Notes and limitations

- The app requires an internet connection and a valid Google API key.
- PDF text extraction quality depends on the source document. Scanned PDFs may need OCR, which this app does not currently provide.
- Answers are based on retrieved text and can still be incomplete or incorrect; check important details against the original PDF.
- The vector index is created again when a new PDF is uploaded and is not saved as a durable database.
- The app uses the `gemini-2.5-flash` chat model and `models/gemini-embedding-001` embeddings.

## License

No license is specified in the project files provided. Add a `LICENSE` file if you want to make the terms for reuse clear.
