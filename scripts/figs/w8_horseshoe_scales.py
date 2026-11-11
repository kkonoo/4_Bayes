# W8 「Horseshoe: 전역 척도로 누르고 국소 척도로 빠져나가기」: 전역 τ → 국소 λⱼ → βⱼ 계층과 잡음·신호 계수의 축소
from medfig import *

W, H = 8.0, 5.7
fig, ax = new(W, H)
C_NOISE, C_SIG = CAT[2], CAT[1]          # 잡음 / 신호 (나란한 두 집단)

xs = [1.95 + 0.92 * i for i in range(7)]  # 계수 7개의 x 위치
signal = [False, False, True, False, False, True, False]
heights = [0.10, 0.06, 1.15, 0.12, 0.05, 0.85, 0.08]   # 설명용 |βⱼ| 막대 높이 (숫자 표시 안 함)
sub = "₁₂₃₄₅₆₇"

YT, YL, YB = 5.2, 3.9, 1.6   # τ, λ, β 기준선 높이

# 왼쪽 행 이름
label(ax, 0.1, YT + 0.08, "전역 척도 τ", fs=12.5, w="bold", ha="left")
label(ax, 0.1, YT - 0.24, "τ ∼ C⁺(0,1)", fs=11, c=TEXT2, ha="left")
label(ax, 0.1, YL + 0.08, "국소 척도 λⱼ", fs=12.5, w="bold", ha="left")
label(ax, 0.1, YL - 0.24, "λⱼ ∼ C⁺(0,1)", fs=11, c=TEXT2, ha="left")
label(ax, 0.1, YB + 0.62, "계수 |βⱼ|", fs=12.5, w="bold", ha="left")
label(ax, 0.1, YB + 0.30, "βⱼ ∼ N(0, λⱼ²τ²σ²)", fs=11, c=TEXT2, ha="left")

# τ 노드
cx = xs[3]
rt = 0.32
ax.add_patch(mp.Circle((cx, YT), rt, fc=PRIMARY, ec="none", zorder=3))
label(ax, cx, YT, "τ", fs=14, w="bold", c="white")
label(ax, cx + rt + 0.15, YT, "모든 계수를 0 쪽으로 누름", fs=11.5, c=TEXT2, ha="left")

# λⱼ 노드: 크기로 국소 척도의 크기 표현
for i, (x, s) in enumerate(zip(xs, signal)):
    r = 0.32 if s else 0.2
    c = C_SIG if s else C_NOISE
    ax.plot([cx, x], [YT - rt, YL + r], color="#9AA1AB", lw=1.2, zorder=1)
    ax.add_patch(mp.Circle((x, YL), r, fc=c, ec="none", zorder=3))
    label(ax, x, YL, f"λ{sub[i]}", fs=13 if s else 11, w="bold", c=on(c))
    # λ → β 막대
    ax.plot([x, x], [YL - r, YB + heights[i] + 0.1], color="#9AA1AB", lw=1.2, zorder=1)

# β 막대
ax.plot([1.6, 7.85], [YB, YB], color="#9AA1AB", lw=1.4, zorder=2)
bw = 0.38
for i, (x, s) in enumerate(zip(xs, signal)):
    c = C_SIG if s else C_NOISE
    box(ax, x - bw / 2, YB, bw, heights[i], fc=c, ec="none", r=0.02, z=3)
    label(ax, x, YB - 0.24, f"β{sub[i]}", fs=12, c=TEXT)

# 아래: κ 정의와 두 집단 설명
label(ax, 0.1, 0.62, "κⱼ = 1/(1 + λⱼ²τ²)", fs=11.5, c=TEXT, ha="left")
rows = [
    (0.82, C_NOISE, "잡음 계수: λⱼ 작음 → κⱼ ≈ 1 (완전 축소, 0 근처로 눌림)"),
    (0.42, C_SIG, "신호 계수: λⱼ 큼 → κⱼ ≈ 0 (축소 없음, 거의 그대로)"),
]
for y, c, t in rows:
    box(ax, 1.95, y - 0.1, 0.2, 0.2, fc=c, ec="none", r=0.03, z=3)
    label(ax, 2.28, y, t, fs=11.5, c=TEXT, ha="left")

save(fig, "../../assets/img/w8/horseshoe_scales.png")
