"""
Step 5-1: LangChain 기본 - invoke와 메시지 관리

LangChain의 가장 기본적인 사용법을 단계별로 학습합니다.
자세한 설명은 01_langchain_basic.md 파일을 참고하세요.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# 환경 설정
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY를 찾을 수 없습니다.")
    exit(1)

print("=" * 70)
print("LangChain 기본 - invoke와 메시지 관리")
print("=" * 70)
print()

# ============================================================
# Step 1: 모델 초기화
# ============================================================
print("📌 Step 1: 모델 초기화")
print("-" * 70)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.7,
    max_output_tokens=1000,
    google_api_key=api_key
)

print("✅ ChatGoogleGenerativeAI 모델 생성 완료")
print(f"   모델: gemini-2.0-flash-exp")
print(f"   Temperature: 0.7")
print()

# ============================================================
# Step 2: 기본 invoke (문자열 직접 전달)
# ============================================================
print("📌 Step 2: 기본 invoke - 문자열 직접 전달")
print("-" * 70)

question = "파이썬의 주요 특징 3가지를 간단히 알려줘"
print(f"질문: {question}")

response = llm.invoke(question)
print(f"\n타입: {type(response).__name__}")
print(f"내용: {response.content[:100]}...")
print()

# ============================================================
# Step 3: 메시지 리스트로 전달 (구조화)
# ============================================================
print("📌 Step 3: 메시지 리스트로 전달 (추천 방식)")
print("-" * 70)

messages = [
    SystemMessage(content="너는 친절한 프로그래밍 튜터입니다. 초보자도 이해하기 쉽게 설명하세요."),
    HumanMessage(content="Python의 리스트란 무엇인가요?")
]

response = llm.invoke(messages)
print(f"응답:\n{response.content[:200]}...")
print()

# ============================================================
# Step 4: 대화 히스토리 관리 (핵심!)
# ============================================================
print("📌 Step 4: 대화 히스토리 관리 (멀티턴 대화)")
print("-" * 70)

# 새로운 대화 시작
conversation = [
    SystemMessage(content="너는 친절한 프로그래밍 튜터입니다."),
    HumanMessage(content="리스트와 튜플의 차이는 뭔가요?")
]

print(f"현재 메시지 수: {len(conversation)}")
response1 = llm.invoke(conversation)
print(f"AI 응답: {response1.content[:100]}...")

# 중요! AI 응답을 히스토리에 추가해야 맥락 유지
conversation.append(response1)
print(f"\nAI 응답 추가 후 메시지 수: {len(conversation)}")

# 후속 질문 추가
conversation.append(HumanMessage(content="그럼 언제 튜플을 사용하나요?"))
print(f"질문 추가 후 메시지 수: {len(conversation)}")

# "그럼"이라는 단어 사용 가능 (이전 맥락 기억)
response2 = llm.invoke(conversation)
print(f"AI 응답: {response2.content[:150]}...")
print()

# ============================================================
# Step 5: 대화 히스토리 시각화
# ============================================================
print("📌 Step 5: 현재 대화 히스토리 확인")
print("-" * 70)

conversation.append(response2)  # 마지막 응답도 추가

print(f"총 메시지 수: {len(conversation)}")
print("\n대화 흐름:")
for i, msg in enumerate(conversation):
    role = msg.__class__.__name__
    icon = "🤖" if role == "AIMessage" else ("👤" if role == "HumanMessage" else "⚙️")
    content_preview = msg.content[:60] + "..." if len(msg.content) > 60 else msg.content
    print(f"  {icon} [{i+1}] {role:15} {content_preview}")
print()
