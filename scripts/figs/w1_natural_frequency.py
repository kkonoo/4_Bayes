# W1 「희귀 변이 판정과 기저율 오류」: 가상의 100만 명을 자연빈도로 나눈 나무와 양성 판정의 구성
from medfig import *

fig, ax = new(8.0, 6.3)
C_VAR, C_NORM = CAT[0], CAT[1]          # 보유 / 비보유 (대등한 두 집단)

def node(x, y, w, h, title, sub, fc, tc=None, ec="none"):
    box(ax, x - w / 2, y - h / 2, w, h, fc=fc, ec=ec, lw=1.2, r=0.1)
    tc = tc or on(fc)
    if sub:
        label(ax, x, y + 0.12, title, fs=13, w="bold", c=tc)
        label(ax, x, y - 0.16, sub, fs=11, c=tc if tc != TEXT else TEXT2)
    else:
        label(ax, x, y, title, fs=13, w="bold", c=tc)

def edge(x1, y1, x2, y2, text, side):
    ax.plot([x1, x2], [y1, y2], color="#9AA1AB", lw=1.4, zorder=1)
    xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
    label(ax, xm + (0.12 if side == "r" else -0.12), ym, text, fs=11, c=TEXT2,
          ha="left" if side == "r" else "right")

# ① 전체
node(4.0, 5.85, 2.9, 0.62, "검사 대상 100만 명", "가상의 예", FAINT, tc=TEXT)
# ② 보유 / 비보유
node(2.0, 4.45, 2.5, 0.56, "변이 보유 1,000명", "", C_VAR)
node(6.0, 4.45, 2.5, 0.56, "비보유 999,000명", "", C_NORM)
edge(3.4, 5.54, 2.4, 4.73, "유병률 0.1%", "l")
edge(4.6, 5.54, 5.6, 4.73, "99.9%", "r")
# ③ 검사 결과 네 칸: 양성은 집단 색 옅은 면, 음성은 흰 칸
leaves = [  # x, 제목, 부제, 집단 색, 양성?
    (1.05, "양성 990", "진양성", C_VAR, True),
    (2.95, "음성 10", "위음성", C_VAR, False),
    (5.05, "양성 9,990", "위양성", C_NORM, True),
    (6.95, "음성 989,010", "진음성", C_NORM, False),
]
for x, t, s, c, pos in leaves:
    if pos:
        node(x, 2.95, 1.75, 0.62, t, s, mix(c, 0.16), tc=TEXT, ec=c)
    else:
        node(x, 2.95, 1.75, 0.62, t, s, "white", tc=TEXT2, ec=LINE)
edge(1.75, 4.17, 1.2, 3.26, "민감도 99%", "l")
edge(2.25, 4.17, 2.8, 3.26, "1%", "r")
edge(5.75, 4.17, 5.2, 3.26, "1%", "l")
edge(6.25, 4.17, 6.8, 3.26, "특이도 99%", "r")

# ④ 양성 판정 10,980건의 구성: 폭을 실제 비율대로
x0, bw, y0, bh = 0.6, 6.8, 1.2, 0.5
tot = 990 + 9990
w1 = bw * 990 / tot
box(ax, x0, y0, w1, bh, fc=C_VAR, ec="none", r=0.04)
box(ax, x0 + w1 + 0.03, y0, bw - w1 - 0.03, bh, fc=C_NORM, ec="none", r=0.04)
label(ax, x0 + w1 + 0.03 + (bw - w1) / 2, y0 + bh / 2, "위양성 9,990", fs=12, w="bold", c="white")
label(ax, x0 + bw, y0 + bh + 0.2, "양성 판정 10,980건", fs=12, w="bold", ha="right")
label(ax, x0, y0 - 0.22, "진양성 990", fs=11, c=TEXT, ha="left")
arrow(ax, 1.05, 2.62, x0 + w1 / 2, y0 + bh + 0.04, color="#9AA1AB")
arrow(ax, 5.05, 2.62, 5.05, y0 + bh + 0.04, color="#9AA1AB")
# 결론 한 곳만 강조색
pill(ax, 4.0, 0.35, "양성 중 진짜는 990 / 10,980 ≈ 9%", fc=ACCENT, tc=ON_ACCENT, fs=13, h=0.42, padx=0.22)

save(fig, "../../assets/img/w1/natural_frequency.png")
