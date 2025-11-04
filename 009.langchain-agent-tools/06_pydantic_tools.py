# -*- coding: utf-8 -*-
"""
Step 6: Pydantic로 복잡한 도구 입력 정의하기

Pydantic 모델을 사용하여 복잡한 구조의 도구 입력을 정의하고 검증하는 방법을 학습합니다.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from pydantic import BaseModel, Field

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

print("=" * 70)
print("Step 6: Pydantic로 복잡한 도구 입력 정의하기")
print("=" * 70)
print()

# -----------------------------
# 1) Pydantic 모델 정의
# -----------------------------
class StockHistoryInput(BaseModel):
    """주식 조회를 위한 입력 모델"""
    ticker: str = Field(..., title="주식 코드", description="주식 코드 (예: AAPL, TSLA, MSFT)")
    period: str = Field(..., title="기간", description="주식 데이터 조회 기간 (예: 1d, 5d, 1mo, 3mo, 6mo, 1y)")

print("📋 Pydantic 모델 정의:")
print(f"  - 모델명: StockHistoryInput")
for field_name, field in StockHistoryInput.model_fields.items():
    title = getattr(field, 'title', field_name)
    description = getattr(field, 'description', '설명 없음')
    print(f"  - {field_name}: {title} - {description}")
print()

# -----------------------------
# 2) Pydantic 모델을 사용하는 도구 정의
# -----------------------------
@tool
def get_stock_history(stock_history_input: StockHistoryInput) -> str:
    """주식 종목의 가격 데이터를 조회하는 함수

    yfinance를 사용하여 실시간 주식 데이터를 가져옵니다.
    """
    try:
        import yfinance as yf

        ticker = stock_history_input.ticker.upper()
        period = stock_history_input.period

        print(f"  🔍 주식 조회 중: {ticker} ({period})")

        # yfinance로 주식 데이터 가져오기
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            return f"❌ {ticker} 주식 데이터를 찾을 수 없습니다. 티커를 확인해주세요."

        # 최근 5개 데이터 포맷팅
        recent_data = hist.tail(5)

        # 결과 포맷팅
        result = f"📊 {ticker} 주식 데이터 ({period}):\n\n"
        result += "| Date       | Open   | High   | Low    | Close  | Volume     |\n"
        result += "|------------|--------|--------|--------|--------|------------|\n"

        for date, row in recent_data.iterrows():
            date_str = date.strftime('%Y-%m-%d')
            open_price = f"${row['Open']:.2f}"
            high_price = f"${row['High']:.2f}"
            low_price = f"${row['Low']:.2f}"
            close_price = f"${row['Close']:.2f}"
            volume = f"{row['Volume']:,}"

            result += f"| {date_str} | {open_price:>7} | {high_price:>7} | {low_price:>7} | {close_price:>7} | {volume:>10} |\n"

        # 현재 가격 정보 추가
        current_price = stock.info.get('currentPrice', hist['Close'].iloc[-1])
        result += f"\n💰 현재 가격: ${current_price:.2f}"

        return result

    except ImportError:
        return "❌ yfinance 패키지가 설치되지 않았습니다. 'pip install yfinance'로 설치해주세요."
    except Exception as e:
        error_msg = f"주식 데이터 조회 실패: {str(e)}"
        return error_msg

print("✅ Pydantic 도구 정의 완료")
print("  - 도구명: get_stock_history")
print("  - 입력 모델: StockHistoryInput (ticker, period)")
print()

# -----------------------------
# 3) Agent 생성 및 테스트
# -----------------------------
tools = [get_stock_history]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="너는 주식 정보를 조회할 수 있는 AI 어시스턴트입니다. 사용자의 질문에 도구를 사용하여 답변하세요."
)

print("✅ Agent가 생성되었습니다.")
print("💡 Pydantic 모델이 도구 입력을 자동으로 검증합니다.")
print()

# 테스트 질문들
test_questions = [
    "테슬라 주식의 최근 1개월 성과는?",
    "애플의 최근 5일 주가는?",
]

for question in test_questions:
    print("=" * 70)
    print(f"💬 질문: {question}")
    print("-" * 70)

    try:
        result = agent.invoke({"messages": [("user", question)]})
        final_message = result["messages"][-1]
        print("-" * 70)
        print(f"🎯 최종 답변:\n{final_message.content}")
        print()

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print()

