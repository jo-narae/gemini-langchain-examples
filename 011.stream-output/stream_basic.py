"""
LangChain 스트리밍 출력 기본 예제

실시간으로 토큰 단위로 응답을 스트리밍하는 방법을 보여줍니다.
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
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time

# 환경변수 로드 (상위 폴더의 .env 파일 사용)
from pathlib import Path
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# API 키 확인 및 설정
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please check .env file")
os.environ["GOOGLE_API_KEY"] = api_key

print("=" * 60)
print("LangChain 스트리밍 출력 예제")
print("=" * 60)
print()

# 1. 모델 초기화
print("🤖 Gemini 모델 초기화 중...")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    streaming=True  # 스트리밍 활성화
)
print("✅ 모델 초기화 완료!")
print()

# 2. 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_template("{question}")

# 3. Output Parser
output_parser = StrOutputParser()

# 4. 체인 구성
chain = prompt | llm | output_parser

# 예제 1: 기본 스트리밍
print("=" * 60)
print("예제 1: 기본 스트리밍 출력")
print("=" * 60)

question1 = "파이썬의 주요 특징 5가지를 자세히 설명해주세요."
print(f"📝 질문: {question1}")
print()
print("🤖 AI 응답 (실시간 스트리밍):")
print("-" * 60)

start_time = time.time()

for chunk in chain.stream({"question": question1}):
    print(chunk, end="", flush=True)

elapsed_time = time.time() - start_time
print()
print("-" * 60)
print(f"⏱️ 응답 시간: {elapsed_time:.2f}초")
print()

# 예제 2: 스트리밍 vs 일반 호출 비교
print("=" * 60)
print("예제 2: 스트리밍 vs 일반 호출 성능 비교")
print("=" * 60)

question2 = "머신러닝과 딥러닝의 차이점을 설명해주세요."
print(f"📝 질문: {question2}")
print()

# 스트리밍 방식
print("[방식 1] 스트리밍 출력:")
print("-" * 60)
stream_start = time.time()

for chunk in chain.stream({"question": question2}):
    print(chunk, end="", flush=True)

stream_time = time.time() - stream_start
print()
print("-" * 60)
print(f"⏱️ 스트리밍 시간: {stream_time:.2f}초")
print()

# 일반 호출 방식
print("[방식 2] 일반 호출 출력:")
print("-" * 60)
invoke_start = time.time()

response = chain.invoke({"question": question2})
print(response)

invoke_time = time.time() - invoke_start
print("-" * 60)
print(f"⏱️ 일반 호출 시간: {invoke_time:.2f}초")
print()

# 예제 3: 긴 응답 스트리밍
print("=" * 60)
print("예제 3: 긴 응답의 스트리밍 효과")
print("=" * 60)

question3 = "웹 개발 초보자를 위한 학습 로드맵을 단계별로 상세히 작성해주세요."
print(f"📝 질문: {question3}")
print()
print("🤖 AI 응답 (실시간 스트리밍):")
print("-" * 60)

chunk_count = 0
start_time = time.time()

for chunk in chain.stream({"question": question3}):
    print(chunk, end="", flush=True)
    chunk_count += 1

elapsed_time = time.time() - start_time
print()
print("-" * 60)
print(f"⏱️ 응답 시간: {elapsed_time:.2f}초")
print(f"📦 총 청크 수: {chunk_count}개")
print()

