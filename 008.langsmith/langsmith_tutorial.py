"""
LangSmith 튜토리얼 - LLM 애플리케이션 추적 및 모니터링

상세 가이드: langsmith_tutorial.md 참고
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationChain

load_dotenv()

print("=" * 70)
print("LangSmith 튜토리얼 - LLM 애플리케이션 추적 및 모니터링")
print("=" * 70)
print()

def step1_setup():
    """Step 1: LangSmith 설정 확인"""
    print("📌 Step 1: LangSmith 설정 확인")
    print("=" * 70)
    print()

    google_api_key = os.environ.get("GOOGLE_API_KEY")
    langchain_tracing = os.environ.get("LANGCHAIN_TRACING_V2")
    langchain_api_key = os.environ.get("LANGCHAIN_API_KEY")
    langchain_project = os.environ.get("LANGCHAIN_PROJECT", "default")

    print("🔍 환경변수 상태:")
    print(f"  ✓ GOOGLE_API_KEY: {'설정됨' if google_api_key else '❌ 없음'}")
    print(f"  ✓ LANGCHAIN_TRACING_V2: {langchain_tracing or '❌ 없음 (추적 비활성화)'}")
    print(f"  ✓ LANGCHAIN_API_KEY: {'설정됨' if langchain_api_key else '❌ 없음'}")
    print(f"  ✓ LANGCHAIN_PROJECT: {langchain_project}")
    print()

    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found. Please check .env file")

    if langchain_tracing == "true" and langchain_api_key:
        print("✅ LangSmith 추적이 활성화되었습니다!")
        print(f"   프로젝트: {langchain_project}")
        print("   https://smith.langchain.com 에서 확인하세요.")
    else:
        print("⚠️ LangSmith 추적이 비활성화되었습니다.")
        print("   상세 설정 방법은 langsmith_tutorial.md 파일을 참고하세요.")

    print()
    return google_api_key, langchain_tracing == "true"

def step2_basic_tracking(llm):
    """Step 2: 기본 추적 (단일 LLM 호출)"""
    print("=" * 70)
    print("📌 Step 2: 기본 추적 - 단일 LLM 호출")
    print("=" * 70)
    print()

    print("💬 테스트 2-1: 간단한 질문")
    print("-" * 70)
    question1 = "파이썬의 주요 특징 3가지를 간단히 알려줘"
    print(f"질문: {question1}")
    print()

    response1 = llm.invoke(question1)
    print(f"🤖 AI 응답:\n{response1.content}")
    print()

    print("💬 테스트 2-2: 복잡한 질문")
    print("-" * 70)
    question2 = "머신러닝과 딥러닝의 차이점을 초보자도 이해할 수 있게 설명해줘"
    print(f"질문: {question2}")
    print()

    response2 = llm.invoke(question2)
    print(f"🤖 AI 응답:\n{response2.content}")
    print()

def step3_streaming_tracking(llm):
    """Step 3: 스트리밍 추적"""
    print("=" * 70)
    print("📌 Step 3: 스트리밍 응답 추적")
    print("=" * 70)
    print()

    question = "웹 개발 초보자를 위한 학습 로드맵을 단계별로 작성해줘"
    print(f"💬 질문: {question}")
    print()
    print("🤖 AI 응답 (스트리밍):")
    print("-" * 70)

    for chunk in llm.stream(question):
        print(chunk.content, end="", flush=True)

    print()
    print("-" * 70)
    print()

def step4_conversation_tracking(llm):
    """Step 4: 대화 체인 추적"""
    print("=" * 70)
    print("📌 Step 4: 대화 체인 추적 (ConversationChain)")
    print("=" * 70)
    print()

    memory = ConversationBufferMemory()
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )

    dialogue = [
        "안녕하세요! 저는 파이썬을 배우고 싶어요.",
        "파이썬으로 무엇을 만들 수 있나요?",
        "웹 개발을 하려면 어떤 프레임워크를 배워야 하나요?",
        "Django와 Flask 중 어떤 것을 추천하시나요?"
    ]

    print("💬 연속 대화 시작:")
    print("=" * 70)

    for i, question in enumerate(dialogue, 1):
        print(f"\n[대화 {i}]")
        print(f"👤 사용자: {question}")
        answer = conversation.predict(input=question)
        print(f"🤖 AI: {answer}")
        print("-" * 70)

    print()

def step5_advanced_features(llm):
    """Step 5: 고급 기능 (태그, 메타데이터)"""
    print("=" * 70)
    print("📌 Step 5: 고급 추적 기능 (태그, 메타데이터)")
    print("=" * 70)
    print()

    print("🏷️ 테스트 5-1: 태그를 사용한 분류")
    print("-" * 70)
    question = "LangChain이 뭐야?"
    print(f"질문: {question}")
    print("태그: ['tutorial', 'langchain', 'beginner']")
    print()

    response = llm.invoke(
        question,
        config={"tags": ["tutorial", "langchain", "beginner"]}
    )
    print(f"🤖 AI 응답:\n{response.content}")
    print()

    print("📊 테스트 5-2: 메타데이터 추가")
    print("-" * 70)
    question = "Python의 리스트와 튜플의 차이는?"
    print(f"질문: {question}")
    print("메타데이터: user_id=user_123, session=session_456")
    print()

    response = llm.invoke(
        question,
        config={
            "metadata": {
                "user_id": "user_123",
                "session": "session_456",
                "environment": "development"
            }
        }
    )
    print(f"🤖 AI 응답:\n{response.content}")
    print()

def step6_dashboard_guide():
    """Step 6: LangSmith 대시보드 활용 가이드"""
    print("=" * 70)
    print("📌 Step 6: LangSmith 대시보드 활용법")
    print("=" * 70)
    print()

    print("🌐 대시보드 접속: https://smith.langchain.com")
    print()
    print("📊 확인 가능한 정보:")
    print("   - 총 실행 횟수 및 성공/실패율")
    print("   - 평균 응답 시간")
    print("   - 토큰 사용량 및 예상 비용")
    print("   - 개별 실행의 입력/출력 데이터")
    print("   - 체인 실행 흐름 시각화")
    print("   - 에러 추적 및 디버깅 정보")
    print()
    print("💡 상세 활용법은 langsmith_tutorial.md 파일을 참고하세요.")
    print()

def main():
    """메인 실행 함수"""
    try:
        api_key, tracing_enabled = step1_setup()

        print("🤖 Gemini 모델 초기화 중...")
        llm = ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
            temperature=0.7
        )
        print("✅ 모델 초기화 완료!")
        print()

        step2_basic_tracking(llm)
        step3_streaming_tracking(llm)
        step4_conversation_tracking(llm)
        step5_advanced_features(llm)
        step6_dashboard_guide()

        print("=" * 70)
        print("🎉 튜토리얼 완료!")
        print("=" * 70)
        print()

        if tracing_enabled:
            print("✅ LangSmith 대시보드에서 모든 실행 내역을 확인하세요:")
            print("   https://smith.langchain.com")
            print()
            print("📊 확인 가능한 내역:")
            print("   - Step 2: 단일 LLM 호출 2건")
            print("   - Step 3: 스트리밍 호출 1건")
            print("   - Step 4: 대화 체인 (4턴)")
            print("   - Step 5: 태그/메타데이터가 포함된 호출 2건")
        else:
            print("⚠️ LangSmith 추적이 비활성화되어 있습니다.")
            print("   .env 파일에 LangSmith 설정을 추가하면 추적 기능을 사용할 수 있습니다.")
            print("   상세 설정 방법: langsmith_tutorial.md")

        print()
        print("📚 학습 내용 정리:")
        print("   1. LangSmith는 환경변수만으로 자동 추적")
        print("   2. 모든 LLM 호출(invoke, stream)이 기록됨")
        print("   3. ConversationChain 같은 복잡한 체인도 시각화")
        print("   4. 태그와 메타데이터로 실행 분류 및 검색")
        print("   5. 대시보드에서 성능, 비용, 에러 분석 가능")
        print("=" * 70)

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print()
        print("💡 문제 해결:")
        print("   1. .env 파일에 GOOGLE_API_KEY가 설정되어 있는지 확인")
        print("   2. LangSmith를 사용하려면 LANGCHAIN_API_KEY도 필요")
        print("   3. 상세 내용: langsmith_tutorial.md 참고")

if __name__ == "__main__":
    main()
