from typing import Sequence, Optional, Tuple
from . import ui


def horizontal_bars(
    values: Sequence[float],
    labels: Optional[Sequence[str]] = None,
    width: int = 30,
    show_zero_line: bool = True,
) -> str:
    if not values:
        return ""
    labels = labels or [str(i) for i in range(len(values))]
    label_w = max(len(str(l)) for l in labels)
    max_abs = max(abs(v) for v in values) or 1.0
    half = width // 2

    lines = []
    for label, value in zip(labels, values):
        bar_len = int(round(abs(value) / max_abs * half))
        bar = "#" * max(1, bar_len) if value != 0 else ""
        if value >= 0:
            left = " " * half
            right = ui.green(bar) + " " * (half - len(bar))
        else:
            left = " " * (half - len(bar)) + ui.red(bar)
            right = " " * half
        amount = ui.colored_money(value, width=12)
        lines.append(f" {str(label).rjust(label_w)} | {left}|{right} {amount}")

    if show_zero_line:
        sep = " " * (label_w + 2) + "+" + "-" * half + "+" + "-" * half + "+"
        lines.insert(0, ui.gray(sep))
        lines.append(ui.gray(sep))
    return "\n".join(lines)


def line_chart(
    points: Sequence[Tuple[float, float]],
    width: int = 50,
    height: int = 12,
    title: Optional[str] = None,
) -> str:
    if not points:
        return ""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    if x_max == x_min:
        x_max = x_min + 1
    if y_max == y_min:
        y_max = y_min + 1

    grid = [[" "] * width for _ in range(height)]

    if y_min < 0 < y_max:
        zero_row = int((y_max - 0) / (y_max - y_min) * (height - 1))
        for c in range(width):
            grid[zero_row][c] = "-"

    for x, y in points:
        col = int((x - x_min) / (x_max - x_min) * (width - 1))
        row = int((y_max - y) / (y_max - y_min) * (height - 1))
        col = min(max(col, 0), width - 1)
        row = min(max(row, 0), height - 1)
        ch = "+" if y >= 0 else "x"
        grid[row][col] = ui.green(ch) if y >= 0 else ui.red(ch)

    body = []
    for r, row in enumerate(grid):
        if r == 0:
            tag = f"{y_max:>10,.2f} |"
        elif r == height - 1:
            tag = f"{y_min:>10,.2f} |"
        else:
            tag = " " * 10 + " |"
        body.append(ui.gray(tag) + "".join(row))
    body.append(ui.gray(" " * 11 + "+" + "-" * width))
    body.append(ui.gray(f"{x_min:>11,.2f}" + " " * (width - 12) + f"{x_max:,.2f}"))

    out = []
    if title:
        out.append(ui.bold(ui.cyan(title)))
    out.extend(body)
    return "\n".join(out)
