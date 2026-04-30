import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("統計力学ゲーム１")
st.text("プレイヤー間でランダムにチップを移動させ、チップ枚数の時間変化を観察するシミュレーションです。")

with st.sidebar:
    st.header("パラメータ")
    chipN   = st.slider("チップ総数 (chipN)",   10,  100,  30)
    playerN = st.slider("プレイヤー数 (playerN)", 2,   12,   6)
    turnN   = st.slider("ターン数 (turnN)",      10, 1000, 100, 10)
    rate    = st.slider("税率 (%)",              0,   99,   0)
    run     = st.button("実行", use_container_width=True)

if run or "chips" not in st.session_state:
    chips0 = [0] * playerN
    for k in range(chipN):
        i = np.random.randint(0, playerN)
        chips0[i] += 1

    chips = [chips0[:]]

    for k in range(turnN):
        i = np.random.randint(0, playerN)
        j = np.random.randint(0, playerN)
        if chips0[i] > 0 and i != j:
            nn = 1
            if rate > 0:
                nn += int(chips0[i] * rate / 100.0)
            chips0[i] -= nn
            chips0[j] += nn
        chips.append(chips0[:])

    st.session_state.chips = chips
    st.session_state.playerN = playerN
    st.session_state.turnN = turnN

chips   = st.session_state.chips
playerN = st.session_state.playerN
turnN   = st.session_state.turnN

turns = np.arange(turnN + 1)
chips_t = np.array(chips).T  # shape: (playerN, turnN+1)

fig, ax = plt.subplots(figsize=(10, 5))
for p in range(playerN):
    ax.plot(turns, chips_t[p], label=f"Player {p+1}")
ax.set_xlabel("ターン")
ax.set_ylabel("チップ枚数")
ax.legend(fontsize="small", ncol=max(1, playerN // 6), bbox_to_anchor=(1, 1))
st.pyplot(fig)
plt.close(fig)

df = pd.DataFrame(
    chips,
    index=pd.RangeIndex(turnN + 1, name="turn"),
    columns=[f"Player{p+1}" for p in range(playerN)],
)
csv = df.to_csv(index=True).encode("utf-8")
st.download_button("chips.csv をダウンロード", csv, "chips.csv", "text/csv")
