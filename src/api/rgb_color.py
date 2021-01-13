import random as rnd

def random(min = 0, max = 0xffffff):
    return rnd.randint(min, max)


def average(colors):
    count = len(colors)
    if count == 0:
        return 0

    red = 0
    green = 0
    blue = 0
    
    for color in colors:
        red += (color & 0xff0000) >> 16
        green += (color & 0xff00) >> 8
        blue += (color & 0xff)
    
    red //= count
    green //= count
    blue //=count

    average =  (int(red) << 16) + (int(green) << 8) + int(blue)
    return average