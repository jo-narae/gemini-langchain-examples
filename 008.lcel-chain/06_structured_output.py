"""
Step 6: 구조화된 출력 (Pydantic 모델)

Pydantic 모델을 사용하여 AI의 응답을 구조화된 데이터로 받는 방법을 학습합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Literal
from pydantic import BaseModel, Field

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
print("Step 6: 구조화된 출력 (Pydantic 모델)")
print("=" * 70)
print()

# Pydantic 모델 정의
class Adlib(BaseModel):
    """스토리 설정과 사용자 입력에 반응하는 대사를 만드는 클래스"""
    answer: str = Field(description="스토리 설정과 사용자와의 대화 기록에 따라 생성된 대사")
    main_emotion: Literal["기쁨", "분노", "슬픔", "공포", "냉소", "불쾌", "중립"] = Field(description="대사의 주요 감정")
    main_emotion_intensity: float = Field(description="대사의 주요 감정의 강도 (0.0 ~ 1.0)")

print("📦 Pydantic 모델 정의:")
print("   - answer: 생성된 대사 (문자열)")
print("   - main_emotion: 주요 감정 (7가지 중 하나)")
print("   - main_emotion_intensity: 감정 강도 (0.0 ~ 1.0)")
print()

# 템플릿 정의
system_template = "너는 {story}에 나오는 {character_a} 역할이다. 그 캐릭터에 맞게 사용자와 대화하라."
human_template = "안녕? 저는 {character_b}입니다. 오늘 시간 괜찮으시면 {activity} 같이 할까요?"

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", human_template),
])

try:
    # 구조화된 출력을 강제하는 모델 생성
    structured_llm = model.with_structured_output(Adlib)
    adlib_chain = prompt_template | structured_llm
    
    print("🔗 체인 구성: prompt_template | structured_llm")
    print("   ➜ Gemini가 Pydantic 모델 형식으로 응답을 생성합니다")
    print()
    
    # 개스톤과의 대화
    print("=" * 50)
    print("💪 시나리오: 개스톤의 저녁 초대")
    print("=" * 50)
    result = adlib_chain.invoke({
        "story": "미녀와 야수",
        "character_a": "벨",
        "character_b": "개스톤",
        "activity": "저녁"
    })
    
    print("📥 구조화된 응답:")
    print(f"   💬 대사: {result.answer}")
    print(f"   😊 감정: {result.main_emotion}")
    print(f"   📊 강도: {result.main_emotion_intensity}")
    print()
    print("💡 포인트: AI 응답이 정의된 구조에 맞춰 자동으로 파싱됩니다!")

except Exception as e:
    # 환경/버전에 따라 미지원일 수 있어 폴백 제공
    print(f"⚠️ 구조화된 출력 지원 안됨: {e}")
    print()
    print("💡 일반 체인으로 대체 실행:")
    
    parser = StrOutputParser()
    fallback_chain = prompt_template | model | parser
    
    result = fallback_chain.invoke({
        "story": "미녀와 야수",
        "character_a": "벨",
        "character_b": "개스톤",
        "activity": "저녁"
    })
    print(f"🤖 일반 응답: {result}")
