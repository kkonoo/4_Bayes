# W7 「세 가지 선택: 완전 통합, 무통합, 부분 통합」: 세 모형의 구조와 τ 축 위의 위치
from medfig import *

W, H = 8.2, 5.0
fig, ax = new(W, H)
cols = [  # 중심 x, 이름, 한 줄 설명, 색
    (1.35, "① 완전 통합", "모든 θⱼ = μ", CAT[0]),
    (4.1, "② 부분 통합", "θⱼ ~ N(μ, τ²)", CAT[2]),
    (6.85, "③ 무통합", "θⱼ끼리 무관", CAT[1]),
]
YH, YT, YY = 3.75, 2.75, 1.75     # 상위 모수, θ, y 의 높이
dx = 0.78                        # 배치 칸 간격 (1, 2, …, 8 중 세 칸만 그림)

def circ(x, y, text, fc, r=0.27, fs=12):
    ax.add_patch(mp.Circle((x, y), r, fc=fc, ec="none", zorder=3))
    label(ax, x, y, text, fs=fs, w="bold", c=on(fc), z=4)

def obs(x, y, text, c):
    box(ax, x - 0.27, y - 0.22, 0.54, 0.44, fc="white", ec=c, lw=1.3, r=0.06)
    label(ax, x, y, text, fs=12, c=TEXT)

def link(x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color="#9AA1AB", lw=1.3, zorder=1)

for k, (cx, name, note, c) in enumerate(cols):
    label(ax, cx, 4.75, name, fs=13, w="bold", c=c)
    label(ax, cx, 4.38, note, fs=11.5, c=TEXT2)
    xs = [cx - dx, cx, cx + dx]
    names = ["1", "2", "8"]
    for x, j in zip(xs, names):                       # 관측값 y_j
        obs(x, YY, f"y{chr(0x2080 + int(j))}", c)
    label(ax, cx + dx / 2, YY, "⋯", fs=12, c=TEXT2)
    if k == 0:                                        # 완전 통합: μ 하나가 모든 y로
        circ(cx, YT + 0.5, "μ", c)
        for x in xs:
            link(cx, YT + 0.5 - 0.27, x, YY + 0.22)
    else:
        for x, j in zip(xs, names):                   # 배치별 θ_j
            circ(x, YT, f"θ{chr(0x2080 + int(j))}", mix(c, 0.75), r=0.27, fs=11.5)
            link(x, YT - 0.27, x, YY + 0.22)
        label(ax, cx + dx / 2, YT, "⋯", fs=12, c=TEXT2)
        if k == 1:                                    # 부분 통합: μ, τ 층이 θ를 묶음
            circ(cx, YH, "μ, τ", c, r=0.33, fs=11.5)
            for x in xs:
                link(cx, YH - 0.33, x, YT + 0.27)

# 아래: τ 축 위에서 세 모형의 위치
y = 0.75
ax.plot([0.6, 7.6], [y, y], color="#9AA1AB", lw=1.4, zorder=1)
for cx, _, _, c in cols:
    ax.add_patch(mp.Circle((cx, y), 0.09, fc=c, ec="none", zorder=3))
label(ax, 1.35, y - 0.32, "τ → 0", fs=11.5, c=TEXT2)
label(ax, 6.85, y - 0.32, "τ → ∞", fs=11.5, c=TEXT2)
label(ax, 4.1, y - 0.32, "데이터가 τ를 추정해 위치를 정함", fs=11.5, c=TEXT2)

save(fig, "../../assets/img/w7/pooling.png")
