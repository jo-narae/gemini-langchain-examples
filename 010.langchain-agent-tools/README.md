# 009. LangChain Agent Tools - 도구를 사용하는 AI 에이전트

LangChain의 Tools와 Agent를 사용하여 AI가 외부 함수를 호출하고 활용하는 방법을 학습합니다.

## 핵심 개념

### Tools (도구)
- Python 함수를 AI가 호출할 수 있는 도구로 변환
- `@tool` 데코레이터로 간단하게 생성
- 함수 이름, 설명, 파라미터 정보를 AI에게 제공

### 두 가지 방식

#### 1. 수동 방식 (Step 3-4)
- `bind_tools()`로 도구를 모델에 바인딩
- `tool_calls`를 직접 확인하고 처리
- 코드가 반복적이지만 과정을 이해하기 좋음

#### 2. 자동 방식 (Step 5) ⭐ 권장
- `create_agent()`가 도구 호출 루프를 자동 처리
- 코드가 간결하고 강력함
- LangChain 1.0의 공식 방식

## 파일 구조

```
009.langchain-agent-tools/
├── README.md                          # 이 문서
├── langchain_tool_gemini.py           # 전체 예제 (통합 버전)
├── 01_basic_chat.py                   # Step 1: 기본 채팅 (도구 없음)
├── 02_tool_definition.py              # Step 2: 도구 정의
├── 03_tool_calling.py                 # Step 3: 도구 호출 - 단일 질문 (수동)
├── 04_multiple_calls.py               # Step 4: 도구 호출 - 여러 질문 (수동)
├── 05_agent_auto.py                   # Step 5: LangChain Agent 자동 호출 ⭐
└── 06_pydantic_tools.py               # Step 6: Pydantic로 복잡한 입력 정의
```

## 필수 패키지

```bash
pip install langchain langchain-google-genai langchain-core pytz pydantic yfinance
```

또는:

```bash
pip install -r requirements.txt
```

## 학습 순서

```bash
python 009.langchain-agent-tools/01_basic_chat.py
python 009.langchain-agent-tools/02_tool_definition.py
python 009.langchain-agent-tools/03_tool_calling.py
python 009.langchain-agent-tools/04_multiple_calls.py
python 009.langchain-agent-tools/05_agent_auto.py
python 009.langchain-agent-tools/06_pydantic_tools.py
```

## 학습 내용

### Step 1: 기본 채팅
- 도구 없이 기본 LLM 대화
- Gemini 모델 초기화

### Step 2: 도구 정의
- `@tool` 데코레이터 사용법
- `get_current_time` 도구 예제

### Step 3: 도구 호출 - 단일 질문 (수동)
- `bind_tools()`로 도구 바인딩
- `tool_calls` 수동 처리
- 단일 질문에 대한 도구 호출 흐름

### Step 4: 도구 호출 - 여러 질문 (수동)
- 여러 질문을 반복 처리
- 수동 방식의 반복적인 코드 패턴

### Step 5: LangChain Agent 자동 호출 ⭐
- `create_agent()` 사용 (LangChain 1.0 공식 API)
- 도구 호출 루프 자동 처리
- Deprecation 경고 없는 최신 방식

### Step 6: Pydantic로 복잡한 입력 정의
- Pydantic 모델을 사용한 도구 입력 검증
- `StockHistoryInput` 모델 예제
- yfinance로 실제 주식 데이터 조회
- Agent와 Pydantic 모델 결합

## 코드 비교

### 수동 방식 (Step 3-4)

```python
llm_with_tools = llm.bind_tools(tools)
response = llm_with_tools.invoke(messages)

if hasattr(response, 'tool_calls') and response.tool_calls:
    for tool_call in response.tool_calls:
        selected_tool = tool_dict[tool_call["name"]]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)

    final_response = llm_with_tools.invoke(messages)
```

### 자동 방식 (Step 5) ⭐

```python
from langchain.agents import create_agent

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="너는 유용한 AI 어시스턴트입니다."
)

result = agent.invoke({"messages": [("user", "부산은 지금 몇시야?")]})
final_message = result["messages"][-1]
print(final_message.content)
```

## LangChain Agent의 장점

1. **자동화**: 도구 호출 루프를 자동 처리
2. **간결함**: 반복적인 코드 제거
3. **공식 API**: LangChain 1.0의 표준 방식
4. **안정성**: Deprecation 경고 없음
5. **재사용성**: 한 번 만든 Agent를 여러 곳에서 사용

## 주의사항

### API 쿼터
- Gemini API 무료 티어: 하루 50회 제한
- 여러 파일 연속 실행 시 쿼터 초과 가능

### 버전 변경 사항
- LangChain 1.0부터 `AgentExecutor`가 제거됨
- `create_agent()`가 새로운 공식 API
- Deprecation 경고 없이 깔끔하게 작동

## 참고 자료

- [LangChain Agents 문서](https://python.langchain.com/docs/modules/agents/)
- [Tool Calling 가이드](https://python.langchain.com/docs/how_to/tool_calling/)
- [Gemini API 문서](https://ai.google.dev/gemini-api/docs)
