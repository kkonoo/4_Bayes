# W3 「신용구간: ETI와 HPD 영역」: 한쪽으로 치우친 Beta(1.2, 12) 사후에서 두 95% 구간이 갈리는 모습
# 구간 값은 본문 실습(ETI와 HPDI 직접 구현)의 결과와 같다: ETI [0.0042, 0.2873], HPDI [0.0003, 0.2438]
from math import lgamma
from medfig import *

a, b = 1.2, 12
x = np.linspace(0, 0.5, 2001)
dens = np.exp(lgamma(a + b) - lgamma(a) - lgamma(b)) * x ** (a - 1) * (1 - x) ** (b - 1)
eti, hpd = (0.0042, 0.2873), (0.0003, 0.2438)
C_ETI, C_HPD = CAT[1], CAT[0]

fig, axs = plt.subplots(2, 1, figsize=(7.2, 4.6), sharex=True,
                        gridspec_kw=dict(height_ratios=[3, 1.25], hspace=0.08))
ax = axs[0]
ax.plot(x, dens, color=TEXT, lw=2)
m = (x >= hpd[0]) & (x <= hpd[1])
ax.fill_between(x[m], 0, dens[m], color=mix(C_HPD, 0.16), lw=0)
ax.set_ylabel("사후 밀도", fontsize=11.5)
ax.set_ylim(0, dens.max() * 1.12)
ax.tick_params(labelsize=11)
ax.text(0.32, dens.max() * 0.55, "Beta(1.2, 12) 사후\n최빈값 0.018", fontsize=11.5, color=TEXT2, va="center")

# 아래 칸: 두 구간을 막대로
bx = axs[1]
rows = [(1.0, "ETI", eti, C_ETI, "0.283"), (0.0, "HPDI", hpd, C_HPD, "0.244")]   # 폭은 본문 값
for yv, name, (lo, hi), c, width in rows:
    bx.plot([lo, hi], [yv, yv], color=c, lw=7, solid_capstyle="butt")
    bx.text(-0.012, yv, name, ha="right", va="center", fontsize=12, fontweight="bold", color=c)
    bx.text(hi + 0.012, yv, f"[{lo}, {hi}]  폭 {width}", va="center", fontsize=11, color=TEXT)
    ax.axvline(lo, color=c, lw=1.2, ls=(0, (4, 3)) if name == "ETI" else "-", ymax=0.97)
    ax.axvline(hi, color=c, lw=1.2, ls=(0, (4, 3)) if name == "ETI" else "-", ymax=0.97)
bx.set_ylim(-0.6, 1.6)
bx.set_yticks([])
bx.spines["left"].set_visible(False)
bx.set_xlim(0, 0.5)
bx.set_xlabel("θ", fontsize=12)
bx.tick_params(labelsize=11)

save(fig, "../../assets/img/w3/eti_hpdi.png")
