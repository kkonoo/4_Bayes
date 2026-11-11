# W10 「다섯 가지 가설」: coloc의 H0~H4를 같은 영역 위 두 트랙(형질1 GWAS, 형질2 eQTL)의 연관 신호 모양으로 보기
from medfig import *

W, H = 8.0, 7.7
fig, ax = new(W, H)
rng = np.random.default_rng(10)
C1, C2 = CAT[0], CAT[1]            # 형질1 GWAS / 형질2 eQTL (대등한 두 트랙)

xs = np.linspace(2.6, 7.6, 41)       # 영역 안 SNP 위치 (간격 0.125)
C = xs[20]                           # 가운데 위치 (H1, H2, H4의 봉우리)
J, K = xs[11], xs[27]                # H3의 서로 다른 두 위치
A, S = 0.42, 0.28                    # 봉우리 높이, 폭 (LD로 주변 SNP가 함께 솟음)
ROWH, TOP = 1.3, 7.15

def signal(center):
    u = rng.uniform(0, 1, xs.size)
    noise = 0.06 * rng.uniform(0, 1, xs.size)
    if center is None:
        return noise
    h = A * np.exp(-0.5 * ((xs - center) / S) ** 2) * (0.8 + 0.2 * u) + noise
    h[np.argmin(np.abs(xs - center))] = A
    return h

def track(base, center, c):
    ax.plot([xs[0] - 0.1, xs[-1] + 0.1], [base, base], color="#9AA1AB", lw=1.0, zorder=1)
    ax.scatter(xs, base + signal(center), s=14, color=c, zorder=3, linewidths=0)

rows = [  # 이름, 짧은 설명, GWAS 봉우리 위치, eQTL 봉우리 위치
    ("H0", "두 형질 모두 연관 없음", None, None),
    ("H1", "형질1만 연관", C, None),
    ("H2", "형질2만 연관", None, C),
    ("H3", "둘 다 연관, 다른 변이", J, K),
    ("H4", "둘 다 연관, 같은 변이", C, C),
]

# 트랙 범례
ax.scatter([2.6], [7.45], s=40, color=C1, linewidths=0)
label(ax, 2.75, 7.45, "형질1 GWAS (위 트랙)", fs=11.5, ha="left")
ax.scatter([5.0], [7.45], s=40, color=C2, linewidths=0)
label(ax, 5.15, 7.45, "형질2 eQTL (아래 트랙)", fs=11.5, ha="left")

ax.plot([0.2, 7.75], [TOP, TOP], color=LINE, lw=1.0, zorder=0)
for i, (name, desc, cg, ce) in enumerate(rows):
    y0 = TOP - (i + 1) * ROWH
    ax.plot([0.2, 7.75], [y0, y0], color=LINE, lw=1.0, zorder=0)
    label(ax, 0.3, y0 + 0.85, name, fs=13, w="bold", ha="left")
    label(ax, 0.3, y0 + 0.48, desc, fs=11, c=TEXT2, ha="left")
    bg, be = y0 + 0.72, y0 + 0.15
    track(bg, cg, C1)
    track(be, ce, C2)
    if name == "H3":                 # 두 봉우리의 위치가 다름
        for x in (J, K):
            ax.plot([x, x], [y0 + 0.08, y0 + 1.2], color="#9AA1AB", lw=1.2, ls=(0, (3, 3)), zorder=2)
        label(ax, J + 0.12, bg + A, "j", fs=11.5, w="bold", c=TEXT, ha="left")
        label(ax, K + 0.12, be + A, "k", fs=11.5, w="bold", c=TEXT, ha="left")
    elif name == "H4":               # 같은 위치: 강조색은 이 연결선 한 곳
        ax.plot([C, C], [y0 + 0.08, y0 + 1.2], color=ACCENT_INK, lw=2.0, ls=(0, (3, 2.5)), zorder=2)
        label(ax, C + 0.14, bg + A, "j = k", fs=11.5, w="bold", c=ACCENT_INK, ha="left")
    else:
        if cg is not None:
            label(ax, cg + 0.12, bg + A, "j", fs=11.5, w="bold", c=TEXT, ha="left")
        if ce is not None:
            label(ax, ce + 0.12, be + A, "k", fs=11.5, w="bold", c=TEXT, ha="left")

save(fig, "../../assets/img/w10/five_hypotheses.png")
