import streamlit as st
import random
import time
import pandas as pd  # 그래프를 위해 pandas를 추가합니다.

# --- 페이지 설정 ---
st.set_page_config(
    page_title="💰 스트림릿 홀짝 게임",
    page_icon="🎲",
    layout="centered"
)

# --- 세션 상태 초기화 ---
if 'money' not in st.session_state:
    st.session_state.money = 1000
    # 자금 변동을 기록할 리스트를 만들고, 시작 자금을 첫 값으로 넣습니다.
    st.session_state.money_history = [1000]
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
        st.success(log_message)
    else:
        payout = bet_amount // random_number
        st.session_state.money += payout
        log_message = f"😥 실패... [{random_number}]이(가) 나왔습니다. {payout}원을 돌려받았습니다."
        st.error(log_message)

    st.session_state.log.insert(0, log_message)
    # 게임 후 자금을 history 리스트에 추가합니다.
    st.session_state.money_history.append(st.session_state.money)

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
            st.rerun()

st.markdown("---")

# --- 자금 변동 그래프 ---
# 게임을 한 번 이상 진행했을 때만 그래프를 표시합니다.
if len(st.session_state.money_history) > 1:
    st.subheader("💸 자금 변동 그래프")
    # pandas DataFrame으로 데이터를 변환하여 보기 좋게 만듭니다.
    chart_data = pd.DataFrame({
        '자금': st.session_state.money_history
    })
    # x축은 '게임 횟수'를 의미하게 됩니다 (0회차, 1회차, ...)
    st.line_chart(chart_data)


# --- 게임 로그 표시 ---
st.subheader("📜 게임 기록")
if not st.session_state.log:
    st.info("아직 게임 기록이 없습니다.")
else:
    for message in st.session_state.log:
        if "성공" in message:
            st.success(message)
        else:
            st.error(message)
