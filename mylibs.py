from math import exp

def get_color(rating: int) -> int:
    if rating < 400:
        return 0x7c7c7c
    elif rating < 800:
        return 0x7b3a00
    elif rating < 1200:
        return 0x007b00
    elif rating < 1600:
        return 0x00b8b8
    elif rating < 2000:
        return 0x0000f6
    elif rating < 2400:
        return 0xc0c000
    elif rating < 2800:
        return 0xff8005
    else:
        return 0xff0000

def arrange_diff(difficulty):
    if difficulty >= 400: return difficulty
    else: return round(400 / exp(1.0 - difficulty / 400))