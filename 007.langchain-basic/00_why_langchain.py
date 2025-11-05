"""
Step 5-0: 왜 LangChain을 사용하나?

Gemini API를 직접 사용하는 것과 LangChain을 사용하는 것의 차이를 비교합니다.
자세한 설명은 00_why_langchain.md 파일을 참고하세요.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# 환경 설정
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY를 찾을 수 없습니다.")
    exit(1)

print("=" * 70)
print("왜 LangChain을 사용하나? - Gemini API vs LangChain 비교")
print("=" * 70)
print()

# ============================================================
# Part 1: Gemini API 직접 사용 (최신 google-genai SDK)
# ============================================================
print("📌 Part 1: Gemini API 직접 사용")
print("=" * 70)

client = genai.Client(api_key=api_key)
system_instruction = "너는 친절한 AI 어시스턴트입니다."

# 단일 질문
print("\n✅ 단일 질문:")
response = client.models.generate_content(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
    contents="파이썬이란?",
    config=types.GenerateContentConfig(system_instruction=system_instruction)
)
print(f"응답: {response.text[:100]}...")

# 대화 히스토리 관리
print("\n✅ 대화 히스토리 관리:")
history = []

# 첫 번째 질문
history.append(types.Content(role="user", parts=[types.Part(text="파이썬이란?")]))
response1 = client.models.generate_content(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
    contents=history,
    config=types.GenerateContentConfig(system_instruction=system_instruction)
)
print(f"Q1: 파이썬이란?")
print(f"A1: {response1.text[:80]}...")
history.append(types.Content(role="model", parts=[types.Part(text=response1.text)]))

# 두 번째 질문
history.append(types.Content(role="user", parts=[types.Part(text="그럼 자바는?")]))
response2 = client.models.generate_content(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
    contents=history,
    config=types.GenerateContentConfig(system_instruction=system_instruction)
)
print(f"Q2: 그럼 자바는?")
print(f"A2: {response2.text[:80]}...")

# ============================================================
# Part 2: LangChain 사용 (권장 방식)
# ============================================================
print("\n\n📌 Part 2: LangChain 사용")
print("=" * 70)

langchain_model = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
    temperature=0.7,
    google_api_key=api_key
)

# 단일 질문
print("\n✅ 단일 질문:")
response = langchain_model.invoke("파이썬이란?")
print(f"응답: {response.content[:100]}...")

# 대화 히스토리 관리
print("\n✅ 대화 히스토리 관리:")
messages = [
    SystemMessage(content="너는 친절한 AI 어시스턴트입니다."),
    HumanMessage(content="파이썬이란?")
]
response1 = langchain_model.invoke(messages)
print(f"Q1: 파이썬이란?")
print(f"A1: {response1.content[:80]}...")

messages.append(response1)
messages.append(HumanMessage(content="그럼 자바는?"))
response2 = langchain_model.invoke(messages)
print(f"Q2: 그럼 자바는?")
print(f"A2: {response2.content[:80]}...")
