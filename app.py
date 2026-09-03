import os
import base64
import streamlit as st
from google import genai
from rag import answer_question

st.set_page_config(
    page_title="PDF AI Assistant",
    page_icon="📄",
    layout="centered"
)

def load_font_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

font_base64 = load_font_base64("fonts/iranyekan.woff")

st.markdown(
    f"""
    <style>
    @font-face {{
        font-family: 'IranYekan';
        src: url(data:font/woff;base64,{font_base64}) format('woff');
        font-weight: normal;
        font-style: normal;
        font-display: block;
    }}

    * {{
        font-family: 'IranYekan', sans-serif !important;
    }}

    .stApp {{
        background: radial-gradient(circle at 50% 0%, #14141a 0%, #0a0a0c 60%) !important;
    }}
    .block-container {{
        max-width: 800px;
        padding-top: 2rem;
    }}

    .title-wrap {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.6rem;
        margin-bottom: 0.3rem;
    }}
    .title-icon {{
        width: 48px;
        height: 48px;
        border-radius: 14px;
        background: linear-gradient(135deg, #3b9dff, #1e5fd9);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        box-shadow: 0 4px 14px rgba(59,157,255,0.35);
    }}
    h1, .stApp h1 {{
        color: #ffffff !important;
        text-align: center;
        font-size: 2.1rem !important;
        margin: 0 !important;
    }}
    .subtitle {{
        text-align: center;
        color: #9a9aa0 !important;
        margin-bottom: 1.8rem;
        font-size: 1rem;
        direction: rtl;
    }}

    div[data-testid="stFileUploader"] {{
        border: 1px solid #2a2a30 !important;
        border-radius: 20px;
        padding: 1.2rem;
        background: linear-gradient(180deg, #1c1c22, #17171b) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.35);
        transition: border-color 0.15s ease;
    }}
    div[data-testid="stFileUploader"]:hover {{
        border-color: #3b9dff55 !important;
    }}
    div[data-testid="stFileUploader"] section {{
        background: transparent !important;
        border: none !important;
    }}
    div[data-testid="stFileUploader"] label,
    div[data-testid="stFileUploader"] p,
    div[data-testid="stFileUploader"] span,
    div[data-testid="stFileUploader"] small {{
        color: #d0d0d5 !important;
        direction: rtl;
    }}

    .st-key-pdf_upload button[kind="secondary"] {{
        width: 44px !important;
        height: 44px !important;
        min-width: 44px !important;
        min-height: 44px !important;
        padding: 0 !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #3b9dff, #1e7bfd) !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(59,157,255,0.3) !important;
        color: transparent !important;
        font-size: 0 !important;
        position: relative !important;
        transition: transform 0.12s ease, box-shadow 0.12s ease;
    }}
    .st-key-pdf_upload button[kind="secondary"] * {{
        display: none !important;
    }}
    .st-key-pdf_upload button[kind="secondary"]::after {{
        content: "↑" !important;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -52%);
        color: #ffffff !important;
        font-size: 22px !important;
        font-weight: bold;
        line-height: 1;
    }}
    .st-key-pdf_upload button[kind="secondary"]:hover {{
        transform: scale(1.06);
        box-shadow: 0 6px 18px rgba(59,157,255,0.45) !important;
    }}

    .stTextArea label {{
        color: #ffffff !important;
        direction: rtl;
        font-weight: 500;
    }}
    .stTextArea div[data-baseweb="textarea"] {{
        border-radius: 18px !important;
        border: 1px solid #2a2a30 !important;
        background: linear-gradient(180deg, #1c1c22, #17171b) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.35);
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }}
    .stTextArea div[data-baseweb="textarea"]:focus-within {{
        border-color: #3b9dff !important;
        box-shadow: 0 0 0 3px rgba(59,157,255,0.25), 0 4px 20px rgba(0,0,0,0.35) !important;
        outline: none !important;
    }}
    .stTextArea textarea {{
        direction: rtl;
        text-align: right;
        background: transparent !important;
        color: #ffffff !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        padding: 1rem !important;
        caret-color: #3b9dff;
    }}
    .stTextArea textarea::placeholder {{
        color: #6e6e75 !important;
    }}

    .stButton > button {{
        width: 100%;
        background: linear-gradient(135deg, #3b9dff, #1e7bfd) !important;
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 14px !important;
        padding: 0.85rem 1rem !important;
        border: none !important;
        direction: rtl;
        white-space: nowrap;
        letter-spacing: 0.2px;
        box-shadow: 0 4px 14px rgba(59,157,255,0.3);
        transition: transform 0.12s ease, box-shadow 0.12s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(59,157,255,0.45);
        color: #ffffff !important;
    }}
    .stButton > button:active {{
        transform: translateY(0px);
    }}

    .stAlert, div[data-testid="stNotification"] {{
        direction: rtl;
        text-align: right;
        background: linear-gradient(180deg, #1c1c22, #17171b) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        border: 1px solid #2a2a30 !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.35);
    }}
    .stAlert p, div[data-testid="stNotification"] p {{
        color: #ffffff !important;
    }}

    .answer-card, .answer-card * {{
        color: #ffffff !important;
    }}
    .answer-card {{
        background: linear-gradient(180deg, #1c1c22, #17171b) !important;
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid #2a2a30;
        box-shadow: 0 4px 20px rgba(0,0,0,0.35);
        margin-top: 1.2rem;
        line-height: 1.9;
        direction: rtl;
        text-align: right;
    }}
    .source-badge {{
        display: inline-block;
        margin-top: 1rem;
        background: linear-gradient(135deg, #12294a, #0d1f3d) !important;
        color: #6cb4ff !important;
        padding: 0.4rem 0.9rem;
        border-radius: 999px;
        font-size: 0.85rem;
        direction: rtl;
        font-weight: 500;
        box-shadow: 0 2px 10px rgba(59,157,255,0.15);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="title-wrap">
        <div class="title-icon">📄</div>
        <h1>PDF AI Assistant</h1>
    </div>
    """,
    unsafe_allow_html=True
)
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
    type=["pdf"],
    key="pdf_upload"
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
    st.info("برای شروع، یک فایل PDF آپلود کنید.")
