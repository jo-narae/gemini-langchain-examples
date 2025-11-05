"""
Step 5-2-1: 모델 초기화 및 기본 설정

메시지 히스토리 시스템의 기본 설정을 학습합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

# 환경 설정
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY를 찾을 수 없습니다.")
    exit(1)

print("=" * 70)
print("Step 1: 모델 초기화 및 메시지 히스토리 시스템 설정")
print("=" * 70)
print()

# ============================================================
# 1. 모델 초기화
# ============================================================
print("📌 1-1. Gemini 모델 초기화")
print("-" * 70)

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

print("✅ Gemini 모델 초기화 완료")
print(f"   - 모델: {os.getenv('GEMINI_MODEL', 'gemini-2.5-flash-lite')}")
print(f"   - Temperature: 0.7")
print(f"   - System Instruction: 설정됨")
print()

# ============================================================
# 2. 메시지 히스토리 시스템 설정
# ============================================================
print("📌 1-2. 메시지 히스토리 시스템 설정")
print("-" * 70)

# 세션 ID별로 대화 기록을 저장할 딕셔너리
store = {}

def get_session_history(session_id: str):
    """세션 ID에 따른 대화 기록 반환 (없으면 새로 생성)"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
        print(f"   ✨ 새로운 세션 생성: {session_id}")
    return store[session_id]

print("✅ get_session_history 함수 정의 완료")
print("   - 세션별로 독립적인 대화 기록 관리")
print("   - InMemoryChatMessageHistory 사용 (메모리 저장)")
print()

# ============================================================
# 3. RunnableWithMessageHistory 래퍼 생성
# ============================================================
print("📌 1-3. RunnableWithMessageHistory 래퍼 생성")
print("-" * 70)

# 모델 실행 시 대화 기록을 자동으로 관리하는 래퍼
with_message_history = RunnableWithMessageHistory(model, get_session_history)

print("✅ RunnableWithMessageHistory 래퍼 생성 완료")
print("   - 메시지 입출력에 자동으로 히스토리 추가")
print("   - 수동으로 append() 할 필요 없음")
print()
