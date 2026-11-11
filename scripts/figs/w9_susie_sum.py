# W9 「SuSiE: 단일효과의 합」: 효과마다 SNP 위의 확률분포 α와 신용집합을 내는 단일효과들, 그리고 IBSS 순환
from medfig import *

W, H = 8.0, 7.3
fig, ax = new(W, H)

p = 24                                   # 설명용 SNP 개수
X0, X1 = 1.35, 5.85                      # 막대 영역
xs = np.linspace(X0, X1, p)
BW = 0.11                                # 막대 폭
S = 0.7                                  # alpha = 1 일 때 막대 높이(인치)

# 설명용 alpha 벡터 (합 1)
a1 = np.full(p, 0.001); a1[[5, 6, 7, 8]] = [0.02, 0.56, 0.35, 0.05]
a1 = a1 / a1.sum()
a2 = np.full(p, 0.0005); a2[[16, 17, 18]] = [0.015, 0.96, 0.015]
a2 = a2 / a2.sum()
aL = np.full(p, 1.0 / p)                 # 꺼진 효과: 모든 SNP에 고르게

def cred(a, cov=0.95):
    o = np.argsort(-a)
    k = int(np.argmax(np.cumsum(a[o]) >= cov)) + 1
    return set(o[:k].tolist())

cs1, cs2 = cred(a1), cred(a2)

def bars(base, a, colors):
    ax.plot([X0 - 0.12, X1 + 0.12], [base, base], color="#9AA1AB", lw=1.0, zorder=1)
    for x, v, c in zip(xs, a, colors):
        if v * S > 0.004:
            ax.add_patch(mp.Rectangle((x - BW / 2, base), BW, v * S, fc=c, ec="none", zorder=2))

def row_label(base, tex, name, c):
    label(ax, 0.6, base + 0.42, tex, fs=15, c=c)
    label(ax, 0.6, base + 0.12, name, fs=11, c=TEXT2)

# ① 단일효과의 합
label(ax, 0.2, 7.05, "① 단일효과의 합", fs=12, w="bold", c=PRIMARY, ha="left")
label(ax, 3.6, 7.05, r"$\mathrm{b} = \mathrm{b}_1 + \mathrm{b}_2 + \cdots + \mathrm{b}_\mathrm{L}$", fs=14, c=TEXT)

rows = [  # 바닥 y, 기호, 이름, alpha, 신용집합, 색, 오른쪽 표시
    (6.05, r"$\mathrm{b}_1$", "효과 1", a1, cs1, CAT[0], "신용집합 1"),
    (5.15, r"$\mathrm{b}_2$", "효과 2", a2, cs2, CAT[1], "신용집합 2"),
    (4.05, r"$\mathrm{b}_\mathrm{L}$", "효과 L", aL, set(), CAT[2], None),
]
for base, tex, name, a, cs, c, tag in rows:
    row_label(base, tex, name, c)
    if cs:
        cols = [c if j in cs else mix(c, 0.35) for j in range(p)]
    else:
        cols = [mix(c, 0.6)] * p
    bars(base, a, cols)
    if tag:
        pill(ax, 6.25, base + 0.3, tag, fc=c, fs=11, ha="left")
    else:
        label(ax, 6.25, base + 0.3, "꺼짐 (σ₀² = 0)", fs=11.5, c=TEXT2, ha="left")

# 효과 2와 효과 L 사이의 생략
label(ax, 0.6, 4.72, "⋮", fs=13, c=TEXT2)
label(ax, (X0 + X1) / 2, 4.72, "⋮", fs=13, c=TEXT2)

# 합친 PIP (꺼진 효과는 제외)
ax.plot([X0 - 0.12, X1 + 0.12], [3.82, 3.82], color=LINE, lw=1.2, zorder=1)
pip = 1 - (1 - a1) * (1 - a2)
pcols = [CAT[0] if j in cs1 else CAT[1] if j in cs2 else "#9AA1AB" for j in range(p)]
base_c = 2.95
label(ax, 0.6, base_c + 0.3, "전체 PIP", fs=12, w="bold", c=TEXT)
bars(base_c, pip, pcols)
label(ax, 6.25, base_c + 0.3, "= 1 − ∏(1 − α)", fs=12, c=TEXT, ha="left")
label(ax, X1 + 0.12, 2.72, "SNP 위치 →", fs=11, c=TEXT2, ha="right")

# ② IBSS 순환
label(ax, 0.2, 2.35, "② IBSS", fs=12, w="bold", c=PRIMARY, ha="left")
bw, bh, by = 2.3, 1.0, 0.95
steps = [
    (0.2, "잔차 만들기", "y − (효과 ℓ 외 적합값)"),
    (2.85, "단일효과회귀(SER)", "효과 ℓ의 α, μ, σ₀² 갱신"),
    (5.5, "다음 효과로", "ℓ → ℓ + 1, L 다음은 다시 1"),
]
for x, t, s in steps:
    box(ax, x, by, bw, bh, fc=FAINT, ec=LINE, lw=1.2, r=0.1)
    label(ax, x + bw / 2, by + 0.67, t, fs=12, w="bold", c=PRIMARY)
    label(ax, x + bw / 2, by + 0.31, s, fs=11, c=TEXT)
arrow(ax, 0.2 + bw + 0.03, by + bh / 2, 2.85 - 0.03, by + bh / 2)
arrow(ax, 2.85 + bw + 0.03, by + bh / 2, 5.5 - 0.03, by + bh / 2)
# 되돌아가는 고리
yl = 0.6
ax.plot([5.5 + bw / 2, 5.5 + bw / 2, 0.2 + bw / 2], [by - 0.02, yl, yl], color="#9AA1AB", lw=1.6, zorder=3)
arrow(ax, 0.2 + bw / 2, yl, 0.2 + bw / 2, by - 0.03)
label(ax, 4.0, 0.3, "한 바퀴마다 σ² 갱신 · α 변화가 10⁻⁴ 미만이면 멈춤", fs=11, c=TEXT2)

save(fig, "../../assets/img/w9/susie_sum.png")
