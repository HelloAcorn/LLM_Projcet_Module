import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

st.set_page_config(
    page_title="LLM Project Module",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 LLM Project Module")
st.markdown("범용 Prompt Engineering 및 RAG 프로젝트를 위한 대화형 인터페이스")

# Sidebar navigation
st.sidebar.title("네비게이션")
page = st.sidebar.radio(
    "페이지 선택",
    ["홈", "Simple Prompt", "RAG 검색", "에이전트", "설정"]
)

if page == "홈":
    st.markdown("""
    ## 환영합니다! 👋
    
    이 애플리케이션은 다양한 LLM 기반 작업을 수행할 수 있습니다:
    
    - **Simple Prompt**: 기본 LLM 쿼리
    - **RAG 검색**: 문서 기반 검색 및 응답 생성
    - **에이전트**: 복잡한 작업 자동화
    - **설정**: API 키 및 모델 설정
    """)

elif page == "Simple Prompt":
    st.header("Simple Prompt")
    user_query = st.text_area("질문을 입력하세요:", height=100)
    
    if st.button("전송"):
        if user_query:
            st.info("응답 생성 중...")
            # LLM 호출 로직
            st.success("응답이 생성되었습니다!")
        else:
            st.warning("질문을 입력해주세요.")

elif page == "RAG 검색":
    st.header("RAG 검색")
    st.markdown("문서 기반 검색 및 응답 생성")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("문서 업로드", type=["pdf", "txt", "md"])
    
    with col2:
        st.write("업로드된 문서 수: 0")
    
    query = st.text_input("검색 쿼리:")
    if st.button("검색"):
        if query:
            st.info("검색 중...")
            st.success("결과를 찾았습니다!")
        else:
            st.warning("쿼리를 입력해주세요.")

elif page == "에이전트":
    st.header("에이전트")
    st.markdown("복잡한 작업을 자동으로 처리합니다")
    
    agent_type = st.selectbox("에이전트 선택", ["ReAct", "Plan & Execute", "Reflection"])
    task = st.text_area("작업 설명:", height=100)
    
    if st.button("실행"):
        if task:
            st.info("에이전트 실행 중...")
            st.success("작업이 완료되었습니다!")
        else:
            st.warning("작업을 입력해주세요.")

elif page == "설정":
    st.header("⚙️ 설정")
    
    with st.expander("API 설정"):
        openai_key = st.text_input("OpenAI API Key", type="password")
        anthropic_key = st.text_input("Anthropic API Key", type="password")
    
    with st.expander("모델 설정"):
        llm_model = st.selectbox("LLM 모델", ["gpt-4", "gpt-3.5-turbo", "claude-3-opus"])
        embedding_model = st.selectbox("Embedding 모델", ["text-embedding-3-large", "bge-base-en-v1.5"])
    
    if st.button("저장"):
        st.success("설정이 저장되었습니다!")

