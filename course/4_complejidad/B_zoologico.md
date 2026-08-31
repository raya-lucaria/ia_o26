---
id: zoologico-de-problemas
title: El zoológico de problemas
nav_title: Zoológico
summary: Cada problema que aparece en la unidad, su enunciado en una línea, la clase a la que pertenece y dónde se presentó.
status: ready
estimated_time: 5m
tags: [complejidad, referencia, problemas]
---

# El zoológico de problemas

Los problemas de la unidad, todos en un lugar. Sirve para dos cosas: repasar
antes del examen, y comprobar si sabes ubicar un problema sin mirar.

**Cómo leer la columna «Clase».** Dice lo mejor que se sabe hoy, no lo que es.
«En $NP$» significa que está en $NP$ y que nadie ha probado que esté en $P$ ni
que sea NP-completo.

## En P — se resuelven de verdad

| Problema | La pregunta | Con qué | Se presenta en |
|---|---|---|---|
| **Búsqueda lineal** | ¿está $x$ en la lista? | recorrer, $\Theta(n)$ | [[contar-un-algoritmo|Contar un algoritmo]] |
| **Búsqueda binaria** | ídem, lista ordenada | partir a la mitad, $\Theta(\log n)$ | [[contar-un-algoritmo|Contar un algoritmo]] |
| **Ordenar** | — | *mergesort*, $\Theta(n\log n)$ | [[contar-un-algoritmo|Contar un algoritmo]] |
| **Multiplicar matrices** | $C = A\cdot B$ | tres ciclos, $\Theta(n^3)$; Strassen, $O(n^{2{,}807})$ | [[contar-un-algoritmo|Contar un algoritmo]] |
| **Caminos mínimos** | ¿el camino más barato de $s$ a $t$? | Dijkstra, $O(m + n\log n)$ | [[las-clases|P, NP y EXP]] |
| **Árbol generador mínimo** | ¿cómo conecto todo al menor costo? | Kruskal o Prim, $O(m\log n)$ | [[las-clases|P, NP y EXP]] |
| **Emparejamiento bipartito** | ¿puedo asignar todas las tareas? | Hopcroft-Karp, $O(m\sqrt{n})$ | [[las-clases|P, NP y EXP]] |
| **Flujo máximo** | ¿cuánto pasa por la red? | Edmonds-Karp, $O(nm^2)$ | [[las-clases|P, NP y EXP]] |
| **2-SAT** | ¿satisfacible, 2 literales por cláusula? | componentes fuertemente conexas, $O(n+m)$ | [[completos-y-duros|Reducciones, duros y completos]] |
| **Programación lineal** | optimizar lineal con restricciones lineales | elipsoide (1979). **El simplex es exponencial en el peor caso** | [[las-clases|P, NP y EXP]] |
| **Primalidad** | ¿es $N$ primo? | AKS (2002). En la práctica, Miller-Rabin | [[azar-y-bpp|Máquinas que tiran monedas]] |
| **Conectividad en grafos** | ¿hay camino de $s$ a $t$? | está incluso en $L$ (Reingold, 2004) | [[complejidad-de-espacio|Contar memoria]] |

## NP-completos — todos el mismo problema

| Problema | La pregunta | Certificado | Se presenta en |
|---|---|---|---|
| **SAT** | ¿es satisfacible esta fórmula booleana? | la asignación | [[completos-y-duros|Reducciones, duros y completos]] |
| **3-SAT** | ídem, exactamente 3 literales por cláusula | la asignación | [[completos-y-duros|Reducciones, duros y completos]] |
| **Ciclo hamiltoniano** | ¿hay un ciclo que pase por cada vértice una vez? | el ciclo | [[las-clases|P, NP y EXP]] |
| **TSP (decisión)** | ¿hay un tour de costo $\le k$? | el tour | [[por-que-importa|Por qué esto importa]] |
| **Clique** | ¿hay $k$ vértices todos conectados entre sí? | los vértices | [[las-clases|P, NP y EXP]] |
| **Cubierta de vértices** | ¿hay $k$ vértices que toquen todas las aristas? | los vértices | [[completos-y-duros|Reducciones, duros y completos]] |
| **Coloreo con 3 colores** | ¿se puede colorear sin vecinos iguales? | el coloreo | [[completos-y-duros|Reducciones, duros y completos]] |
| **Suma de subconjuntos** | ¿hay un subconjunto que sume exactamente $S$? | el subconjunto | [[completos-y-duros|Reducciones, duros y completos]] |
| **Mochila** | ¿hay un subconjunto de valor $\ge V$ y peso $\le W$? | el subconjunto | [[completos-y-duros|Reducciones, duros y completos]] |

## En NP, y en tierra de nadie

| Problema | La pregunta | Estado | Se presenta en |
|---|---|---|---|
| **Factorización** | ¿tiene $N$ un factor menor que $k$? | en $NP$; no se sabe si en $P$ ni si NP-completo. Toda la criptografía de clave pública descansa en que sea difícil | [[las-clases|P, NP y EXP]] |
| **Isomorfismo de grafos** | ¿son el mismo grafo con otros nombres? | en $NP$; casi polinomial (Babai, 2015). El candidato clásico al [[el-mapa-de-las-clases|teorema de Ladner]] | [[el-mapa-de-las-clases|El mapa completo]] |

## Con azar

| Problema | La pregunta | Clase | Se presenta en |
|---|---|---|---|
| **Primalidad (Miller-Rabin)** | ¿es $N$ primo? | $coRP \subseteq BPP$; y desde 2002 también en $P$ | [[azar-y-bpp|Máquinas que tiran monedas]] |
| **Identidad de polinomios** | ¿son el mismo polinomio? | $coRP$. **No se conoce algoritmo determinista polinomial** | [[azar-y-bpp|Máquinas que tiran monedas]] |
| **Corte mínimo (Karger)** | ¿cuál es el corte más chico del grafo? | Monte Carlo, y también hay algoritmos deterministas polinomiales | [[azar-y-bpp|Máquinas que tiran monedas]] |

## Más arriba

| Problema | La pregunta | Clase | Se presenta en |
|---|---|---|---|
| **Fórmula booleana cuantificada** | ¿es cierta $\forall x \exists y \dots$? | PSPACE-completo | [[complejidad-de-espacio|Contar memoria]] |
| **Hex generalizado** | ¿gana el que sale, en tablero $n\times n$? | PSPACE-completo | [[complejidad-de-espacio|Contar memoria]] |
| **Ajedrez generalizado** | ¿gana el que sale, en tablero $n\times n$, sin la regla de las 50 jugadas? | EXP-completo: **demostradamente fuera de $P$** | [[las-clases|P, NP y EXP]] |
| **Problema de la parada** | ¿se detiene esta máquina? | **indecidible**, y NP-duro sin ser NP-completo | [[completos-y-duros|Reducciones, duros y completos]] |

## Tres casos que enseñan algo

**Programación lineal** enseña que la clase es del **problema**, no de tu
algoritmo: está en $P$, y el método que todo el mundo usa —el simplex— es
exponencial en el peor caso.

**Primalidad** enseña que estas clasificaciones son sobre lo que **sabemos**:
vivió treinta años como ejemplo de «esto solo se puede con azar» y en 2002 se
mudó a $P$.

**El problema de la parada** enseña la diferencia entre duro y completo: es
NP-duro y no es NP-completo, porque ni siquiera está en $NP$ — no está en
ninguna clase de esta unidad, porque no tiene algoritmo en absoluto.
