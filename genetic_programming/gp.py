from random import random, randint, seed
from statistics import mean
from copy import deepcopy


def add(x, y): return x + y
def sub(x, y): return x - y
def mul(x, y): return x * y


FUNC = [add, sub, mul]
MODS = ['x', -2, -1, 0, 1, 2]

P_SIZE = 60
MIN_D = 2
MAX_D = 5
GENS = 250
T_SIZE = 5
CROSS_RATE = 0.8
MUT_PRBB = 0.2


def target_func(x):  # evolution's target
    return x*x*x + x*x + x + 1


class GPTree:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def node_label(self):  # string label
        if (self.data in FUNC):
            return self.data.__name__
        else:
            return str(self.data)

    def print_tree(self, prefix=""):  # prints the tree to be read through text
        print("%s%s" % (prefix, self.node_label()))
        if self.left:
            self.left.print_tree(prefix + "   ")
        if self.right:
            self.right.print_tree(prefix + "   ")

    def compute_tree(self, x):  # traverses the tree to check the generated function
        if (self.data in FUNC):
            return self.data(self.left.compute_tree(x), self.right.compute_tree(x))
        elif self.data == 'x':
            return x
        else:
            return self.data

    def random_tree(self, grow, max_depth, depth=0):
        # create random tree using either grow or full method
        if depth < MIN_D or (depth < max_depth and not grow):
            self.data = FUNC[randint(0, len(FUNC)-1)]
        elif depth >= max_depth:
            self.data = MODS[randint(0, len(MODS)-1)]
        else:  # intermediate depth, grow
            if random() > 0.5:
                self.data = MODS[randint(0, len(MODS)-1)]
            else:
                self.data = FUNC[randint(0, len(FUNC)-1)]
        if self.data in FUNC:
            self.left = GPTree()
            self.left.random_tree(grow, max_depth, depth=depth + 1)
            self.right = GPTree()
            self.right.random_tree(grow, max_depth, depth=depth + 1)

    def mutation(self):
        if random() < MUT_PRBB:  # mutate at this node
            self.random_tree(grow=True, max_depth=2)
        elif self.left:
            self.left.mutation()  # gives child nodes chance to mutate if this one doesn't
        elif self.right:
            self.right.mutation()

    def size(self):  # tree size based on number of nodes
        if self.data in MODS:
            return 1
        l = self.left.size() if self.left else 0
        r = self.right.size() if self.right else 0
        return 1 + l + r

    def build_subtree(self):
        t = GPTree()
        t.data = self.data
        if self.left:
            t.left = self.left.build_subtree()
        if self.right:
            t.right = self.right.build_subtree()
        return t

    def scan_tree(self, count, second):  # note: count is a list, so it's passed "by reference"
        count[0] -= 1
        if count[0] <= 1:
            if not second:  # return subtree rooted here
                return self.build_subtree()
            else:  # glue subtree here
                self.data = second.data
                self.left = second.left
                self.right = second.right
        else:
            ret = None
            if self.left and count[0] > 1:
                ret = self.left.scan_tree(count, second)
            if self.right and count[0] > 1:
                ret = self.right.scan_tree(count, second)
            return ret

    def crossover(self, other):  # xo 2 trees at random nodes
        if random() < CROSS_RATE:
            second = other.scan_tree(
                [randint(1, other.size())], None)  # 2nd random subtree
            # 2nd subtree put inside 1st tree
            self.scan_tree([randint(1, self.size())], second)


def generate_dataset():  # generate 101 data points from target_func
    dataset = []
    for x in range(-100, 101, 2):
        x /= 100
        dataset.append([x, target_func(x)])
    return dataset


def init_population():  # half are full trees and half are tress that are able to grow
    pop = []
    for md in range(3, MAX_D + 1):
        for i in range(int(P_SIZE/6)):
            t = GPTree()
            t.random_tree(grow=True, max_depth=md)  # grow
            pop.append(t)
        for i in range(int(P_SIZE/6)):
            t = GPTree()
            t.random_tree(grow=False, max_depth=md)  # full
            pop.append(t)
    return pop


def fitness(individual, dataset):
    return 1 / (1 + mean([abs(individual.compute_tree(data[0]) - data[1]) for data in dataset]))


def selection(population, fitnesses):  # select one individual using tournament selection
    tournament = [randint(0, len(population)-1)
                  for i in range(T_SIZE)]  # select tournament contenders
    tournament_fitnesses = [fitnesses[tournament[i]] for i in range(T_SIZE)]
    return deepcopy(population[tournament[tournament_fitnesses.index(max(tournament_fitnesses))]])


def main():
    seed()  # init internal state of random number generator
    dataset = generate_dataset()
    population = init_population()
    best_of_run = None
    best_of_run_f = 0
    best_of_run_gen = 0
    fitnesses = [fitness(population[i], dataset) for i in range(P_SIZE)]

    # go evolution!
    for gen in range(GENS):
        nextgen_population = []
        for i in range(P_SIZE):
            parent1 = selection(population, fitnesses)
            parent2 = selection(population, fitnesses)
            parent1.crossover(parent2)
            parent1.mutation()
            nextgen_population.append(parent1)
        population = nextgen_population
        fitnesses = [fitness(population[i], dataset) for i in range(P_SIZE)]
        if max(fitnesses) > best_of_run_f:
            best_of_run_f = max(fitnesses)
            best_of_run_gen = gen
            best_of_run = deepcopy(population[fitnesses.index(max(fitnesses))])
            print("________________________")
            print("gen:", gen, ", best_of_run_f:", round(
                max(fitnesses), 3), ", best_of_run:")
            best_of_run.print_tree()
        if best_of_run_f == 1:
            break

    print("\n\n_________________________________________________\nEND OF RUN\nbest_of_run attained at gen " + str(best_of_run_gen) +
          " and has f=" + str(round(best_of_run_f, 3)))
    best_of_run.print_tree()


if __name__ == "__main__":
  main()
