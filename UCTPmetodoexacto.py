import pulp

# Conjuntos
courses = ['C1', 'C2']
professors = ['P1', 'P2']
rooms = ['R1', 'R2']
times = ['T1', 'T2']

# Parámetros
sizes = {'C1': 20, 'C2': 30}
capacities = {'R1': 25, 'R2': 40}
availability = {('C1', 'P1'): 1, ('C1', 'P2'): 1, ('C2', 'P1'): 1, ('C2', 'P2'): 0}

# Modelo
prob = pulp.LpProblem("Timetabling", pulp.LpMaximize)

# Variables
x = pulp.LpVariable.dicts("x", (courses, times, rooms, professors), cat='Binary')

# Función objetivo: Maximizar la utilización de salones
prob += pulp.lpSum(x[c][t][r][p] * (sizes[c] / capacities[r]) for c in courses for t in times for r in rooms for p in professors if (c, p) in availability)

# Restricciones

# 1. Cada curso se asigna exactamente una vez
for c in courses:
    prob += pulp.lpSum(x[c][t][r][p] for t in times for r in rooms for p in professors) == 1

# 2. Disponibilidad del profesor
for c in courses:
    for t in times:
        for r in rooms:
            for p in professors:
                if (c, p) in availability:
                    prob += x[c][t][r][p] <= availability[(c, p)]
                else:
                    prob += x[c][t][r][p] == 0

# 3. No solapamiento de profesores
for t in times:
    for p in professors:
        prob += pulp.lpSum(x[c][t][r][p] for c in courses for r in rooms) <= 1

# 4. No solapamiento de salones
for t in times:
    for r in rooms:
        prob += pulp.lpSum(x[c][t][r][p] for c in courses for p in professors) <= 1

# 5. Capacidad del salón
for t in times:
    for r in rooms:
        prob += pulp.lpSum(x[c][t][r][p] * sizes[c] for c in courses for p in professors) <= capacities[r]

# Resolver el problema (usando solver CBC, sin mensajes)
prob.solve(pulp.PULP_CBC_CMD(msg=0))

# Imprimir resultados
print("Status:", pulp.LpStatus[prob.status])
print("Objective value:", pulp.value(prob.objective))
for c in courses:
    for t in times:
        for r in rooms:
            for p in professors:
                if pulp.value(x[c][t][r][p]) == 1:
                    print(f"{c} assigned to {t}, {r}, {p}")