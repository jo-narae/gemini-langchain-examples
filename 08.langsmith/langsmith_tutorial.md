# LangSmith 튜토리얼 가이드

LangSmith를 활용하여 LLM 애플리케이션을 추적하고 모니터링하는 방법을 학습합니다.

## 📦 필수 패키지 설치

프로젝트 루트 디렉토리에서 다음 명령을 실행하세요:

```bash
pip install -r requirements.txt
```

또는 개별 설치:

```bash
pip install langchain>=0.3.0
pip install langchain-classic>=1.0.0
pip install langchain-community>=0.4.0
pip install langchain-google-genai>=3.0.0
pip install python-dotenv>=1.2.1
```

**중요**: LangChain 1.0 이상에서는 `ConversationBufferMemory`와 `ConversationChain`이 `langchain-classic` 패키지로 이동되었습니다.

---

## 📋 학습 내용

1. LangSmith 설정 확인
2. 기본 추적 (단일 LLM 호출)
3. 스트리밍 추적
4. 대화 체인 추적
5. 고급 기능 (태그, 메타데이터)
6. LangSmith 대시보드 활용법

---

## Step 1: LangSmith 설정 확인

### 필수 환경변수

`.env` 파일에 다음 내용을 추가하세요:

```bash
# Gemini API (필수)
GOOGLE_API_KEY=your_gemini_api_key_here

# LangSmith 설정 (선택)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=my-chatbot-project
```

### LangSmith API 키 발급

1. https://smith.langchain.com 접속
2. 계정 생성 및 로그인
3. Settings → API Keys에서 키 발급

### 확인 가능한 정보

- ✓ GOOGLE_API_KEY: Gemini API 키 설정 여부
- ✓ LANGCHAIN_TRACING_V2: 추적 활성화 여부 (true/false)
- ✓ LANGCHAIN_API_KEY: LangSmith API 키
- ✓ LANGCHAIN_PROJECT: 프로젝트 이름

---

## Step 2: 기본 추적

### LangSmith에 기록되는 정보

단일 `invoke()` 호출 시:

- **입력**: 사용자 질문
- **출력**: AI 응답
- **토큰 사용량**: 입력/출력 토큰 수
- **응답 시간**: 실행 시간 (ms)
- **모델 정보**: gemini-2.0-flash

### 학습 포인트

- LangSmith는 모든 `invoke()` 호출을 자동으로 추적
- 환경변수만 설정하면 코드 수정 없이 추적 가능
- 대시보드에서 각 호출의 성능과 비용을 실시간 확인

---

## Step 3: 스트리밍 추적

### 특징

- `stream()` 메서드도 자동으로 추적됨
- 전체 응답이 완료된 후 대시보드에 기록
- 총 응답 시간과 토큰 사용량 확인 가능

---

## Step 4: 대화 체인 추적

### ConversationChain 추적 정보

- 각 대화 턴별 입력/출력
- 메모리 상태 변화
- 프롬프트 템플릿 적용 과정
- 체인 실행 흐름 시각화
- 누적 토큰 사용량

### 학습 포인트

- ConversationChain은 내부적으로 여러 단계를 거침
- LangSmith는 각 단계를 트리 구조로 시각화
- 메모리에 저장된 대화 히스토리도 추적 가능

---

## Step 5: 고급 기능

### 태그 (Tags)

실행을 카테고리별로 분류:

```python
llm.invoke(
    "질문",
    config={"tags": ["tutorial", "langchain", "beginner"]}
)
```

**활용:**
- LangSmith 대시보드에서 태그로 필터링 가능
- 예: 'tutorial' 태그가 달린 모든 실행 보기

### 메타데이터 (Metadata)

추가 컨텍스트 정보 저장:

```python
llm.invoke(
    "질문",
    config={
        "metadata": {
            "user_id": "user_123",
            "session": "session_456",
            "environment": "development"
        }
    }
)
```

**활용:**
- 사용자별 토큰 사용량 분석
- 세션별 대화 추적
- 환경별(개발/프로덕션) 성능 비교

### 학습 포인트

- 태그: 실행을 카테고리별로 분류
- 메타데이터: 추가 컨텍스트 정보 저장
- 프로덕션 환경에서 디버깅 시 매우 유용

---

## Step 6: LangSmith 대시보드 활용

### 대시보드 접속

1. https://smith.langchain.com 접속
2. 로그인 (GitHub, Google 등)
3. 프로젝트 선택 (LANGCHAIN_PROJECT 이름)

### 프로젝트 전체 메트릭

- 총 실행 횟수 (Total Runs)
- 성공/실패율
- 평균 응답 시간
- 총 토큰 사용량
- 예상 비용 (USD)

### 개별 실행(Run) 상세 정보

#### 1. 입력/출력 데이터
- 사용자 질문 (Input)
- AI 응답 (Output)

#### 2. 성능 메트릭
- **Latency**: 응답 시간 (ms)
- **Prompt Tokens**: 입력 토큰 수
- **Completion Tokens**: 출력 토큰 수
- **Total Tokens**: 총 토큰 수
- **Cost**: 예상 비용

#### 3. 실행 흐름 (Trace)
- 체인 실행 단계별 시각화
- 각 컴포넌트의 입력/출력
- 에러 발생 지점 추적

#### 4. 메타데이터
- 태그
- 사용자 정의 메타데이터
- 모델 정보
- 실행 시각

### 필터링 및 검색

- 태그로 필터링
- 날짜/시간 범위 선택
- 성공/실패 상태 필터
- 메타데이터 기반 검색

---

## 💡 실전 활용 팁

### 개발 단계
- 모든 실행을 추적하여 디버깅
- 프롬프트 최적화 A/B 테스트
- 토큰 사용량 분석으로 비용 최적화

### 배포 단계
- 에러 모니터링 및 알림 설정
- 사용자별 토큰 사용량 추적
- 응답 시간 지연 감지

### 최적화 단계
- 느린 실행 찾기 (Latency 정렬)
- 토큰 사용량 많은 쿼리 분석
- 에러율 높은 패턴 파악

---

## ⚙️ 추가 설정

- 프로젝트별 API 키 발급
- 팀원 초대 및 권한 관리
- 알림 설정 (Slack, Email)
- Export 기능으로 데이터 분석

---

## 📊 튜토리얼 완료 후 확인 사항

### 대시보드에서 확인 가능한 내역

- Step 2: 단일 LLM 호출 2건
- Step 3: 스트리밍 호출 1건
- Step 4: 대화 체인 (4턴)
- Step 5: 태그/메타데이터가 포함된 호출 2건

**총 9개 실행 내역**

---

## 📚 학습 내용 정리

1. LangSmith는 환경변수만으로 자동 추적
2. 모든 LLM 호출(invoke, stream)이 기록됨
3. ConversationChain 같은 복잡한 체인도 시각화
4. 태그와 메타데이터로 실행 분류 및 검색
5. 대시보드에서 성능, 비용, 에러 분석 가능

---

## 🚀 다음 단계

- 실제 프로젝트에 LangSmith 적용
- 프롬프트 최적화 실험
- 토큰 사용량 기반 비용 절감
- 에러 모니터링 및 알림 설정

---

## 🔧 문제 해결

### LangSmith 추적이 안 되는 경우

```python
import os
print("LANGCHAIN_TRACING_V2:", os.environ.get("LANGCHAIN_TRACING_V2"))
print("LANGCHAIN_API_KEY:", os.environ.get("LANGCHAIN_API_KEY"))
print("LANGCHAIN_PROJECT:", os.environ.get("LANGCHAIN_PROJECT"))
```

### API 키 오류

```
ValueError: LANGCHAIN_API_KEY not found
```

**해결방법:**
- `.env` 파일에 올바른 LangSmith API 키 설정 확인
- 키에 따옴표나 공백이 없는지 확인

### 추적 비활성화

```python
# 일시적 비활성화
os.environ["LANGCHAIN_TRACING_V2"] = "false"

# 또는 환경변수 삭제
del os.environ["LANGCHAIN_TRACING_V2"]
```

---

## 📚 참고 자료

- [LangSmith 공식 문서](https://docs.smith.langchain.com/)
- [LangChain 공식 문서](https://python.langchain.com/docs/get_started/introduction)
- [LangSmith 추적 설정 가이드](https://wikidocs.net/250954)
