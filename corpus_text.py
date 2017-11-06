#!/usr/bin/python3
import unicodedata
import string
from collections import Counter


class CorpusText:
    chars = []
    filename = None
    debug = False

    valid_keystroke_chars = "W#ΕΡΤΥΘΙΟΠ[]"
    valid_keystroke_chars += "ΑΣΔΦΓΗΞΚΛ';@"
    valid_keystroke_chars += "«ΖΧΨΩΒΝΜ,./"
    valid_keystroke_reject_chars = ''

    def __init__(self, filename, num_chars=None):
        handle = open(filename, 'r')
        contents = handle.read(num_chars)
        result = ''
        for c in contents:
            result += self.uninorm(c)
        self.chars = list(result)
        self.filename = filename

    def __repr__(self):
        return "<Corpus of '%s' keystrokes:%s>" % (self.filename, len(self.chars))

    def __str__(self):
        res = self.__repr__() + "\n"
        line_num = 0
        chars = 0
        text_line = ''
        for x in self.chars:
            text_line += x
            chars += 1
            if chars == 60:
                line_num += 1
                res += "{:3}: {}\n".format(line_num, text_line)
                chars = 0
                text_line = ''
        line_num += 1
        res += "{:3}: {}\n".format(line_num, text_line)
        return res

    def stats(self):
        """ Return sorted list (key, count, percent """
        frequencies = Counter(self.chars)
        statistics = [(c, frequencies[c], frequencies[c] / len(self.chars)) for c in frequencies]
        statistics.sort(key=lambda x: x[2], reverse=True)
        return statistics

    @staticmethod
    def uninorm(uni_char):
        """ Convert a unicode character to keystrokes """
        # Remove enter
        if uni_char == '\n':
            return ''
        # Remove space
        if uni_char == ' ':
            return ''

        unicode_name = unicodedata.name(uni_char)
        no_accent_char = unicodedata.lookup(unicode_name.replace(' WITH TONOS', ''))
        no_accent_char_upper = no_accent_char.upper()

        if unicode_name == 'GREEK SMALL LETTER FINAL SIGMA':
            no_accent_char_upper = 'W'
        if unicode_name == 'GREEK SMALL LETTER IOTA WITH DIALYTIKA':
            no_accent_char_upper = 'Ι'
        if unicode_name == 'GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS':
            no_accent_char_upper = '@Ι'
        if unicode_name == 'RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK':
            no_accent_char_upper = '«'
        if unicode_name == 'RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK':
            no_accent_char_upper = '«'
        if unicode_name == 'MIDDLE DOT':
            no_accent_char_upper = '#'

        # Reject strange characters and report only once
        if CorpusText.valid_keystroke_chars.find(no_accent_char_upper) < 0:
            if CorpusText.valid_keystroke_reject_chars.find(uni_char) <0:
                # Don't report ascii printable characters
                if not uni_char in string.printable:
                    if CorpusText.debug is True:
                        print("Reject char |{}| '{}'".format(unicode_name, uni_char))
                    CorpusText.valid_keystroke_reject_chars += uni_char
            return ''

        extra_return=''
        if unicode_name.endswith(" WITH TONOS"):
            extra_return = '@'
        return extra_return + no_accent_char_upper


if __name__ == '__main__':
    def print_long_text(text, show_lines=3):
        lines = text.split('\n')
        print("\n".join(lines[0:(show_lines + 1)]))
        print("         ... more  ...")
        print("\n".join(lines[-(show_lines + 1):]))


    def print_stats(statistics, show_lines=3):
        if show_lines == 0:
            for item in statistics:
                print("keystroke:'{}' {:5.2f}% count={}".format(item[0], item[2] * 100, item[1]))
            return

        for item in statistics[:show_lines]:
            print("keystroke:'{}' {:5.2f}% count={}".format(item[0], item[2] * 100, item[1]))
        print("         ... more  ...")
        for item in statistics[-show_lines:]:
            print("keystroke:'{}' {:6.3f}% count={}".format(item[0], item[2] * 100, item[1]))


    # Get some text
    # path = 'data/longos_intro.txt'
    # path = 'data/alphabet.txt'
    path = 'data/longus_full.txt'
    # corpus = CorpusText(path, 200)
    corpus = CorpusText(path)
    print_long_text(corpus.__str__())

    # Get some statistics from text
    print("Statistics")
    stats = corpus.stats()
    print_stats(stats, 9)
    # print("Total keystrokes in file: {}".format(len(corpus.chars)))
