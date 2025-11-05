"""
Step 5-2-3: 새로운 세션 - 독립적인 대화

새로운 세션을 만들어서 세션 간 독립성을 확인합니다.
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
print("Step 3: 새로운 세션 - 독립적인 대화")
print("=" * 70)
print()

# ============================================================
# 먼저 abc2 세션 재현 (이전 대화 복원)
# ============================================================
print("📌 3-1. 세션 abc2 재현 (이전 대화)")
print("-" * 70)

config_abc2 = {"configurable": {"session_id": "abc2"}}

# 이전 대화 재현
with_message_history.invoke(
    [HumanMessage(content="안녕? 난 김철수이야.")],
    config_abc2,
)
with_message_history.invoke(
    [HumanMessage(content="내 이름이 뭐지?")],
    config_abc2,
)

print("✅ 세션 abc2에 이전 대화 기록 저장됨")
print(f"   메시지 수: {len(store['abc2'].messages)}개")
print()

# ============================================================
# 새로운 세션 abc3 생성
# ============================================================
print("📌 3-2. 새 세션 abc3에서 동일한 질문")
print("-" * 70)

config_abc3 = {"configurable": {"session_id": "abc3"}}

print("👤 사용자 (새 세션): 내 이름이 뭐지?")
print("🤖 AI 응답 중...")
print()

response = with_message_history.invoke(
    [HumanMessage(content="내 이름이 뭐지?")],
    config_abc3,
)

print(f"🤖 AI: {response.content}")
print()

# ============================================================
# 세션 abc2로 복귀
# ============================================================
print("📌 3-3. 세션 abc2로 복귀")
print("-" * 70)

print("👤 사용자 (abc2): 아까 우리가 무슨 얘기 했지?")
print("🤖 AI 응답 중...")
print()

response = with_message_history.invoke(
    [HumanMessage(content="아까 우리가 무슨 얘기 했지?")],
    config_abc2,
)

print(f"🤖 AI: {response.content}")
print()

# ============================================================
# 세션 상태 비교
# ============================================================
print("📌 3-4. 세션 상태 비교")
print("-" * 70)

print(f"전체 활성 세션: {len(store)}개")
print()
print("세션별 메시지 수:")
for session_id in store.keys():
    message_count = len(store[session_id].messages)
    print(f"  • 세션 {session_id}: {message_count}개 메시지")
print()
