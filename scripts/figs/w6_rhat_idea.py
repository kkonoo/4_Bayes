# W6 「수렴 진단: 결과를 믿어도 되는지」: 잘 섞인 네 체인과 서로 다른 층에 갇힌 네 체인으로 본 R-hat의 아이디어
from medfig import *

W, H = 8.0, 5.6
fig, ax = new(W, H)
rng = np.random.default_rng(20240606)   # 설명용 모의실험 (AR(1) 잡음 경로)
N = 300
phi = 0.5

def ar1(n, sd, mean=0.0):
    v = np.empty(n)
    v[0] = rng.normal(0, sd)
    e = rng.normal(0, sd * np.sqrt(1 - phi ** 2), n)
    for t in range(1, n):
        v[t] = phi * v[t - 1] + e[t]
    return mean + v

X0, X1 = 0.55, 5.0          # 그래프 영역 가로 범위
XS = np.linspace(X0 + 0.1, X1 - 0.05, N)
SC = 0.25                   # θ 1단위 = 0.25인치

def frame(y0, y1, tag):
    ax.plot([X0, X0], [y0, y1], color="#9AA1AB", lw=1.3, zorder=1)
    arrow(ax, X0, y0, X1 + 0.1, y0, color="#9AA1AB", lw=1.3, ms=10)
    label(ax, X0 - 0.2, (y0 + y1) / 2, "θ", fs=12, c=TEXT2)
    label(ax, X1 + 0.1, y0 - 0.24, "반복", fs=11, c=TEXT2, ha="right")
    label(ax, X0, y1 + 0.32, tag, fs=12.5, w="bold", ha="left")

def traces(paths, ymid):
    for k, v in enumerate(paths):
        ax.plot(XS, ymid + np.clip(v, -3.2, 3.2) * SC, color=CAT[k], lw=1.0, zorder=2 + k * 0.1)

# ① 잘 섞인 경우: 네 체인이 같은 구간을 겹쳐 덮음
B1, T1 = 3.15, 4.85
frame(B1, T1, "① 잘 섞인 경우")
traces([ar1(N, 1.0) for _ in range(4)], (B1 + T1) / 2)

# ② 안 섞인 경우: 체인마다 다른 층에 갇힘
B2, T2 = 0.45, 2.15
frame(B2, T2, "② 안 섞인 경우")
levels = [2.25, 0.75, -0.75, -2.25]
traces([ar1(N, 0.33, m) for m in levels], (B2 + T2) / 2)

# 오른쪽 판정 문구
RX = 5.45
ym1 = (B1 + T1) / 2
label(ax, RX, ym1 + 0.5, "체인 사이 분산 ≈ 체인 안 분산", fs=11.5, c=TEXT2, ha="left")
label(ax, RX, ym1, "R-hat ≈ 1", fs=13, w="bold", c=PRIMARY, ha="left")
label(ax, RX, ym1 - 0.5, "1.01 이하: 실패 증거 없음", fs=11.5, c=TEXT, ha="left")

ym2 = (B2 + T2) / 2
label(ax, RX, ym2 + 0.5, "체인 사이 분산 ≫ 체인 안 분산", fs=11.5, c=TEXT2, ha="left")
label(ax, RX, ym2, "R-hat > 1.01", fs=13, w="bold", c=TEXT, ha="left")
pill(ax, RX, ym2 - 0.52, "결과를 믿을 수 없음", fc=ACCENT, tc=ON_ACCENT, fs=12, h=0.38, padx=0.18, ha="left")

save(fig, "../../assets/img/w6/rhat_idea.png")
