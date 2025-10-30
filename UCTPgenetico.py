import random
from deap import base, creator, tools, algorithms  # Agregado 'algorithms' aquí

# Conjuntos y parámetros
courses = ['C1', 'C2']
professors = ['P1', 'P2']
rooms = ['R1', 'R2']
times = ['T1', 'T2']

sizes = {'C1': 20, 'C2': 30}
capacities = {'R1': 25, 'R2': 40}
availability = {('C1', 'P1'): 1, ('C1', 'P2'): 1, ('C2', 'P1'): 1, ('C2', 'P2'): 0}

# Mapeo para codificar: índices para time, room, prof
time_idx = {t: i for i, t in enumerate(times)}
room_idx = {r: i for i, r in enumerate(rooms)}
prof_idx = {p: i for i, p in enumerate(professors)}

# Representación: para cada curso, (time_idx, room_idx, prof_idx)
# Individuo: lista de 6 enteros [t1, r1, p1, t2, r2, p2]

def decode_individual(ind):
    ass1 = (times[ind[0]], rooms[ind[1]], professors[ind[2]])
    ass2 = (times[ind[3]], rooms[ind[4]], professors[ind[5]])
    return {'C1': ass1, 'C2': ass2}

def evaluate(individual):
    assignments = decode_individual(individual)
    penalty = 0
    fitness = 0

    # Verificar disponibilidad
    for c in courses:
        t, r, p = assignments[c]
        if availability.get((c, p), 0) == 0:
            penalty += 100

    # Verificar capacidad
    for c in courses:
        t, r, p = assignments[c]
        if sizes[c] > capacities[r]:
            penalty += 100

    # Verificar no solapamiento profesores y salones
    prof_used = {}
    room_used = {}
    for c in courses:
        t, r, p = assignments[c]
        if (t, p) in prof_used:
            penalty += 100
        prof_used[(t, p)] = True
        if (t, r) in room_used:
            penalty += 100
        room_used[(t, r)] = True

    # Fitness si no hay penalizaciones
    if penalty == 0:
        for c in courses:
            t, r, p = assignments[c]
            fitness += sizes[c] / capacities[r]

    return fitness - penalty,

# Configuración DEAP
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_int", random.randint, 0, 1)  # 0-1 para 2 opciones cada uno
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=6)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Ejecución
pop = toolbox.population(n=50)
hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("max", max)

algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, stats=stats, halloffame=hof, verbose=False)  # Cambiado a 'algorithms.eaSimple'

best = hof[0]
print("Mejor individuo:", best)
print("Asignaciones:", decode_individual(best))
print("Fitness:", evaluate(best)[0])
print("Prueba de cambio")
