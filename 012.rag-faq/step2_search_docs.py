"""
RAG FAQ 챗봇 - Step 2: 벡터DB 검색 및 관련 문서 표시

학습 목표:
- step1의 기능 (PDF 업로드 및 벡터DB 저장) 포함
- 벡터DB에서 유사한 문서를 검색하는 방법
- 검색된 관련 문서를 화면에 표시하는 방법
"""

import streamlit as st

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


############################### 벡터DB에서 관련 문서 검색 ##########################

@st.cache_data
def search_related_docs(user_question: str) -> List[Document]:
    """사용자 질문과 유사한 문서를 벡터DB에서 검색"""
    # 임베딩 모델 생성 (저장할 때와 동일한 모델 사용)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # 벡터 DB 로드
    vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    # 관련 문서 3개 검색
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    related_docs: List[Document] = retriever.invoke(user_question)

    return related_docs


############################### Streamlit UI ##########################

def main():
    st.set_page_config("Step 2: 문서 검색", layout="wide")
    st.header("🔍 Step 2: 벡터DB 검색 및 관련 문서 표시")

    st.markdown("""
    ### 이 단계에서 배우는 것:
    1. **전제조건**: step1에서 이미 벡터DB가 생성되어 있어야 함
    2. **새로운 내용**: 사용자 질문으로 유사 문서 검색
    3. 검색된 문서를 화면에 표시

    💡 **참고**: 먼저 step1을 실행하여 벡터DB를 생성해야 합니다!
    """)

    st.divider()

    # 질문 입력
    user_question = st.text_input(
        "질문을 입력해주세요",
        placeholder="예) 청약 1순위 조건이 어떻게 되나요?"
    )

    if user_question:
        st.subheader("📚 검색된 관련 문서")

        # 벡터DB에서 관련 문서 검색
        try:
            related_docs = search_related_docs(user_question)

            # 관련 문서 표시
            for idx, document in enumerate(related_docs, 1):
                with st.expander(f"📄 관련 문서 {idx}"):
                    st.write(document.page_content)

                    # 메타데이터 표시
                    file_path = document.metadata.get('file_path', '')
                    page_number = document.metadata.get('page', 0) + 1
                    st.caption(f"출처: {os.path.basename(file_path)} | 페이지: {page_number}")

            st.info("""
            ### 다음 단계 (step3)에서는:
            - 검색된 문서를 활용하여 Gemini로 답변을 생성합니다
            """)

        except Exception as e:
            st.error(f"❌ 벡터DB를 찾을 수 없습니다. 먼저 PDF를 업로드해주세요.\n오류: {e}")

if __name__ == "__main__":
    main()
