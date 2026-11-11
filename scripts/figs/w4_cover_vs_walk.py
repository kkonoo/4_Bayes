# W4 「네 방법 비교, 그리고 왜 MCMC인가」: 공간을 미리 덮는 방식(격자·기각·중요도)과 걸어 다니는 방식(MCMC)의 대비
from medfig import *
from matplotlib.patches import Ellipse

rng = np.random.default_rng(42)          # 설명용 모의실험
A, B, ANG = 0.85, 0.14, 38.0              # 사후가 차지하는 가늘고 기울어진 타원
ca, sa = np.cos(np.radians(ANG)), np.sin(np.radians(ANG))
C_COVER, C_WALK = CAT[0], CAT[1]          # 나란한 두 방식
LIM = 1.08

def to_uv(x, y):
    return x * ca + y * sa, -x * sa + y * ca

def inside(x, y):
    u, v = to_uv(x, y)
    return (u / A) ** 2 + (v / B) ** 2 <= 1.0

def draw_region(ax, c):
    ax.add_patch(Ellipse((0, 0), 2 * A, 2 * B, angle=ANG, fc=mix(c, 0.13), ec=c, lw=1.4, zorder=1))

def style(ax, mark, c):
    ax.set_xlim(-LIM, LIM); ax.set_ylim(-LIM, LIM)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("θ₁", fontsize=12)
    ax.set_ylabel("θ₂", fontsize=12, rotation=0, labelpad=12, va="center")
    ax.set_title(mark, loc="left", fontsize=12.5, fontweight="bold", color=c, pad=10)

fig, axs = plt.subplots(1, 2, figsize=(7.6, 4.0), gridspec_kw=dict(wspace=0.22))

# ① 공간을 덮기: 고른 격자, 타원 안의 점만 쓸모 있음
ax = axs[0]
draw_region(ax, C_COVER)
g = np.linspace(-1, 1, 15)
GX, GY = np.meshgrid(g, g)
GX, GY = GX.ravel(), GY.ravel()
m = inside(GX, GY)
ax.scatter(GX[~m], GY[~m], s=16, color="#C9CDD3", lw=0, zorder=2)
ax.scatter(GX[m], GY[m], s=30, color=C_COVER, lw=0, zorder=3)
style(ax, "① 공간을 덮기", C_COVER)

# ② 걸어 다니기: 타원 안에서 한 걸음씩 움직이는 체인 (랜덤워크 메트로폴리스, 설명용)
ax = axs[1]
draw_region(ax, C_WALK)

def logp(x, y):
    if not inside(x, y):
        return -np.inf
    u, v = to_uv(x, y)
    return -0.5 * ((u / (A / 2)) ** 2 + (v / (B / 2)) ** 2)

u0 = -0.62
x, y = u0 * ca, u0 * sa
path = [(x, y)]
for _ in range(160):                       # 설명용: 타원의 긴 축 방향으로 더 크게 내딛는 랜덤워크
    du, dv = rng.normal(0, 0.10), rng.normal(0, 0.035)
    xp, yp = x + du * ca - dv * sa, y + du * sa + dv * ca
    if np.log(rng.uniform()) < logp(xp, yp) - logp(x, y):
        x, y = xp, yp
    path.append((x, y))
path = np.array(path)
ax.plot(path[:, 0], path[:, 1], color=C_WALK, lw=1.2, alpha=0.9, zorder=3)
ax.scatter(path[:, 0], path[:, 1], s=14, color=C_WALK, lw=0, zorder=4)
ax.scatter([path[0, 0]], [path[0, 1]], s=60, facecolor="white", edgecolor=C_WALK, lw=1.6, zorder=5)
ax.text(path[0, 0] + 0.04, path[0, 1] - 0.24, "시작", fontsize=11, color=TEXT2, ha="left", va="center", zorder=6)
style(ax, "② 걸어 다니기 (MCMC)", C_WALK)

save(fig, "../../assets/img/w4/cover_vs_walk.png")
