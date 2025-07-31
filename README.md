# University-Course-Timetabling-Problem

Repositorio que documenta el estudio del problema de planificación de horarios universitarios.

El archivo "UCTPmetodoexacto" tiene la solución del modelo general del problema con un solver.

# Modelo matemático general

A continuación, se proporciona un modelo matemático general para el problema de planificación de materias, profesores y salones en una universidad. El modelo se presenta como un problema de programación entera binaria (binary integer programming), que es una forma común de representar el University Course Timetabling Problem (UCTP) de manera formal. Este modelo es simplificado para enfocarse en las restricciones básicas: asignar cada curso a un profesor, un salón y un slot de tiempo, evitando solapamientos, y respetando capacidades. Se ignoran restricciones blandas complejas como preferencias para mantenerse general.

## Conjuntos y parámetros:

Definiendo los siguientes conjuntos, parámetros y variables de decisión:

**Conjuntos:**

* $C$: Conjunto de cursos (materias). Por ejemplo, $|C| = n$ cursos.

* $P$: Conjunto de profesores. Por ejemplo, $|P| = m$ profesores.

* $R$: Conjunto de salones. Por ejemplo, $|R| = k$ salones.

* $T$: Conjunto de slots de tiempo (horarios disponibles, e.g., lunes 8-10 AM, etc.). Por ejemplo, $|T| = l$ slots.

**Parámetros:**

* $S_c$: Tamaño del curso $c$ (número de estudiantes).

* $Cap_r$: Capacidad del salón $r$.

* $A_{c,p}$: Matriz de disponibilidad: 1 si el profesor $p$ puede enseñar el curso $c$, 0 en otro caso (para simplificar, asumimos que no todos los profesores pueden enseñar todos los cursos).

* $D_c$: Duración o requisitos del curso $c$ (asumimos que todos los cursos caben en un slot para simplicidad).

**Variables de decisión**

Se usan variables binarias para las asignaciones:

* $x_{c,t,r,p}$: 1 si el curso $c$ se asigna al slot de tiempo $t$, salón $r$ y profesor $p$; 0 en otro caso.

Entonces, el problema de planificación de horarios universitarios (UCTP) se puede modelar de la siguiente manera:


## Función objetivo:

Maximizar la utilización de salones:

$\max \sum_{c \in C} \sum_{t \in T} \sum_{r \in R} \sum_{p \in P} x_{c,t,r,p} \cdot \frac{S_c}{Cap_r}$

Esta función objetivo premia asignaciones donde el tamaño del curso se acerca a la capacidad del salón. Alternativamente, si se quieren minimizar violaciones, se pueden definir penalizaciones y minimizarlas.

## Restricciones

Las siguientes restricciones aseguran factibilidad:

1. **Cada curso se asigna exactamente una vez** (a un slot, salón y profesor):

$\sum_{t \in T} \sum_{r \in R} \sum_{p \in P} x_{c,t,r,p} = 1 \quad \forall c \in C$

2. **Disponibilidad del profesor:** Solo asignar si el profesor puede enseñar el curso:

$x_{c,t,r,p} \leq A_{c,p} \quad \forall c \in C, t \in T, r \in R, p \in P$

3. **No solapamiento de profesores:** Un profesor no puede estar en dos cursos al mismo tiempo:

$\sum_{c \in C} \sum_{r \in R} x_{c,t,r,p} \leq 1 \quad \forall t \in T, p \in P$

4. **No solapamiento de salones:** Un salón no puede usarse para dos cursos al mismo tiempo:

$\sum_{c \in C} \sum_{p \in P} x_{c,t,r,p} \leq 1 \quad \forall t \in T, r \in R$

5. **Capacidad del salón:** El tamaño del curso no excede la capacidad:

$\sum_{c \in C} \sum_{p \in P} x_{c,t,r,p} \cdot S_c \leq Cap_r \quad \forall t \in T, r \in R$

6. **Variables binarias:** Si el curso $c$ se imparte en el horario $t$ en el salón $r$ con el profesor $p$, entonces la variable toma valor de 1, el valor es 0 en caso contrario.

$x_{c,t,r,p} \in \{0,1\} \quad \forall c \in C, t \in T, r \in R, p \in P$
