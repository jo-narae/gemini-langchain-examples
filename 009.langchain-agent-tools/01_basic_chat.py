# -*- coding: utf-8 -*-
"""
Step 1: 기본 채팅

LangChain과 Gemini를 사용한 기본 채팅 기능을 학습합니다.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

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
print("Step 1: 기본 채팅")
print("=" * 70)
print()

# 기본 채팅 테스트
print("💬 사용자: 잘 지냈어?")
response = llm.invoke([HumanMessage("잘 지냈어?")])
print(f"🤖 Gemini 응답: {response.content}")
