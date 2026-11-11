# W12 「기대값의 산수: log2 ratio와 BAF」: 염색체를 따라 이어진 다섯 상태에서 순도 1일 때 log2 ratio와 BAF의 기대 모양
# 기대값은 장의 expected_cn(cn, m, rho = 1)과 같다: log2(CN/2), BAF는 m/CN 또는 1 - m/CN
# 점은 고정 시드로 만든 설명용 잡음이며 본문의 숫자가 아니다
from medfig import *

rng = np.random.default_rng(12)

# (이름, CN, m, 구간 수, 색) — 정상은 회색 바탕, 나머지 상태는 CAT로 구분 (나란한 항목)
segs = [
    ("정상", 2, 1, 50, None),
    ("결실", 1, 0, 55, CAT[0]),
    ("정상", 2, 1, 50, None),
    ("CN-LOH", 2, 0, 75, CAT[2]),
    ("정상", 2, 1, 50, None),
    ("증가", 3, 1, 60, CAT[1]),
    ("증폭", 4, 2, 60, CAT[3]),
]
N = sum(s[3] for s in segs)

fig, (ax, bx) = plt.subplots(2, 1, figsize=(8.0, 5.8), sharex=True)
fig.subplots_adjust(left=0.11, right=0.98, top=0.85, bottom=0.18, hspace=0.12)

# log2 ratio 0 기준선: CN-LOH가 정상과 같은 높이임을 보이기 위해
ax.axhline(0, color="#9AA1AB", lw=0.9, ls=(0, (3, 3)), zorder=1)

x0 = 0
loh_center = None
for name, cn, m, L, c in segs:
    x1 = x0 + L
    bg = FAINT if c is None else mix(c, 0.14)
    lc = TEXT2 if c is None else c
    dc = "#9AA1AB" if c is None else mix(c, 0.55)
    for a in (ax, bx):
        a.axvspan(x0, x1, color=bg, lw=0, zorder=0)

    mu = np.log2(cn / 2)          # 순도 1의 기대 log2 ratio
    b = m / cn                    # 순도 1의 기대 BAF (소수 쪽)
    xs = np.arange(x0, x1) + 0.5

    # 위: log2 ratio (설명용 잡음 점 + 기대값 수평선)
    y = mu + 0.22 * rng.standard_normal(L)
    ax.scatter(xs, y, s=7, color=dc, lw=0, zorder=2)
    ax.plot([x0 + 1, x1 - 1], [mu, mu], color=lc, lw=2.6, zorder=3, solid_capstyle="butt")

    # 아래: BAF (이형접합 SNP가 있는 구간만, b 또는 1 - b에 무작위로 모임)
    het = rng.random(L) < 0.5
    xb = xs[het]
    side = rng.random(het.sum()) < 0.5
    tgt = np.where(side, b, 1 - b)
    v = tgt + 0.035 * rng.standard_normal(len(xb))
    v = np.abs(v)
    v = 1 - np.abs(1 - v)        # 0..1 안으로 반사
    bx.scatter(xb, v, s=8, color=dc, lw=0, zorder=2)
    for t in sorted({round(b, 6), round(1 - b, 6)}):
        bx.plot([x0 + 1, x1 - 1], [t, t], color=lc, lw=2.6, zorder=3, solid_capstyle="butt")

    # 구간 라벨: 상태 이름과 (CN, m)
    xm = (x0 + x1) / 2
    ax.text(xm, 1.20, name, transform=ax.get_xaxis_transform(), ha="center", va="bottom",
            fontsize=12, fontweight="bold", color=TEXT)
    ax.text(xm, 1.05, f"({cn}, {m})", transform=ax.get_xaxis_transform(), ha="center", va="bottom",
            fontsize=11, color=TEXT2)
    if name == "CN-LOH":
        loh_center = xm
    x0 = x1

# 축 꾸밈
ax.set_ylim(-1.75, 1.6)
ax.set_yticks([-1, 0, np.log2(1.5), 1])
ax.set_yticklabels(["−1", "0", "0.585", "1"])
ax.set_ylabel("log2 ratio", fontsize=12)
ax.tick_params(axis="y", labelsize=11)
ax.tick_params(axis="x", bottom=False)

bx.set_ylim(-0.07, 1.07)
bx.set_yticks([0, 1 / 3, 0.5, 2 / 3, 1])
bx.set_yticklabels(["0", "1/3", "0.5", "2/3", "1"])
bx.set_ylabel("BAF", fontsize=12)
bx.tick_params(axis="y", labelsize=11)
bx.set_xlim(0, N)
bx.set_xticks([])
bx.set_xlabel("염색체 위치 →", fontsize=11.5, color=TEXT2, loc="right")

# 강조 한 곳: CN-LOH는 log2로는 정상과 같고 BAF로만 보임
bx.annotate("CN-LOH: log2로는 정상과 같고 BAF로만 보임",
            xy=(loh_center, 0.0), xycoords=("data", "axes fraction"),
            xytext=(loh_center, -0.36), textcoords=("data", "axes fraction"),
            ha="center", va="top", fontsize=12, fontweight="bold", color=ON_ACCENT,
            bbox=dict(boxstyle="round,pad=0.4", fc=ACCENT, ec="none"),
            arrowprops=dict(arrowstyle="-|>", color=ACCENT_INK, lw=1.4, shrinkA=0, shrinkB=2),
            annotation_clip=False, zorder=6)

save(fig, "../../assets/img/w12/cn_patterns.png")
