# W11 「은닉 마르코프 모형의 세 부품」: 숨은 상태 사슬 z₁→…→z_T와 표지 5개 관측 x_t, 세 부품(초기확률·전이행렬·방출확률)의 위치
from medfig import *

plt.rcParams["mathtext.default"] = "regular"   # 수식 기호를 기울이지 않음

W, H = 8.0, 5.2
fig, ax = new(W, H)
C_INIT, C_TRANS, C_EMIS = CAT[0], CAT[1], CAT[2]   # 나란한 세 부품
YS, R = 3.9, 0.32                  # 숨은 상태 줄 높이, 원 반지름
cols = [(2.3, "1"), (3.55, "2"), (4.8, "3"), (6.75, "T")]
XD = 5.78                          # ⋯ 위치
pats = [[1, 1, 0, 0, 0],           # 설명용 0/1 패턴 (위에서부터 표지 순서)
        [1, 1, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 1, 0]]
marks = ["H3K4me3", "H3K27ac", "H3K4me1", "H3K36me3", "H3K27me3"]
CW, CH, GAP, TOP = 0.3, 0.24, 0.05, 2.85
BOT = TOP - 5 * CH - 4 * GAP
FILL1 = "#6B7280"

# 숨은 상태, 관측 칸, 방출 화살표
for (x, s), p in zip(cols, pats):
    ax.add_patch(mp.Circle((x, YS), R, fc=STEPS[3], ec=STEPS[0], lw=1.4, zorder=3))
    label(ax, x, YS, f"$z_{{{s}}}$", fs=13, w="bold")
    for i, v in enumerate(p):
        y0 = TOP - (i + 1) * CH - i * GAP
        box(ax, x - CW / 2, y0, CW, CH, fc=FILL1 if v else "white",
            ec=FILL1 if v else "#9AA1AB", lw=1.0, r=0.03)
    arrow(ax, x, YS - R - 0.03, x, TOP + 0.06, color=C_EMIS, lw=2.0)
    label(ax, x, BOT - 0.27, f"$x_{{{s}}}$", fs=13)

# 전이 화살표
xs = [c[0] for c in cols]
arrow(ax, xs[0] + R + 0.03, YS, xs[1] - R - 0.03, YS, color=C_TRANS, lw=2.0)
arrow(ax, xs[1] + R + 0.03, YS, xs[2] - R - 0.03, YS, color=C_TRANS, lw=2.0)
arrow(ax, xs[2] + R + 0.03, YS, XD - 0.22, YS, color=C_TRANS, lw=2.0)
arrow(ax, XD + 0.22, YS, xs[3] - R - 0.03, YS, color=C_TRANS, lw=2.0)
label(ax, XD, YS, "⋯", fs=14, c=TEXT2)
label(ax, XD, (TOP + BOT) / 2, "⋯", fs=14, c=TEXT2)

# 초기확률
arrow(ax, 0.85, YS, xs[0] - R - 0.03, YS, color=C_INIT, lw=2.0)
label(ax, 1.4, 4.85, "초기확률  $\\pi_k$", fs=12.5, w="bold", c=C_INIT)
label(ax, 1.4, 4.52, "$p(z_1 = k)$", fs=11.5, c=TEXT2)

# 전이행렬
tx = (xs[1] + xs[2]) / 2
label(ax, tx, 4.85, "전이행렬  $A_{jk}$", fs=12.5, w="bold", c=C_TRANS)
label(ax, tx, 4.52, "$p(z_t = k \\mid z_{t-1} = j)$", fs=11.5, c=TEXT2)

# 방출확률 (z₁ 방출 화살표 왼쪽)
label(ax, 2.15, 3.36, "방출확률  $\\theta_{km}$", fs=12.5, w="bold", c=C_EMIS, ha="right")
label(ax, 2.15, 3.05, "$p(x_{tm} = 1 \\mid z_t = k)$", fs=11.5, c=TEXT2, ha="right")

# 줄 설명
label(ax, xs[3], 4.6, "숨은 상태 (chromatin state)", fs=11.5, c=TEXT2)
label(ax, 2.0, 2.32, "관측", fs=12, w="bold", ha="right")
label(ax, 2.0, 2.02, "표지 5개의 0/1", fs=11.5, c=TEXT2, ha="right")
for i, m in enumerate(marks):
    yc = TOP - (i + 1) * CH - i * GAP + CH / 2
    label(ax, xs[3] + CW / 2 + 0.12, yc, m, fs=11, c=TEXT2, ha="left")

# 칸 읽는 법
box(ax, 2.15, 0.63, CW, CH, fc=FILL1, ec=FILL1, lw=1.0, r=0.03)
label(ax, 2.55, 0.75, "신호 1", fs=11, c=TEXT2, ha="left")
box(ax, 3.45, 0.63, CW, CH, fc="white", ec="#9AA1AB", lw=1.0, r=0.03)
label(ax, 3.85, 0.75, "신호 0", fs=11, c=TEXT2, ha="left")

save(fig, "../../assets/img/w11/hmm_structure.png")
