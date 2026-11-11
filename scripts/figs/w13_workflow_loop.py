# W13 「베이지안 워크플로우」: 10단계의 순서와 점검 실패 시 되돌아가는 세 고리
from medfig import *

W, H = 8.0, 4.6
fig, ax = new(W, H)

BW, BH, GAP = 1.28, 1.05, 0.36   # 상자 폭·높이, 상자 사이 간격
X0 = 0.08
Y1, Y2 = 3.2, 0.9               # 위 줄(1~5), 아래 줄(6~10) 중심 높이
FWD = TEXT2                      # 진행 화살표
BACK = "#9AA1AB"                 # 되돌아가는 고리 (점선 회색)
DASH = (0, (4, 3))

def cx(col):
    return X0 + col * (BW + GAP) + BW / 2

names = ["질문·\n추정 대상", "생성 모형", "사전예측검사", "가짜 데이터로\n모수 복원", "적합",
         "수렴 진단", "사후예측검사\n(PPC)", "민감도 분석", "모형 비교", "보고"]
cols = ramp(10)                  # 순서 있는 단계 → ramp 단색

def pos(i):                      # 0-based 단계 번호 → 중심 좌표 (아래 줄은 오른쪽에서 왼쪽)
    return (cx(i), Y1) if i < 5 else (cx(9 - i), Y2)

for i, (nm, c) in enumerate(zip(names, cols)):
    x, y = pos(i)
    box(ax, x - BW / 2, y - BH / 2, BW, BH, fc=c, ec="none", r=0.1)
    num(ax, x, y + 0.27, i + 1, fc="white", tc=c, r=0.15, fs=11)
    label(ax, x, y - 0.16, nm, fs=12, w="bold", c=on(c), linespacing=1.15)

# 진행 화살표 (실선)
for k in range(4):               # 위 줄: 왼쪽 → 오른쪽
    arrow(ax, cx(k) + BW / 2 + 0.04, Y1, cx(k + 1) - BW / 2 - 0.04, Y1, color=FWD, lw=1.6)
for k in range(4, 0, -1):        # 아래 줄: 오른쪽 → 왼쪽
    arrow(ax, cx(k) - BW / 2 - 0.04, Y2, cx(k - 1) + BW / 2 + 0.04, Y2, color=FWD, lw=1.6)
arrow(ax, cx(4) + 0.25, Y1 - BH / 2 - 0.04, cx(4) + 0.25, Y2 + BH / 2 + 0.04, color=FWD, lw=1.6)  # 5 → 6

# 되돌아가는 고리: 점선 몸통 + 실선 화살촉
def back_path(xs, ys):
    xs, ys = list(xs), list(ys)
    ex, ey = xs[-1], ys[-1]
    px, py = xs[-2], ys[-2]
    d = np.hypot(ex - px, ey - py)
    hx, hy = ex - (ex - px) * 0.14 / d, ey - (ey - py) * 0.14 / d
    ax.plot(xs[:-1] + [hx], ys[:-1] + [hy], color=BACK, lw=1.6, ls=DASH, zorder=3,
            solid_capstyle="butt")
    arrow(ax, hx, hy, ex, ey, color=BACK, lw=1.6, ms=12)

top1, bot1, top2 = Y1 + BH / 2 + 0.04, Y1 - BH / 2 - 0.04, Y2 + BH / 2 + 0.04

# ① 3 → 2: 사전예측이 말이 안 되면 사전분포로 (위쪽 호)
p0, p2 = np.array([cx(2), top1]), np.array([cx(1), top1])
pc = np.array([(cx(1) + cx(2)) / 2, top1 + 0.75])
t = np.linspace(0, 1, 60)
curve = (1 - t)[:, None] ** 2 * p0 + 2 * ((1 - t) * t)[:, None] * pc + (t ** 2)[:, None] * p2
back_path(curve[:, 0], curve[:, 1])
label(ax, (cx(1) + cx(2)) / 2, top1 + 0.62, "사전예측이 말이 안 되면 → 사전분포로", fs=11, c=TEXT2)

# ② 6 → 5: 수렴 진단 실패면 모수화·표집기로 (오른쪽 세로)
back_path([cx(4) - 0.25, cx(4) - 0.25], [top2, bot1])
label(ax, cx(4) - 0.4, 2.2, "수렴 진단 실패 →\n모수화·표집기로", fs=11, c=TEXT2, ha="right",
      linespacing=1.2)

# ③ 7 → 2: PPC 실패면 생성 모형으로 (두 줄 사이를 지나는 꺾은 길)
yr = 1.8
back_path([cx(3), cx(3), cx(1), cx(1)], [top2, yr, yr, bot1])
label(ax, (cx(1) + cx(3)) / 2 + 0.05, yr + 0.2, "PPC 실패 → 생성 모형으로", fs=11, c=TEXT2)

save(fig, "../../assets/img/w13/workflow_loop.png")
