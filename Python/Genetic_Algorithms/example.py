from ga_class import GeneticAlgorithm
import random
import time

def fitness_func(selected_individuals, data):
    weight = value = 0
    for amount, item in zip(selected_individuals, data):
        weight += amount*item['weight']
        value += amount*item['value']

    if weight > 15: value = 0
    return value

def create_individual(data):
    return [random.randint(0,int(15/data[i]['weight']))
                for i in range(len(data))]


# tipos de caixa
boxes=[ {'name': 'green',   'value': 4,  'weight': 12},
        {'name': 'blue',    'value': 2,  'weight': 2},
        {'name': 'brown',  'value': 1,  'weight': 1},
        {'name': 'yellow', 'value': 10, 'weight': 4},
        {'name': 'grey',   'value': 2,  'weight': 1}]

# instanciando o algoritmo genetico
ga = GeneticAlgorithm(boxes,
                      fitness_func,
                      population_size=70,
                      generations=200,
                      mutation_rate=0.3,
                      elitism=True,
                      maximise_fitness=True,
                      parent_selection_function="tournament",
                      create_individual_callback=create_individual,
                      show_best=False)

start = time.time()
# rodando o algoritmo
ga.run_evolution()
end = time.time()

print("runs in {} s".format(end-start))

# mostrando o resultado
best = ga.best
best = [best.fitness, best.genes]
peso = sum([qtt*item['weight'] for qtt, item in zip(best[1],boxes)])
print("="*70)
print("\n>>> Melhor resultado encontrado: valor: {} / peso: {}".format(best[0], peso))
for qtt, item in zip(best[1], boxes):
    if qtt > 0:
        print("\t- {}\n\t\t=> qtd: {}\n\t\t=> preco: {} ({}/u)\n\t\t=> peso: {} ({}/u)\n".format(
            item['name'],
            qtt,
            item['value']*qtt, item['value'],
            item['weight']*qtt, item['weight']))
print("="*70)
