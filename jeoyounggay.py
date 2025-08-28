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
if 'money' not in st.session_state:
    st.session_state.money = 1000
if 'log' not in st.session_state:
    st.session_state.log = []

# --- 게임 로직 함수 ---
def play_game(bet_amount, choice):
    if bet_amount <= 0:
        st.warning("베팅 금액은 0보다 커야 합니다!")
        return
    if bet_amount > st.session_state.money:
        st.warning("가진 돈보다 많이 베팅할 수 없습니다!")
        return

    st.session_state.money -= bet_amount
    random_number = random.randint(1, 10)
    result = "짝" if (random_number % 2 == 0) else "홀"
    win = (choice == result)

    if win:
        payout = bet_amount * random_number
        st.session_state.money += payout
        log_message = f"🎉 성공! [{random_number}]이(가) 나왔습니다! {payout}원을 얻었습니다."
        # 성공 메시지는 success 박스로 표시 (rerun 되기 전 잠시 보임)
        st.success(log_message)
    else:
        payout = bet_amount // random_number
        st.session_state.money += payout
        log_message = f"😥 실패... [{random_number}]이(가) 나왔습니다. {payout}원을 돌려받았습니다."
        # 실패 메시지는 error 박스로 표시 (rerun 되기 전 잠시 보임)
        st.error(log_message)

    st.session_state.log.insert(0, log_message)

    if st.session_state.money <= 0:
        st.balloons()

# --- 화면 UI 구성 ---
st.title("🎲 스트림릿 홀짝 게임 🎲")
st.markdown("---")

st.header(f"💰 현재 자금: {st.session_state.money:,}원")

if st.session_state.money <= 0:
    st.header("GAME OVER")
    st.info("새 게임을 시작하려면 브라우저를 새로고침(F5)하세요.")
else:
    with st.form("bet_form"):
        col1, col2 = st.columns(2)
        with col1:
            bet_money = st.number_input(
                "베팅할 금액",
                min_value=1,
                max_value=st.session_state.money,
                value=min(100, st.session_state.money),
                step=100
            )
        with col2:
            choice = st.radio(
                "선택하세요",
                ("홀", "짝"),
                horizontal=True
            )
        submitted = st.form_submit_button("💥 결과 확인!", use_container_width=True)

    if submitted:
        with st.spinner('숫자를 굴리는 중...'):
            time.sleep(1)
            play_game(bet_money, choice)
            # 게임 로직 실행 후 즉시 스크립트를 재실행하여 화면을 업데이트합니다.
            st.rerun()

st.markdown("---")

st.subheader("📜 게임 기록")
if not st.session_state.log:
    st.info("아직 게임 기록이 없습니다.")
else:
    # 성공/실패 메시지를 로그에서 직접 렌더링
    for message in st.session_state.log:
        if "성공" in message:
            st.success(message)
        else:
            st.error(message)
