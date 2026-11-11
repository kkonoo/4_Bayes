# W8 「축소 곡선: 네 사전분포를 한 그림에」: 정규·Laplace·horseshoe 사전 밀도를 0 근처와 꼬리(로그 축)에서 비교
# 척도는 본문 축소 곡선과 같다: 정규 τ = 1(ridge), Laplace b = 1(lasso), horseshoe τ = 1 (σ = 1)
from medfig import *

TAU_N, B_LAP, TAU_HS = 1.0, 1.0, 1.0
C_N, C_L, C_H = CAT[0], CAT[1], CAT[2]

def normal_pdf(b):
    return np.exp(-0.5 * (b / TAU_N) ** 2) / (np.sqrt(2 * np.pi) * TAU_N)

def laplace_pdf(b):
    return np.exp(-np.abs(b) / B_LAP) / (2 * B_LAP)

# horseshoe: p(β) = ∫ N(β; 0, λ²τ²) · 2/(π(1+λ²)) dλ, λ = e^u 로 바꿔 사다리꼴 적분 (numpy만)
u = np.linspace(-20, 20, 4001)
du = u[1] - u[0]
lam = np.exp(u)
w_lam = 2 / (np.pi * (1 + lam ** 2)) * lam          # 반코시 밀도 × dλ/du
s = lam * TAU_HS

def hs_pdf(beta):
    beta = np.atleast_1d(beta)
    out = np.empty(beta.size)
    for i0 in range(0, beta.size, 200):              # 메모리 절약용 묶음 계산
        b = beta[i0:i0 + 200, None]
        f = np.exp(-0.5 * (b / s) ** 2) / (np.sqrt(2 * np.pi) * s) * w_lam
        out[i0:i0 + 200] = (f.sum(axis=1) - 0.5 * (f[:, 0] + f[:, -1])) * du
    return out

x1 = np.linspace(-3, 3, 1200)       # 짝수 개: β = 0 정확히는 피함 (horseshoe는 0에서 발산)
x2 = np.linspace(0.02, 8, 800)

fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.4, 6.8), gridspec_kw=dict(hspace=0.38))

# ① 0 근처: 선형 축
a1.plot(x1, normal_pdf(x1), color=C_N, lw=2.2, label="정규 (ridge), τ = 1")
a1.plot(x1, laplace_pdf(x1), color=C_L, lw=2.2, ls=(0, (5, 3)), label="Laplace (lasso), b = 1")
a1.plot(x1, hs_pdf(x1), color=C_H, lw=2.6, label="horseshoe, τ = 1")
a1.set_xlim(-3, 3)
a1.set_ylim(0, 1.05)
a1.set_xlabel("β", fontsize=12)
a1.set_ylabel("사전 밀도", fontsize=11.5)
a1.tick_params(labelsize=11)
a1.text(0.015, 0.97, "① 0 근처", transform=a1.transAxes, fontsize=12.5, fontweight="bold",
        color=TEXT, va="top", ha="left")
a1.text(-0.18, 0.93, "0에서 끝없이 솟음", fontsize=11, color=C_H, ha="right", va="center")
a1.legend(loc="upper right", fontsize=11, frameon=False, handlelength=2.6)

# ② 꼬리: 세로축 로그
a2.plot(x2, normal_pdf(x2), color=C_N, lw=2.2)
a2.plot(x2, laplace_pdf(x2), color=C_L, lw=2.2, ls=(0, (5, 3)))
a2.plot(x2, hs_pdf(x2), color=C_H, lw=2.6)
a2.set_yscale("log")
a2.set_xlim(0, 8)
a2.set_ylim(1e-7, 3)
a2.set_xlabel("|β|", fontsize=12)
a2.set_ylabel("사전 밀도 (로그 축)", fontsize=11.5)
a2.tick_params(labelsize=11)
a2.text(0.985, 0.97, "② 꼬리 (세로축 로그)", transform=a2.transAxes, fontsize=12.5,
        fontweight="bold", color=TEXT, va="top", ha="right")
a2.text(6.5, 0.03, "horseshoe", fontsize=11, color=C_H, ha="center", va="center")
a2.text(6.5, 1.3e-4, "Laplace", fontsize=11, color=C_L, ha="center", va="center")
a2.text(3.5, 1e-5, "정규", fontsize=11, color=C_N, ha="right", va="center")

save(fig, "../../assets/img/w8/prior_shapes.png")
