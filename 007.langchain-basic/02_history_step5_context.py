"""
Step 5-2-5: 대화 맥락 연결

새로운 주제로 대화를 이어가면서 이전 맥락을 유지하는 방법을 학습합니다.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Rate Limit 재시도 경고 메시지 숨기기 (실제 에러는 여전히 표시됨)
logging.getLogger("langchain_google_genai").setLevel(logging.ERROR)

# 환경 설정
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY를 찾을 수 없습니다.")
    exit(1)

# 모델 및 히스토리 시스템 설정
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.7,
    google_api_key=api_key,
    max_retries=5,  # 재시도 횟수 증가
    request_timeout=60,  # 타임아웃 증가
    model_kwargs={
        "system_instruction": (
            "너는 사용자를 도와주는 상담사야. 공감적으로 답하고, "
            "모호하면 짧게 되물어봐. 필요하면 단계별로 안내해줘."
        )
    },
)

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(model, get_session_history)

print("=" * 70)
print("Step 5: 대화 맥락 연결")
print("=" * 70)
print()

# ============================================================
# 세션 abc2 재현 (전체 이전 대화)
# ============================================================
print("📌 5-1. 세션 abc2 재현")
print("-" * 70)

config = {"configurable": {"session_id": "abc2"}}

# 이전 대화 재현
with_message_history.invoke([HumanMessage(content="안녕? 난 김철수이야.")], config)
with_message_history.invoke([HumanMessage(content="내 이름이 뭐지?")], config)
with_message_history.invoke([HumanMessage(content="내가 어느 나라 사람인지 추측하고, 그 나라 문화 한 가지를 말해줘")], config)

print("✅ 세션 abc2 준비 완료")
print(f"   현재 메시지 수: {len(store['abc2'].messages)}개")
print()

# ============================================================
# 새로운 주제로 대화
# ============================================================
print("📌 5-2. 새로운 주제로 대화")
print("-" * 70)

print("👤 사용자: 오늘 날씨가 좋다면 뭘 하면 좋을까?")
print("🤖 AI 응답 중...")
print()

response = with_message_history.invoke(
    [HumanMessage(content="오늘 날씨가 좋다면 뭘 하면 좋을까?")],
    config,
)

print(f"🤖 AI: {response.content}")
print()

# ============================================================
# 이전 대화 맥락 연결
# ============================================================
print("📌 5-3. 이전 대화 맥락 연결")
print("-" * 70)

print("👤 사용자: 아까 내 이름과 함께 추천해줄 수 있어?")
print("🤖 AI 응답 중...")
print()

response = with_message_history.invoke(
    [HumanMessage(content="아까 내 이름과 함께 추천해줄 수 있어?")],
    config,
)

print(f"🤖 AI: {response.content}")
print()

# ============================================================
# 전체 대화 기록 확인
# ============================================================
print("📌 5-4. 전체 대화 기록")
print("-" * 70)

print(f"💬 세션 'abc2'의 전체 대화:")
print()
for i, message in enumerate(store['abc2'].messages, 1):
    speaker = "👤 사용자" if message.__class__.__name__ == "HumanMessage" else "🤖 AI"
    content = message.content[:80] + "..." if len(message.content) > 80 else message.content
    print(f"{i}. {speaker}: {content}")
print()
