import numpy as np
import pandas as pd
import random as rd
from random import randint
import matplotlib.pyplot as plt


# Initializing the list of items, we have 10 items
item_number = np.arange(1, 11)
weight = np.random.randint(1, 15, size=10)
cost = np.random.randint(10, 750, size=10)
knapsack_limit = 35  # Maximum weight of the bag
print('The Items:')
print('Number   Weight   Cost')
for i in range(item_number.shape[0]):
    print(f"{item_number[i]}          {weight[i]}         {cost[i]}\n")


# Initial Population
# Each gene has a cost 1 or 0 which tells whether the corresponding item is present or not
solutionsPopulation = 8
populationSize = (solutionsPopulation, item_number.shape[0])
print(f"Population size = {populationSize}")
initial_population = np.random.randint(2, size=populationSize)
initial_population = initial_population.astype(int)
numberOfGenerations = 50
print(f"Initial population: \n{initial_population}")


# The fitness function, limit = knapsack weight
def fitnessFunction(weight, cost, population, limit):
    fitness = np.empty(population.shape[0])
    for i in range(population.shape[0]):
        # Calculate cost of chromosome
        sigma_1 = np.sum(population[i] * cost)
        sigma_2 = np.sum(population[i] * weight)
        if sigma_2 <= limit:
            fitness[i] = sigma_1
        else:
            fitness[i] = 0
    return fitness.astype(int)


# Now we select the fittest individuals so that they can undergo crossover
def selection(fitness, num_parents, population):
    fitness = list(fitness)
    parents = np.empty((num_parents, population.shape[1]))
    for i in range(num_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        parents[i, :] = population[max_fitness_idx[0][0], :]
        fitness[max_fitness_idx[0][0]] = -999999
    return parents


# For crossover we will be using one-point crossover: two individuals create two offsprings.
def crossover(parents, num_offsprings):
    offsprings = np.empty((num_offsprings, parents.shape[1]))
    crossover_point = int(parents.shape[1]/2)
    crossover_rate = 0.8
    i = 0
    while (parents.shape[0] < num_offsprings):
        parent1_index = i % parents.shape[0]
        parent2_index = (i+1) % parents.shape[0]
        crossover_chance = rd.random()
        if crossover_chance > crossover_rate:
            continue
        parent1_index = i % parents.shape[0]
        parent2_index = (i+1) % parents.shape[0]
        offsprings[i, 0:crossover_point] = parents[parent1_index,
                                                   0: crossover_point]
        offsprings[i, crossover_point:] = parents[parent2_index,
                                                  crossover_point:]
        i = +1
    return offsprings


# In Mutation, which chromosome will undergo mutation is being done randomly.
# if the selected gene which is going to undergo mutation is 1 then change it to 0 and vice-versa.
def mutation(offsprings):
    mutants = np.empty((offsprings.shape))
    mutation_rate = 0.4
    for i in range(mutants.shape[0]):
        random_value = rd.random()
        mutants[i, :] = offsprings[i, :]
        if random_value > mutation_rate:
            continue
        int_random_value = randint(0, offsprings.shape[1]-1)
        if mutants[i, int_random_value] == 0:
            mutants[i, int_random_value] = 1
        else:
            mutants[i, int_random_value] = 0
    return mutants


# now we will call them in the order of the flow chart to find the required parameters
# and make all the necessary initializations.
def optimization(weight, cost, population, populationSize, numberOfGenerations, limit):
    parameters = []
    num_parents = int(populationSize[0]/2)
    num_offsprings = populationSize[0] - num_parents
    for i in range(numberOfGenerations):
        fitness = fitnessFunction(weight, cost, population, limit)
        parents = selection(fitness, num_parents, population)
        offsprings = crossover(parents, num_offsprings)
        mutants = mutation(offsprings)
        population[0:parents.shape[0], :] = parents
        population[parents.shape[0]:, :] = mutants

    print('Last generation: \n{population}\n')
    fitness_last_gen = fitnessFunction(weight, cost, population, limit)
    print("Fitness of the last generation: \n{fitness_last_gen}\n")
    max_fitness = np.where(fitness_last_gen == np.max(fitness_last_gen))
    parameters.append(population[max_fitness[0][0], :])
    return parameters


parameters = optimization(
    weight, cost, initial_population, populationSize, numberOfGenerations, knapsack_limit)

print(f"The optimized parameters: \n{parameters}")
selected_items = item_number * parameters
print("\nSelected items for this problem: ")
for i in range(selected_items.shape[1]):
    if selected_items[0][i] != 0:
        print(selected_items[0][i])
