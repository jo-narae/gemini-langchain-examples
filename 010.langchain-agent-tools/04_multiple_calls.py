# -*- coding: utf-8 -*-
"""
Step 4: 여러 지역 시간 조회 (수동 방식)

여러 지역의 시간을 조회하면서 도구 호출 패턴을 학습합니다.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
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
    model="gemini-2.0-flash-exp",
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
print("Step 4: 여러 지역 시간 조회")
print("=" * 70)
print()

# 도구 설정
tools = [get_current_time]
tool_dict = {"get_current_time": get_current_time}
llm_with_tools = llm.bind_tools(tools)

# 테스트 질문들
test_questions = [
    "서울은 지금 몇시야?",
    "도쿄의 현재 시간은?",
    "뉴욕은 지금 몇시지?",
    "런던의 현재 시간을 알려줘"
]

for question in test_questions:
    print(f"💬 질문: {question}")

    messages = [
        SystemMessage("너는 사용자의 질문에 답변을 하기 위해 tools를 사용할 수 있다."),
        HumanMessage(question),
    ]

    try:
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if hasattr(response, 'tool_calls') and response.tool_calls:
            for tool_call in response.tool_calls:
                selected_tool = tool_dict[tool_call["name"]]
                tool_msg = selected_tool.invoke(tool_call["args"])
                messages.append(tool_msg)

            final_response = llm_with_tools.invoke(messages)
            print(f"🎯 답변: {final_response.content}")
        else:
            print(f"🤖 답변: {response.content}")

        print()

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print()
