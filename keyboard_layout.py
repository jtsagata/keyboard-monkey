#!/usr/bin/python3
import unicodedata
import editdistance
import random

def str_replace_at(s, newstring, index):
    # raise an error if index is outside of the string
    if index < 0 and index >= len(s):
        raise ValueError("index outside given string")
    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]


class KeyboardLayout:
    querty_layout = "W#ΕΡΤΥΘΙΟΠ[]"
    querty_layout += "ΑΣΔΦΓΗΞΚΛ';@"
    querty_layout += "«ΖΧΨΩΒΝΜ,./"

    # [finger, hand L=1,R=2, baseline key effort
    efforts =[
        #    Q         W         E           R           T
        [0,1,2.0], [1,1,2.0], [2,1,2.0], [2,1,2.0], [2,1,2.5],
        #   Y          U         I           o           P        [           ]
        [6,2,3.0], [6,2,2.0], [8,2,2.0], [8,2,3.0], [9,2,2.0] , [9,2,2.5], [9,2, 4.0],
        #   A          S         D           F          G
        [0,1,0.0], [1,1,0.0],  [2,1,0.0], [3,1,0.0], [3, 1, 2.0],
        #   H          J         K           L          ;        '         \
        [6,2,2.0], [6,2,0.0], [7,2,0.0], [8,2,0.0], [8,2,0.0],[9,2,0.0], [9,2,2.0],
        #   <          z         x           c         v           B
        [0,1,2.0], [1,1,2.0], [1,1,2.0],[2,1,2.0],[3,1,2.0],  [3,2,2.0],
        #   N          M         <           <         \
        [6,2,2.0], [7,2,2.0], [8,2,2.0], [9,2,2.0],[9,2,3.0]
    ]

    layout = ''

    def __init__(self, layout=None):
        if layout is None:
            self.layout = KeyboardLayout.querty_layout
        else:
            if len(layout) != len(self.querty_layout):
                raise ValueError('Bad lenght for keyboard layout. ')
            # Must be a rearrangement of querty
            if ''.join(set(sorted(layout))) != ''.join(set(sorted(KeyboardLayout.querty_layout))):
                raise ValueError('Bad keyboard layout. ')
            self.layout = layout

    def mutate(self, mutations=3):
        l = [x for x in range(len(self))]
        for i in range(mutations):
            r1 = l.pop(random.randrange(len(l)))
            r2 = l.pop(random.randrange(len(l)))
            tmp = self[r1]
            self[r1] = self[r2]
            self[r2] = tmp
            # print("Swapping {}: {}<->{}".format(i,r1,r2))

    def distance(self, other_keyboard):
        return editdistance.eval(self.layout, other_keyboard.the_layout)

    def __len__(self):
        return len(self.layout)

    def __getitem__(self, index):
        return self.layout[index]

    def __setitem__(self, key, value):
        self.layout = str_replace_at(self.layout, value, key)

    def __str__(self):
        line_a = self._print_keyboard_line(self.layout[0:12])
        line_b = self._print_keyboard_line(self.layout[12:24])
        line_c = self._print_keyboard_line(self.layout[24:])
        return (line_a + line_b + line_c).rstrip()

    def _print_keyboard_line(self, line):
        res = ''
        for c in line:
            c = unicodedata.lookup('MIDDLE DOT') if c == '#' else c
            c = "΄" if c == '#' else c
            res += " [{}] ".format(c)
        return res.center(60, ' ') + '\n'

    def keybord_costs(self):
        line_a = self._print_keyboard_line_cost(self.layout[0:12])
        line_b = self._print_keyboard_line_cost(self.layout[12:24])
        line_c = self._print_keyboard_line_cost(self.layout[24:])
        return (line_a + line_b + line_c).rstrip()

    def _print_keyboard_line_cost(self, line):
        res1 = ''
        for c in line:
            stats = self.get_stats_for_key(c)
            key = unicodedata.lookup('LEFT HAND TELEPHONE RECEIVER') if stats[1] == 1 else unicodedata.lookup('RIGHT HAND TELEPHONE RECEIVER')
            c = unicodedata.lookup('MIDDLE DOT') if c == '#' else c
            c = "΄" if c == '#' else c
            res1 += " ⎡{}   {}{}⎤ ".format(c,stats[0],key)
        res2 = ''
        for c in line:
            stats = self.get_stats_for_key(c)
            res2 += " ⎣ {}  ⎦ ".format(stats[2])
        return res1.center(120, ' ') + '\n'+res2.center(120, ' ') + "\n\n"
        # return res1 + '\n' + res2+ "\n\n"

    def get_stats_for_key(self, c):
        index = self.layout.find(c)
        stats = self.efforts[index]
        return stats


# Some famous keyboards
QuertyKeyboard = KeyboardLayout()

if __name__ == '__main__':
    print("A starting querty keyboard")
    print(QuertyKeyboard)
    print("A starting querty keyboard with costs")
    print(QuertyKeyboard.keybord_costs())

    # print("\nA mutating keyboard")
    # alayout = KeyboardLayout("ΑΣΔΦΓΗΞΚΛ';@" + "«ΖΧΨΩΒΝΜ,./" + "W#ΕΡΤΥΘΙΟΠ[]")
    # print(alayout)
    # print("Distance from querty:{}".format(alayout.distance(QuertyKeyboard)))
    #
    # print("Make 3 mutattions")
    # k = KeyboardLayout()
    # k.mutate()
    # print(k)
    # print("Distance from querty:{}".format(k.distance(QuertyKeyboard)))
