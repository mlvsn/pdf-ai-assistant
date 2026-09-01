import os
import streamlit as st
from google import genai
from rag import answer_question

st.set_page_config(
    page_title="PDF AI Assistant",
    page_icon="📄",
    layout="centered"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0d0d0f !important;
    }
    .block-container {
        max-width: 800px;
        padding-top: 2.5rem;
    }
    h1, .stApp h1 {
        color: #ffffff !important;
        text-align: center;
        font-size: 2.2rem !important;
        margin-bottom: 0.2rem !important;
    }
    .subtitle {
        text-align: center;
        color: #9a9aa0 !important;
        margin-bottom: 1.8rem;
        font-size: 1rem;
        direction: rtl;
    }
    div[data-testid="stFileUploader"] {
        border: none !important;
        border-radius: 20px;
        padding: 1.2rem;
        background-color: #1c1c1f !important;
    }
    div[data-testid="stFileUploader"] section {
        background-color: #1c1c1f !important;
        border: none !important;
    }
    div[data-testid="stFileUploader"] label,
    div[data-testid="stFileUploader"] p,
    div[data-testid="stFileUploader"] span,
    div[data-testid="stFileUploader"] small {
        color: #d0d0d5 !important;
        direction: rtl;
    }
    div[data-testid="stFileUploader"] button {
        background-color: #3b9dff !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
    }
    .stTextArea label {
        color: #ffffff !important;
        direction: rtl;
        font-weight: 500;
    }
    .stTextArea textarea {
        direction: rtl;
        text-align: right;
        background-color: #1c1c1f !important;
        color: #ffffff !important;
        border-radius: 18px !important;
        border: none !important;
        padding: 1rem !important;
        caret-color: #3b9dff;
    }
    .stTextArea textarea::placeholder {
        color: #6e6e75 !important;
    }
    .stTextArea textarea:focus {
        box-shadow: 0 0 0 2px #3b9dff !important;
    }
    .stButton > button {
        width: 100%;
        background-color: #3b9dff !important;
        color: #ffffff !important;
        font-weight: 600;
        border-radius: 14px !important;
        padding: 0.7rem 0 !important;
        border: none !important;
        direction: rtl;
        transition: background-color 0.15s ease;
    }
    .stButton > button:hover {
        background-color: #1e8bfd !important;
        color: #ffffff !important;
    }
    .stAlert, div[data-testid="stNotification"] {
        direction: rtl;
        text-align: right;
        background-color: #1c1c1f !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        border: none !important;
    }
    .stAlert p, div[data-testid="stNotification"] p {
        color: #ffffff !important;
    }
    .answer-card, .answer-card * {
        color: #ffffff !important;
    }
    .answer-card {
        background-color: #1c1c1f !important;
        border-radius: 20px;
        padding: 1.5rem;
        border: none;
        margin-top: 1.2rem;
        line-height: 1.9;
        direction: rtl;
        text-align: right;
    }
    .source-badge {
        display: inline-block;
        margin-top: 1rem;
        background-color: #12294a !important;
        color: #3b9dff !important;
        padding: 0.4rem 0.9rem;
        border-radius: 999px;
        font-size: 0.85rem;
        direction: rtl;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📄 PDF AI Assistant")
st.markdown(
    '<div class="subtitle">سوال خود را درباره محتوای PDF بپرسید و پاسخ را همراه با منبع دریافت کنید</div>',
    unsafe_allow_html=True
)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY پیدا نشد.")
    st.stop()

client = genai.Client(api_key=api_key)

uploaded_file = st.file_uploader(
    "PDF خود را آپلود کنید",
    type=["pdf"]
)

if uploaded_file:
    st.success(f"فایل آپلود شد: {uploaded_file.name}")
    pdf_bytes = uploaded_file.getvalue()

    question = st.text_area(
        "سوال خود را بنویسید",
        placeholder="مثلا: خلاصه این فایل را در سه خط بگو"
    )

    if st.button("پرسیدن از هوش مصنوعی"):
        if not question.strip():
            st.warning("لطفا ابتدا یک سوال بنویسید.")
        else:
            try:
                with st.spinner("در حال پیدا کردن پاسخ..."):
                    answer = answer_question(client, question, pdf_bytes)

                if "منبع:" in answer:
                    body, source = answer.split("منبع:", 1)
                    body = body.strip()
                    source = source.strip()
                else:
                    body = answer.strip()
                    source = None

                st.markdown(
                    f'<div class="answer-card">{body}</div>',
                    unsafe_allow_html=True
                )

                if source:
                    st.markdown(
                        f'<div class="source-badge">📌 منبع: {source}</div>',
                        unsafe_allow_html=True
                    )

            except RuntimeError as error:
                st.error(str(error))
            except Exception:
                st.error("خطایی در پردازش درخواست رخ داد. لطفا دوباره تلاش کنید.")
else:
    st.info("برای شروع یک فایل PDF آپلود کنید.")
