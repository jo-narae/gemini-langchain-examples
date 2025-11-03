"""
Step 4: 프롬프트 템플릿

ChatPromptTemplate을 사용하여 동적으로 프롬프트를 생성하는 방법을 학습합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 환경설정
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY를 찾을 수 없습니다.")
    exit(1)

print("=" * 70)
print("Step 4: 프롬프트 템플릿")
print("=" * 70)
print()

# 템플릿 정의
system_template = "너는 {story}에 나오는 {character_a} 역할이다. 그 캐릭터에 맞게 사용자와 대화하라."
human_template = "안녕? 저는 {character_b}입니다. 오늘 시간 괜찮으시면 {activity} 같이 할까요?"

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", human_template),
])

print("📝 템플릿 정의:")
print(f"   System: {system_template}")
print(f"   User: {human_template}")
print()

# 템플릿에 값 채우기
prompt_value = prompt_template.invoke({
    "story": "미녀와 야수",
    "character_a": "미녀",
    "character_b": "야수",
    "activity": "저녁"
})

print("🔄 생성된 메시지:")
for msg in prompt_value.to_messages():
    role = msg.__class__.__name__
    print(f"   {role}: {msg.content}")
print()

print("💡 포인트: 템플릿을 사용하면 동일한 구조로 다양한 프롬프트를 생성할 수 있습니다!")
print()

# 다른 값으로 다시 생성
prompt_value2 = prompt_template.invoke({
    "story": "미녀와 야수",
    "character_a": "미녀",
    "character_b": "개스톤",
    "activity": "사냥"
})

print("🔄 다른 값으로 생성:")
for msg in prompt_value2.to_messages():
    role = msg.__class__.__name__
    print(f"   {role}: {msg.content}")
