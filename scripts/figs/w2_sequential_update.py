# W2 「순차 업데이트: 오늘의 사후가 내일의 사전」: read 40개를 10개씩 네 번 넣는 길과 한 번에 넣는 길이 같은 사후에 도착
from medfig import *

W, H = 8.0, 3.5
fig, ax = new(W, H)
cols = ramp(5)                      # 사전 → 사후1 → 사후2 → 사후3 → 최종 사후 (순서 있는 단계)

YT, YB = 2.45, 1.15                 # 위 줄(나눠 넣기), 아래 줄(한 번에) 높이
BY0, BY1 = 0.75, 2.85               # 양 끝 공용 상자의 세로 범위

# 출발: 사전 Beta(a, b) (두 줄이 공유)
sx0, sw = 0.1, 1.25
box(ax, sx0, BY0, sw, BY1 - BY0, fc=cols[0], ec="none", r=0.1)
label(ax, sx0 + sw / 2, 1.95, "Beta(a, b)", fs=13, w="bold", c=on(cols[0]))
label(ax, sx0 + sw / 2, 1.6, "사전", fs=11.5, c=on(cols[0]))

# 도착: 최종 사후 (두 줄이 공유)
fx0, fw = 6.45, 1.45
box(ax, fx0, BY0, fw, BY1 - BY0, fc=cols[4], ec="none", r=0.1)
label(ax, fx0 + fw / 2, 2.05, "Beta(a+k,", fs=13, w="bold", c=on(cols[4]))
label(ax, fx0 + fw / 2, 1.75, "b+40−k)", fs=13, w="bold", c=on(cols[4]))
label(ax, fx0 + fw / 2, 1.38, "마지막 사후", fs=11.5, c=on(cols[4]))

# 위 줄: 10개씩 네 번
x_left, x_right = sx0 + sw, fx0
bw, bh = 0.8, 0.66
gap = (x_right - x_left - 3 * bw) / 4
label(ax, (x_left + x_right) / 2, 3.22, "10개씩 네 번 나눠 넣기", fs=12, w="bold", c=TEXT)
sub = ["₁", "₂", "₃", "₄"]
edges = [x_left]
for i in range(3):
    bx = x_left + gap * (i + 1) + bw * i
    c = cols[i + 1]
    box(ax, bx, YT - bh / 2, bw, bh, fc=c, ec="none", r=0.08)
    label(ax, bx + bw / 2, YT + 0.13, f"사후{sub[i]}", fs=12, w="bold", c=on(c))
    label(ax, bx + bw / 2, YT - 0.15, f"{10 * (i + 1)}개 뒤", fs=11, c=on(c))
    edges += [bx, bx + bw]
edges.append(x_right)
for j in range(4):                  # 화살표와 갱신 표시: 윗줄은 a에, 아랫줄은 b에 더하는 값
    a0, a1 = edges[2 * j] + 0.05, edges[2 * j + 1] - 0.05
    arrow(ax, a0, YT, a1, YT, color="#9AA1AB", lw=1.6, ms=11)
    xm = (edges[2 * j] + edges[2 * j + 1]) / 2
    label(ax, xm, YT + 0.44, f"+k{sub[j]}", fs=11, c=TEXT)
    label(ax, xm, YT + 0.19, f"+10−k{sub[j]}", fs=11, c=TEXT)
label(ax, (x_left + x_right) / 2, YT - 0.6, "각 단계의 사후가 다음 단계의 사전", fs=11, c=TEXT2)

# 아래 줄: 40개를 한 번에
arrow(ax, x_left + 0.05, YB, x_right - 0.05, YB, color="#9AA1AB", lw=1.8, ms=13)
label(ax, (x_left + x_right) / 2, YB + 0.24, "+k,  +40−k", fs=11.5, c=TEXT)
label(ax, (x_left + x_right) / 2, YB - 0.26, "40개를 한 번에   (k = k₁+k₂+k₃+k₄)", fs=11.5, c=TEXT2)

# 결론 한 곳만 강조색
pill(ax, fx0 + fw / 2 - 0.2, 0.38, "마지막 사후는 같다", fc=ACCENT, tc=ON_ACCENT, fs=12, h=0.4, padx=0.2)

save(fig, "../../assets/img/w2/sequential_update.png")
