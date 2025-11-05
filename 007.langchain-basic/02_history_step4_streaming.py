"""
Step 5-2-4: 스트리밍 응답

실시간으로 응답을 받아 출력하는 방법을 학습합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# 환경 설정
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY를 찾을 수 없습니다.")
    exit(1)

# 모델 및 히스토리 시스템 설정
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
print("Step 4: 스트리밍 응답")
print("=" * 70)
print()

# ============================================================
# 세션 abc2 재현 (이전 대화 맥락)
# ============================================================
print("📌 4-1. 세션 abc2 재현")
print("-" * 70)

config = {"configurable": {"session_id": "abc2"}}

# 이전 대화 재현
with_message_history.invoke(
    [HumanMessage(content="안녕? 난 김철수이야.")],
    config,
)

print("✅ 세션 abc2 준비 완료")
print()

# ============================================================
# 일반 응답 (비교용)
# ============================================================
print("📌 4-2. 일반 응답 방식 (invoke)")
print("-" * 70)

print("👤 사용자: 파이썬의 장점을 말해줘")
print("🤖 AI 응답 대기 중...")
print()

response = with_message_history.invoke(
    [HumanMessage(content="파이썬의 장점을 말해줘")],
    config,
)

print(f"🤖 AI: {response.content[:200]}...")
print()
print("💡 일반 방식: 전체 응답이 완성될 때까지 대기")
print()

# ============================================================
# 스트리밍 응답
# ============================================================
print("📌 4-3. 스트리밍 응답 방식 (stream)")
print("-" * 70)

print("👤 사용자: 내가 어느 나라 사람인지 추측하고, 그 나라 문화 한 가지를 말해줘")
print()
print("🤖 AI (실시간 스트리밍): ", end="", flush=True)

for chunk in with_message_history.stream(
    [HumanMessage(content="내가 어느 나라 사람인지 추측하고, 그 나라 문화 한 가지를 말해줘")],
    config,
):
    print(chunk.content, end="", flush=True)

print("\n")
print("💡 스트리밍 방식: 응답이 생성되는 대로 즉시 출력")
print()
