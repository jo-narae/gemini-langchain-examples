# Gemini 2.0 Flash Example

Google Gemini 2.0 Flash 모델을 사용한 Python 예제 프로젝트입니다.

## 프로젝트 구조

```
gemini-example/
├── venv/               # 가상환경 (자동 생성)
├── .env               # API 키 설정 파일
├── .gitignore         # Git 제외 파일 목록
├── example.py         # 실행 예제 파일
├── README.md          # 프로젝트 문서
└── requirements.txt   # 의존성 목록 (선택사항)
```

## 설치 방법

### 1. API 키 발급

Google AI Studio에서 API 키를 발급받으세요:
- https://aistudio.google.com/app/apikey

### 2. 환경 변수 설정

`.env` 파일을 열고 발급받은 API 키를 입력하세요:

```bash
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. 가상환경 생성 및 활성화

#### 가상환경 생성 (처음 한 번만)

**Windows:**
```bash
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

#### 가상환경 활성화

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### 가상환경 비활성화

**모든 OS:**
```bash
deactivate
```

### 4. 의존성 설치

가상환경이 활성화된 상태에서 필요한 패키지를 설치하세요:

```bash
pip install google-genai python-dotenv
```

> **중요**: `google-generativeai`는 2025년 11월 30일에 지원이 종료됩니다. 최신 `google-genai` 패키지를 사용하세요.

## 실행 방법

가상환경이 활성화된 상태에서 예제를 실행하세요:

```bash
python example.py
```

## 예제 내용

`example.py`는 다음과 같은 4가지 예제를 포함합니다:

1. **Simple Text Generation**: 기본 텍스트 생성
2. **Code Generation**: 코드 생성 요청
3. **Interactive Chat**: 대화형 채팅
4. **Streaming Response**: 스트리밍 응답

## 주요 기능

- 환경 변수를 통한 안전한 API 키 관리
- gemini-2.0-flash-exp 모델 사용
- 다양한 사용 사례 예제 제공
- 스트리밍 응답 지원

## 문제 해결

### API 키 오류
- `.env` 파일에 올바른 API 키가 입력되었는지 확인하세요
- API 키에 공백이나 따옴표가 포함되지 않았는지 확인하세요

### 모듈 import 오류
- 가상환경이 활성화되었는지 확인하세요
- 의존성이 올바르게 설치되었는지 확인하세요: `pip list`

### 모델 이름 오류
- gemini-2.0-flash-exp 모델이 사용 가능한지 확인하세요
- 필요시 다른 모델 이름으로 변경할 수 있습니다 (예: gemini-1.5-flash)

## 참고 자료

- [Google AI for Developers](https://ai.google.dev/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Python SDK Documentation](https://ai.google.dev/tutorials/python_quickstart)
