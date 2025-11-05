"""
LangChain Tools 스트리밍 예제

스트리밍 모드에서 도구를 사용하는 핵심 패턴:
1. 도구 호출 청크들을 모으기 (gathered += chunk)
2. 도구 실행
3. 최종 답변 스트리밍
"""

import os
import sys

# Windows 콘솔 UTF-8 인코딩 설정
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from datetime import datetime
import pytz
from pathlib import Path

# 환경설정
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("환경변수 GEMINI_API_KEY가 설정되지 않았습니다.")
os.environ["GOOGLE_API_KEY"] = api_key

print("=" * 60)
print("LangChain Tools 스트리밍 예제")
print("=" * 60)
print()

# 모델 초기화
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
    temperature=0.7,
)

# 도구 정의
@tool
def get_current_time(timezone: str, location: str) -> str:
    """현재 시각을 반환하는 함수

    Args:
        timezone: 타임존 (예: 'Asia/Seoul')
        location: 지역명
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        result = f'{timezone} ({location}) 현재시각 {now}'
        print(f"  🕐 {result}")
        return result
    except Exception as e:
        return f"시간 조회 실패: {str(e)}"

# 도구 설정
tools = [get_current_time]
tool_dict = {"get_current_time": get_current_time}
llm_with_tools = llm.bind_tools(tools)

print("✅ 모델과 도구가 준비되었습니다.")
print()

# -----------------------------
# 핵심 패턴: 스트리밍에서 도구 사용
# -----------------------------
print("=" * 60)
print("스트리밍에서 도구 사용하기")
print("=" * 60)
print()

messages = [
    SystemMessage("너는 사용자의 질문에 답변할 때 반드시 get_current_time 도구를 사용해서 정확한 시간을 조회해야 한다. 시간 관련 질문이 나오면 반드시 도구를 먼저 호출하라."),
    HumanMessage("서울의 현재 시각을 알려주고, 서울의 역사와 주요 관광지에 대해서도 자세히 설명해줘"),
]

print("💬 질문: 서울의 현재 시각을 알려주고, 서울의 역사와 주요 관광지에 대해서도 자세히 설명해줘")
print()

# 1단계: 도구 호출 청크 모으기
print("📍 1단계: 도구 호출 청크 모으기")
response_stream = llm_with_tools.stream(messages)

is_first = True
for chunk in response_stream:
    if is_first:
        is_first = False
        gathered = chunk
    else:
        gathered += chunk  # 핵심: 청크를 누적

print(f"  ✅ 청크 모으기 완료")
print(f"  📋 도구 호출: {gathered.tool_calls}")
print()

messages.append(gathered)

# 2단계: 도구 실행
if gathered.tool_calls:
    print("📍 2단계: 도구 실행")

    for tool_call in gathered.tool_calls:
        tool_name = tool_call["name"]
        selected_tool = tool_dict[tool_name]
        tool_result = selected_tool.invoke(tool_call["args"])

        tool_msg = ToolMessage(
            content=tool_result,
            tool_call_id=tool_call["id"]
        )
        messages.append(tool_msg)

    print()

    # 3단계: 최종 답변 스트리밍
    print("📍 3단계: 최종 답변 스트리밍")
    print("🎯 답변: ", end='')

    for chunk in llm_with_tools.stream(messages):
        print(chunk.content, end='', flush=True)

    print()
