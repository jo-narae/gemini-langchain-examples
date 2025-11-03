import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# -----------------------------
# 1) API 키 로드
# -----------------------------
# .env 파일에서 GEMINI_API_KEY 값을 불러옵니다.
# 없으면 프로그램 실행을 중단합니다.
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")

# -----------------------------
# 2) 클라이언트 생성
# -----------------------------
# genai.Client를 초기화하여 Gemini API와 통신할 준비를 합니다.
client = genai.Client(api_key=api_key)

# -----------------------------
# 3) 시스템 지시어(역할 설정)
# -----------------------------
# 모델이 어떤 역할/스타일로 답변할지를 지정합니다.
system_instruction = (
    "당신은 사용자를 도와주는 유용한 조수입니다. "
    "항상 친절하고 도움이 되는 답변을 제공하세요."
)

# -----------------------------
# 4) 싱글턴 호출
# -----------------------------
# 사용자 입력을 반복적으로 받고, 그 입력을 모델에 전달합니다.
while True:
    user_input = input("사용자: ")
    if user_input.lower() == "exit":
        break

    # 모델 호출
    response = client.models.generate_content(
        model="gemini-2.0-flash",     # 사용할 Gemini 모델
        contents=user_input,          # 사용자 입력 프롬프트
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,   # 시스템 지시어 반영
            temperature=0.9,                         # 창의성/가변성 조절 (0=일관, 1=창의적)
            thinking_config=types.ThinkingConfig(
                thinking_budget=0                    # Thinking 모드 비활성화 (옵션)
            )
        ),
    )

    # -----------------------------
    # 5) 응답 출력
    # -----------------------------
    # 모델이 생성한 답변을 출력합니다.
    print("AI:", response.text)