# W3 「사후예측분포」: θ⁽ˢ⁾ 추출 → ỹ⁽ˢ⁾ 시뮬레이션 → p(ỹ|y) 절차와 점추정 대입과의 폭 비교
# 숫자는 본문 실습과 같다: 사후 Beta(15, 9) (사전 Beta(2,2), 20개 중 13개), 다음 배치 m = 20, 점추정 표준편차 약 25% 작음
from math import lgamma, comb, exp, log
from medfig import *

a_post, b_post, m_new = 15, 9, 20
R = ramp(3)
W, H = 8.0, 6.1
fig, ax = new(W, H)

def lbeta(p, q):
    return lgamma(p) + lgamma(q) - lgamma(p + q)

def bdens(t):
    return np.exp(-lbeta(a_post, b_post) + (a_post - 1) * np.log(t) + (b_post - 1) * np.log(1 - t))

k = np.arange(m_new + 1)
pp = np.array([exp(log(comb(m_new, int(i))) + lbeta(i + a_post, m_new - i + b_post)
                   - lbeta(a_post, b_post)) for i in k])          # 베타-이항 (수식)
p_hat = a_post / (a_post + b_post)                                  # 사후 평균
plug = np.array([comb(m_new, int(i)) * p_hat ** i * (1 - p_hat) ** (m_new - i) for i in k])

# ── 위: 세 단계 ─────────────────────────────────────────────
PY0, PH, PW = 3.3, 2.65, 2.3
xs = [0.15, 2.85, 5.55]
heads = ["사후에서 θ⁽ˢ⁾ 뽑기", "ỹ⁽ˢ⁾ 시뮬레이션", "ỹ⁽ˢ⁾ 모으기"]
for i, (x0, t) in enumerate(zip(xs, heads)):
    box(ax, x0, PY0, PW, PH, fc="white", ec=LINE, lw=1.2, r=0.1, z=1)
    num(ax, x0 + 0.3, 5.65, i + 1, fc=R[i], r=0.16, fs=12)
    label(ax, x0 + 0.56, 5.65, t, fs=12, w="bold", ha="left")
for xa in (2.5, 5.2):
    arrow(ax, xa, 4.6, xa + 0.28, 4.6)

# ① 사후 밀도와 뽑힌 θ⁽ˢ⁾ (설명용 모의 추출)
x0 = xs[0]
gx0, gx1, gy0, gh = x0 + 0.2, x0 + 2.0, 3.95, 1.25
th = np.linspace(0.3, 0.95, 300)
dens = bdens(th)
dmax = dens.max()
mx = lambda t: gx0 + (t - 0.3) / 0.65 * (gx1 - gx0)
my = lambda d: gy0 + d / dmax * gh
ax.fill_between(mx(th), gy0, my(dens), color=mix(R[0], 0.15), lw=0, zorder=2)
ax.plot(mx(th), my(dens), color=TEXT, lw=1.8, zorder=3)
ax.plot([gx0 - 0.05, gx1 + 0.05], [gy0, gy0], color="#9AA1AB", lw=1.2, zorder=3)
label(ax, gx1 + 0.12, gy0, "θ", fs=12, c=TEXT2, ha="left")
rng = np.random.default_rng(3)
for t in rng.beta(a_post, b_post, 6):
    ax.plot([mx(t), mx(t)], [gy0, my(bdens(t))], color=R[0], lw=1.4, zorder=4)
    ax.add_patch(mp.Circle((mx(t), gy0), 0.05, fc=R[0], ec="none", zorder=5))
label(ax, x0 + PW / 2, 3.58, "p(θ|y) = Beta(15, 9)", fs=11, c=TEXT2)

# ② 각 θ⁽ˢ⁾로 새 데이터 생성
cx = xs[1] + PW / 2
rows = [(5.1, "⁽¹⁾"), (4.72, "⁽²⁾"), (4.37, None), (4.0, "⁽ˢ⁾")]
for y, s in rows:
    if s is None:
        label(ax, cx - 0.55, y, "⋮", fs=12, c=TEXT2)
        label(ax, cx + 0.55, y, "⋮", fs=12, c=TEXT2)
    else:
        label(ax, cx - 0.55, y, "θ" + s, fs=12, w="bold", c=R[0])
        arrow(ax, cx - 0.27, y, cx + 0.27, y, ms=10, lw=1.3)
        label(ax, cx + 0.55, y, "ỹ" + s, fs=12, w="bold", c=R[1])
label(ax, cx, 3.58, "ỹ⁽ˢ⁾ ∼ Binomial(20, θ⁽ˢ⁾)", fs=11, c=TEXT2)

# ③ 모은 ỹ⁽ˢ⁾ = 사후예측분포
x0 = xs[2]
kmin = 3
gx0, gx1 = x0 + 0.25, x0 + 2.0
kx = lambda i: gx0 + (i - kmin) / (m_new - kmin) * (gx1 - gx0)
for i in range(kmin, m_new + 1):
    hgt = pp[i] / pp.max() * 1.25
    ax.add_patch(mp.Rectangle((kx(i) - 0.035, gy0), 0.07, hgt, fc=R[2], ec="none", zorder=3))
ax.plot([gx0 - 0.08, gx1 + 0.08], [gy0, gy0], color="#9AA1AB", lw=1.2, zorder=4)
label(ax, gx1 + 0.14, gy0, "ỹ", fs=12, c=TEXT2, ha="left")
label(ax, x0 + PW / 2, 3.58, "p(ỹ|y): 베타-이항분포", fs=11, c=TEXT2)

# ── 아래: 점추정 대입과의 비교 ─────────────────────────────
box(ax, 0.15, 1.1, 2.95, 1.75, fc=FAINT, ec="none", r=0.1, z=1)
label(ax, 1.62, 2.55, "점추정 대입", fs=12, w="bold", c=TEXT2)
label(ax, 1.62, 2.15, "θ̂ = 사후 평균 하나", fs=11, c=TEXT)
label(ax, 1.62, 1.8, "ỹ ∼ Binomial(20, θ̂)", fs=11, c=TEXT)
label(ax, 1.62, 1.4, "θ를 정확히 안다고 가정", fs=11, c=TEXT2)
arrow(ax, 3.15, 1.95, 3.58, 1.95)

BY = 1.25
bx0, bx1 = 3.85, 7.7
kx2 = lambda i: bx0 + (i - kmin) / (m_new - kmin) * (bx1 - bx0)
sc = 1.4 / max(pp.max(), plug.max())
for i in range(kmin, m_new + 1):
    ax.add_patch(mp.Rectangle((kx2(i) - 0.06, BY), 0.12, pp[i] * sc, fc=R[2], ec="none", zorder=3))
kk = np.arange(kmin, m_new + 1)
ax.plot([kx2(i) for i in kk], BY + plug[kmin:] * sc, color=TEXT2, lw=1.6, ls=(0, (4, 3)),
        marker="o", mfc="white", mec=TEXT2, ms=5, zorder=5)
ax.plot([bx0 - 0.12, bx1 + 0.12], [BY, BY], color="#9AA1AB", lw=1.2, zorder=4)
for t in (5, 10, 15, 20):
    label(ax, kx2(t), 1.07, str(t), fs=11, c=TEXT2)
label(ax, (bx0 + bx1) / 2, 0.8, "ỹ: 다음 20개 중 검증될 개수", fs=11, c=TEXT2)

# 범례
ax.add_patch(mp.Rectangle((3.85, 2.62), 0.22, 0.14, fc=R[2], ec="none", zorder=5))
label(ax, 4.17, 2.69, "사후예측 p(ỹ|y)", fs=11, ha="left")
ax.plot([3.83, 4.09], [2.38, 2.38], color=TEXT2, lw=1.6, ls=(0, (4, 3)), zorder=5)
ax.plot([3.96], [2.38], marker="o", mfc="white", mec=TEXT2, ms=5, zorder=6)
label(ax, 4.17, 2.38, "점추정 대입", fs=11, ha="left", c=TEXT2)

# 경고 한 곳만 강조색
pill(ax, 4.0, 0.32, "θ의 불확실성이 빠져 예측 표준편차가 약 25% 작아짐", fc=ACCENT, tc=ON_ACCENT,
     fs=12, h=0.42, padx=0.22)

save(fig, "../../assets/img/w3/posterior_predictive.png")
