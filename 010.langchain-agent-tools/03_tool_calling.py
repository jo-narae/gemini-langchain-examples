# -*- coding: utf-8 -*-
"""
Step 3: 도구 호출 기본 (수동 방식)

모델에 도구를 바인딩하고, AI가 도구를 호출하여 답변하는 방법을 학습합니다.
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
print("Step 3: 도구 호출 기본")
print("=" * 70)
print()

# 도구를 모델에 바인딩
tools = [get_current_time]
tool_dict = {"get_current_time": get_current_time}
llm_with_tools = llm.bind_tools(tools)

print("🔗 도구가 모델에 바인딩되었습니다.")
print(f"📋 사용 가능한 도구: {[tool.name for tool in tools]}")
print()

# 사용자 질문
messages = [
    SystemMessage("너는 사용자의 질문에 답변을 하기 위해 tools를 사용할 수 있다."),
    HumanMessage("부산은 지금 몇시야?"),
]

print("💬 사용자 질문: 부산은 지금 몇시야?")
print()

# AI 응답 (도구 호출 포함)
response = llm_with_tools.invoke(messages)
messages.append(response)

print(f"🤖 AI 응답: {response.content}")

# 도구 호출 확인
if hasattr(response, 'tool_calls') and response.tool_calls:
    print(f"🔧 호출된 도구 수: {len(response.tool_calls)}")
    print()
    
    # 각 도구 호출 처리
    for tool_call in response.tool_calls:
        selected_tool = tool_dict[tool_call["name"]]
        print(f"🛠️  도구 호출: {tool_call['name']}")
        print(f"📥 전달된 인자: {tool_call['args']}")
        
        # 도구 실행
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)
        print(f"📤 도구 결과: {tool_msg.content}")
        print()
    
    # 도구 실행 결과를 바탕으로 최종 답변 생성
    print("🔄 도구 실행 결과를 바탕으로 최종 답변 생성 중...")
    final_response = llm_with_tools.invoke(messages)
    print(f"🎯 최종 답변: {final_response.content}")
else:
    print("ℹ️  도구 호출이 없었습니다.")
