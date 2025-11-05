import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. .env 로드
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")

# 2. 클라이언트 초기화
client = genai.Client(api_key=api_key)

# 3. 시스템 지시어 (system_instruction)
system_instruction = (
    "당신은 유치원 선생님입니다. 쉽고 친절하게 한 문장으로 대답해 주세요."
)

# 4. 프롬프트 (One-shot: 1개의 예시 제공)
prompt = """
[예시]
학생: 고양이는 무슨 동물일까요?
선생님: 고양이는 귀여운 털이 있는 집에서 기르는 동물이에요.

[질문]
학생: 호랑이는 무슨 동물일까요?
선생님:
"""

# 5. 모델 호출 (신 SDK 방식)
response = client.models.generate_content(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),   # 모델명 문자열로 직접 지정
    contents=prompt,            # 사용자 프롬프트
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,           # 시스템 지시어를 config에 전달
        thinking_config=types.ThinkingConfig(thinking_budget=0)  # Thinking 비활성화
    ),
)

# 6. 응답 출력
print(response.text)