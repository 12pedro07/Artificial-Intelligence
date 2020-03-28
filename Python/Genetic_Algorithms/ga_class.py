import random
import copy

class Chromosome():
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0

class GeneticAlgorithm:
    def __init__(self, individual_concept, fitness_function,
                 population_size=50,
                 generations=300,
                 mutation_rate=0.1,
                 elitism=True,
                 maximise_fitness=True,
                 parent_selection_function="tournament",
                 create_individual_callback=None,
                 mutation_callback=None,
                 stop_callback=None,
                 verbose=False,
                 show_best=True
                 ):

        # list
        self.individual_concept = individual_concept

        # numeric value
        self.mutation_rate = mutation_rate
        self.max_generations = generations
        self.population_size = population_size

        # boolean
        self.elitism = elitism
        self.maximise_fitness = maximise_fitness
        self.verbose = verbose
        self.show_best = show_best

        # string
        self.__available_selections = {
            "random":        self.random_selection,
            "tournament":    self.tournament_selection,
            "roulette":      self.roulette_selection
        }

        self.select_parents = self.__available_selections[parent_selection_function]

        # callbacks
        self.fitness = fitness_function
        self.create_individual = create_individual_callback if create_individual_callback else self.create_individual
        self.mutate = mutation_callback if mutation_callback else self.mutate
        self.stop_evolution = stop_callback if stop_callback else self.stop_evolution

        # internal only atributes
        self.population = []
        self.next_gen = []
        self.next_gen_parents = []
        self.best = Chromosome([0 for _ in range(len(individual_concept))])
        self.generation = 0

        """

        Structure:

        Population
        #############################################################################
        #                                                                           #
        #   Chromosome                                                              #
        #   &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&   #
        #   &                                                                   &   #
        #   &    individual    individual_concept (immutable)                   &   #
        #   &    -----------   <><><><><><><><><><><><><><><><><><><><><><><>   &   #
        #   &    -         -   <>                                          <>   &   #
        #   &    - Gene    -   <>  [                                       <>   &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @  1    -   <>    {"Name": "Greg",       "Value": "5",  <> @ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    -         -   <>                                          <>   &   #
        #   &    - Gene    -   <>                                          <>   &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @  0    -   <>    {"Name": "Pedro",      "Value": "3",  <> @ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    -         -   <>                                          <>   &   #
        #   &    - Gene    -   <>                                          <>   &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @  0    -   <>    {"Name": "Jeff",       "Value": "2",  <> @ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    -         -   <>                                          <>   &   #
        #   &    - Gene    -   <>                                          <>   &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @  1    -   <>    {"Name": "Amanda",     "Value": "10", <> @ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    -         -   <>                                          <>   &   #
        #   &    -----------   <><><><><><><><><><><><><><><><><><><><><><><>   &   #
        #   &                                                                   &   #
        #   &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&   #
        #                                                                           #
        #                                                                           #
        #                                                                           #
        #   Chromosome                                                              #
        #   &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&   #
        #   &                                                                   &   #
        #   &    individual    individual_concept (immutable)                   &   #
        #   &    -----------   <><><><><><><><><><><><><><><><><><><><><><><>   &   #
        #   &    -         -   <>                                          <>   &   #
        #   &    - Gene    -   <>  [                                       <>   &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @  1    -   <>    {"Name": "Greg",       "Value": "5",  <> @ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    -         -   <>                                          <>   &   #
        #   &    - Gene    -   <>                                          <>   &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @  0    -   <>    {"Name": "Pedro",      "Value": "3",  <> @ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    -         -   <>                                          <>   &   #
        #   &    - Gene    -   <>                                          <>   &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @  0    -   <>    {"Name": "Jeff",       "Value": "2",  <> @ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    -         -   <>                                          <>   &   #
        #   &    - Gene    -   <>                                          <>   &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @  1    -   <>    {"Name": "Amanda",     "Value": "10"  <> @ &   #
        #   &    - @       -   <>                                          <> @ &   #
        #   &    - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ &   #
        #   &    -         -   <>                                          <>   &   #
        #   &    -         -   <>  ]                                       <>   &   #
        #   &    -----------   <><><><><><><><><><><><><><><><><><><><><><><>   &   #
        #   &                                                                   &   #
        #   &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&   #
        #                                                                           #
        #                                                                           #
        #                                   *****                                   #
        #                                   ** **                                   #
        #                                   *****                                   #
        #                                                                           #
        #                                   *****                                   #
        #                                   ** **                                   #
        #                                   *****                                   #
        #                                                                           #
        #                                   *****                                   #
        #                                   ** **                                   #
        #                                   *****                                   #
        #                                                                           #
        #                                                                           #
        #############################################################################

        Atribute definitions:

                >> Lists <<
            - individual_concept:   List containing a single, or, sequence of values, strings etc. It represents the data to be optmized
            - population:           List containing all the population chromosomes
            - next_gen:             Helps controlling the data flow in the evolution
            - next_gen_parents:     Helps controlling the data flow in the evolution

                >> Numerical <<
            - mutation_rate:        Rate in which mutations occur
            - max_generations:      Max number of generations before the algorithm stops (only usefull if not using an external stop_evolution function
            - population_size:      Quantity of individuals per generation
            - generation:           Current generation

                >> Boolean <<
            - elitism:              Decides if elitism (carry the best individual to the next generation) will occur
            - maximise_fitness:     If true, tries to maximize the result of the fitness function, otherwise tries to minimize

                >> Functions <<
            - create_individual:
                |- Definition: Function that quantify the the gene (standard is binary)
                |- Input: None
                |- Output: List with the same length as the individual_concept
            - fitness:
                |- Definition: Function to evaluate how good is the chromosome
                |- Input: gene of the chromosome / chromosome concept
                |- Output: fitness value for the chromosome
            - select_parents:
                |- Definition: Function to do the crossoveri, called until a new population is formed (select 2 parents from the population)
                |- Input: list with ____ (population)
                |- Output: 2 new child chromosomes
            - mutate:
                |- Definition: Called when a gene must be mutated (obligatory to define when using a non binary individual)
                |- Input: chromosome gene
                |- Output: Mutated gene
            - stop_evolution:
                |- Definition: Called once per generation
                |- Input: Best fit value
                |- Output: True to stop the evolution

                >> Object <<
            - best:                 Best chromosome of the population
        """

    ##### RUN SIMULATION #####

    def run_evolution(self):
        evolution = [self.select, self.crossover, self.mutation, self.fitness_population]
        self.initialize_population()
        self.fitness_population()
        self.update_best()
        while not self.stop_evolution(self.best.fitness):
            # start cleaning
            self.next_gen_parents = []
            self.next_gen = []

            # log
            if self.verbose or self.show_best:
                print("="*50)
                print("GENERATION {}".format(self.generation))
            if self.verbose:
                print("population: {}".format([chromo.genes for chromo in self.population]))

            for step in evolution:
                if self.verbose: print("-"*50)
                step()

            # updates
            #if self.elitism:
            #    self.population[-1] = self.best_backup
            self.update_best()
            self.generation+=1
            self.population=self.next_gen.copy()

            if self.verbose or self.show_best:
                print("generation best: {} - {}".format(self.best.genes, self.best.fitness))

        return
    ##### FITNESS #####

    def fitness_population(self):
        for chromosome in self.population:
            chromosome.fitness = self.fitness(chromosome.genes, self.individual_concept)
        return

    ##### SELECTION #####

    def select(self):
        while len(self.next_gen_parents) < len(self.population):
            self.next_gen_parents.append(self.select_parents())

        if self.verbose:print("selected parents: {}".format([[[p1.genes,"fitness: {}".format(p1.fitness)], [p2.genes, "fitness: {}".format(p2.fitness)]] for p1,p2 in self.next_gen_parents]))
        return


    ##### PARENT SELECTION METHODS #####

    def random_selection(self):
        return (random.choice(self.population), random.choice(self.population))

    def roulette_selection(self):
        parents = []
        # then we compute a cumulative list for the fitness values
        cumulative_fitness = []
        before = 0
        for chromosome in self.population:
            cumulative_fitness.append(chromosome.fitness+before)
            before = chromosome.fitness
        while len(parents) < 2:
            # draw a value from 0 to the maximum accumulated value
            random_value = random.random()*cumulative_fitness[-1]
            idx = 0
            # find the corresponding value in the vector
            while random_value > 0:
                idx+=1
                random_value -= cumulative_fitness[idx]
            # append to the next gen the selected chromosome
            parents.append(self.population[idx])
        return tuple(parents)

    def tournament_selection(self):
        parents = []
        for i in range(2):
            sample_rate = 1 if len(self.population) < 2 else 2 if len(self.population) < 5 else int(0.2*len(self.population))
            sample = random.sample(self.population, sample_rate)
            sample.sort(key=lambda chromosome: chromosome.fitness, reverse=self.maximise_fitness)
            parents.append(sample[0])
        return tuple(parents)

    ##### CROSSOVER #####

    def crossover(self):
        for p1, p2 in self.next_gen_parents:
            if self.verbose:print("crossing {} and {}".format(p1.genes, p2.genes))
            # select a crossover point
            cut_point = random.randint(0, len(self.individual_concept))
            # do the crossover
            if random.randint(0,1):
                son = p1.genes[:cut_point] + p2.genes[cut_point:]
            else:
                son = p1.genes[cut_point:] + p2.genes[:cut_point]
            # append on the next gen
            self.next_gen.append(Chromosome(son))
            if self.verbose:
                print("cut point: {}".format(cut_point))
                print("son: {}".format(son))
                print()
        self.population = copy.deepcopy(self.next_gen)
        return

    ##### MUTATION #####

    def mutation(self):
        for chromosome in self.population:
            chromosome.genes = self.mutate(chromosome.genes, self.mutation_rate)

    def mutate(self, genes, mutation_rate):
        # flip bit function
        flip = lambda bit: '0' if bit=='1' else '1'

        mutated_genes = []

        for idx, gene in enumerate(genes):
            integer = int(gene)
            # if is float, add a decimal control
            decimal = int((gene%1)*1000) if gene == float else 0 # 3 decimal precision
            # convert to binary
            integer = bin(integer)
            decimal = bin(decimal)
            # flip the bits at random with a mutation_rate chance
            integer = '0b'+"".join([flip(bit) if random.random()<mutation_rate else bit for bit in integer[2:]])
            new_gene = int(integer,2)
            # flip the decimals if there are any
            if decimal[2:] != '0':
                decimal = '0b'+"".join([flip(bit) if random.random()<mutation_rate else bit for bit in decimal[2:]])
                new_gene = (new_gene*1000 + int(decimal,2))/1000
            # append gene to the new genes
            mutated_genes.append(new_gene)

        if self.verbose:print("mutating: {} -> {}".format(genes,mutated_genes))
        return mutated_genes

    ##### INITIALIZATIONS #####

    def initialize_population(self):
        # create a initial population
        self.population = [Chromosome(self.create_individual(self.individual_concept)) for _ in range(self.population_size)]
        self.update_best()
        self.sort_population()
        return

    ##### CREATION #####

    def create_individual(self, individual_concept):
        return [random.randint(0,1) for _ in individual_concept]

    ##### AUXILIAR METHODS #####

    def sort_population(self):
        self.population.sort(key=lambda chromosome: chromosome.fitness, reverse=self.maximise_fitness)
        return

    def stop_evolution(self, best_fit):
        # best fit not used in standard definition
        return self.generation > self.max_generations

    def update_best(self):
        # backup the best
        self.best_backup = copy.deepcopy(self.best)
        self.population[-1] = self.best_backup
        # sort the population by fitness
        self.sort_population()
        # update the new best
        self.best = self.population[0]
        return

    ##############################






