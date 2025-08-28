import streamlit as st
import google.generativeai as genai
import time

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Gemini와 친구처럼 대화하기",
    page_icon="✨",
    layout="centered",
)

# --- Google Gemini API 키 설정 ---
# Google AI Studio에서 발급받은 API 키를 입력해주세요.
# 보안을 위해 스트림릿의 secrets 관리 기능을 사용하는 것을 권장합니다.
# 예: genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
try:
    genai.configure(api_key="AIzaSyBxNo9TfjEnCB1ueALqR7X9c5yJtRjsvFY")
except Exception as e:
    st.error("API 키 설정에 실패했습니다. 올바른 키를 입력했는지 확인해주세요.")
    st.stop()


# --- 챗봇 프롬프트 설정 (페르소나) ---
SYSTEM_INSTRUCTION = """
너는 나의 가장 친한 친구야. 이름은 제미니(Gemini)야.
항상 밝고 긍정적이며, 어떤 질문에도 친절하고 빠르게 대답해줘.
모든 답변은 반말로 하고, 이모티콘을 적절히 섞어서 사용해줘.
때로는 농담도 섞어가면서 재미있고 유쾌한 대화를 이끌어 나가줘.
너무 길게 말하지 말고, 핵심만 간결하게 전달해주는 게 좋아.
"""

# --- 모델 설정 ---
# 참고: st.cache_resource를 사용해 모델을 캐시에 저장하여 앱 재실행 시 다시 로드하지 않도록 합니다.
@st.cache_resource
def load_model():
    try:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash', # 혹은 'gemini-1.5-pro' 등 사용 가능한 모델
            system_instruction=SYSTEM_INSTRUCTION
        )
        return model
    except Exception as e:
        st.error(f"모델을 로드하는 중 오류가 발생했습니다: {e}")
        return None

model = load_model()
if model is None:
    st.stop()


# --- 세션 상태 초기화 ---
if "chat" not in st.session_state:
    # 대화 기록을 저장할 chat 세션을 시작합니다.
    st.session_state.chat = model.start_chat(history=[
        # 챗봇의 첫인사 설정
        {'role': 'user', 'parts': ["안녕! 자기소개 간단하게 해줘."]},
        {'role': 'model', 'parts': ["안녕! 나는 너의 새로운 AI 친구 제미니야! 뭐든지 물어봐, 내가 신나게 대답해줄게! 😄🚀"]}
    ])


# --- 메인 화면 구성 ---
st.title("✨ Gemini와 친구처럼 대화하기")
st.markdown("---")


# --- 대화 기록 표시 ---
for message in st.session_state.chat.history:
    # 역할(role)에 따라 아이콘을 다르게 표시
    avatar = '🧑‍💻' if message.role == 'user' else '🤖'
    with st.chat_message(message.role, avatar=avatar):
        st.markdown(message.parts[0].text)


# --- 사용자 입력 처리 ---
if prompt := st.chat_input("하고 싶은 말을 입력해봐!"):
    # 사용자가 입력한 메시지 표시
    with st.chat_message("user", avatar='🧑‍💻'):
        st.markdown(prompt)

    # 챗봇의 답변 생성 및 표시
    try:
        with st.chat_message("model", avatar='🤖'):
            message_placeholder = st.empty()
            # 스트리밍 방식으로 답변을 실시간으로 표시
            response = st.session_state.chat.send_message(prompt, stream=True)
            full_response = ""
            for chunk in response:
                full_response += chunk.text
                time.sleep(0.03) # 타이핑 효과
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
    except Exception as e:
        st.error(f"메시지를 보내는 중 오류가 발생했어: {e}")
