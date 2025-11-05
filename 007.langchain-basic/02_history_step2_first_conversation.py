"""
Step 5-2-2: 첫 번째 대화 - 세션 생성 및 이름 기억

세션을 생성하고 AI가 사용자 정보를 기억하는지 확인합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# 환경 설정 (Step 1과 동일)
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY를 찾을 수 없습니다.")
    exit(1)

# 모델 및 히스토리 시스템 설정 (Step 1과 동일)
model = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
    temperature=0.7,
    google_api_key=api_key,
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
print("Step 2: 첫 번째 대화 - 세션 생성 및 이름 기억")
print("=" * 70)
print()

# ============================================================
# 세션 abc2에서 대화 시작
# ============================================================
print("📌 2-1. 세션 abc2 생성 및 자기소개")
print("-" * 70)

config = {"configurable": {"session_id": "abc2"}}

# 첫 메시지: 자기소개
print("👤 사용자: 안녕? 난 김철수이야.")
print("🤖 AI 응답 중...")
print()

response = with_message_history.invoke(
    [HumanMessage(content="안녕? 난 김철수이야.")],
    config=config,
)

print(f"🤖 AI: {response.content}")
print()

# ============================================================
# 같은 세션에서 이름 확인
# ============================================================
print("📌 2-2. AI가 이름을 기억하는지 확인")
print("-" * 70)

print("👤 사용자: 내 이름이 뭐지?")
print("🤖 AI 응답 중...")
print()

response = with_message_history.invoke(
    [HumanMessage(content="내 이름이 뭐지?")],
    config=config,
)

print(f"🤖 AI: {response.content}")
print()

# ============================================================
# 현재 세션 상태 확인
# ============================================================
print("📌 2-3. 현재 세션 상태")
print("-" * 70)

print(f"활성 세션 수: {len(store)}")
for session_id in store.keys():
    message_count = len(store[session_id].messages)
    print(f"  • 세션 {session_id}: {message_count}개 메시지")
print()
