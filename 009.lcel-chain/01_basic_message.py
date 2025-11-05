"""
Step 1: 기본 메시지와 모델 호출

LangChain에서 SystemMessage와 HumanMessage를 사용하여 
Gemini 모델과 기본적인 대화를 하는 방법을 학습합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# 환경설정
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY를 찾을 수 없습니다.")
    exit(1)

# Gemini 모델 초기화
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.7,
    google_api_key=api_key,
)

print("=" * 70)
print("Step 1: 기본 메시지와 모델 호출")
print("=" * 70)
print()

# 메시지 구성
messages = [
    SystemMessage(content="너는 미녀와 야수에 나오는 미녀야. 그 캐릭터에 맞게 사용자와 대화하라."),
    HumanMessage(content="안녕? 저는 개스톤입니다. 오늘 시간 괜찮으시면 저녁 같이 먹을까요?"),
]

print("📤 전송 메시지:")
print(f"   System: {messages[0].content}")
print(f"   User: {messages[1].content}")
print()

# 모델 호출
result = model.invoke(messages)

print("📥 응답 타입:", type(result).__name__)
print("🤖 AI 응답:", result.content)
print()
print("💡 포인트: model.invoke()는 AIMessage 객체를 반환합니다")
