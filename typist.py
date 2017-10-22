#!/usr/bin/python3
from corpus_text import CorpusText
from keyboard_layout import *


class Typist:
    debug = False

    def __init__(self, the_keyboard, the_corpus):
        self.keyboard = the_keyboard
        self.corpus = the_corpus
        self.keyboard_name = the_keyboard.layout
        self.reset()
        self.exercise()
        self.calculate_fitness()

    def reset(self):
        self.hands = [0, 0]
        self.fingers = [0] * 10
        self.keystrokes = 0
        self.effort = 0
        self.fitness = 0

    def exercise(self):
        if len(self.corpus.chars) == 0:
            raise ValueError("Corpus have no data to train")
        for c in self.corpus.chars:
            stats = keyboard.get_stats_for_key(c)
            if self.debug:
                print("char:{} finger:{}, hand:{}, effort:{}".format(c, stats[0], stats[1], stats[2]))
            self.keystrokes += 1
            self.effort += stats[2]
            self.fingers[stats[0]] += 1
            self.hands[stats[1] - 1] += 1

    def calculate_fitness(self):
        self.fitness = self.effort / self.keystrokes

    def print_stats(self):
        print(self)
        if self.keystrokes > 0:
            finger_freq = [x / session.keystrokes * 100 for x in session.fingers]
            print(',  '.join('F{}:{:5.2f}%'.format(*k) for k in enumerate(finger_freq)))
            hand_freq = [x / session.keystrokes * 100 for x in session.hands]
            print('Left hand: {:5.2f}%, Right hand: {:5.2f}%'.format(*hand_freq))

    def __repr__(self):
        if self.keystrokes > 0:
            effort = self.effort / self.keystrokes
            res = '<session:{},on:"{}",strokes:{},effort:{:4.2f},fitness:{:8.5f}>'.format(self.corpus.filename,
                                                                                          self.keyboard.layout,
                                                                                          self.keystrokes, effort,
                                                                                          self.fitness)
        else:
            res = '<session:{},on:"{}", untrained>'.format(self.corpus.filename, self.keyboard.layout)
        return res


if __name__ == '__main__':
    path = 'data/longus.txt'
    # path = 'data/alphabet.txt'
    corpus = CorpusText(path)

    keyboard = QuertyKeyboard

    session = Typist(keyboard, corpus)
    session.print_stats()
