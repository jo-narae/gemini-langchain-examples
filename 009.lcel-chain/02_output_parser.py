"""
Step 2: 출력 파서 사용

AIMessage를 문자열로 변환하는 StrOutputParser의 사용법을 학습합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

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
print("Step 2: 출력 파서 사용")
print("=" * 70)
print()

# 파서 생성
parser = StrOutputParser()

# 메시지 구성
messages = [
    SystemMessage(content="너는 미녀와 야수에 나오는 미녀야. 그 캐릭터에 맞게 사용자와 대화하라."),
    HumanMessage(content="안녕? 저는 개스톤입니다. 오늘 시간 괜찮으시면 저녁 같이 먹을까요?"),
]

print("📤 전송 메시지:")
print(f"   User: {messages[1].content}")
print()

# 모델 호출 후 파싱
result = model.invoke(messages)          # AIMessage
parsed_result = parser.invoke(result)    # 문자열로 파싱

print("📥 파싱 전 타입:", type(result).__name__)
print("📥 파싱 후 타입:", type(parsed_result).__name__)
print()
print("🤖 파싱된 응답:", parsed_result)
print()
print("💡 포인트: StrOutputParser는 AIMessage.content를 추출하여 문자열로 변환합니다")
