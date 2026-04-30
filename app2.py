import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("統計力学ゲーム2")
st.text("複数のプレイヤーにチップをランダムに配布し、毎ターン無作為に選ばれた2人の間でチップを移動させるシミュレーションです。初期分布と最終分布を比較することで、ランダムな取引がチップの分配に与える影響を観察できます。")

with st.sidebar:
    st.header("パラメータ")
    chipN   = st.slider("チップ総数 (chipN)",        10,  60,  30)
    playerN = st.slider("プレイヤー数 (playerN)",     2,  12,   6)
    turnN   = st.slider("ターン数 (turnN)",          10, 1000, 100,  10)
    simN    = st.slider("シミュレーション回数 (simN)", 10, 1000, 200,  10)
    rate    = st.slider("税率 (%)",                 0,  0,  99)
    run     = st.button("実行", use_container_width=True)

if run or "chipsINI" not in st.session_state:
    chipsINI = []
    chipsEND = []

    for _ in range(simN):
        chips0 = [0] * playerN
        for k in range(chipN):
            i = np.random.randint(0, playerN)
            chips0[i] += 1

        chipsINI.extend(chips0)

        for k in range(turnN):
            i = np.random.randint(0, playerN)
            j = np.random.randint(0, playerN)
            if chips0[i] > 0 and i != j:
                nn = 1
                if rate > 0:
                    nn += int(chips0[i] * rate / 100.0)
                chips0[i] -= nn
                chips0[j] += nn

        chipsEND.extend(chips0)

    st.session_state.chipsINI = chipsINI
    st.session_state.chipsEND = chipsEND

chipsINI = st.session_state.chipsINI
chipsEND = st.session_state.chipsEND

xmax = max(max(chipsINI), max(chipsEND)) + 1
bins = np.arange(0, xmax + 1) - 0.5

col1, col2 = st.columns(2)

with col1:
    st.subheader("初期分布")
    fig1, ax1 = plt.subplots()
    ax1.hist(chipsINI, bins=bins, density=True, color='red', alpha=0.7)
    ax1.set_xlabel("chip N")
    ax1.set_ylabel("density")
    st.pyplot(fig1)
    plt.close(fig1)

with col2:
    st.subheader("最終分布")
    fig2, ax2 = plt.subplots()
    ax2.hist(chipsEND, bins=bins, density=True, color='blue', alpha=0.7)
    ax2.set_xlabel("chip N")
    ax2.set_ylabel("density")
    st.pyplot(fig2)
    plt.close(fig2)
