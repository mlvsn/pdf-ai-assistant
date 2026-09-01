# PDF AI Assistant

A RAG-based PDF Question Answering system that retrieves relevant content from a PDF and uses Gemini to generate grounded, source-cited answers.

> **Current status:** Working prototype with a Streamlit UI. Users can upload any PDF, ask questions in Persian, and receive answers grounded in the document along with the source page numbers.

## How It Works

```text
PDF Upload
 ->
Text Extraction
 ->
Chunking
 ->
Embeddings
 ->
Embedding Cache
 ->
Semantic Retrieval (Cosine Similarity)
 ->
Top-K Relevant Chunks
 ->
Gemini LLM
 ->
Answer + Source Pages
```

The system does not send the entire PDF directly to the language model. Instead, it:

1. Extracts text from the uploaded PDF.
2. Splits the text into overlapping chunks, keeping track of the page each chunk came from.
3. Creates an embedding for each chunk (cached per-file to avoid recomputation).
4. Converts the user's question into an embedding.
5. Uses cosine similarity to retrieve the most relevant chunks.
6. Sends the question and retrieved context to Gemini.
7. Generates a Persian answer based only on the retrieved context, along with the source page numbers.

## Features

* Streamlit UI with PDF upload
* PDF text extraction with pypdf
* Word-based chunking with overlap
* Gemini embeddings for semantic search
* Per-file embedding cache to avoid unnecessary API calls
* Cosine similarity retrieval
* Top-K relevant chunk selection
* Persian question answering
* Context-grounded Gemini responses
* Source page citation in every answer
* Git-ready project structure with sensitive files excluded

## Project Structure

```text
pdf-ai-assistant/
├── main.py              # CLI entry point
├── app.py               # Streamlit UI
├── rag.py               # RAG pipeline (chunking, embeddings, retrieval, generation)
├── requirements.txt     # Python dependencies
└── .gitignore           # Ignored local and sensitive files
```

Local files such as source PDFs, embedding caches, extracted text, and API credentials are intentionally excluded from the public repository.

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

Set the GEMINI_API_KEY environment variable before running the application.

PowerShell example:

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

> Never commit your API key to GitHub.

### 4. Run the app

```powershell
streamlit run app.py
```

Then upload a PDF and ask your question in Persian.

## Example

**Question**

```text
خلاصه فایل رو در سه خط بده
```

**Example answer**

```text
کتاب «اثر مرکب» بیان می‌کند موفقیت حاصل اقدامات بزرگ نیست، بلکه نتیجه انتخاب‌ها و عادت‌های کوچک، درست و مداوم در طول زمان است.
تغییرات کوچک چه مثبت و چه منفی در ابتدا دیده نمی‌شوند، اما با تکرار و استمرار، نتایجی بسیار بزرگ و تصاعدی در زندگی ایجاد می‌کنند.
برای رسیدن به اهداف باید به جای انگیزه بر نظم، ثبات قدم، ثبت روزانه عملکرد و حذف عادت‌های بد تکیه کرد.

منبع: صفحات 1، 4، 30
```

## Current RAG Configuration

| Component        | Current approach       |
| ---------------- | ----------------------- |
| Chunking         | 500 words                |
| Chunk overlap    | 100 words                |
| Embedding model  | gemini-embedding-001   |
| Retrieval        | Cosine similarity        |
| Retrieved chunks | Top 3                    |
| LLM              | gemini-3.6-flash       |

## Current Limitations

This is a portfolio prototype and still has known limitations:

* Retrieval and answer quality have not yet been formally evaluated.
* Chunking is currently word-based rather than structure-aware.
* No automated tests yet.
* Error handling for API failures (e.g. rate limits) is minimal.

## Roadmap

### Core

* [x] PDF upload and text extraction
* [x] Chunking
* [x] Embeddings
* [x] Semantic similarity retrieval
* [x] Gemini answer generation
* [x] Embedding caching
* [x] Source page citations
* [x] Streamlit UI

### Next

* [ ] Improved error handling for API errors
* [ ] Retrieval evaluation
* [ ] Answer evaluation
* [ ] Architecture diagram
* [ ] Automated tests
* [ ] Technical report and documentation

## Tech Stack

* Python
* Streamlit
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