# Gemini API with LangChain Examples

Google Gemini API와 LangChain을 활용한 Python 예제 모음 프로젝트입니다.

## 프로젝트 구조

```
gemini-example/
├── 001.single-turn/              # 단일 턴 대화 예제
├── 002.multi-turn/               # 다중 턴 대화 예제
├── 003.zero-shot/                # Zero-shot 프롬프팅
├── 004.one-shot/                 # One-shot 프롬프팅
├── 005.few-shot/                 # Few-shot 프롬프팅
├── 006.streamlit/                # Streamlit 챗봇 UI
├── 007.langchain-basic/          # LangChain 기초
├── 008.langsmith/                # LangSmith 추적 및 모니터링
├── 009.lcel-chain/               # LCEL Chain 예제
├── 010.langchain-agent-tools/    # LangChain Agent & Tools
├── 011.stream-output/            # 스트리밍 출력 처리
├── 012.rag-faq/                  # RAG 기반 FAQ 챗봇
├── venv/                         # 가상환경 (자동 생성)
├── .env                          # 환경 변수 설정
├── .env.example                  # 환경 변수 템플릿
├── .gitignore                    # Git 제외 파일
├── example.py                    # 기본 실행 예제
├── requirements.txt              # 의존성 목록
└── README.md                     # 프로젝트 문서
```

## 빠른 시작

### 1. API 키 발급

Google AI Studio에서 API 키를 발급받으세요:
- https://aistudio.google.com/app/apikey

### 2. 환경 설정

`.env.example` 파일을 `.env`로 복사하고 API 키를 입력하세요:

```bash
cp .env.example .env
```

`.env` 파일 편집:

```bash
# Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Gemini Model Configuration
GEMINI_MODEL=gemini-2.5-flash-lite

# Embedding Model Configuration
EMBEDDING_MODEL=BAAI/bge-m3
```

### 3. 가상환경 설정

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. 의존성 설치

```bash
pip install -r requirements.txt
```

## 튜토리얼 가이드

### 기초 예제 (001-005)

**001.single-turn**: Gemini API를 사용한 기본 단일 턴 대화
```bash
python 001.single-turn/single_turn.py
```

**002.multi-turn**: 대화 히스토리를 유지하는 다중 턴 대화
```bash
python 002.multi-turn/multi-turn.py
```

**003.zero-shot**: 예제 없이 프롬프트만으로 작업 수행
```bash
python 003.zero-shot/zero-shot.py
```

**004.one-shot**: 하나의 예제를 제공하여 작업 수행
```bash
python 004.one-shot/one-shot.py
```

**005.few-shot**: 여러 예제를 제공하여 더 나은 결과 도출
```bash
python 005.few-shot/few-shot.py
```

### Streamlit 챗봇 (006)

**006.streamlit**: 웹 UI 기반 대화형 챗봇
```bash
cd 006.streamlit
streamlit run start.py
```

### LangChain 기초 (007)

**007.langchain-basic**: LangChain의 기본 개념과 대화 히스토리 관리
- `00_why_langchain.py`: LangChain을 사용하는 이유
- `01_langchain_basic.py`: 기본 사용법
- `02_history_step*.py`: 대화 히스토리 관리 단계별 학습

상세한 내용은 [007.langchain-basic/README.md](007.langchain-basic/README.md)를 참고하세요.

### LangSmith 모니터링 (008)

**008.langsmith**: LLM 애플리케이션 추적 및 모니터링
```bash
python 008.langsmith/langsmith_tutorial.py
```

LangSmith 대시보드에서 실행 내역, 토큰 사용량, 성능 분석이 가능합니다.
상세 가이드: [008.langsmith/langsmith_tutorial.md](008.langsmith/langsmith_tutorial.md)

### LCEL Chain (009)

**009.lcel-chain**: LangChain Expression Language를 사용한 체인 구성
- 메시지 처리, 출력 파싱, 프롬프트 템플릿, 구조화된 출력 등

각 파일을 순서대로 실행하여 LCEL의 개념을 학습할 수 있습니다.

### Agent & Tools (010)

**010.langchain-agent-tools**: LangChain Agent와 도구 활용
- 기본 채팅, 도구 정의, 도구 호출, 자동 에이전트 등

```bash
python 010.langchain-agent-tools/01_basic_chat.py
```

### 스트리밍 (011)

**011.stream-output**: 실시간 스트리밍 응답 처리
- 기본 스트리밍
- 도구와 함께 사용하는 스트리밍

```bash
python 011.stream-output/stream_basic.py
```

### RAG FAQ 챗봇 (012)

**012.rag-faq**: Retrieval-Augmented Generation 기반 FAQ 챗봇

단계별 학습:
1. `step1_upload_pdf.py`: PDF 업로드 및 벡터DB 저장
2. `step2_search_docs.py`: 벡터DB 검색
3. `step3_rag_answer.py`: RAG 기반 답변 생성
4. `step4_show_pdf_page.py`: PDF 페이지 표시
5. `finish.py`: 완성된 챗봇

```bash
cd 012.rag-faq
streamlit run step1_upload_pdf.py
```

## 주요 기능

### 환경 변수 기반 설정
- `.env` 파일에서 모든 설정 관리
- 모델명과 임베딩 모델을 중앙에서 제어
- API 키 안전 관리

### 다양한 Gemini 모델 지원
- gemini-2.5-flash-lite (기본값)
- gemini-2.0-flash
- gemini-2.0-flash-exp
- gemini-1.5-pro

### LangChain 통합
- ChatGoogleGenerativeAI 활용
- 대화 히스토리 관리
- LCEL 체인 구성
- Agent 및 Tools 활용

### 벡터 데이터베이스
- FAISS를 사용한 로컬 벡터 검색
- HuggingFace 임베딩 모델 (BAAI/bge-m3)
- RAG 구현

## 환경 변수 설정

### GEMINI_API_KEY
Google AI Studio에서 발급받은 API 키

### GEMINI_MODEL
사용할 Gemini 모델명 (기본값: gemini-2.5-flash-lite)

### EMBEDDING_MODEL
벡터 임베딩 모델명 (기본값: BAAI/bge-m3)
- API 키 불필요
- 로컬에서 실행
- 다국어 지원

### LangSmith 설정 (선택사항)
```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=my-project-name
```

## 문제 해결

### API 키 오류
- `.env` 파일에 올바른 API 키가 입력되었는지 확인
- API 키에 공백이나 따옴표가 포함되지 않았는지 확인

### 모듈 import 오류
- 가상환경이 활성화되었는지 확인
- 의존성 설치 확인: `pip list`

### LangChain 관련 오류
LangChain 1.0 이상에서는 일부 모듈이 이동되었습니다:
- `langchain.chains` → `langchain-classic`
- `langchain.memory` → `langchain-classic`

필요한 패키지를 설치하세요:
```bash
pip install langchain-classic langchain-community
```

### 임베딩 모델 다운로드
첫 실행 시 HuggingFace에서 모델을 자동으로 다운로드합니다.
- API 키 불필요
- 인터넷 연결 필요 (첫 실행 시만)
- 로컬 캐시에 저장: `~/.cache/huggingface/`

## 패키지 버전

주요 의존성:
- `google-genai>=1.47.0`
- `langchain>=0.3.0`
- `langchain-google-genai>=3.0.0`
- `langchain-classic>=1.0.0`
- `langchain-community>=0.4.0`
- `streamlit>=1.51.0`
- `python-dotenv>=1.2.1`

전체 목록은 [requirements.txt](requirements.txt)를 참고하세요.

## 참고 자료

### Google Gemini
- [Google AI for Developers](https://ai.google.dev/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Python SDK Documentation](https://ai.google.dev/tutorials/python_quickstart)

### LangChain
- [LangChain 공식 문서](https://python.langchain.com/)
- [LangChain Expression Language (LCEL)](https://python.langchain.com/docs/expression_language/)
- [LangSmith](https://smith.langchain.com/)

### Vector Databases
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [HuggingFace Embeddings](https://huggingface.co/models?pipeline_tag=sentence-similarity)

## 라이선스

이 프로젝트는 교육 목적으로 제공됩니다.

## 기여

이슈나 개선 사항이 있으면 GitHub Issues를 통해 알려주세요.
