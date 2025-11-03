# LangChain 기본 예제

LangChain을 사용한 Gemini 2.0 Flash 기본 예제입니다.

## 목차

- **00_why_langchain.py** + **00_why_langchain.md** - Gemini API vs LangChain 비교
- **01_langchain_basic.py** + **01_langchain_basic.md** - LangChain 기본 사용법
- **02_stepX_xxx.py** (5개 파일) + **02_langchain_message_history.md** - 메시지 히스토리 관리 (단계별)

**참고:**
- 각 Python 파일은 실행 코드만 포함하고, 자세한 설명은 동일한 이름의 `.md` 파일에 있습니다.
- 02번은 학습 효과를 위해 5개의 단계별 파일로 분리되어 있습니다.

---

## 특징

- 🔄 Gemini API 직접 사용 vs LangChain 사용 비교
- 📚 통일된 인터페이스로 여러 LLM 쉽게 교체 가능
- 💬 대화 히스토리 관리 (SystemMessage, HumanMessage, AIMessage)
- 🎯 프롬프트 템플릿, Chain, Agent 등 고급 기능 활용 가능

---

## 설치

### 1. 가상환경 활성화

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 2. 의존성 설치

프로젝트 루트에서:

```bash
pip install -r requirements.txt
```

또는 LangChain 패키지만 개별 설치:

```bash
pip install langchain-google-genai langchain-core
```

---

## 실행 방법

### 00_why_langchain.py

Gemini API를 직접 사용하는 것과 LangChain을 사용하는 것의 차이를 비교합니다.

**Windows:**
```bash
venv\Scripts\python.exe 007.langchain-basic\00_why_langchain.py
```

**macOS/Linux:**
```bash
venv/bin/python 007.langchain-basic/00_why_langchain.py
```

**또는 폴더 내에서:**
```bash
cd 007.langchain-basic
python 00_why_langchain.py
```

### 01_langchain_basic.py

LangChain의 기본 사용법 (invoke, 메시지 관리)을 학습합니다.

**Windows:**
```bash
venv\Scripts\python.exe 007.langchain-basic\01_langchain_basic.py
```

**macOS/Linux:**
```bash
venv/bin/python 007.langchain-basic/01_langchain_basic.py
```

---

## 주요 개념

### 1. 왜 LangChain을 사용하나?

#### Gemini API 직접 사용의 문제점:
- ❌ 다른 LLM(OpenAI, Claude 등)으로 바꾸려면 코드 전체 수정 필요
- ❌ 히스토리 형식이 Gemini 전용 (`types.Content`)
- ❌ 고급 기능(Chain, Agent, RAG)을 직접 구현해야 함
- ❌ 프롬프트 템플릿, 출력 파싱 등 매번 새로 만들어야 함

#### LangChain 사용의 장점:
- ✅ 통일된 인터페이스 - 다른 LLM으로 교체 쉬움
- ✅ 표준 메시지 형식 - `SystemMessage`, `HumanMessage`, `AIMessage`
- ✅ 풍부한 생태계 - Chain, Agent, RAG 등 바로 사용 가능
- ✅ 재사용 가능한 컴포넌트 - 프롬프트 템플릿, 파서 등

### 2. 모델 교체 예시

#### ❌ Gemini API 직접 사용:
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
#   전체 코드 다시 작성! (openai.chat.completions.create 등)
```

#### ✅ LangChain 사용:
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

### 3. LangChain 메시지 타입

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 1. SystemMessage: 챗봇의 페르소나/역할 정의
SystemMessage(content="너는 친절한 AI 어시스턴트입니다.")

# 2. HumanMessage: 사용자 입력
HumanMessage(content="파이썬이란?")

# 3. AIMessage: AI 응답 (llm.invoke()가 자동 생성)
# response = llm.invoke(messages)  # → AIMessage 반환
```

### 4. 대화 히스토리 관리 패턴

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

# 대화 시작
conversation = [
    SystemMessage(content="너는 친절한 프로그래밍 튜터입니다."),
    HumanMessage(content="파이썬이란?")
]

# 첫 번째 응답
response1 = llm.invoke(conversation)
print(response1.content)

# 중요! AI 응답을 히스토리에 추가해야 맥락 유지
conversation.append(response1)

# 후속 질문
conversation.append(HumanMessage(content="그럼 자바는?"))
response2 = llm.invoke(conversation)
print(response2.content)
```

---

## 실전 시나리오

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

## LangChain으로 할 수 있는 것들 (미리보기)

### 1️⃣ 프롬프트 템플릿
```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("다음을 요약: {text}")
chain = prompt | llm
result = chain.invoke({"text": "긴 텍스트..."})
```

### 2️⃣ LCEL 체인 (LangChain Expression Language)
```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"input": "..."})
```

### 3️⃣ 도구(Tool) 사용
```python
from langchain.tools import tool

@tool
def calculator(expression: str) -> float:
    """수식을 계산합니다."""
    return eval(expression)

# 도구를 LLM과 연결
```

### 4️⃣ RAG 시스템 (Retrieval-Augmented Generation)
```python
retriever = vector_store.as_retriever()
chain = retriever | llm
result = chain.invoke("질문")
```

### 5️⃣ 에이전트 (Agent)
```python
from langchain.agents import initialize_agent

agent = initialize_agent(tools, llm, agent_type="...")
agent.run("현재 날씨 알려줘")
```

---

## 실전 팁

### ✅ DO (좋은 습관):
1. 대화 시작 시 `SystemMessage`로 페르소나 설정
2. AI 응답을 항상 히스토리에 추가
3. 메시지 타입을 명확히 구분 (System/Human/AI)
4. 히스토리가 너무 길면 요약하거나 일부 제거

### ❌ DON'T (피해야 할 것):
1. AI 응답을 히스토리에 추가 안 함 → 맥락 끊김!
2. 문자열만 계속 전달 → 페르소나 설정 불가
3. 히스토리 무한 증가 → 토큰/비용 폭증
4. `SystemMessage`를 중간에 추가 → 의도대로 안 됨

### 💰 비용 최적화:
```python
# 히스토리가 길수록 토큰 많이 소비
# 오래된 메시지는 제거 or 요약
conversation = conversation[-10:]  # 최근 10개만 유지
```

---

## API 키 설정

`.env` 파일에 다음 내용 추가:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## 문제 해결

### ImportError: No module named 'langchain_google_genai'

```bash
pip install langchain-google-genai langchain-core
```

### API 키 오류

- `.env` 파일에 `GEMINI_API_KEY` 확인
- API 키가 유효한지 확인

### 유니코드 인코딩 오류 (Windows)

Windows 콘솔에서 이모지 출력 시 인코딩 오류가 발생할 수 있습니다. 이는 표시 문제일 뿐 코드 실행에는 문제가 없습니다.

---

## 파일 구조

```
007.langchain-basic/
├── 00_why_langchain.py             # Gemini API vs LangChain 비교
├── 00_why_langchain.md             # 00번 상세 설명
├── 01_langchain_basic.py           # LangChain 기본 사용법
├── 01_langchain_basic.md           # 01번 상세 설명
├── 02_step1_setup.py               # 메시지 히스토리 - Step 1: 초기 설정
├── 02_step2_first_conversation.py  # 메시지 히스토리 - Step 2: 첫 대화
├── 02_step3_new_session.py         # 메시지 히스토리 - Step 3: 새 세션
├── 02_step4_streaming.py           # 메시지 히스토리 - Step 4: 스트리밍
├── 02_step5_context.py             # 메시지 히스토리 - Step 5: 맥락 연결
├── 02_langchain_message_history.md # 02번 상세 설명
└── README.md                       # 이 파일
```

---

## 참고 자료

- [LangChain Documentation](https://python.langchain.com/docs/)
- [LangChain Google GenAI](https://python.langchain.com/docs/integrations/providers/google_generative_ai/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google Gen AI SDK](https://googleapis.github.io/python-genai/)

---

## 다음 단계

1. **00_why_langchain.py**: LangChain을 왜 사용하는지 이해
2. **01_langchain_basic.py**: LangChain 기본 사용법 학습
3. 프롬프트 템플릿, Chain, RAG 등 고급 기능 학습

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
