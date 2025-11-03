# 02_langchain_message_history.py 설명

## 개요

LangChain의 메시지 히스토리 관리 시스템을 학습합니다. 세션별로 대화를 관리하고, 이전 맥락을 유지하며 대화를 이어가는 방법을 다룹니다.

---

## 주요 개념

### 1. InMemoryChatMessageHistory

메모리에 대화 기록을 저장하는 클래스입니다.

```python
from langchain_core.chat_history import InMemoryChatMessageHistory

history = InMemoryChatMessageHistory()
```

**특징:**
- 메모리(RAM)에 저장되므로 프로그램 종료 시 사라짐
- 빠르고 간단하지만 영구 저장 불가
- 프로토타입이나 테스트에 적합

### 2. RunnableWithMessageHistory

메시지 기록을 자동으로 관리해주는 래퍼 클래스입니다.

```python
from langchain_core.runnables.history import RunnableWithMessageHistory

with_message_history = RunnableWithMessageHistory(
    model,  # LangChain 모델
    get_session_history  # 세션 히스토리를 반환하는 함수
)
```

**장점:**
- 메시지 입출력에 자동으로 히스토리 추가
- 세션별로 독립적인 대화 관리
- 수동으로 `append()` 할 필요 없음

---

## 세션 관리

### 세션 ID란?

각 사용자 또는 대화 스레드를 구분하는 고유 식별자입니다.

```python
# 세션별 대화 기록 저장소
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
```

**사용 예시:**
- `session_id = "user123"` - 특정 사용자의 대화
- `session_id = "thread-456"` - 특정 대화 스레드
- `session_id = "temp-abc"` - 임시 세션

### 세션별 대화 실행

```python
# 세션 abc2에서 대화
config = {"configurable": {"session_id": "abc2"}}

response = with_message_history.invoke(
    [HumanMessage(content="안녕? 난 김철수이야.")],
    config=config
)

# 같은 세션에서 이름 기억
response = with_message_history.invoke(
    [HumanMessage(content="내 이름이 뭐지?")],
    config=config
)
# 출력: "김철수님이라고 하셨죠!"
```

### 새로운 세션

```python
# 새 세션 abc3에서 질문
config_new = {"configurable": {"session_id": "abc3"}}

response = with_message_history.invoke(
    [HumanMessage(content="내 이름이 뭐지?")],
    config_new
)
# 출력: "죄송하지만 알려주신 적이 없으신 것 같아요."
```

---

## 스트리밍 응답

실시간으로 응답을 받아 출력하는 방법입니다.

```python
for r in with_message_history.stream(
    [HumanMessage(content="긴 이야기를 들려줘")],
    config=config
):
    print(r.content, end="", flush=True)
```

**특징:**
- 응답이 생성되는 대로 즉시 출력
- 사용자 경험 향상 (대기 시간 단축)
- 긴 응답에 유용

---

## 세션 상태 확인

### 활성 세션 목록

```python
print("📊 현재 활성 세션들:")
for session_id in store.keys():
    history = store[session_id]
    message_count = len(history.messages)
    print(f"  - 세션 {session_id}: {message_count}개 메시지")
```

### 특정 세션 대화 기록 출력

```python
session_to_check = "abc2"
if session_to_check in store:
    print(f"💬 세션 '{session_to_check}'의 대화 기록:")
    for i, message in enumerate(store[session_to_check].messages, 1):
        speaker = "👤 사용자" if message.__class__.__name__ == "HumanMessage" else "🤖 AI"
        print(f"{i}. {speaker}: {message.content[:100]}")
```

---

## 대화 맥락 유지

### 장기 대화에서 맥락 연결

```python
# 첫 번째 대화
response = with_message_history.invoke(
    [HumanMessage(content="안녕? 난 김철수이야.")],
    config=config
)

# 두 번째 대화 (이름 기억)
response = with_message_history.invoke(
    [HumanMessage(content="내 이름이 뭐지?")],
    config=config
)
# 출력: "김철수님이라고 하셨죠!"

# 새로운 주제
response = with_message_history.invoke(
    [HumanMessage(content="오늘 날씨가 좋다면 뭘 하면 좋을까?")],
    config=config
)

# 이전 대화 맥락 연결
response = with_message_history.invoke(
    [HumanMessage(content="아까 내 이름과 함께 추천해줄 수 있어?")],
    config=config
)
# 출력: "김철수님, 날씨가 좋으시다면 산책을 추천드려요!"
```

---

## 실전 활용 시나리오

### 1. 웹 애플리케이션

```python
# 각 사용자마다 독립적인 세션
user_id = "user_12345"
config = {"configurable": {"session_id": user_id}}

response = with_message_history.invoke(
    [HumanMessage(content=user_input)],
    config=config
)
```

### 2. 챗봇 서비스

```python
# 대화 스레드별 관리
thread_id = f"thread_{conversation_id}"
config = {"configurable": {"session_id": thread_id}}
```

### 3. 멀티 에이전트 시스템

```python
# 에이전트별 독립적인 메모리
agent_id = "support_agent_1"
config = {"configurable": {"session_id": f"agent_{agent_id}"}}
```

---

## 주의사항

### ⚠️ 메모리 관리

```python
# InMemoryChatMessageHistory는 메모리에 저장
# 프로그램 종료 시 모든 대화 내역 사라짐

# 영구 저장이 필요하면:
# - FileChatMessageHistory (파일 저장)
# - RedisChatMessageHistory (Redis 저장)
# - PostgresChatMessageHistory (DB 저장)
```

### ⚠️ 토큰 관리

```python
# 대화가 길어지면 토큰 소비 증가
# 주기적으로 오래된 메시지 제거 필요

# 예: 최근 10개 메시지만 유지
if len(history.messages) > 20:
    history.messages = history.messages[-20:]
```

### ⚠️ 세션 정리

```python
# 사용하지 않는 세션은 주기적으로 정리
# 메모리 누수 방지

def cleanup_old_sessions():
    for session_id in list(store.keys()):
        # 마지막 활동 시간 체크 로직
        if should_remove(session_id):
            del store[session_id]
```

---

## 비교: 수동 vs 자동 히스토리 관리

### 수동 관리 (01_langchain_basic.py 방식)

```python
messages = [
    SystemMessage(content="너는 친절한 AI입니다."),
    HumanMessage(content="안녕?")
]

response = llm.invoke(messages)
messages.append(response)  # 수동으로 추가

messages.append(HumanMessage(content="날씨는?"))
response = llm.invoke(messages)
messages.append(response)  # 수동으로 추가
```

**장점:** 세밀한 제어 가능
**단점:** 매번 수동으로 추가 필요

### 자동 관리 (RunnableWithMessageHistory)

```python
with_message_history = RunnableWithMessageHistory(llm, get_session_history)

# 자동으로 히스토리 관리
response = with_message_history.invoke(
    [HumanMessage(content="안녕?")],
    config={"configurable": {"session_id": "abc"}}
)

response = with_message_history.invoke(
    [HumanMessage(content="날씨는?")],
    config={"configurable": {"session_id": "abc"}}
)
```

**장점:** 자동 관리, 세션별 독립
**단점:** 커스터마이징 제한

---

## 정리

### 핵심 개념

1. **InMemoryChatMessageHistory** - 메모리 기반 대화 저장소
2. **RunnableWithMessageHistory** - 자동 히스토리 관리 래퍼
3. **세션 ID** - 대화를 구분하는 고유 식별자
4. **스트리밍** - 실시간 응답 출력

### 언제 사용하나?

- ✅ 멀티 유저 챗봇 애플리케이션
- ✅ 세션별로 독립적인 대화 필요
- ✅ 자동으로 히스토리 관리하고 싶을 때
- ✅ 웹 서비스, API 서버 구축 시

### 다음 단계

- 영구 저장소 연동 (Redis, PostgreSQL)
- 대화 요약 및 압축
- 멀티모달 메시지 처리
- RAG와 통합

---

## 참고 자료

- [LangChain Message History](https://python.langchain.com/docs/modules/memory/chat_messages/)
- [RunnableWithMessageHistory API](https://api.python.langchain.com/en/latest/runnables/langchain_core.runnables.history.RunnableWithMessageHistory.html)
