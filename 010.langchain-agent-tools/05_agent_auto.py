# -*- coding: utf-8 -*-
"""
Step 5: LangChain Agent - 자동 도구 호출

LangChain 1.0의 create_agent를 사용하면 도구 호출 루프를 자동으로 처리합니다.
Step 3-4의 수동 방식보다 훨씬 간단하고 강력합니다.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from datetime import datetime
import pytz

# 환경설정
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY를 찾을 수 없습니다.")
    exit(1)

# Gemini 모델 초기화
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
    temperature=0.7,
    google_api_key=api_key,
)

# 도구 정의
@tool
def get_current_time(timezone: str, location: str) -> str:
    """현재 시각을 반환하는 함수

    Args:
        timezone (str): 타임존 (예: 'Asia/Seoul')
        location (str): 지역명
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f'{timezone} ({location}) 현재시각 {now}'
    except Exception as e:
        return f"시간 조회 실패: {str(e)}"

print("=" * 70)
print("Step 5: LangChain Agent - 자동 도구 호출")
print("=" * 70)
print()

# 도구 리스트
tools = [get_current_time]

print("🔧 도구 설정:")
print(f"  📋 사용 가능한 도구: {[tool.name for tool in tools]}")
print()

# LangChain Agent 생성 (LangChain 1.0 방식)
# create_agent는 도구 호출 루프를 자동으로 처리합니다
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="너는 사용자의 질문에 답변을 하기 위해 도구를 사용할 수 있는 AI 어시스턴트입니다."
)

print("✅ LangChain Agent가 생성되었습니다.")
print("💡 Step 3-4와 달리 tool_calls를 수동으로 처리할 필요가 없습니다!")
print()

# 테스트 질문들
test_questions = [
    "부산은 지금 몇시야?",
    "도쿄의 현재 시간은?",
]

for question in test_questions:
    print("=" * 70)
    print(f"💬 질문: {question}")
    print("-" * 70)

    try:
        # LangGraph Agent는 메시지 형태로 입력을 받습니다
        result = agent.invoke({"messages": [("user", question)]})

        # 결과에서 마지막 메시지를 가져옵니다
        final_message = result["messages"][-1]
        print("-" * 70)
        print(f"🎯 최종 답변: {final_message.content}")
        print()

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print()
