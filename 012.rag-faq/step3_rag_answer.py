"""
RAG FAQ 챗봇 - Step 3: RAG 답변 생성

학습 목표:
- step1, step2의 기능 포함
- 검색된 문서를 컨텍스트로 활용
- Gemini API로 답변 생성하는 방법
- RAG(Retrieval Augmented Generation)의 완성
"""

import streamlit as st

import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents.base import Document
from langchain_community.vectorstores import FAISS
from typing import List
import os
from pathlib import Path

# 환경변수 설정
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Gemini API 키 설정
api_key = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=api_key)


############################### RAG - 검색 및 답변 생성 ##########################

@st.cache_data
def process_question(user_question: str):
    """사용자 질문에 대한 RAG 처리"""
    # 임베딩 모델 생성 (저장할 때와 동일한 모델 사용)
    embeddings = HuggingFaceEmbeddings(
        model_name=os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
    )

    # 벡터 DB 로드
    vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    # 관련 문서 3개 검색
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    related_docs: List[Document] = retriever.invoke(user_question)

    # Gemini로 답변 생성
    response = generate_answer(user_question, related_docs)

    return response, related_docs


def generate_answer(question: str, context: List[Document]) -> str:
    """Gemini API를 직접 사용해서 답변 생성"""
    # API 키 재설정 (캐싱 문제 방지) - dotenv를 다시 로드
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("GEMINI_API_KEY", "")
    genai.configure(api_key=api_key)

    # 컨텍스트를 문자열로 변환
    context_text = "\n\n".join([doc.page_content for doc in context])

    # 프롬프트 생성
    prompt = f"""다음의 컨텍스트를 활용해서 질문에 답변해줘
- 질문에 대한 응답을 해줘
- 간결하게 5줄 이내로 해줘
- 곧바로 응답결과를 말해줘

컨텍스트 : {context_text}

질문: {question}

응답:"""

    # Gemini 모델 호출
    model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"))
    response = model.generate_content(prompt)

    return response.text


############################### Streamlit UI ##########################

def main():
    st.set_page_config("Step 3: RAG 답변 생성", layout="wide")
    st.header("🤖 Step 3: RAG 답변 생성")

    st.markdown("""
    ### 이 단계에서 배우는 것:
    1. **전제조건**: step1에서 벡터DB가 이미 생성되어 있어야 함
    2. **새로운 내용**: 검색된 문서를 컨텍스트로 활용하여 Gemini로 답변 생성
    3. **RAG 완성**: Retrieval (검색) + Augmented (보강) + Generation (생성)

    💡 **참고**: 먼저 step1을 실행하여 벡터DB를 생성해야 합니다!
    """)

    st.divider()

    # 질문 입력
    user_question = st.text_input(
        "질문을 입력해주세요",
        placeholder="예) 청약 1순위 조건이 어떻게 되나요?"
    )

    if user_question:
        try:
            # RAG 처리: 검색 + 답변 생성
            response, context = process_question(user_question)

            # Gemini 답변 표시
            st.subheader("💬 Gemini 답변")
            st.write(response)

            st.divider()

            # 관련 문서 표시
            st.subheader("📚 참조한 문서")
            for idx, document in enumerate(context, 1):
                with st.expander(f"📄 관련 문서 {idx}"):
                    st.write(document.page_content)

                    # 메타데이터 표시
                    file_path = document.metadata.get('file_path', '')
                    page_number = document.metadata.get('page', 0) + 1
                    st.caption(f"출처: {os.path.basename(file_path)} | 페이지: {page_number}")

            st.info("""
            ### 다음 단계 (step4)에서는:
            - 참조 문서를 클릭하면 해당 PDF 페이지를 이미지로 표시하는 기능을 추가합니다
            """)

        except Exception as e:
            st.error(f"❌ 오류가 발생했습니다: {e}")
            st.info("먼저 PDF를 업로드해주세요.")

if __name__ == "__main__":
    main()
