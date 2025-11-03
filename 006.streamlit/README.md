# Streamlit Gemini Chat

Streamlit을 사용한 Gemini 2.0 Flash 채팅 웹 애플리케이션입니다.

## 특징

- 💬 실시간 채팅 인터페이스
- ⚙️ Temperature, System Instruction 설정 가능
- 🔄 대화 히스토리 관리 (reset 기능)
- 🎯 Thinking 모드 제어
- 🔐 안전한 API 키 입력 (password 타입)

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

### 2. Streamlit 설치

```bash
pip install streamlit
```

또는 프로젝트 루트에서:

```bash
pip install -r requirements.txt
```

## 실행 방법

### 방법 1: streamlit 명령어 사용

```bash
streamlit run 006.streamlit/streamlit-chat.py
```

### 방법 2: 가상환경의 streamlit 직접 사용

**Windows:**
```bash
venv\Scripts\streamlit.exe run 006.streamlit/streamlit-chat.py
```

**macOS/Linux:**
```bash
venv/bin/streamlit run 006.streamlit/streamlit-chat.py
```

### 방법 3: 폴더 내에서 실행

```bash
cd 006.streamlit
streamlit run streamlit-chat.py
```

## 사용 방법

1. **API 키 설정**
   - 좌측 사이드바에서 `GEMINI_API_KEY` 입력
   - 또는 프로젝트 루트의 `.env` 파일에 설정

2. **설정 조정**
   - **Temperature**: 0.0 (일관적) ~ 1.0 (창의적)
   - **Disable Thinking**: Thinking 모드 비활성화 여부
   - **System Instruction**: AI의 역할/스타일 지정

3. **채팅 시작**
   - 하단 입력창에 메시지 입력
   - `reset` 명령어로 대화 초기화

## 주요 설정

### Temperature
- `0.0`: 가장 일관적이고 결정론적인 답변
- `0.7`: 균형잡힌 설정 (기본값)
- `1.0`: 가장 창의적이고 다양한 답변

### System Instruction
AI의 성격과 답변 스타일을 지정합니다.

**예시:**
```
너는 친절한 선생님이야. 쉽게 설명해줘.
```

### Thinking Mode
- **활성화**: AI가 내부적으로 사고 과정을 거침 (느리지만 정확)
- **비활성화**: 빠른 답변 (기본값)

## 명령어

채팅 입력창에서 사용 가능한 명령어:

- `reset`: 대화 히스토리 초기화

## 주의사항

1. **API 키 보안**
   - `.env` 파일을 git에 커밋하지 마세요
   - API 키를 공개적으로 공유하지 마세요

2. **포트 충돌**
   - 기본 포트: `8501`
   - 다른 포트 사용: `streamlit run app.py --server.port 8502`

3. **브라우저**
   - 실행 후 자동으로 브라우저가 열립니다
   - 수동 접속: `http://localhost:8501`

## 파일 구조

```
006.streamlit/
├── streamlit-chat.py    # 메인 애플리케이션
└── README.md            # 이 파일
```

## 문제 해결

### Streamlit이 설치되지 않음
```bash
pip install streamlit
```

### 포트가 이미 사용 중
```bash
streamlit run streamlit-chat.py --server.port 8502
```

### API 키 오류
- `.env` 파일에 `GEMINI_API_KEY` 확인
- 사이드바에서 직접 입력

### 대화가 초기화되지 않음
- 브라우저 새로고침 (F5)
- 또는 `reset` 명령어 입력

## 참고 자료

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google Gen AI SDK](https://googleapis.github.io/python-genai/)
