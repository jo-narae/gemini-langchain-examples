"""
RAG FAQ 챗봇 - Step 4: PDF 페이지 이미지 표시 (완성본)

학습 목표:
- step1~3의 모든 기능 포함
- PDF를 페이지별 이미지로 변환
- 참조 문서 클릭 시 해당 페이지를 화면에 표시
- 2컬럼 레이아웃으로 답변과 PDF를 동시에 확인
"""

import streamlit as st

import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents.base import Document
from langchain_community.vectorstores import FAISS
from typing import List
import os
import fitz  # PyMuPDF
import re
from pathlib import Path

# 환경변수 설정
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Gemini API 키 설정
api_key = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=api_key)


############################### RAG 기능 구현 ##########################

@st.cache_data
def process_question(user_question: str):
    """사용자 질문에 대한 RAG 처리"""
    embeddings = HuggingFaceEmbeddings(
        model_name=os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
    )

    vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    related_docs: List[Document] = retriever.invoke(user_question)

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

    context_text = "\n\n".join([doc.page_content for doc in context])

    prompt = f"""다음의 컨텍스트를 활용해서 질문에 답변해줘
- 질문에 대한 응답을 해줘
- 간결하게 5줄 이내로 해줘
- 곧바로 응답결과를 말해줘

컨텍스트 : {context_text}

질문: {question}

응답:"""

    model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"))
    response = model.generate_content(prompt)

    return response.text


############################### 3단계: PDF 페이지 이미지 변환 및 표시 ##########################

@st.cache_data(show_spinner=False)
def convert_pdf_to_images(pdf_path: str, dpi: int = 250) -> List[str]:
    """PDF의 각 페이지를 이미지로 변환"""
    doc = fitz.open(pdf_path)
    image_paths = []

    # 이미지 저장용 폴더 생성
    output_folder = "PDF_이미지"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        zoom = dpi / 72  # 72이 디폴트 DPI
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat) # type: ignore

        image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        pix.save(image_path)
        image_paths.append(image_path)

    return image_paths

def display_pdf_page(image_path: str, page_number: int) -> None:
    """PDF 페이지 이미지를 표시"""
    image_bytes = open(image_path, "rb").read()
    st.image(image_bytes, caption=f"Page {page_number}", output_format="PNG", width=600)


def natural_sort_key(s):
    """자연스러운 숫자 정렬을 위한 키 함수"""
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)]


############################### Streamlit UI ##########################

def main():
    st.set_page_config("Step 4: PDF 페이지 표시", layout="wide")

    # 2컬럼 레이아웃
    left_column, right_column = st.columns([1, 1])

    with left_column:
        st.header("🎯 Step 4: PDF 페이지 이미지 표시 (완성)")

        st.markdown("""
        ### 이 단계에서 배우는 것:
        1. **전제조건**: step1에서 벡터DB가 이미 생성되어 있어야 함
        2. **새로운 내용**: PDF를 페이지별 이미지로 변환하는 방법
        3. **UI 개선**: 참조 문서 클릭 시 오른쪽에 PDF 페이지 표시
        4. **2컬럼 레이아웃**: 답변과 원본 문서를 동시에 확인

        💡 **참고**: 먼저 step1을 실행하여 벡터DB를 생성해야 합니다!
        """)

        # PDF 이미지 변환 (step1에서 저장한 PDF 사용)
        st.subheader("📄 PDF 이미지 변환")

        # PDF_임시폴더에서 PDF 파일 찾기
        temp_dir = "PDF_임시폴더"
        if os.path.exists(temp_dir):
            pdf_files = [f for f in os.listdir(temp_dir) if f.endswith('.pdf')]
            if pdf_files:
                pdf_file = pdf_files[0]  # 첫 번째 PDF 사용
                pdf_path = os.path.join(temp_dir, pdf_file)

                st.info(f"발견된 PDF: {pdf_file}")

                convert_button = st.button("🖼️ PDF를 이미지로 변환")

                if convert_button:
                    with st.spinner("PDF 페이지를 이미지로 변환하는 중입니다..."):
                        images = convert_pdf_to_images(pdf_path)
                        st.session_state.images = images
                        st.success(f"✅ {len(images)}개 페이지 이미지 변환 완료!")
            else:
                st.warning("PDF_임시폴더에 PDF 파일이 없습니다. step1을 먼저 실행해주세요.")
        else:
            st.warning("PDF_임시폴더가 없습니다. step1을 먼저 실행해주세요.")

        st.divider()

        # 질문 입력
        user_question = st.text_input(
            "질문을 입력해주세요",
            placeholder="예) 청약 1순위 조건이 어떻게 되나요?"
        )

        if user_question:
            try:
                response, context = process_question(user_question)

                # Gemini 답변 표시
                st.subheader("💬 답변")
                st.write(response)

                st.divider()

                # 관련 문서 표시
                st.subheader("📚 참조 문서")
                for idx, document in enumerate(context):
                    with st.expander(f"📄 관련 문서 {idx + 1}"):
                        st.write(document.page_content)

                        # 참조 버튼 (PDF 페이지로 이동)
                        file_path = document.metadata.get('file_path', '')
                        page_number = document.metadata.get('page', 0) + 1
                        button_key = f"link_{file_path}_{page_number}_{idx}"
                        reference_button = st.button(
                            f"🔍 {os.path.basename(file_path)} pg.{page_number}",
                            key=button_key
                        )

                        if reference_button:
                            st.session_state.page_number = str(page_number)

                st.success("""
                ✅ **RAG FAQ 챗봇 완성!**
                - 오른쪽의 '🔍' 버튼을 클릭하면 해당 PDF 페이지가 오른쪽에 표시됩니다
                """)

            except Exception as e:
                st.error(f"❌ 오류가 발생했습니다: {e}")
                st.info("먼저 PDF를 업로드해주세요.")

    # 오른쪽: PDF 페이지 이미지 표시
    with right_column:
        st.header("📄 PDF 페이지")

        page_number = st.session_state.get("page_number")

        if page_number:
            page_number = int(page_number)
            image_folder = "PDF_이미지"
            if os.path.exists(image_folder):
                images = sorted(os.listdir(image_folder), key=natural_sort_key)
                image_paths = [os.path.join(image_folder, img) for img in images]
                if page_number - 1 < len(image_paths):
                    display_pdf_page(image_paths[page_number - 1], page_number)
                else:
                    st.warning("해당 페이지를 찾을 수 없습니다.")
            else:
                st.info("PDF 이미지가 아직 생성되지 않았습니다.")
        else:
            st.info("왼쪽에서 참조 문서의 '🔍' 버튼을 클릭하면 해당 페이지가 여기에 표시됩니다.")

if __name__ == "__main__":
    main()
