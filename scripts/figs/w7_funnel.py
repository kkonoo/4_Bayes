# W7 「tau의 사전분포와 깔때기」: 중심화(θⱼ − μ 대 log τ)의 깔때기와 비중심화(ηⱼ 대 log τ)의 직사각형
from medfig import *

# 설명용 모의실험: log τ 는 정규분포에서, ηⱼ 는 표준정규에서 뽑고 θⱼ − μ = τ·ηⱼ 로 만든다
rng = np.random.default_rng(7)
n = 1500
log_tau = rng.normal(0.0, 0.8, n)
log_tau = log_tau[(log_tau > -2.6) & (log_tau < 2.6)]
eta = rng.normal(0.0, 1.0, log_tau.size)
dev = np.exp(log_tau) * eta          # θⱼ − μ = τ·ηⱼ

C1, C2 = CAT[0], CAT[2]              # 두 모수화는 나란한 항목
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.0, 4.2), sharey=True,
                             gridspec_kw=dict(wspace=0.12))
a1.scatter(dev, log_tau, s=7, color=C1, alpha=0.45, lw=0)
a2.scatter(eta, log_tau, s=7, color=C2, alpha=0.45, lw=0)
a1.set_xlim(-32, 32)
a2.set_xlim(-3.6, 3.6)
a1.set_ylim(-2.8, 2.8)
a1.set_xlabel('θⱼ − μ', fontsize=12)
a2.set_xlabel('ηⱼ', fontsize=12)
a1.set_ylabel('log τ', fontsize=12)

for ax, mark, note, c in [(a1, '① 중심화', 'θⱼ 직접 표집', C1),
                          (a2, '② 비중심화', 'ηⱼ ∼ N(0, 1)', C2)]:
    ax.tick_params(labelsize=11)
    ax.text(0.0, 1.03, mark, transform=ax.transAxes, ha='left', va='bottom',
            fontsize=12.5, fontweight='bold', color=c)
    ax.text(1.0, 1.03, note, transform=ax.transAxes, ha='right', va='bottom',
            fontsize=11, color=TEXT2)

# 강조는 깔때기 목 한 곳에만
a1.annotate('이동 폭 하나로는\n깔때기 목까지\n내려가기 어려움', xy=(0.6, -2.25), xytext=(5, -1.5),
            ha='left', va='center', fontsize=11, fontweight='bold', color=ACCENT_INK,
            arrowprops=dict(arrowstyle='-|>', color=ACCENT_INK, lw=1.4, shrinkA=4, shrinkB=2))

save(fig, '../../assets/img/w7/funnel.png')
