#!/usr/bin/python3
import collections
import subprocess
import random
import numpy

DEFINITIONS_KBD = 'definitions.kbd'

KeySwitch = collections.namedtuple('KeySwitch', ['keycode', 'finger', 'hand', 'line', 'effort', 'special'])
KeyAction = collections.namedtuple('KeyAction', ['a', 'sa', 'b', 'sb'])

PC_keyboard = {
    24: KeySwitch(keycode=24, hand='L', finger=0, line=1, effort=2.0, special=0),  # Q
    25: KeySwitch(keycode=25, hand='L', finger=1, line=1, effort=2.0, special=0),  # W
    26: KeySwitch(keycode=26, hand='L', finger=2, line=1, effort=2.0, special=0),  # E
    27: KeySwitch(keycode=27, hand='L', finger=3, line=1, effort=2.0, special=0),  # R
    28: KeySwitch(keycode=28, hand='L', finger=3, line=1, effort=2.5, special=0),  # T
    29: KeySwitch(keycode=29, hand='R', finger=6, line=1, effort=3.0, special=0),  # Y
    30: KeySwitch(keycode=30, hand='R', finger=6, line=1, effort=2.0, special=0),  # U
    31: KeySwitch(keycode=31, hand='R', finger=7, line=1, effort=2.0, special=0),  # I
    32: KeySwitch(keycode=32, hand='R', finger=8, line=1, effort=2.0, special=0),  # O
    33: KeySwitch(keycode=33, hand='R', finger=9, line=1, effort=2.0, special=0),  # P
    #
    38: KeySwitch(keycode=38, hand='L', finger=0, line=2, effort=0.0, special=0),  # A
    39: KeySwitch(keycode=39, hand='L', finger=1, line=2, effort=0.0, special=2),  # S
    40: KeySwitch(keycode=40, hand='L', finger=2, line=2, effort=0.0, special=0),  # D
    41: KeySwitch(keycode=41, hand='L', finger=3, line=2, effort=0.0, special=0),  # F
    42: KeySwitch(keycode=42, hand='L', finger=3, line=2, effort=0.0, special=0),  # G
    43: KeySwitch(keycode=43, hand='R', finger=6, line=2, effort=0.0, special=0),  # H
    44: KeySwitch(keycode=44, hand='R', finger=6, line=2, effort=0.0, special=0),  # J
    45: KeySwitch(keycode=45, hand='R', finger=7, line=2, effort=0.0, special=0),  # K
    46: KeySwitch(keycode=46, hand='R', finger=8, line=2, effort=0.0, special=0),  # L
    47: KeySwitch(keycode=47, hand='R', finger=9, line=2, effort=0.0, special=0),  # TONOS
    #
    51: KeySwitch(keycode=51, hand='L', finger=0, line=3, effort=2.5, special=0),  # Z
    52: KeySwitch(keycode=52, hand='L', finger=0, line=3, effort=2.0, special=0),  # Z
    53: KeySwitch(keycode=53, hand='L', finger=1, line=3, effort=2.0, special=1),  # X
    54: KeySwitch(keycode=54, hand='L', finger=2, line=3, effort=2.0, special=1),  # C
    55: KeySwitch(keycode=55, hand='L', finger=3, line=3, effort=2.0, special=1),  # V
    56: KeySwitch(keycode=56, hand='L', finger=3, line=3, effort=3.5, special=0),  # B
    57: KeySwitch(keycode=57, hand='R', finger=6, line=3, effort=3.0, special=0),  # N
    58: KeySwitch(keycode=58, hand='R', finger=6, line=3, effort=2.0, special=0),  # M
    59: KeySwitch(keycode=59, hand='R', finger=7, line=3, effort=2.0, special=0),  # <
    60: KeySwitch(keycode=60, hand='R', finger=8, line=3, effort=2.0, special=0),  # >
    61: KeySwitch(keycode=61, hand='R', finger=9, line=3, effort=2.0, special=0),  # /
}
PC_keyboard_keys = list(PC_keyboard.keys())


def kbd_getKeyAction(keyboard, n, layout=PC_keyboard):
    return keyboard[layout[n]]


def kbd_getX11_def(keyboard):
    res = ""
    for key in keyboard.keys():
        ksw = keyboard[key]
        res += "keycode  {} = {} {} {} {}\n".format(key.keycode, ksw.a, ksw.sa, ksw.b, ksw.sb)
    return res


def bash_command(cmd):
    proc = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
    proc.wait()


def kbd_getX11_image(keyboard, fname="layout", label="A Keyboard"):
    rules_fname = "{}.kmap".format(fname)
    with open('%s' % rules_fname, 'w') as f:
        f.write(kbd_getX11_def(keyboard))

    bash_command("xmodmap %s" % rules_fname)
    bash_command("./layout_img.sh {image} \"{label}\"".format(image=fname, label=label))
    return fname + ".png"


def kbd_swap_keys(keyboard, keyA, keyB, model=PC_keyboard):
    a = model[keyA]
    b = model[keyB]
    t = keyboard[a]
    keyboard[a] = keyboard[b]
    keyboard[b] = t


Querty = {
    PC_keyboard[24]: KeyAction('q', 'Q', 'semicolon', 'colon'),
    PC_keyboard[25]: KeyAction('w', 'W', 'Greek_finalsmallsigma', 'Greek_SIGMA'),
    PC_keyboard[26]: KeyAction('e', 'E', 'Greek_epsilon', 'Greek_EPSILON'),
    PC_keyboard[27]: KeyAction('r', 'R', 'Greek_rho', 'Greek_RHO'),
    PC_keyboard[28]: KeyAction('t', 'T', 'Greek_tau', 'Greek_TAU'),
    PC_keyboard[29]: KeyAction('y', 'Y', 'Greek_upsilon', 'Greek_UPSILON'),
    PC_keyboard[30]: KeyAction('u', 'U', 'Greek_theta', 'Greek_THETA'),
    PC_keyboard[31]: KeyAction('i', 'I', 'Greek_iota', 'Greek_IOTA'),
    PC_keyboard[32]: KeyAction('o', 'O', 'Greek_omicron', 'Greek_OMICRON'),
    PC_keyboard[33]: KeyAction('p', 'P', 'Greek_pi', 'Greek_pi'),
    #
    PC_keyboard[38]: KeyAction('a', 'A', 'Greek_alpha', 'Greek_ALPHA'),
    PC_keyboard[39]: KeyAction('s', 'S', 'Greek_sigma', 'Greek_SIGMA'),
    PC_keyboard[40]: KeyAction('d', 'D', 'Greek_delta', 'Greek_SIGMA'),
    PC_keyboard[41]: KeyAction('f', 'F', 'Greek_phi', 'Greek_PHI'),
    PC_keyboard[42]: KeyAction('g', 'G', 'Greek_gamma', 'Greek_GAMMA'),
    PC_keyboard[43]: KeyAction('h', 'H', 'Greek_eta', 'Greek_ETA'),
    PC_keyboard[44]: KeyAction('j', 'J', 'Greek_xi', 'Greek_XI'),  # Ξ
    PC_keyboard[45]: KeyAction('k', 'K', 'Greek_kappa', 'Greek_KAPPA'),  # Ξ
    PC_keyboard[46]: KeyAction('l', 'L', 'Greek_lamda', 'Greek_LAMDA'),
    PC_keyboard[47]: KeyAction('semicolon', 'colon', 'dead_acute', 'dead_diaeresis'),
    #
    PC_keyboard[51]: KeyAction('backslash', 'bar', 'backslash', 'bar'),
    PC_keyboard[52]: KeyAction('z', 'Z', 'Greek_zeta', 'Greek_ZETA'),
    PC_keyboard[53]: KeyAction('x', 'X', 'Greek_chi', 'Greek_CHI'),
    PC_keyboard[54]: KeyAction('c', 'C', 'Greek_psi', 'Greek_PSI'),
    PC_keyboard[55]: KeyAction('v', 'V', 'Greek_omega', 'Greek_OMEGA'),
    PC_keyboard[56]: KeyAction('b', 'B', 'Greek_beta', 'Greek_BETA'),
    PC_keyboard[57]: KeyAction('n', 'N', 'Greek_nu', 'Greek_NU'),
    PC_keyboard[58]: KeyAction('m', 'M', 'Greek_mu', 'Greek_MU'),
    PC_keyboard[59]: KeyAction('comma', 'less', 'comma', 'less'),
    PC_keyboard[60]: KeyAction('period', 'greater', 'period', 'greater'),
    PC_keyboard[61]: KeyAction('slash', 'question', 'slash', 'question'),
}


def kbd_mutate(keyboard, mutations=3, indexes=PC_keyboard_keys, model=PC_keyboard):
    l = indexes.copy()
    random.shuffle(l)
    for i in range(mutations):
        r1 = l.pop()
        r2 = l[random.randrange(len(l))]
        kbd_swap_keys(keyboard, r1, r2, model)


def kbd_diffs(kbdA, kbdB=Querty):
    s = set(kbdA.items()) ^ set(kbdB.items())
    u = set([l[0].keycode for l in s])
    return list(u)


def kbd_distance(kbdA, kbdB=Querty):
    u = kbd_diffs(kbdA, kbdB)
    return len(u)


def kbd_getSwitch_forAction(keyboard, the_action):
    return [switch for switch, action in keyboard.items() if action == the_action].pop()


def kbd_crossover(keyboardA, keyboardB, percent=0.5, debug=False):
    processed = []
    keyboardNew = keyboardA.copy()
    for switchA, actionA in keyboardA.items():
        # Find the action at the other keyboard
        actionB = keyboardB[switchA]

        # Don't do anything if the mapping is the same
        if actionA != actionB:
            # Reverse search the switch
            switchB = kbd_getSwitch_forAction(keyboardB, actionA)

            # Now we wave a pair or positions to exchange
            r1 = switchA.keycode
            r2 = switchB.keycode
            if r1 not in processed:
                processed.append(r1)
                if random.randrange(0, 100) / 100 < percent:
                    if debug:
                        print("A_{}:{} -> B_{}:{}".format(switchA.keycode, actionA.a, switchB.keycode, actionB.a))
                    kbd_swap_keys(keyboardNew, r1, r2)
    return keyboardNew


def generate_population_from(keyboard, populationSize=12, mutations=31):
    population = [keyboard.copy() for x in range(populationSize)]
    # print population
    for x in population:
        kbd_mutate(x)
    return population

def population_matrix(population):
    l = len(population)
    res = numpy.zeros([l,l])
    for i in range(l):
        for j in range(i):
            res[i,j]=kbd_distance(population[i],population[j])
            res[j, i]=res[i,j]
    return res

population = generate_population_from(Querty)
pm= population_matrix(population)
