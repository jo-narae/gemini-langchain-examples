import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import Literal
from pydantic import BaseModel, Field

# -----------------------------
# 1) 환경설정
# -----------------------------
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY를 찾을 수 없습니다.")
    exit(1)

# -----------------------------
# 2) Gemini 모델 초기화
# -----------------------------
model = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
    temperature=0.7,
    google_api_key=api_key,
)
print("✅ Gemini 모델이 초기화되었습니다.")

def test_basic_messages():
    """기본 메시지 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 1: 기본 메시지와 모델 호출")
    print("="*50)

    messages = [
        SystemMessage(content="너는 미녀와 야수에 나오는 미녀야. 그 캐릭터에 맞게 사용자와 대화하라."),
        HumanMessage(content="안녕? 저는 개스톤입니다. 오늘 시간 괜찮으시면 저녁 같이 먹을까요?"),
    ]

    result = model.invoke(messages)
    print(f"🤖 AI 응답: {result.content}")
    return result

def test_output_parser():
    """출력 파서 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 2: 출력 파서 사용")
    print("="*50)

    parser = StrOutputParser()

    messages = [
        SystemMessage(content="너는 미녀와 야수에 나오는 미녀야. 그 캐릭터에 맞게 사용자와 대화하라."),
        HumanMessage(content="안녕? 저는 개스톤입니다. 오늘 시간 괜찮으시면 저녁 같이 먹을까요?"),
    ]

    result = model.invoke(messages)          # AIMessage
    parsed_result = parser.invoke(result)    # 문자열로 파싱
    print(f"🤖 파싱된 응답: {parsed_result}")
    return parsed_result

def test_chain_basic():
    """기본 체인 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 3: 기본 체인 (모델 | 파서)")
    print("="*50)

    parser = StrOutputParser()
    chain = model | parser

    messages = [
        SystemMessage(content="너는 미녀와 야수에 나오는 미녀야. 그 캐릭터에 맞게 사용자와 대화하라."),
        HumanMessage(content="안녕? 저는 개스톤입니다. 오늘 시간 괜찮으시면 저녁 같이 먹을까요?"),
    ]

    result = chain.invoke(messages)          # 최종 문자열
    print(f"🤖 체인 응답: {result}")
    return result

def test_prompt_template():
    """프롬프트 템플릿 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 4: 프롬프트 템플릿 사용")
    print("="*50)

    system_template = "너는 {story}에 나오는 {character_a} 역할이다. 그 캐릭터에 맞게 사용자와 대화하라."
    human_template  = "안녕? 저는 {character_b}입니다. 오늘 시간 괜찮으시면 {activity} 같이 할까요?"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("user", human_template),
    ])

    # 프롬프트 템플릿 결과 확인
    prompt_value = prompt_template.invoke({
        "story": "미녀와 야수",
        "character_a": "미녀",
        "character_b": "야수",
        "activity": "저녁"
    })
    # 사람이 보기 좋게:
    print("📋 생성된 메시지들:", prompt_value.to_messages())
    # 또는 print("📋 생성된 프롬프트(문자열):", prompt_value.to_string())

    return prompt_template

def test_complete_chain():
    """완전한 체인 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 5: 완전한 체인 (프롬프트 | 모델 | 파서)")
    print("="*50)

    system_template = "너는 {story}에 나오는 {character_a} 역할이다. 그 캐릭터에 맞게 사용자와 대화하라."
    human_template  = "안녕? 저는 {character_b}입니다. 오늘 시간 괜찮으시면 {activity} 같이 할까요?"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("user", human_template),
    ])

    parser = StrOutputParser()
    chain = prompt_template | model | parser

    # 야수와의 대화
    print("\n🌹 야수와의 대화:")
    result1 = chain.invoke({
        "story": "미녀와 야수",
        "character_a": "미녀",
        "character_b": "야수",
        "activity": "저녁"
    })
    print(f"🤖 미녀의 응답: {result1}")

    # 개스톤과의 대화
    print("\n💪 개스톤과의 대화:")
    result2 = chain.invoke({
        "story": "미녀와 야수",
        "character_a": "미녀",
        "character_b": "개스톤",
        "activity": "저녁"
    })
    print(f"🤖 미녀의 응답: {result2}")

    return chain

def test_structured_output():
    """구조화된 출력 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 6: 구조화된 출력 (Pydantic 모델)")
    print("="*50)

    class Adlib(BaseModel):
        """스토리 설정과 사용자 입력에 반응하는 대사를 만드는 클래스"""
        answer: str = Field(description="스토리 설정과 사용자와의 대화 기록에 따라 생성된 대사")
        main_emotion: Literal["기쁨", "분노", "슬픔", "공포", "냉소", "불쾌", "중립"] = Field(description="대사의 주요 감정")
        main_emotion_intensity: float = Field(description="대사의 주요 감정의 강도 (0.0 ~ 1.0)")

    system_template = "너는 {story}에 나오는 {character_a} 역할이다. 그 캐릭터에 맞게 사용자와 대화하라."
    human_template  = "안녕? 저는 {character_b}입니다. 오늘 시간 괜찮으시면 {activity} 같이 할까요?"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("user", human_template),
    ])

    try:
        # LangChain이 Gemini의 response schema를 활용하여 JSON 구조로 강제
        structured_llm = model.with_structured_output(Adlib)
        adlib_chain = prompt_template | structured_llm

        result = adlib_chain.invoke({
            "story": "미녀와 야수",
            "character_a": "벨",
            "character_b": "개스톤",
            "activity": "저녁"
        })

        print(f"🤖 구조화된 응답:")
        print(f"   💬 대사: {result.answer}")
        print(f"   😊 감정: {result.main_emotion}")
        print(f"   📊 강도: {result.main_emotion_intensity}")

    except Exception as e:
        # 환경/버전에 따라 미지원일 수 있어 안전한 폴백 제공
        print(f"⚠️ 구조화된 출력 지원 안됨: {e}")
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

def main():
    """메인 실행 함수"""
    print("\n🎭 LCEL 체인 예제 - Gemini API 버전")
    print("="*50)

    test_basic_messages()
    test_output_parser()
    test_chain_basic()
    test_prompt_template()
    test_complete_chain()
    test_structured_output()

    print("\n✅ 모든 테스트가 완료되었습니다!")

if __name__ == "__main__":
    main()