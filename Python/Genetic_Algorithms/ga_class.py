from random import randint

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
                 create_individual_callback=None,
                 crossover_callback=None,
                 mutation_callback=None,
                 stop_callback=None
                 ):

        self.individual_concept = individual_concept
        self.mutation_rate = mutation_rate
        self.max_generations = generations
        self.population_size = population_size
        self.elitism = elitism
        self.maximise_fitness = maximise_fitness
        self.fitness = fitness_function
        self.create_individual = create_individual_callback if create_individual_callback else self.create_individual
        self.crossover = crossover_callback if crossover_callback else self.crossover
        self.mutation = mutation_callback if mutation_callback else self.mutation
        self.stop_evolution = stop_callback if stop_callback else self.stop_evolution

        self.population = []
        self.best = None
        self.generation = 0

        """

        Structure:

        Population
        #############################################################################
        #                                                                           #
        #   Chromossome                                                             #
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
        #   Chromossome                                                             #
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
            - individual_concept:   A single, or, sequence of values, strings etc. It represents the data to be optmized
            - mutation_rate:        Rate in which mutations occur
            - max_generations:      Max number of generations before the algorithm stops (only usefull if not using an external stop_evolution function
            - population_size:      Quantity of individuals per generation
            - elitism:              Decides if elitism (carry the best individual to the next generation) will occur
            - maximise_fitness:     If true, tries to maximize the result of the fitness function, otherwise tries to minimize
            - create_individual:    Function that quantify the the gene
            - fitness:              Function to evaluate how good is the chromosome
            - crossover:            Function to do the crossover (change parts of the chromossome within the population
            - mutation:             Function to mutate the genes in the chromossome with a certain chance
            - stop_evolution:       Function to set when to stop the evolution (std = stop with generations atribute)
            - population:           List containing all the population chromosomes
            - best:                 Best chromossome of the population
            - generation:           Current generation
        """

    def create_individual(self):
        return [Chromosome(randint(0,1)) for _ in self.individual_concept]

    def initialize_population(self):
        # create a initial population
        self.population = [self.create_individual() for _ in range(self.population_size)]

    def stop_evolution(self):
        # Must return a boolean
        return self.generation > self.max_generations

    def run_evolution(self):
        self.initialize_population()
        self.fitness_callback()
        while not self.stop_evolution():
            self.select()
            self.crossover()
            self.mutation()
            self.fitness()
        return
