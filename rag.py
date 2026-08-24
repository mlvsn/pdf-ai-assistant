from pypdf import PdfReader
from google import genai
import math
import json
import os


PDF_PATH = "اثر مرکب.pdf"
CACHE_PATH = "embeddings_cache.json"

EMBEDDING_MODEL = "gemini-embedding-001"
LLM_MODEL = "gemini-3.6-flash"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 3


def load_pdf(pdf_path):
    pdf = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append({
                "page": page_number,
                "text": text.strip()
            })

    return pages


def create_chunks(pages):
    chunks = []

    for page in pages:
        words = page["text"].split()
        start = 0

        while start < len(words):
            end = start + CHUNK_SIZE
            chunk_text = " ".join(words[start:end])

            if chunk_text.strip():
                chunks.append({
                    "page": page["page"],
                    "text": chunk_text
                })

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def create_embeddings(client, chunks):
    embeddings = []

    for chunk in chunks:
        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=chunk["text"]
        )

        embeddings.append(result.embeddings[0].values)

    return embeddings


def load_or_create_embeddings(client, chunks):
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as file:
            cached_data = json.load(file)

        if (
            len(cached_data) == len(chunks)
            and all(
                cached_data[i]["text"] == chunks[i]["text"]
                for i in range(len(chunks))
            )
        ):
            return [
                item["embedding"]
                for item in cached_data
            ]

    embeddings = create_embeddings(client, chunks)

    cache_data = []

    for chunk, embedding in zip(chunks, embeddings):
        cache_data.append({
            "page": chunk["page"],
            "text": chunk["text"],
            "embedding": embedding
        })

    with open(CACHE_PATH, "w", encoding="utf-8") as file:
        json.dump(cache_data, file)

    return embeddings


def cosine_similarity(a, b):
    dot_product = sum(
        x * y for x, y in zip(a, b)
    )

    magnitude_a = math.sqrt(
        sum(x * x for x in a)
    )

    magnitude_b = math.sqrt(
        sum(y * y for y in b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (
        magnitude_a * magnitude_b
    )


def retrieve(client, question, chunks, embeddings):
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=question
    )

    question_embedding = result.embeddings[0].values

    scored_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        score = cosine_similarity(
            question_embedding,
            embedding
        )

        scored_chunks.append({
            "page": chunk["page"],
            "text": chunk["text"],
            "score": score
        })

    scored_chunks.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scored_chunks[:TOP_K]


def generate_answer(client, question, retrieved_chunks):
    context_parts = []

    for item in retrieved_chunks:
        context_parts.append(
            f"[صفحه {item['page']}]\n{item['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
تو یک دستیار پاسخ‌گویی درباره یک PDF هستی.

فقط بر اساس Context زیر پاسخ بده.
اگر اطلاعات کافی برای پاسخ وجود ندارد، بگو:
«اطلاعات کافی در PDF پیدا نشد.»

سؤال کاربر:
{question}

Context:
{context}

قوانین پاسخ:
- پاسخ را به زبان فارسی بده.
- مستقیم و بدون مقدمه پاسخ بده.
- اگر کاربر تعداد مشخصی خط یا جمله خواست، دقیقاً همان مقدار را رعایت کن.
- اگر تعداد مشخص نکرد، پاسخ را کوتاه و مفید نگه دار.
- اطلاعاتی خارج از Context اضافه نکن.
"""

    response = client.interactions.create(
        model=LLM_MODEL,
        input=prompt
    )

    return response.output_text.strip()


def answer_question(client, question):
    pages = load_pdf(PDF_PATH)
    chunks = create_chunks(pages)

    embeddings = load_or_create_embeddings(
        client,
        chunks
    )

    retrieved_chunks = retrieve(
        client,
        question,
        chunks,
        embeddings
    )

    return generate_answer(
        client,
        question,
        retrieved_chunks
    )