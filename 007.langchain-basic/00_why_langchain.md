# 00_why_langchain.py 설명

## 개요

Gemini API를 직접 사용하는 것과 LangChain을 사용하는 것의 차이를 비교합니다.

---

## Part 1: Gemini API 직접 사용 (최신 google-genai SDK)

### 특징
- 간단하고 직관적
- Gemini 전용 기능 활용 가능
- 학습 목적으로 좋음

### 코드 구조
```python
from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)
system_instruction = "너는 친절한 AI 어시스턴트입니다."

# 단일 질문
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="파이썬이란?",
    config=types.GenerateContentConfig(system_instruction=system_instruction)
)

# 대화 히스토리 관리
history = []
history.append(types.Content(role="user", parts=[types.Part(text="파이썬이란?")]))
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=history,
    config=types.GenerateContentConfig(system_instruction=system_instruction)
)
history.append(types.Content(role="model", parts=[types.Part(text=response.text)]))
```

### 문제점
- ❌ 다른 LLM(OpenAI, Claude 등)으로 바꾸려면 코드 전체 수정
- ❌ 히스토리 형식이 Gemini 전용 (`types.Content`)
- ❌ 고급 기능(Chain, Agent, RAG)을 직접 구현해야 함
- ❌ 프롬프트 템플릿, 출력 파싱 등 매번 새로 만들어야 함

---

## Part 2: LangChain 사용 (권장 방식)

### 특징
- 표준화되고 유지보수 쉬움
- 다른 LLM으로 쉽게 교체
- 고급 기능(Chain, RAG) 바로 사용
- 프로덕션 환경에 적합

### 코드 구조
```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

langchain_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.7,
    google_api_key=api_key
)

# 단일 질문
response = langchain_model.invoke("파이썬이란?")

# 대화 히스토리 관리
messages = [
    SystemMessage(content="너는 친절한 AI 어시스턴트입니다."),
    HumanMessage(content="파이썬이란?")
]
response1 = langchain_model.invoke(messages)
messages.append(response1)
messages.append(HumanMessage(content="그럼 자바는?"))
response2 = langchain_model.invoke(messages)
```

### 장점
- ✅ 통일된 인터페이스 - 다른 LLM으로 교체 쉬움
- ✅ 표준 메시지 형식 - `SystemMessage`, `HumanMessage`, `AIMessage`
- ✅ 풍부한 생태계 - Chain, Agent, RAG 등 바로 사용 가능
- ✅ 재사용 가능한 컴포넌트 - 프롬프트 템플릿, 파서 등

---

## Part 3: 모델 교체가 얼마나 쉬운가?

### ❌ Gemini API 직접 사용
```python
from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)
history = [types.Content(role="user", parts=[types.Part(text="안녕")])]
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=history
)

# → OpenAI로 교체하려면?
# 전체 코드 다시 작성! (openai.chat.completions.create 등)
```

### ✅ LangChain 사용
```python
# Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# OpenAI로 교체? 딱 2줄만 바꾸면 됨!
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4")

# 나머지 코드는 동일!
response = llm.invoke("안녕")
```

---

## Part 4: 실전 시나리오 - 언제 LangChain을 사용하나?

### ✅ LangChain 사용을 권장:
- 프로덕션 환경 (유지보수 중요)
- 여러 LLM 프로바이더 테스트 필요
- Chain, Agent, RAG 등 고급 기능 필요
- 팀 프로젝트 (표준화된 코드)

### ❌ Gemini API 직접 사용도 괜찮음:
- 빠른 프로토타입 (단순 테스트)
- Gemini 전용 기능 사용 (Thinking 모드 등)
- 학습 목적 (API 동작 원리 이해)
- 초경량 애플리케이션

💡 **권장: 학습은 Gemini API로, 실전은 LangChain으로!**

---

## Part 5: LangChain으로 할 수 있는 것들 (미리보기)

### 1️⃣ 프롬프트 템플릿 (Step 5-2)
```python
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_template("다음을 요약: {text}")
```

### 2️⃣ LCEL 체인 (Step 5-3)
```python
chain = prompt | llm | output_parser
result = chain.invoke({"text": "..."})
```

### 3️⃣ 도구(Tool) 사용 (Step 6)
```python
from langchain.tools import tool

@tool
def calculator(expression: str) -> float:
    return eval(expression)
```

### 4️⃣ RAG 시스템 (Step 7)
```python
retriever = vector_store.as_retriever()
chain = retriever | llm
```

### 5️⃣ 에이전트 (고급)
```python
agent = initialize_agent(tools, llm)
agent.run("현재 날씨 알려줘")
```

---

## 정리

### Gemini API 직접 사용:
- 간단하고 직관적
- Gemini 전용 기능 활용 가능
- 학습 목적으로 좋음

### LangChain 사용:
- 표준화되고 유지보수 쉬움
- 다른 LLM으로 쉽게 교체
- 고급 기능(Chain, RAG) 바로 사용
- 프로덕션 환경에 적합

🎯 **이제부터는 LangChain 방식으로 배워봅시다!**

---

## 다음 단계
```bash
python 007.langchain-basic/01_langchain_basic.py
```
