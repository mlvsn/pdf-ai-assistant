import os
import streamlit as st
from google import genai

from rag import answer_question


st.set_page_config(
    page_title="PDF AI Assistant",
    page_icon="📄",
    layout="centered"
)


st.title("📄 PDF AI Assistant")

st.write(
    "PDF خود را آپلود کنید و از محتوای آن سؤال بپرسید."
)


api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    st.error(
        "GEMINI_API_KEY پیدا نشد."
    )
    st.stop()


client = genai.Client(
    api_key=api_key
)


uploaded_file = st.file_uploader(
    "PDF خود را آپلود کنید:",
    type=["pdf"]
)


if uploaded_file:

    st.success(
        f"فایل آپلود شد: {uploaded_file.name}"
    )

    pdf_bytes = uploaded_file.getvalue()

    question = st.text_area(
        "سؤال خود را بنویسید:",
        placeholder=(
            "مثلاً: خلاصه این فایل را "
            "در سه خط بگو"
        )
    )

    if st.button("Ask AI"):

        if not question.strip():

            st.warning(
                "لطفاً ابتدا یک سؤال بنویسید."
            )

        else:

            try:

                with st.spinner(
                    "در حال پیدا کردن پاسخ..."
                ):

                    answer = answer_question(
                        client,
                        question,
                        pdf_bytes
                    )

                st.subheader("پاسخ")
                st.write(answer)

            except RuntimeError as error:

                st.error(str(error))

            except Exception:

                st.error(
                    "خطایی در پردازش درخواست رخ داد. "
                    "لطفاً دوباره تلاش کنید."
                )

else:

    st.info(
        "برای شروع، یک فایل PDF آپلود کنید."
    )