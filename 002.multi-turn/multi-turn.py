import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# -----------------------------
# 1) API 키 로드
# -----------------------------
# .env 파일에서 GEMINI_API_KEY 값을 불러옵니다.
# API 키가 없으면 실행을 중단합니다.
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")

# -----------------------------
# 2) 클라이언트 생성
# -----------------------------
# Gemini API를 호출하기 위한 클라이언트 객체를 생성합니다.
client = genai.Client(api_key=api_key)

# -----------------------------
# 3) 시스템 지시어(역할 설정)
# -----------------------------
# 모델의 대답 스타일과 역할을 지정합니다.
# 여기서는 "상담사" 역할로 공감적인 대답을 하도록 설정합니다.
system_instruction = (
    "너는 사용자를 도와주는 상담사야. 공감적으로 답하고, "
    "불명확하면 짧게 되물어봐. 필요하면 단계별로 안내해줘."
)

# -----------------------------
# 4) 대화 히스토리 초기화
# -----------------------------
# 멀티턴 대화를 위해 user / model 메시지를 순서대로 기록할 리스트입니다.
history: list[types.Content] = []

print("대화를 시작합니다. 'exit'으로 종료, 'reset'으로 히스토리 초기화.")

# -----------------------------
# 5) 대화 루프 시작
# -----------------------------
while True:
    try:
        # 사용자 입력 대기
        user_input = input("사용자: ").strip()
    except (EOFError, KeyboardInterrupt):
        # Ctrl+D 또는 Ctrl+C 입력 시 종료
        print("\n종료합니다.")
        break

    if not user_input:  # 빈 입력은 무시
        continue

    if user_input.lower() == "exit":  # 'exit' 입력 시 종료
        print("종료합니다.")
        break

    if user_input.lower() == "reset":  # 'reset' 입력 시 히스토리 초기화
        history = []
        print("히스토리를 초기화했어요.")
        continue

    # -----------------------------
    # 6) 사용자 메시지를 히스토리에 추가
    # -----------------------------
    history.append(
        types.Content(role="user", parts=[types.Part(text=user_input)])
    )

    # -----------------------------
    # 7) 모델 호출 (전체 히스토리 전달)
    # -----------------------------
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=history,  # 지금까지의 대화 기록 전체
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,  # 시스템 지시어 반영
            temperature=0.9,                        # 창의성/가변성 조절
            thinking_config=types.ThinkingConfig(thinking_budget=0),  # Thinking 비활성화
        ),
    )

    # -----------------------------
    # 8) 모델 응답 텍스트 추출
    # -----------------------------
    assistant_text = response.text  # 대표 응답을 편리하게 가져옴

    # -----------------------------
    # 9) 모델 응답을 히스토리에 추가
    # -----------------------------
    history.append(
        types.Content(role="model", parts=[types.Part(text=assistant_text)])
    )

    # -----------------------------
    # 10) 출력
    # -----------------------------
    print("AI:", assistant_text)

    # (선택) 히스토리 길이 확인
    # print(f"(history turns: {len(history)})")