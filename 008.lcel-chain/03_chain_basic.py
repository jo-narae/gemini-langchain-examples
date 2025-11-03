"""
Step 3: 기본 체인 (파이프 연산자)

LCEL의 핵심인 파이프(|) 연산자를 사용하여 
모델과 파서를 연결하는 첫 번째 체인을 만듭니다.
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
print("Step 3: 기본 체인 (모델 | 파서)")
print("=" * 70)
print()

# 파서와 체인 생성
parser = StrOutputParser()
chain = model | parser  # 파이프 연산자로 연결!

print("🔗 체인 구성: model | parser")
print("   ➜ model: AIMessage 생성")
print("   ➜ parser: AIMessage → 문자열 변환")
print()

# 메시지 구성
messages = [
    SystemMessage(content="너는 미녀와 야수에 나오는 미녀야. 그 캐릭터에 맞게 사용자와 대화하라."),
    HumanMessage(content="안녕? 저는 개스톤입니다. 오늘 시간 괜찮으시면 저녁 같이 먹을까요?"),
]

print("📤 전송 메시지:")
print(f"   User: {messages[1].content}")
print()

# 체인 호출 (한 번에 처리!)
result = chain.invoke(messages)

print("📥 결과 타입:", type(result).__name__)
print("🤖 체인 응답:", result)
print()
print("💡 포인트: 체인을 사용하면 model.invoke() → parser.invoke()를 한 번에 처리!")
