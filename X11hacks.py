#!/usr/bin/python3

# Contains code from ActiveState Recipie
# Parser Keylogger based on a Finite State Machine (Python recipe)
# http://code.activestate.com/recipes/577952-parser-keylogger-based-on-a-finite-state-machine/


import re
from subprocess import *

key_map = {}
table = Popen("xmodmap -pke", shell=True, bufsize=1, stdout=PIPE).stdout
for line in table:
    m = re.match('keycode +(\d+) = (.+)', line.decode())
    if m:
        code = m.groups()[0]
        specline = m.groups()[1]
        if "Greek" in specline:
            print("{}: {}".format(code,specline))
            key_map[code]=specline


# # List of of the modifiers that represent also all the states of the FSM (Finite State Machine)
# mod_keys = ['NORMAL', 'SHIFT_L', 'SHIFT_R', 'ISO_LEVEL3_SHIFT', 'SHIFT_R_ALT_R', 'SHIFT_L_ALT_R']
# # Extended modifiers Keys don't give a concrete char in xmodmap command but only combinations of keys.
# ext_mod_keys = ['CONTROL_L', 'CONTROL_R', 'ALT_L', 'SUPER_L']
# # List of keys that will be excluded by the parser
# special_keys = ["UP", "DOWN", "LEFT", "RIGHT", "BACKSPACE", "TAB", "HOME", "END", "DELETE"]

# Maps the kewords appear in xmodmap -pke command into the corresponding char
transform = {}
# transform['RETURN'] = '\n'
# transform['SPACE'] = ' '
# transform['PLUS'] = '+'
# transform['MINUS'] = '-'
# transform['COMMA'] = ','
# transform['UNDERSCORE'] = '_'
# transform['PERIOD'] = '.'
# transform['COLON'] = ':'
# transform['SEMICOLON'] = ';'
# transform['DOLLAR'] = '$'
# transform['STERLING'] = '£'
# transform['QUOTEDBL'] = '"'
# transform['EXCLAM'] = '!'
# transform['SLASH'] = '/'
# transform['BRACKETLEFT'] = '['
# transform['BRACKETRIGHT'] = ']'
# transform['AT'] = '@'
# transform['EUROSIGN'] = '€'
# transform['NUMBERSIGN'] = '#'
# transform['BRACELEFT'] = '{'
# transform['BRACERIGHT'] = '}'
# transform['EGRAVE'] = 'è'
# transform['OGRAVE'] = 'ò'
# transform['AGRAVE'] = 'à'
# transform['UGRAVE'] = 'ù'
# transform['IGRAVE'] = 'ì'
# transform['EACUTE'] = 'é'
# transform['CCEDILLA'] = 'ç'
# transform['DEGREE'] = '°'
# transform['SECTION'] = '§'
# transform['APOSTROPHE'] = '\''
# transform['ASCIICIRCUM'] = '^'
# transform['QUESTION'] = '?'
# transform['PERCENT'] = '%'
# transform['AMPERSAND'] = '&'
# transform['PARENLEFT'] = '('
# transform['PARENRIGHT'] = ')'
# transform['EQUAL'] = '='
# transform['BAR'] = '|'
# transform['BACKSLASH'] = '\\'
# transform['ASTERISK'] = '*'
# transform['MULTIPLY'] = '×'
# transform['DIVISION'] = '÷'
# transform['QUESTIONDOWN'] = '¿'
# transform['EXCLAMDOWN'] = '¡'
# transform['PLUSMINUS'] = '±'
# transform['TRADEMARK'] = '™'
# transform['SEVENEIGHTHS'] = '⅞'
# transform['FIVEEIGHTHS'] = '⅝'
# transform['THREEEIGHTHS'] = '⅜'
# transform['ONEEIGHTH'] = '⅛'
# transform['ASCIITILDE'] = '~'
# transform['ONESUPERIOR'] = '¹'
# transform['TWOSUPERIOR'] = '²'
# transform['THREESUPERIOR'] = '³'
# transform['ONEQUARTER'] = '¼'
# transform['ONEHALF'] = '½'
# transform['NOTSIGN'] = '¬'
# transform['GRAVE'] = '`'
# transform['BROKENBAR'] = '¦'
# transform['PARAGRAPH'] = '¶'
# transform['COPYRIGHT'] = '©'
# transform['REGISTERED'] = '®'
# transform['NOSYMBOL'] = None




# def get_key_map():
#     """
#     Returns the corrisponding Key based on the current status (modifier) and the keycode of the key typed.
#          char = f(keycode, modifier)
#     Where char is the corresponding character given by the combination.
#     """
#     table = Popen("xmodmap -pke", shell=True, bufsize=1, stdout=PIPE).stdout
#     key_map = {}
#     for line in table:
#         m = re.match('keycode +(\d+) = (.+)', line.decode())
#         if m:
#             l = m.groups()[1].split()
#             # Wipes out all the useless elements that appears in xmodmap
#             nl = []
#             for i in range(len(l)):
#                 if i == 0:  # NORMAL
#                     nl.append(l[i])
#                 if i == 1:  # SHIFT_L
#                     nl.append(l[i])
#                 if i == 3:  # SHIFT_R
#                     nl.append(l[i])
#                 if i == 4:  # ISO_LEVEL3_SHIFT
#                     nl.append(l[i])
#                 if i == 5:  # SHIFT_?_ALT_R
#                     nl.append(l[i])
#                     nl.append(l[i])
#
#             seq = [transform.get(letter.upper(), letter) for letter in nl]
#             # Add None element for the rest of the table
#             seq.extend([None for i in range(len(mod_keys) - len(seq))])
#             # Pad out with the remained extended combinations
#             seq.extend([mod + '+' + str(seq[0]) for mod in ext_mod_keys])
#
#             assert len(seq) == len(mod_keys) + len(ext_mod_keys), \
#                 "Err:" + str(seq) + " has not the same size of " + str(mod_keys) + str(ext_mod_keys)
#
#             key_map[m.groups()[0]] = {}
#             for mod, s in zip(mod_keys + ext_mod_keys, seq):
#                 # key_map[m.groups()[0]][mod] = s
#
#     return key_map
#     # return seq
#
# keyMap = get_key_map()
# for key,value in keyMap.items():
#     print("{} -> {}".format(key,value))