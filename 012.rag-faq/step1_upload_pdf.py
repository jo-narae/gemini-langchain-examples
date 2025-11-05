"""
RAG FAQ 챗봇 - Step 1: PDF 업로드 및 벡터DB 저장

학습 목표:
- PDF 파일을 업로드하는 방법
- PDF를 Document로 변환하는 방법
- Document를 작은 청크로 나누는 방법
- 벡터DB(FAISS)에 저장하는 방법
"""

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyMuPDFLoader
from typing import List
import os
from pathlib import Path
from dotenv import load_dotenv

# 환경변수 설정
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


############################### PDF 문서를 벡터DB에 저장하는 함수들 ##########################

## 1: 임시폴더에 파일 저장
def save_uploadedfile(uploadedfile: UploadedFile) -> str :
    """업로드된 PDF 파일을 임시 폴더에 저장"""
    temp_dir = "PDF_임시폴더"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_path = os.path.join(temp_dir, uploadedfile.name)
    with open(file_path, "wb") as f:
        f.write(uploadedfile.read())
    return file_path

## 2: 저장된 PDF 파일을 Document로 변환
def pdf_to_documents(pdf_path: str) -> List[Document]:
    """PDF 파일을 LangChain Document 객체로 변환"""
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()
    # metadata에 file_path 추가 (나중에 참조용)
    for doc in documents:
        doc.metadata['file_path'] = pdf_path
    return documents

## 3: Document를 더 작은 document로 변환
def chunk_documents(documents: List[Document]) -> List[Document]:
    """큰 Document를 작은 청크로 분할"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # 청크 크기
        chunk_overlap=150  # 청크 간 겹치는 부분
    )
    return text_splitter.split_documents(documents)

## 4: Document를 벡터DB로 저장
def save_to_vector_store(documents: List[Document]) -> None:
    """청크를 벡터 임베딩으로 변환하여 FAISS DB에 저장"""
    # 로컬 임베딩 모델 사용 (무료, Google Cloud 인증 불필요)
    embeddings = HuggingFaceEmbeddings(
        model_name=os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
    )
    vector_store = FAISS.from_documents(documents, embedding=embeddings)
    vector_store.save_local("faiss_index")


############################### Streamlit UI ##########################

def main():
    st.set_page_config("Step 1: PDF 업로드", layout="wide")
    st.header("📄 Step 1: PDF 업로드 및 벡터DB 저장")

    st.markdown("""
    ### 이 단계에서 배우는 것:
    1. PDF 파일을 업로드하는 방법
    2. PDF를 Document로 변환
    3. Document를 작은 청크로 분할
    4. 벡터 임베딩을 생성하여 FAISS DB에 저장
    """)

    # PDF 업로드
    pdf_doc = st.file_uploader("PDF 파일을 업로드 해주세요", type=["pdf"])
    upload_button = st.button("PDF 문서 저장")

    if pdf_doc and upload_button:
        # 진행 상황을 보여줄 컨테이너 생성
        progress_container = st.container()

        with progress_container:
            # 1단계: PDF 파일 저장
            with st.spinner("1️⃣ PDF 파일을 저장하는 중..."):
                pdf_path = save_uploadedfile(pdf_doc)
            st.success(f"✅ 1단계 완료: PDF 파일 저장 → `{pdf_path}`")

            # 2단계: PDF를 Document로 변환
            with st.spinner("2️⃣ PDF를 Document로 변환하는 중..."):
                pdf_documents = pdf_to_documents(pdf_path)
            st.success(f"✅ 2단계 완료: Document 변환 → {len(pdf_documents)}개 페이지")

            # 3단계: Document를 작은 청크로 분할
            with st.spinner("3️⃣ Document를 작은 청크로 분할하는 중..."):
                smaller_documents = chunk_documents(pdf_documents)
            st.success(f"✅ 3단계 완료: 청크 분할 → {len(smaller_documents)}개 청크")

            # 4단계: 벡터DB에 저장
            with st.spinner("4️⃣ 벡터 임베딩을 생성하고 FAISS DB에 저장하는 중... (시간이 걸릴 수 있습니다)"):
                save_to_vector_store(smaller_documents)
            st.success("✅ 4단계 완료: 벡터DB 저장 성공!")

            st.balloons()

            st.info("""
            ### 🎉 모든 단계 완료!

            다음 단계 (step2)에서는:
            - 저장된 벡터DB에서 관련 문서를 검색하는 방법을 배웁니다
            """)

if __name__ == "__main__":
    main()
