# W5 「Metropolis 알고리즘」: 제안 → 수용확률 → 이동/제자리 → 다음 걸음으로 도는 한 걸음의 순환 흐름
from medfig import *

W, H = 8.0, 6.0
fig, ax = new(W, H)
STEP = ramp(3)                      # ① ② ③ 순서 있는 단계
C_MOVE, C_STAY = CAT[2], CAT[3]     # 이동 / 제자리 (나란한 두 결과)

BX0, BX1 = 0.9, 5.0                 # 단계 칸의 좌우
BW = BX1 - BX0
BH = 0.8

def step(y0, n, title, sub, c):
    box(ax, BX0, y0, BW, BH, fc="white", ec=c, lw=1.5, r=0.1)
    num(ax, BX0 + 0.36, y0 + BH / 2, n, fc=c, r=0.19, fs=12)
    label(ax, BX0 + 0.72, y0 + BH / 2 + 0.16, title, fs=13, w="bold", c=TEXT, ha="left")
    label(ax, BX0 + 0.72, y0 + BH / 2 - 0.18, sub, fs=12, c=TEXT, ha="left")

# ① ② ③ 단계 (위에서 아래로)
Y1, Y2, Y3 = 5.0, 3.7, 2.4
step(Y1, 1, "제안", "현재 위치 θ에서  θ′ ∼ Normal(θ, τ²)", STEP[0])
step(Y2, 2, "수용확률 계산", "α = min{1,  p(θ′|y) / p(θ|y)}", STEP[1])
step(Y3, 3, "이동 여부 결정", "확률 α로 θ′로 이동, 아니면 제자리", STEP[2])
XA = 3.2
arrow(ax, XA, Y1 - 0.02, XA, Y2 + BH + 0.02)
arrow(ax, XA, Y2 - 0.02, XA, Y3 + BH + 0.02)

# ②에 붙인 메모: 정규화상수 소거
MX0, MX1, MY0, MY1 = 5.4, 7.9, 3.6, 4.6
box(ax, MX0, MY0, MX1 - MX0, MY1 - MY0, fc=FAINT, ec="#9AA1AB", lw=1.0, r=0.08, ls=(0, (3, 2)))
mx = (MX0 + MX1) / 2
label(ax, mx, 4.36, "정규화상수 p(y)는", fs=11.5, w="bold", c=TEXT)
label(ax, mx, 4.1, "비율의 분자·분모에서 소거", fs=11, c=TEXT2)
label(ax, mx, 3.84, "→ 비정규화 사후밀도면 충분", fs=11, c=TEXT2)
ax.plot([BX1 + 0.04, MX0 - 0.04], [Y2 + BH / 2, Y2 + BH / 2], color="#9AA1AB", lw=1.2, ls=(0, (2, 2)), zorder=1)

# ③에서 갈라지는 두 결과
BY0, BH2 = 0.9, 0.8
branches = [  # x0, x1, 제목, 설명, 색
    (0.9, 2.85, "이동", "θ′를 새 값으로 기록", C_MOVE),
    (3.05, 5.0, "제자리", "현재 θ를 한 번 더 기록", C_STAY),
]
for x0, x1, t, s, c in branches:
    box(ax, x0, BY0, x1 - x0, BH2, fc=mix(c, 0.2), ec=c, lw=1.4, r=0.1)
    cx = (x0 + x1) / 2
    label(ax, cx, BY0 + BH2 / 2 + 0.15, t, fs=12.5, w="bold", c=TEXT)
    label(ax, cx, BY0 + BH2 / 2 - 0.17, s, fs=11, c=TEXT)
xm, xs = (0.9 + 2.85) / 2, (3.05 + 5.0) / 2
arrow(ax, 2.3, Y3 - 0.02, xm, BY0 + BH2 + 0.02)
arrow(ax, 3.6, Y3 - 0.02, xs, BY0 + BH2 + 0.02)
label(ax, 1.8, 2.06, "확률 α", fs=11.5, c=TEXT2, ha="right")
label(ax, 4.1, 2.06, "확률 1 − α", fs=11.5, c=TEXT2, ha="left")

# 다음 걸음: 두 결과가 모여 ①로 되돌아감
YB, XL = 0.5, 0.4
lc = "#9AA1AB"
ax.plot([xm, xm], [BY0, YB], color=lc, lw=1.6, zorder=1)
ax.plot([xs, xs], [BY0, YB], color=lc, lw=1.6, zorder=1)
ax.plot([xs, XL], [YB, YB], color=lc, lw=1.6, zorder=1)
ax.plot([XL, XL], [YB, Y1 + BH / 2], color=lc, lw=1.6, zorder=1)
arrow(ax, XL, Y1 + BH / 2, BX0 - 0.02, Y1 + BH / 2, color=lc)
label(ax, (XL + xs) / 2, YB - 0.24, "다음 걸음: 기록한 값이 새 현재 위치 θ", fs=11.5, c=TEXT2)

save(fig, "../../assets/img/w5/metropolis_step.png")
