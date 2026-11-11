# W9 「단일 인과 가정: PIP와 신용집합」: PIP 내림차순 막대와 누적합 선, 0.95를 처음 넘는 곳까지가 95% 신용집합
# 1위 PIP 0.62와 신용집합 크기 9개는 본문 강한 LD 좌위(rho = 0.998)의 결과와 같다. 나머지 PIP 값은 설명용(60개 합 = 1).
from medfig import *

# 상위 15개 PIP (설명용, LD로 묶인 이웃이 몫을 나눠 가진 모양). 나머지 45개 SNP의 합은 0.012
pip = np.array([0.62, 0.105, 0.06, 0.04, 0.035, 0.03, 0.025, 0.02, 0.02,
                0.008, 0.007, 0.006, 0.005, 0.004, 0.003])
rest = 0.012
assert abs(pip.sum() + rest - 1) < 1e-9
cum = np.cumsum(pip)
k = int(np.argmax(cum >= 0.95)) + 1          # 신용집합 크기 (= 9)
x = np.arange(1, len(pip) + 1)

C_IN, C_OUT, C_CUM = CAT[0], "#9AA1AB", CAT[1]

fig, ax = plt.subplots(figsize=(7.6, 4.5))
# 신용집합 구간: 옅은 단색 바탕
ax.axvspan(0.5, k + 0.5, color=mix(C_IN, 0.09), lw=0, zorder=0)
# PIP 막대
ax.bar(x, pip, width=0.68, color=[C_IN if i <= k else C_OUT for i in x], zorder=2)
# 0.95 점선
ax.axhline(0.95, color="#9AA1AB", lw=1.3, ls=(0, (4, 3)), zorder=1)
ax.text(13.6, 0.935, "0.95", fontsize=11, color=TEXT2, ha="center", va="top")
# 누적합 선
ax.plot(x, cum, color=C_CUM, lw=2, marker="o", ms=5, zorder=3)
# 처음 0.95 이상이 되는 지점 한 곳만 강조색
ax.scatter([k], [cum[k - 1]], s=120, color=ACCENT, edgecolor=ACCENT_INK, lw=1.2, zorder=5)
ax.annotate("누적합이 처음 0.95 이상", xy=(k, cum[k - 1]), xytext=(9.9, 0.72),
            fontsize=11.5, color=ACCENT_INK, ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color=ACCENT_INK, lw=1.2, shrinkA=2, shrinkB=8))

# 직접 라벨
ax.text((k + 1) / 2, 1.065, f"95% 신용집합 (SNP {k}개)", fontsize=12.5, fontweight="bold",
        color=C_IN, ha="center", va="center")
ax.text(2.3, 0.87, "누적합", fontsize=11.5, fontweight="bold", color=C_CUM, ha="right", va="center")
ax.text(2, 0.155, "PIP", fontsize=11.5, fontweight="bold", color=C_IN, ha="center", va="center")
ax.text(12.5, 0.1, "집합 밖", fontsize=11, color=TEXT2, ha="center", va="center")

ax.set_xlim(0.4, 15.6)
ax.set_ylim(0, 1.13)
ax.set_xticks(x)
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.tick_params(labelsize=11)
ax.set_xlabel("PIP 순위", fontsize=12)
ax.set_ylabel("PIP / 누적합", fontsize=12)

save(fig, "../../assets/img/w9/credible_set.png")
