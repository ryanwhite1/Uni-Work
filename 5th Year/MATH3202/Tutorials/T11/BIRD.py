# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:01:23 2023

@author: ryanw
"""
r = 3.6
E = 32
p_sing = 0.004
p_food = 0.6


def f_sing(s):
    return 12 + 0.002 * s + 0

def f_forage(s):
    return 8 + 0.007 * s + 0

def birdD(t, x, m):
    s = int(x)
    p = x - s
    return p * bird(t, s + 1, m)[0] + (1 - p) * bird(t, s, m)[0]

def birdB(t, s, m):
    return 0.25 * birdD(t, s - 6.4, m) + 0.5 * birdD(t, s, m) + 0.25 * birdD(t, s + 6.4, m)

bird_ = {}
def bird(t, s, m):
    if s <= 0:
        return (0, 'Dead')
    elif t == 150:
        if m == "Y":
            return (2, 'Mate')
        else:
            return (1, 'No mate')
    if (t, s, m) not in bird_:
        if t >= 75:
            bird_[t, s, m] = (birdB(t + 1, s - r, m), 'Rest')
        else:
            bird_[t, s, m] = max([(birdB(t + 1, s - r, m), 'Rest'),
                    (p_sing * birdB(t + 1, s - f_sing(s), 'Y') + (1 - p_sing) * birdB(t + 1, s - f_sing(s), m), 'Sing'),
                    (p_food * birdB(t + 1, s - f_forage(s) + E, m) + (1 - p_food) * birdB(t + 1, s - f_forage(s), m), 'Forage')])
    return bird_[t, s, m]