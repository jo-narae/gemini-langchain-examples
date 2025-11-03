"""
Step 5: 완전한 체인 (프롬프트 | 모델 | 파서)

프롬프트 템플릿, 모델, 출력 파서를 모두 연결한 완전한 LCEL 체인을 구성합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
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
print("Step 5: 완전한 체인 (프롬프트 | 모델 | 파서)")
print("=" * 70)
print()

# 템플릿 정의
system_template = "너는 {story}에 나오는 {character_a} 역할이다. 그 캐릭터에 맞게 사용자와 대화하라."
human_template = "안녕? 저는 {character_b}입니다. 오늘 시간 괜찮으시면 {activity} 같이 할까요?"

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", human_template),
])

# 완전한 체인 구성
parser = StrOutputParser()
chain = prompt_template | model | parser

print("🔗 체인 구성: prompt_template | model | parser")
print("   1️⃣ prompt_template: 변수 → 메시지")
print("   2️⃣ model: 메시지 → AIMessage")
print("   3️⃣ parser: AIMessage → 문자열")
print()

# 야수와의 대화
print("=" * 50)
print("🌹 시나리오 1: 야수와의 대화")
print("=" * 50)
result1 = chain.invoke({
    "story": "미녀와 야수",
    "character_a": "미녀",
    "character_b": "야수",
    "activity": "저녁"
})
print("🤖 미녀의 응답:", result1)
print()

# 개스톤과의 대화
print("=" * 50)
print("💪 시나리오 2: 개스톤과의 대화")
print("=" * 50)
result2 = chain.invoke({
    "story": "미녀와 야수",
    "character_a": "미녀",
    "character_b": "개스톤",
    "activity": "저녁"
})
print("🤖 미녀의 응답:", result2)
print()

print("💡 포인트: 한 번 만든 체인으로 다양한 입력을 처리할 수 있습니다!")
