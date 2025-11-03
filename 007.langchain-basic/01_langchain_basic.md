# 01_langchain_basic.py 설명

## 개요

LangChain의 가장 기본적인 사용법을 단계별로 학습합니다.

---

## Step 1: 모델 초기화 (가장 기본!)

### 코드
```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.7,
    max_output_tokens=1000,
    google_api_key=api_key
)
```

### 설명
- `ChatGoogleGenerativeAI`: LangChain의 Gemini 통합 클래스
- `model`: 사용할 모델 이름
- `temperature`: 0.0 (일관적) ~ 1.0 (창의적)
- `max_output_tokens`: 최대 출력 토큰 수
- `google_api_key`: API 키 (필수)

---

## Step 2: 기본 invoke - 문자열 직접 전달

### 코드
```python
question = "파이썬의 주요 특징 3가지를 간단히 알려줘"
response = llm.invoke(question)

print(f"타입: {type(response)}")
print(f"내용: {response.content}")
```

### 학습 포인트
- `invoke()`는 동기 방식 (응답 올 때까지 대기)
- 반환값은 `AIMessage` 객체
- `response.content`로 텍스트 추출

---

## Step 3: 메시지 리스트로 전달 (추천 방식)

### SystemMessage로 페르소나 설정

```python
from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(content="너는 친절한 프로그래밍 튜터입니다. 초보자도 이해하기 쉽게 설명하세요."),
    HumanMessage(content="Python의 리스트란 무엇인가요?")
]

response = llm.invoke(messages)
print(response.content)
```

### 학습 포인트
- `SystemMessage`: 챗봇의 역할/성격 정의
- `HumanMessage`: 사용자 입력
- `AIMessage`: AI 응답 (자동 생성됨)

---

## Step 4: 대화 히스토리 관리 (핵심!)

### 첫 번째 대화

```python
conversation = [
    SystemMessage(content="너는 친절한 프로그래밍 튜터입니다."),
    HumanMessage(content="리스트와 튜플의 차이는 뭔가요?")
]

response1 = llm.invoke(conversation)
print(f"AI 응답: {response1.content[:100]}...")
```

### AI 응답을 히스토리에 추가

```python
# 중요! AI 응답을 히스토리에 추가해야 맥락 유지
conversation.append(response1)
```

### 후속 질문 (이전 맥락 활용)

```python
conversation.append(HumanMessage(content="그럼 언제 튜플을 사용하나요?"))

# "그럼"이라는 단어 사용 가능 (이전 맥락 기억)
response2 = llm.invoke(conversation)
print(f"AI 응답: {response2.content[:150]}...")
```

### 핵심 포인트
- ✅ AI 응답도 반드시 `conversation`에 추가해야 함
- ✅ 추가 안 하면 AI는 자기가 뭐라고 답했는지 모름!
- ✅ 전체 히스토리를 매번 `invoke()`에 전달

---

## Step 5: 대화 히스토리 시각화

### 대화 흐름 확인

```python
conversation.append(response2)  # 마지막 응답도 추가

print(f"총 메시지 수: {len(conversation)}")
for i, msg in enumerate(conversation):
    role = msg.__class__.__name__
    icon = "🤖" if role == "AIMessage" else ("👤" if role == "HumanMessage" else "⚙️")
    content_preview = msg.content[:60] + "..." if len(msg.content) > 60 else msg.content
    print(f"  {icon} [{i+1}] {role:15} {content_preview}")
```

---

## Step 6: 메시지 타입 정리

### LangChain의 메시지 타입

#### 1. SystemMessage
- **역할**: 챗봇의 페르소나/역할 정의
- **위치**: 보통 맨 앞
- **예시**: "너는 친절한 AI 어시스턴트입니다"

#### 2. HumanMessage
- **역할**: 사용자 입력
- **위치**: 대화 중간중간
- **예시**: "파이썬이란?"

#### 3. AIMessage
- **역할**: AI 응답
- **위치**: HumanMessage 다음
- **자동 생성**: `llm.invoke()`가 반환

### 대화 패턴

```
System → Human → AI → Human → AI → Human → AI ...
(페르소나) (질문1) (답변1) (질문2) (답변2) (질문3) (답변3)
```

---

## Step 7: 실전 팁

### ✅ DO (좋은 습관)

1. 대화 시작 시 `SystemMessage`로 페르소나 설정
2. AI 응답을 항상 히스토리에 추가
3. 메시지 타입을 명확히 구분 (System/Human/AI)
4. 히스토리가 너무 길면 요약하거나 일부 제거

### ❌ DON'T (피해야 할 것)

1. AI 응답을 히스토리에 추가 안 함 → 맥락 끊김!
2. 문자열만 계속 전달 → 페르소나 설정 불가
3. 히스토리 무한 증가 → 토큰/비용 폭증
4. `SystemMessage`를 중간에 추가 → 의도대로 안 됨

### 💰 비용 최적화

```python
# 히스토리가 길수록 토큰 많이 소비
# 오래된 메시지는 제거 or 요약
conversation = conversation[-10:]  # 최근 10개만
```

---

## 학습 정리

### 1️⃣ 모델 초기화
```python
llm = ChatGoogleGenerativeAI(model="...")
```

### 2️⃣ 기본 invoke
```python
response = llm.invoke("질문")
```

### 3️⃣ 메시지 구조화
```python
messages = [SystemMessage(...), HumanMessage(...)]
response = llm.invoke(messages)
```

### 4️⃣ 히스토리 관리
```python
messages.append(response)  # AI 응답 추가
messages.append(HumanMessage(...))  # 다음 질문
response = llm.invoke(messages)
```

---

## 다음 단계

🎯 실제 채팅 앱 만들기

```bash
python 007.langchain-basic/02_chat_app.py
```
