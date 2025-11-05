# -----------------------------
# 1) 라이브러리 임포트
# -----------------------------
import os
from dotenv import load_dotenv   # .env 환경변수 로드
from google import genai         # Google Gemini API SDK
from google.genai import types   # 요청/응답 설정 타입

# -----------------------------
# 2) API 키 로드
# -----------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")

# -----------------------------
# 3) 클라이언트 생성
# -----------------------------
client = genai.Client(api_key=api_key)

# -----------------------------
# 4) 모델 호출
# -----------------------------
response = client.models.generate_content(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),   # 사용할 모델
    contents="이 문장이 긍정적인지 부정적인지 분류해줘: '오늘 날씨 좋다'",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0)  # Thinking 비활성화
    )
)

# -----------------------------
# 5) 응답 출력
# -----------------------------
print(response.text)