---
id: notacion-complejidad
title: Toda la notación, en una hoja
nav_title: Notación
summary: Cada símbolo que usa la unidad, cómo se lee, qué significa y en qué página se presentó.
status: ready
estimated_time: 5m
tags: [complejidad, referencia, notacion]
---

# Toda la notación, en una hoja

Están todos definidos en su página. Si te encuentras uno a media lectura y no
recuerdas de dónde salió, búscalo aquí en vez de retroceder.

**Cómo leer la última columna:** dice dónde se **presentó** el símbolo. Si algo
te resulta opaco, ése es el lugar al que volver.

## Medir

| Símbolo | Se lee | Qué es | Se presenta en |
|---|---|---|---|
| $n$ | «ene» | El **tamaño de la entrada**: cuántos símbolos hacen falta para escribirla | [[cuanto-cuesta|Cuánto cuesta un algoritmo]] |
| $m$ | «eme» | En grafos, la cantidad de **aristas**. Un grafo mide dos números, $n$ y $m$ | [[cuanto-cuesta|Cuánto cuesta un algoritmo]] |
| $N$ | «ene mayúscula» | Un **entero de entrada**. Ojo: su tamaño es $n \approx \log N$, no $N$ | [[cuanto-cuesta|Cuánto cuesta un algoritmo]] |
| $T(n)$ | «te de ene» | Los pasos que tarda el algoritmo con la peor entrada de tamaño $n$ | [[cuanto-cuesta|Cuánto cuesta un algoritmo]] |

## Notación asintótica

| Símbolo | Se lee | Qué es | Se presenta en |
|---|---|---|---|
| $O(g)$ | «o grande de ge» | **Techo**: $f \le c\,g$ desde algún $n_0$. Equivale a $\limsup f/g < \infty$ | [[o-grande|O grande, y su familia]] |
| $\Omega(g)$ | «omega de ge» | **Piso**: $f \ge c\,g$ desde algún $n_0$. Equivale a $\liminf f/g > 0$ | [[o-grande|O grande, y su familia]] |
| $\Theta(g)$ | «theta de ge» | **Las dos**: $O$ y $\Omega$ a la vez. Crece exactamente como $g$ | [[o-grande|O grande, y su familia]] |
| $o(g)$ | «o pequeña de ge» | Techo **estricto**: $\lim f/g = 0$. Crece estrictamente menos | [[o-grande|O grande, y su familia]] |
| $c$ | «ce» | La **constante** de la definición de $O$: existe alguna que sirve | [[o-grande|O grande, y su familia]] |
| $n_0$ | «ene sub cero» | El punto **desde el cual** la cota vale. Antes de él no promete nada | [[o-grande|O grande, y su familia]] |
| $f \prec g$ | «efe crece menos que ge» | Abreviatura de $f = o(g)$, para escribir la jerarquía en una línea | [[o-grande|O grande, y su familia]] |
| $\log n$ | «logaritmo de ene» | Sin base, porque la base solo cambia una constante | [[o-grande|O grande, y su familia]] |

## Clases

| Símbolo | Se lee | Qué es | Se presenta en |
|---|---|---|---|
| $P$ | «pe» | Resoluble por máquina **determinista** en tiempo polinomial | [[las-clases|P, NP y EXP]] |
| $NP$ | «ene pe» | Resoluble por máquina **no determinista** en tiempo polinomial. Equivalente: **verificable** en polinomial. **No** es «no polinomial» | [[las-clases|P, NP y EXP]] |
| $EXP$ | «exp» | Resoluble en tiempo $2^{n^k}$ | [[las-clases|P, NP y EXP]] |
| $BPP$ | «be pe pe» | Resoluble con **azar** en tiempo polinomial, con error acotado $\le 1/3$ | [[azar-y-bpp|Máquinas que tiran monedas]] |
| $RP$, $coRP$ | «erre pe» | Como $BPP$, pero con error de **un solo lado** | [[azar-y-bpp|Máquinas que tiran monedas]] |
| $L$ | «ele» | Decidible con memoria $O(\log n)$, con la entrada de solo lectura | [[complejidad-de-espacio|Contar memoria]] |
| $PSPACE$ | «pe space» | Decidible con memoria polinomial, sin límite de tiempo | [[complejidad-de-espacio|Contar memoria]] |

## Comparar problemas

| Símbolo | Se lee | Qué es | Se presenta en |
|---|---|---|---|
| $A \le_p B$ | «a se reduce a be» | Existe $f$ polinomial con $w \in A \iff f(w) \in B$. Significa que **$B$ es al menos tan difícil como $A$** | [[completos-y-duros|Reducciones, duros y completos]] |
| **NP-duro** | — | Todo problema de $NP$ se le reduce. **Puede estar fuera de $NP$** | [[completos-y-duros|Reducciones, duros y completos]] |
| **NP-completo** | — | NP-duro **y** además está en $NP$ | [[completos-y-duros|Reducciones, duros y completos]] |
| $c$ (certificado) | — | La prueba corta que el verificador revisa. De tamaño polinomial | [[las-clases|P, NP y EXP]] |

## Miller-Rabin

| Símbolo | Se lee | Qué es | Se presenta en |
|---|---|---|---|
| $a^{p-1} \equiv 1 \pmod p$ | — | El **pequeño teorema de Fermat**, para $p$ primo y $a$ no múltiplo de $p$ | [[azar-y-bpp|Máquinas que tiran monedas]] |
| $N - 1 = 2^s d$ | — | La descomposición de partida, con $d$ **impar** | [[azar-y-bpp|Máquinas que tiran monedas]] |
| $s$, $d$ | «ese, de» | Cuántas veces se eleva al cuadrado, y desde qué exponente impar se arranca | [[azar-y-bpp|Máquinas que tiran monedas]] |
| **testigo** | — | Una base $a$ que demuestra que $N$ es compuesto | [[azar-y-bpp|Máquinas que tiran monedas]] |
| $4^{-k}$ | — | La probabilidad de error tras $k$ rondas independientes | [[azar-y-bpp|Máquinas que tiran monedas]] |

## Parejas que se confunden

Ésta es la tabla que conviene mirar antes del examen.

| No es lo mismo | que | La diferencia |
|---|---|---|
| **indecidible** | **intratable** | Lo primero es que no existe algoritmo; lo segundo, que existe y no cabe en tu vida |
| $O$ | $\Theta$ | $O$ es un techo; $\Theta$ es techo y piso. Un algoritmo lineal es $O(n^2)$, y es verdad |
| **NP** | **no polinomial** | $NP$ es *nondeterministic polynomial*, y $P \subseteq NP$: ordenar también es NP |
| **NP-duro** | **NP-completo** | Completo = duro **y** en $NP$. El problema de la parada es duro y no completo |
| **no determinista** | **aleatorio** | La primera explora todas las ramas; la segunda tira una moneda. Son $NP$ y $BPP$ |
| **decisión** | **optimización** | «¿hay tour $\le k$?» es NP-completo; «¿cuál es el mejor?» es NP-duro |
| el tamaño de $N$ | el valor de $N$ | El tamaño es $\log N$. Confundirlos es la complejidad pseudopolinomial |
| **Monte Carlo** | **Las Vegas** | Monte Carlo arriesga la respuesta; Las Vegas arriesga el tiempo |
