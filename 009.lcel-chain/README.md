# 008. LCEL Chain - LangChain Expression Language

LangChain Expression Language (LCEL)을 사용하여 복잡한 체인을 구성하는 방법을 학습합니다.

## LCEL이란?

LCEL은 LangChain의 핵심 개념으로, 파이프(`|`) 연산자를 사용하여 여러 컴포넌트를 연결하는 선언적 방식입니다.

### 기본 구조

```python
chain = component1 | component2 | component3
result = chain.invoke(input)
```

## 파일 구조

```
008.lcel-chain/
├── README.md                    # 이 문서
├── lcel_gemini.py              # 전체 예제 (통합 버전)
├── 01_basic_message.py         # Step 1: 기본 메시지
├── 02_output_parser.py         # Step 2: 출력 파서
├── 03_chain_basic.py           # Step 3: 기본 체인
├── 04_prompt_template.py       # Step 4: 프롬프트 템플릿
├── 05_complete_chain.py        # Step 5: 완전한 체인
└── 06_structured_output.py     # Step 6: 구조화된 출력
```

## 필수 패키지

이 예제를 실행하기 위해 필요한 패키지:

```bash
pip install langchain-google-genai langchain-core pydantic
```

또는 프로젝트 루트에서:

```bash
pip install -r requirements.txt
```

## 학습 순서

단계별로 실행하면서 LCEL의 개념을 이해하세요:

```bash
# 1단계부터 순서대로
python 008.lcel-chain/01_basic_message.py
python 008.lcel-chain/02_output_parser.py
python 008.lcel-chain/03_chain_basic.py
python 008.lcel-chain/04_prompt_template.py
python 008.lcel-chain/05_complete_chain.py
python 008.lcel-chain/06_structured_output.py  # Pydantic 필요
```

## 학습 내용

### Step 1: 기본 메시지 (01_basic_message.py)
- SystemMessage와 HumanMessage 사용
- 모델의 기본 invoke 호출
- AIMessage 응답 받기

### Step 2: 출력 파서 (02_output_parser.py)
- `StrOutputParser`를 사용한 문자열 변환
- AIMessage → 문자열 파싱

### Step 3: 기본 체인 (03_chain_basic.py)
- 첫 번째 체인 구성: `model | parser`
- 파이프 연산자의 동작 원리
- 두 단계를 한 번에 처리

### Step 4: 프롬프트 템플릿 (04_prompt_template.py)
- `ChatPromptTemplate` 사용
- 동적 변수를 활용한 프롬프트 생성
- 템플릿 재사용성

### Step 5: 완전한 체인 (05_complete_chain.py)
- 전체 체인: `prompt | model | parser`
- 여러 시나리오에 동일 체인 재사용
- 입력 변수만 바꿔서 다양한 응답 생성

### Step 6: 구조화된 출력 (06_structured_output.py)
- Pydantic 모델을 사용한 스키마 정의
- `with_structured_output()` 메서드
- 감정 분석과 같은 구조화된 데이터 추출

## LCEL의 장점

1. **가독성**: 데이터 흐름이 명확하게 보임
2. **재사용성**: 한 번 만든 체인을 여러 곳에서 사용
3. **조합성**: 작은 컴포넌트를 조합하여 복잡한 로직 구성
4. **스트리밍**: 자동으로 스트리밍 지원
5. **병렬 처리**: 여러 체인을 동시에 실행 가능

## 주요 컴포넌트

### Prompts
- `ChatPromptTemplate`: 채팅 메시지 템플릿
- `PromptTemplate`: 단순 텍스트 템플릿

### Models
- `ChatGoogleGenerativeAI`: Gemini 채팅 모델
- `with_structured_output()`: 구조화된 출력 강제

### Output Parsers
- `StrOutputParser`: 문자열 파싱
- `JsonOutputParser`: JSON 파싱
- `PydanticOutputParser`: Pydantic 모델 파싱

## 전체 예제 실행

모든 테스트를 한 번에 실행하려면:

```bash
python 008.lcel-chain/lcel_gemini.py
```

## 다음 단계

- 009: 더 복잡한 체인 구성
- RAG (Retrieval-Augmented Generation)
- 에이전트 시스템

## 참고 자료

- [LangChain LCEL 공식 문서](https://python.langchain.com/docs/expression_language/)
- [Gemini API 문서](https://ai.google.dev/gemini-api/docs)
