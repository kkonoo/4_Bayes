# W2 「사후평균은 가중평균입니다」: θ 수직선을 시소로 보고 사전평균·MLE 사이에서 사후평균이 받침점이 되는 모습(n 작을 때와 클 때)
from medfig import *

W, H = 7.9, 5.5
fig, ax = new(W, H)
C_PRI, C_MLE, C_POST = CAT[0], CAT[1], CAT[2]   # 사전평균 / MLE / 사후평균 (나란한 세 항목)

X0, X1 = 0.9, 7.1                                 # θ = 0 … 1 의 가로 위치
def tx(t):
    return X0 + t * (X1 - X0)

P_PRI, P_MLE = 0.25, 0.75                         # 설명용 위치(기호만 표시, 숫자 없음)

def row(yb, tag, w, note, big_prior):
    # 시소 막대 = θ 수직선
    ax.plot([X0, X1], [yb, yb], color="#9AA1AB", lw=3.2, solid_capstyle="round", zorder=2)
    label(ax, X0, yb - 0.28, "0", fs=11, c=TEXT2)
    label(ax, X1, yb - 0.28, "1", fs=11, c=TEXT2)
    label(ax, X1 + 0.22, yb, "θ", fs=12, c=TEXT2, ha="left")
    # 패널 표시와 가중치 설명
    label(ax, 0.15, yb + 1.4, tag, fs=13, w="bold", ha="left")
    label(ax, 7.75, yb + 1.4, note, fs=12, c=TEXT, ha="right")

    xp, xm = tx(P_PRI), tx(P_MLE)
    xq = tx(w * P_PRI + (1 - w) * P_MLE)          # 사후평균 = 받침점 (지렛대가 수평이 되는 자리)
    big, small = (1.1, 0.8), (0.6, 0.44)
    sp, sm = (big, small) if big_prior else (small, big)

    # 무게 상자: 사전 쪽 a+b, 데이터 쪽 n
    for x, (bw, bh), c, txt, cap in [(xp, sp, C_PRI, "a+b", "가상 관측 수"),
                                     (xm, sm, C_MLE, "n", "표본 크기")]:
        box(ax, x - bw / 2, yb + 0.05, bw, bh, fc=c, ec="none", r=0.06, z=3)
        label(ax, x, yb + 0.05 + bh / 2, txt, fs=13 if bw > 1 else 12, w="bold", c=on(c))
        label(ax, x, yb + 0.05 + bh + 0.18, cap, fs=11, c=TEXT2)

    # 받침점(사후평균)
    ax.add_patch(mp.Polygon([(xq, yb - 0.04), (xq - 0.2, yb - 0.36), (xq + 0.2, yb - 0.36)],
                            closed=True, fc=C_POST, ec="none", zorder=3))
    label(ax, xq, yb - 0.62, "사후평균", fs=12, w="bold", c=C_POST)

    # 사전평균과 MLE 이름
    label(ax, xp, yb - 0.28, "사전평균", fs=12, w="bold", c=C_PRI)
    label(ax, xp, yb - 0.55, "a/(a+b)", fs=11, c=TEXT2)
    label(ax, xm, yb - 0.28, "MLE", fs=12, w="bold", c=C_MLE)
    label(ax, xm, yb - 0.55, "k/n", fs=11, c=TEXT2)

# ① n이 작을 때: 사전 무게가 커서 받침점이 사전평균 쪽
row(3.85, "① n이 작을 때", 0.75, "w = (a+b)/(a+b+n) 큼 → 사전평균 쪽", True)
# ② n이 클 때: 데이터 무게가 커서 받침점이 MLE 쪽
row(1.15, "② n이 클 때", 0.25, "w 작음 → MLE 쪽", False)

save(fig, "../../assets/img/w2/weighted_mean.png")
