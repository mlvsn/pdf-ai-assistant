from google import genai
from rag import answer_question
import os


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


question = input("سؤال شما: ")

answer = answer_question(
    client,
    question
)

print("\n--- پاسخ ---")
print(answer)