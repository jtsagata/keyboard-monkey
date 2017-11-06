#!/usr/bin/python3
import re
from subprocess import *

class KeySwitch:
    def __init__(self, keycode, finger, hand, line, effort):
        self.keycode = keycode
        self.finger = finger
        self.hand = hand
        self.line = line
        self.effort = effort


PC_keyboard = {
    24: KeySwitch(keycode=24, hand='L', finger=0, line=1, effort=2.0),  # Q
    25: KeySwitch(keycode=25, hand='L', finger=1, line=1, effort=2.0),  # W
    26: KeySwitch(keycode=26, hand='L', finger=2, line=1, effort=2.0),  # E
    27: KeySwitch(keycode=27, hand='L', finger=3, line=1, effort=2.0),  # R
    28: KeySwitch(keycode=28, hand='L', finger=3, line=1, effort=2.5),  # T
    29: KeySwitch(keycode=29, hand='R', finger=6, line=1, effort=3.0),  # Y
    30: KeySwitch(keycode=30, hand='R', finger=6, line=1, effort=2.0),  # U
    31: KeySwitch(keycode=31, hand='R', finger=7, line=1, effort=2.0),  # I
    32: KeySwitch(keycode=32, hand='R', finger=8, line=1, effort=2.0),  # O
    33: KeySwitch(keycode=33, hand='R', finger=9, line=1, effort=2.0),  # P
    #
    38: KeySwitch(keycode=38, hand='L', finger=0, line=2, effort=0.0),  # A
    39: KeySwitch(keycode=39, hand='L', finger=1, line=2, effort=0.0),  # S
    40: KeySwitch(keycode=40, hand='L', finger=2, line=2, effort=0.0),  # D
    41: KeySwitch(keycode=41, hand='L', finger=3, line=2, effort=0.0),  # F
    42: KeySwitch(keycode=42, hand='L', finger=3, line=2, effort=0.0),  # G
    43: KeySwitch(keycode=43, hand='R', finger=6, line=2, effort=0.0),  # H
    44: KeySwitch(keycode=44, hand='R', finger=6, line=2, effort=0.0),  # J
    45: KeySwitch(keycode=45, hand='R', finger=7, line=2, effort=0.0),  # K
    46: KeySwitch(keycode=46, hand='R', finger=8, line=2, effort=0.0),  # L
    47: KeySwitch(keycode=47, hand='R', finger=9, line=2, effort=0.0),  # TONOS
    #
    52: KeySwitch(keycode=52, hand='L', finger=0, line=3, effort=2.0),  # Z
    53: KeySwitch(keycode=53, hand='L', finger=1, line=3, effort=2.0),  # X
    54: KeySwitch(keycode=54, hand='L', finger=2, line=3, effort=2.0),  # C
    55: KeySwitch(keycode=55, hand='L', finger=3, line=3, effort=2.0),  # V
    56: KeySwitch(keycode=56, hand='L', finger=3, line=3, effort=3.5),  # B
    57: KeySwitch(keycode=57, hand='R', finger=6, line=3, effort=3.0),  # N
    58: KeySwitch(keycode=58, hand='R', finger=6, line=3, effort=2.0),  # M
    59: KeySwitch(keycode=59, hand='R', finger=7, line=3, effort=2.0),  # <
    60: KeySwitch(keycode=60, hand='R', finger=8, line=3, effort=2.0),  # >
    61: KeySwitch(keycode=61, hand='R', finger=9, line=3, effort=2.0),  # /
}


class SwitchToLayout:
    def __init__(self, code, sa: str = None, sa_shift: str = None, sb: str = None, sb_shift: str = None):
        self.code = code
        self.sa = sa
        self.sa_shift = sa_shift
        self.sb = sb
        self.sb_shift = sb_shift

    def __str__(self):
        res = "keycode  {code} = {sa} {sa_shift} {sb} {sb_shift}".format(code=self.code, sa=self.sa,
                                                                         sa_shift=self.sa_shift, sb=self.sb,
                                                                         sb_shift=self.sb_shift)
        return res



class Layout:
    def __init__(self):
        pass

basic_scancodes = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                   38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
                   52, 53, 54, 55, 56, 57, 58, 59, 60, 61]

Querty_Layout = {}
table = Popen("xmodmap -pke", shell=True, bufsize=1, stdout=PIPE).stdout
for line in table:
    m = re.match('keycode +(\d+) = (.+)', line.decode())
    if m:
        code = int(m.groups()[0])
        specline = m.groups()[1]
        if code in basic_scancodes:
            opts = specline.split()
            Querty_Layout[code] = SwitchToLayout(code=code, sa=opts[0], sa_shift=opts[1], sb=opts[2],
                                                 sb_shift=opts[3])


def print_layout(layout, debug=False):
    for k, v in layout.items():
        if debug:
            print("{}:{}".format(k, v))
        else:
            print(v)


if __name__ == '__main__':
    print_layout(Querty_Layout, True)
    pass
