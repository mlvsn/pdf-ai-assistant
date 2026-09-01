# PDF AI Assistant

A RAG-based PDF Question Answering system that retrieves relevant content from a PDF and uses Gemini to generate grounded answers.

> **Current status:** Working prototype. The project currently supports PDF text extraction, chunking, embeddings, semantic retrieval, embedding caching, and answer generation with Gemini.

## How It Works

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
Similarity Search
 ↓
Relevant Chunks
 ↓
Question + Context
 ↓
Gemini
 ↓
Answer
```

The system does not send the entire PDF directly to the language model. Instead, it:

1. Extracts text from the PDF.
2. Splits the text into overlapping chunks.
3. Creates an embedding for each chunk.
4. Converts the user's question into an embedding.
5. Uses cosine similarity to retrieve the most relevant chunks.
6. Sends the question and retrieved context to Gemini.
7. Generates a Persian answer based only on the retrieved context.

## Features

* PDF text extraction with `pypdf`
* Word-based chunking with overlap
* Gemini embeddings for semantic search
* Cosine similarity retrieval
* Top-K relevant chunk selection
* Local embedding cache to avoid unnecessary API calls
* Persian question answering
* Context-grounded Gemini responses
* Git-ready project structure with sensitive files excluded

## Project Structure

```text
pdf-ai-assistant/
├── main.py              # Application entry point
├── rag.py               # RAG pipeline
├── requirements.txt     # Python dependencies
└── .gitignore           # Ignored local and sensitive files
```

Local files such as the source PDF, embedding cache, extracted text, and API credentials are intentionally excluded from the public repository.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mlvsn/pdf-ai-assistant.git
cd pdf-ai-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your Gemini API key

Set the `GEMINI_API_KEY` environment variable before running the application.

PowerShell example:

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

> Never commit your API key to GitHub.

### 4. Add a PDF

The current prototype expects a local PDF file named:

```text
اثر مرکب.pdf
```

This file is not included in the repository.

### 5. Run

```powershell
py main.py
```

Then enter your question in Persian.

## Example

**Question**

```text
خلاصه کتاب اثر مرکب رو در دو جمله بگو
```

**Example output**

```text
موفقیت حاصل اقدامات بزرگ یا تغییرات یک‌شبه نیست، بلکه نتیجه انتخاب‌ها و عادت‌های کوچک و درست روزانه است.
تکرار مداوم و باثبات همین کارهای کوچک در طول زمان، منجر به نتایج بسیار بزرگ و پایدار می‌شود.
```

## Current RAG Configuration

| Component        | Current approach       |
| ---------------- | ---------------------- |
| Chunking         | 500 words              |
| Chunk overlap    | 100 words              |
| Embedding model  | `gemini-embedding-001` |
| Retrieval        | Cosine similarity      |
| Retrieved chunks | Top 3                  |
| LLM              | `gemini-3.6-flash`     |

## Current Limitations

This is an early portfolio prototype and still has limitations:

* The PDF path is currently hard-coded.
* The application currently works with one local PDF at a time.
* Source citations are not yet shown to the user.
* There is no graphical user interface yet.
* Retrieval and answer quality have not yet been formally evaluated.
* Chunking is currently word-based rather than structure-aware.

## Roadmap

### Core

* [x] PDF text extraction
* [x] Chunking
* [x] Embeddings
* [x] Semantic similarity retrieval
* [x] Gemini answer generation
* [x] Embedding caching

### Next

* [ ] Source citations in answers
* [ ] Configurable PDF input
* [ ] Improved error handling
* [ ] Retrieval evaluation
* [ ] Answer evaluation
* [ ] Simple UI
* [ ] Architecture diagram
* [ ] Automated tests
* [ ] Technical report and documentation

## Tech Stack

* Python
* Google GenAI SDK
* Gemini
* RAG
* Embeddings
* Semantic Retrieval
* Cosine Similarity
* PyPDF
* Git / GitHub

## Learning Goal

This project is not only about building a working application. Its goal is also to understand the engineering decisions behind a RAG system:

* Why is chunking necessary?
* How do embeddings represent semantic relationships?
* How does similarity search retrieve relevant context?
* Why does RAG reduce unsupported answers?
* How should a small AI application be structured and evaluated?

## License

No license has been added yet.
