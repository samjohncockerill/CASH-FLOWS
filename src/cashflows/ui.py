import os
import sys

_use_color = os.environ.get("NO_COLOR") is None and sys.stdout.isatty()
if sys.platform == "win32":
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass


def set_color(enabled: bool) -> None:
    global _use_color
    _use_color = enabled


def _wrap(code: str, text: str) -> str:
    if not _use_color:
        return text
    return f"\x1b[{code}m{text}\x1b[0m"


def red(t):     return _wrap("31", t)
def green(t):   return _wrap("32", t)
def yellow(t):  return _wrap("33", t)
def blue(t):    return _wrap("34", t)
def magenta(t): return _wrap("35", t)
def cyan(t):    return _wrap("36", t)
def gray(t):    return _wrap("90", t)
def bold(t):    return _wrap("1", t)
def dim(t):     return _wrap("2", t)


def colored_money(value: float, width: int = 0) -> str:
    sign = "+" if value > 0 else ("-" if value < 0 else " ")
    body = f"{sign}{abs(value):,.2f}"
    if width:
        body = body.rjust(width)
    if value > 0:
        return green(body)
    if value < 0:
        return red(body)
    return body


def colored_pct(value: float, width: int = 0) -> str:
    body = f"{value * 100:+.2f}%"
    if width:
        body = body.rjust(width)
    if value > 0:
        return green(body)
    if value < 0:
        return red(body)
    return body


def box(title: str, lines, width: int = 60, color=cyan) -> str:
    title = f" {title} "
    top = color("+" + title.center(width - 2, "-") + "+")
    bot = color("+" + "-" * (width - 2) + "+")
    side = color("|")
    out = [top]
    for ln in lines:
        out.append(f"{side} {ln}{' ' * max(0, width - 4 - _visible_len(ln))} {side}")
    out.append(bot)
    return "\n".join(out)


def header(title: str, width: int = 60) -> str:
    bar = "=" * width
    return "\n".join([cyan(bar), cyan(bold(title.center(width))), cyan(bar)])


def _visible_len(s: str) -> int:
    out = []
    skip = False
    for ch in s:
        if ch == "\x1b":
            skip = True
            continue
        if skip:
            if ch == "m":
                skip = False
            continue
        out.append(ch)
    return len("".join(out))
