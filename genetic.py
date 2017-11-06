#!/usr/bin/python3
import time
import math
import numpy
from corpus_text import CorpusText
from typist import Typist
from keyboard_layout import *

# set to the number of cores you want to use
import multiprocessing
CORES = min(multiprocessing.cpu_count(), 8)


class Population:
    def __init__(self, filename, population_size=50, mutations=8, fix_mutations=2):
        self.corpus = CorpusText(filename)
        self.population_size = population_size

        # Always start with some well known keyboards
        self.keyboards = [QuertyKeyboard]
        for i in range(population_size - len(self.keyboards)):
            keyboard = QuertyKeyboard.copy()
            keyboard.mutate(mutations)
            self.keyboards.append(keyboard)
        self.generation = 0
        self.fintess_store = []
        self.sessions = None
        self.training_time = 0
        self.fix_mutations = fix_mutations
        self.update()

    def update(self):
        sessions = []
        for i in range(len(self.keyboards)):
            sessions.append(Typist(self.keyboards[i], self.corpus))

        # Run the typing simulation in parallel
        start_time = time.process_time()
        with multiprocessing.Pool(CORES) as p:
            self.sessions = p.map(Typist.exercise, sessions)
        self.training_time = time.process_time() - start_time
        self.generation += 1

        # Sort the keyboards
        self.sessions.sort(key=lambda x: x.fitness)

        # Store last best fastnesses
        self.fintess_store.append(self.sessions[0].fitness)

    def step(self):
        keeep_top = self.population_size // 3
        self.keyboards = []
        # Elitist strategy
        for i in range(keeep_top):
            self.keyboards.append(KeyboardLayout(self.sessions[i].keyboard.layout))
        for i in range(self.population_size - keeep_top):
            p1 = random.randrange(keeep_top)
            while True:
                p2 = random.randrange(keeep_top)
                if p1 != p2:
                    break
            X = self.keyboards[p1]
            Y = self.keyboards[p2]
            C = X.sex(Y)
            C.mutate(self.fix_mutations)
            self.keyboards.append(C)
        self.update()

    def keep_going(self):
        MAX_RUNS = 1000
        moving_length = 10
        check_every = 20
        N2 = 3
        if population.generation % check_every == 0:
            conv = numpy.convolve(self.fintess_store, numpy.ones((moving_length,)) / moving_length, mode='valid')
            # If conv stays the same for N2 runs then pause
            last = conv[-N2:]
            if math.isclose(numpy.mean(last), conv[-1], abs_tol=0.00001) and len(last) >= N2:
                # print("Convolution stop at ",conv[-1])
                return False
                # else:
                #     print("** Convolution",conv[-N2:])
        return self.generation < MAX_RUNS

    def print_population(self, details=False):
        bf = self.sessions[0].fitness
        d = QuertyKeyboard.distance(self.sessions[0].keyboard)
        if details:
            print("Generation: {}, training took {:5.3f}secs.".format(self.generation, self.training_time))
            for i in range(len(self.sessions)):
                session = self.sessions[i]
                d = session.keyboard.distance(QuertyKeyboard)
                layout = session.keyboard.layout
                fitness = session.fitness
                print('{:3}:"{}", d={:2} fitness:{:8.6f}'.format(i, layout, d, fitness))
            print("Best fitness: {:5.3f}".format(bf))
        else:
            layout = self.sessions[0].keyboard.layout
            print(
                "Generation: {gen:3}, fitness={fit:20.17f}.  Best:\"{layout}\" ({dist}).".format(
                    gen=self.generation, fit=bf, layout=layout, dist=d))


if __name__ == '__main__':
    population = Population('data/longus_full.txt')
    population.print_population(False)

    while True:
        population.step()
        population.print_population(False)
        if not population.keep_going():
            break;

    print("\nBest Keyboard:")
    best = population.keyboards[0]
    print(best)

    print("\nStatistics:")
    s = population.sessions[0]
    s.print_stats()
