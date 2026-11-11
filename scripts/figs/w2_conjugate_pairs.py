# W2 「들어가며: 적분이 가로막을 때」: 이 장의 켤레 세 쌍(Beta–Binomial, Gamma–Poisson, Normal–Normal)의 사전 × 가능도 → 사후와 갱신 규칙
from medfig import *

W = 8.0
RH, GAP = 1.55, 0.2                 # 줄 높이, 줄 간격
H = 3 * RH + 2 * GAP
fig, ax = new(W, H)

# 각 줄: 이름, 쓰임 두 줄, 세 칸(머리, 식), 갱신 규칙 줄들
rows = [
    dict(name="Beta–Binomial", use=("비율", "대립유전자 빈도, ASE"),
         cells=[("사전 p(θ)", "Beta(a, b)"),
                ("가능도 p(y | θ)", "Binomial(n, θ)"),
                ("사후 p(θ | y)", "Beta(a+k, b+n−k)")],
         rules=["a ← a + k (성공 수),   b ← b + (n − k) (실패 수)"]),
    dict(name="Gamma–Poisson", use=("카운트", "RNA-seq read count"),
         cells=[("사전 p(λ)", "Gamma(a, b)"),
                ("가능도 p(y | λ)", "Poisson(λ)"),
                ("사후 p(λ | y)", "Gamma(a+Σyᵢ, b+n)")],
         rules=["a ← a + Σyᵢ (총 카운트),   b ← b + n (표본 수, b는 rate)"]),
    dict(name="Normal–Normal", use=("연속값의 평균", "분산 σ² 기지"),
         cells=[("사전 p(μ)", "N(μ₀, τ₀²)"),
                ("가능도 p(y | μ)", "N(μ, σ²)"),
                ("사후 p(μ | y)", "N(평균, 분산)")],
         rules=["정밀도  1/분산 = κ₀ + κₙ   (κ₀ = 1/τ₀², κₙ = n/σ²)",
                "평균  (κ₀μ₀ + κₙȳ) / (κ₀ + κₙ)"]),
]

LX, LW = 0.05, 1.9                 # 왼쪽 쓰임 칸
X0 = 2.15                          # 오른쪽 시작
widths = [1.55, 1.65, 1.85]        # 사전, 가능도, 사후 칸 폭
gaps = [0.3, 0.45]                 # × 자리, → 자리
BH = 0.8                           # 칸 높이

for i, r in enumerate(rows):
    c = CAT[i]
    yt = H - i * (RH + GAP)        # 줄 위끝
    # 왼쪽: 쌍 이름과 쓰임
    box(ax, LX, yt - RH, LW, RH, fc=c, ec="none", r=0.1)
    cx = LX + LW / 2
    label(ax, cx, yt - 0.42, r["name"], fs=12.5, w="bold", c=on(c))
    label(ax, cx, yt - 0.84, r["use"][0], fs=12, w="bold", c=on(c))
    label(ax, cx, yt - 1.14, r["use"][1], fs=11, c=on(c))

    # 오른쪽: [사전] × [가능도] → [사후]
    x = X0
    yb = yt - BH
    for j, ((head, form), w) in enumerate(zip(r["cells"], widths)):
        fc = mix(c, 0.16) if j == 2 else "white"
        box(ax, x, yb, w, BH, fc=fc, ec=c, lw=1.3, r=0.08)
        label(ax, x + w / 2, yt - 0.25, head, fs=11, c=TEXT2)
        label(ax, x + w / 2, yb + 0.25, form, fs=12.5, w="bold", c=TEXT)
        x += w
        if j == 0:
            label(ax, x + gaps[0] / 2, yb + BH / 2, "×", fs=15, w="bold", c=TEXT2)
            x += gaps[0]
        elif j == 1:
            arrow(ax, x + 0.08, yb + BH / 2, x + gaps[1] - 0.08, yb + BH / 2, color="#9AA1AB")
            x += gaps[1]

    # 갱신 규칙
    ys = [yt - 1.15] if len(r["rules"]) == 1 else [yt - 1.05, yt - 1.37]
    label(ax, X0, ys[0], "갱신", fs=11.5, w="bold", c=c, ha="left")
    for yy, rule in zip(ys, r["rules"]):
        label(ax, X0 + 0.6, yy, rule, fs=11.5, c=TEXT, ha="left")

save(fig, "../../assets/img/w2/conjugate_pairs.png")
