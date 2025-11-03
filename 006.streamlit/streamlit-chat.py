import os
from dotenv import load_dotenv
import streamlit as st
from google import genai
from google.genai import types

# =============================================================================
# 상수 정의
# =============================================================================
MODEL_NAME = "gemini-2.0-flash"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_SYSTEM_INSTRUCTION = (
    "너는 사용자를 도와주는 상담사야. 공감적으로 답하고, "
    "불명확하면 짧게 되물어봐. 필요하면 단계별로 안내해줘."
)

# =============================================================================
# 초기화
# =============================================================================
load_dotenv()
DEFAULT_API_KEY = os.getenv("GEMINI_API_KEY", "")

st.set_page_config(page_title="Gemini Chat", page_icon="💬")

# =============================================================================
# 헬퍼 함수
# =============================================================================
def init_session_state():
    """세션 상태 초기화"""
    if "history" not in st.session_state:
        st.session_state.history = []
    if "system_instruction" not in st.session_state:
        st.session_state.system_instruction = DEFAULT_SYSTEM_INSTRUCTION


def reset_conversation():
    """대화 초기화"""
    st.session_state.history = []
    st.session_state.system_instruction = DEFAULT_SYSTEM_INSTRUCTION


def render_sidebar():
    """사이드바 UI 렌더링 및 설정값 반환"""
    st.sidebar.title("⚙️ 설정")

    api_key = st.sidebar.text_input(
        "GEMINI_API_KEY",
        value=DEFAULT_API_KEY,
        type="password"
    )

    temperature = st.sidebar.slider(
        "Temperature",
        0.0, 1.0, DEFAULT_TEMPERATURE, 0.05
    )

    thinking_off = st.sidebar.checkbox("Disable Thinking", value=True)

    if st.sidebar.button("💥 Reset"):
        reset_conversation()
        st.rerun()

    system_instruction = st.sidebar.text_area(
        "System Instruction",
        value=st.session_state.system_instruction,
        height=120
    )
    st.session_state.system_instruction = system_instruction

    return api_key, temperature, thinking_off, system_instruction


def render_chat_history():
    """대화 히스토리 렌더링"""
    for msg in st.session_state.history:
        role = "assistant" if msg.role == "model" else "user"
        text = "".join(p.text for p in msg.parts if hasattr(p, "text"))
        with st.chat_message(role):
            st.markdown(text)


def create_config(system_instruction, temperature, thinking_off):
    """GenerateContentConfig 생성"""
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
    )
    if thinking_off:
        config.thinking_config = types.ThinkingConfig(thinking_budget=0)
    return config


# =============================================================================
# 메인 로직
# =============================================================================
init_session_state()

# 사이드바 설정
api_key, temperature, thinking_off, system_instruction = render_sidebar()

# API 키 검증
if not api_key:
    st.warning("좌측 사이드바에 GEMINI_API_KEY를 입력하세요.")
    st.stop()

# 클라이언트 생성
client = genai.Client(api_key=api_key)

# =============================================================================
# UI 렌더링
# =============================================================================
st.title("💬 Gemini Chat")

# 채팅 히스토리 표시
render_chat_history()

# =============================================================================
# 사용자 입력 처리
# =============================================================================
user_input = st.chat_input("메시지를 입력하세요 (reset 명령어 지원)")

if user_input:
    # reset 명령어 처리
    if user_input.strip().lower() == "reset":
        reset_conversation()
        st.rerun()

    # 사용자 메시지 추가
    st.session_state.history.append(
        types.Content(role="user", parts=[types.Part(text=user_input)])
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    config = create_config(system_instruction, temperature, thinking_off)

    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=st.session_state.history,
                config=config,
            )
            assistant_text = response.text or "(빈 응답)"
            st.markdown(assistant_text)

    # AI 응답 추가
    st.session_state.history.append(
        types.Content(role="model", parts=[types.Part(text=assistant_text)])
    )