# W11 「전방·후방 알고리즘: 숨은 상태의 사후분포」: 격자 위에서 왼쪽의 α와 오른쪽의 r이 구간 t에서 만나 γ를 이루는 모습
from medfig import *

plt.rcParams["mathtext.default"] = "regular"   # 수식 글자를 기울이지 않음 (이 스크립트에만 적용)

W, H = 8.0, 5.6
fig, ax = new(W, H)
C_F, C_B = CAT[0], CAT[1]          # 전방 / 후방 (나란한 두 방향)

xs = [1.35, 2.3, 3.3, 4.25, 5.2, 6.2, 7.15]          # 구간 위치
xlab = ["1", "2", "t−1", "t", "t+1", "T−1", "T"]
ys = [3.75, 3.1, 2.45]                               # 상태 1, k, K
ylab = ["상태 1", "상태 k", "상태 K"]
R = 0.17
T_COL, K_ROW = 3, 1                                  # 결합되는 칸: 구간 t, 상태 k

# 증거 범위: α는 x_1..x_t, r은 x_(t+1)..x_T
box(ax, 1.05, 2.1, 4.57 - 1.05, 2.0, fc=mix(C_F, 0.10), ec="none", r=0.12, z=0)
box(ax, 4.72, 2.1, 7.45 - 4.72, 2.0, fc=mix(C_B, 0.12), ec="none", r=0.12, z=0)

def edge(x1, y1, x2, y2, c, strong):
    d = np.array([x2 - x1, y2 - y1]); u = d / np.linalg.norm(d)
    p1 = np.array([x1, y1]) + R * u; p2 = np.array([x2, y2]) - R * u
    arrow(ax, p1[0], p1[1], p2[0], p2[1], color=c if strong else mix(c, 0.45),
          lw=1.9 if strong else 1.0, ms=9 if strong else 7, z=3 if strong else 2)

# 전방: 왼쪽에서 오른쪽으로 (1→2, t−1→t)
for a, b in [(0, 1), (2, 3)]:
    for j, yj in enumerate(ys):
        for k, yk in enumerate(ys):
            edge(xs[a], yj, xs[b], yk, C_F, b == T_COL and k == K_ROW)
# 후방: 오른쪽에서 왼쪽으로 (T→T−1, t+1→t)
for a, b in [(6, 5), (4, 3)]:
    for j, yj in enumerate(ys):
        for k, yk in enumerate(ys):
            edge(xs[a], yj, xs[b], yk, C_B, b == T_COL and k == K_ROW)

# 생략 표시
for y in ys:
    label(ax, 2.8, y, "⋯", fs=13, c=TEXT2)
    label(ax, 5.7, y, "⋯", fs=13, c=TEXT2)

# 상태 노드
for i, x in enumerate(xs):
    for k, y in enumerate(ys):
        if i == T_COL and k == K_ROW:
            ax.add_patch(mp.Circle((x, y), R + 0.03, fc=ACCENT, ec="none", zorder=5))
        else:
            ec = C_F if i <= T_COL else C_B
            ax.add_patch(mp.Circle((x, y), R, fc="white", ec=ec, lw=1.4, zorder=5))

# 축 라벨
for y, t in zip(ys, ylab):
    label(ax, 0.95, y, t, fs=11, c=TEXT2, ha="right")
label(ax, 0.95, 1.8, "구간", fs=11, c=TEXT2, ha="right")
for i, (x, t) in enumerate(zip(xs, xlab)):
    label(ax, x, 1.8, t, fs=12, w="bold" if i == T_COL else "regular", c=TEXT if i == T_COL else TEXT2)

# 방향 표시와 정의
arrow(ax, 1.2, 4.42, 4.45, 4.42, color=C_F, lw=2.0, ms=14)
arrow(ax, 7.35, 4.42, 4.85, 4.42, color=C_B, lw=2.0, ms=14)
label(ax, 2.8, 5.15, r"① 전방 변수  $\alpha_t(k)$", fs=12.5, w="bold", c=C_F)
label(ax, 2.8, 4.78, r"$= p(x_{1:t},\ z_t = k)$", fs=12, c=TEXT2)
label(ax, 6.1, 5.15, r"② 후방 변수  $r_t(k)$", fs=12.5, w="bold", c=C_B)
label(ax, 6.1, 4.78, r"$= p(x_{t+1:T} \mid z_t = k)$", fs=12, c=TEXT2)

# 결합
label(ax, 4.0, 1.15, r"$\gamma_t(k) = p(z_t = k \mid x_{1:T}) \;\propto\; \alpha_t(k)\, r_t(k)$", fs=14, c=TEXT)
label(ax, 4.0, 0.72, "왼쪽 증거와 오른쪽 증거를 곱해 정규화", fs=11, c=TEXT2)

save(fig, "../../assets/img/w11/forward_backward.png")
