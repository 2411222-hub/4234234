import streamlit as st
import random
import time

# --- 페이지 설정 ---
st.set_page_config(
    page_title="💰 스트림릿 홀짝 게임",
    page_icon="🎲",
    layout="centered"
)

# --- 세션 상태 초기화 ---
# st.session_state를 사용해서 페이지가 새로고침 되어도 값이 유지되도록 합니다.
if 'money' not in st.session_state:
    st.session_state.money = 1000  # 기본 자금 1000원으로 시작
if 'log' not in st.session_state:
    st.session_state.log = [] # 게임 결과를 기록할 리스트

# --- 게임 로직 함수 ---
def play_game(bet_amount, choice):
    # 입력값 검증
    if bet_amount <= 0:
        st.warning("베팅 금액은 0보다 커야 합니다!")
        return
    if bet_amount > st.session_state.money:
        st.warning("가진 돈보다 많이 베팅할 수 없습니다!")
        return

    # 게임 시작: 돈 차감
    st.session_state.money -= bet_amount
    
    # 1부터 10까지 랜덤 숫자 생성
    random_number = random.randint(1, 10)
    
    # 홀/짝 판별
    is_even = (random_number % 2 == 0)
    result = "짝" if is_even else "홀"
    
    # 승패 결정
    win = (choice == result)
    
    # 정산
    if win:
        payout = bet_amount * random_number
        st.session_state.money += payout
        log_message = f"🎉 성공! [{random_number}]이(가) 나왔습니다! {payout}원을 얻었습니다."
        st.success(log_message)
    else:
        payout = bet_amount // random_number  # 나눈 몫만 돌려받음 (소수점 버림)
        st.session_state.money += payout
        log_message = f"😥 실패... [{random_number}]이(가) 나왔습니다. {payout}원을 돌려받았습니다."
        st.error(log_message)

    # 게임 결과 기록
    st.session_state.log.insert(0, log_message) # 최신 기록이 위로 오도록 insert(0, ...) 사용

    # 게임 오버 체크
    if st.session_state.money <= 0:
        st.balloons()
        st.header("GAME OVER")
        st.info("F5를 눌러 게임을 다시 시작하세요.")


# --- 화면 UI 구성 ---
st.title("🎲 스트림릿 홀짝 게임 🎲")
st.markdown("---")

# 현재 자금 표시 (항상 최상단에)
st.header(f"💰 현재 자금: {st.session_state.money:,}원")

# 게임이 끝났는지 확인
if st.session_state.money <= 0:
    st.header("GAME OVER")
    st.info("새 게임을 시작하려면 브라우저를 새로고침(F5)하세요.")
else:
    # --- 입력 폼 (form) ---
    # form을 사용하면 여러 위젯의 입력을 한 번에 처리할 수 있어 편리합니다.
    with st.form("bet_form"):
        col1, col2 = st.columns(2)
        with col1:
            bet_money = st.number_input(
                "베팅할 금액", 
                min_value=1, 
                max_value=st.session_state.money,
                value=min(100, st.session_state.money), # <-- 이 부분이 수정되었습니다!
                step=100
            )
        with col2:
            choice = st.radio(
                "선택하세요",
                ("홀", "짝"),
                horizontal=True
            )
        
        # 폼 제출 버튼
        submitted = st.form_submit_button("💥 결과 확인!", use_container_width=True)

    # "결과 확인" 버튼이 눌렸을 때 게임 로직 실행
    if submitted:
        with st.spinner('숫자를 굴리는 중...'):
            time.sleep(1) # 긴장감을 위한 1초 딜레이
            play_game(bet_money, choice)

st.markdown("---")

# --- 게임 로그 표시 ---
st.subheader("📜 게임 기록")
if not st.session_state.log:
    st.info("아직 게임 기록이 없습니다.")
else:
    for message in st.session_state.log:
        st.text(message)
