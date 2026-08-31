---
id: notacion-computabilidad
title: Toda la notación, en una hoja
nav_title: Notación
summary: Cada símbolo que usa la unidad, cómo se lee, qué significa y en qué página se presentó.
status: ready
estimated_time: 5m
tags: [computabilidad, referencia, notacion]
---

# Toda la notación, en una hoja

Esta unidad introduce cerca de treinta símbolos. Están todos definidos en su
página, pero si te encuentras uno a media lectura y no recuerdas de dónde salió,
búscalo aquí en vez de retroceder.

**Cómo leer la última columna:** dice dónde se **presentó** el símbolo. Si algo
te resulta opaco, ése es el lugar al que volver.

## Cadenas y lenguajes

| Símbolo | Se lee | Qué es | Se presenta en |
|---|---|---|---|
| $\Sigma$ | «sigma» | Un **alfabeto**: conjunto finito y no vacío de símbolos | [[que-es-el-computo|Qué es el cómputo]] |
| $\varepsilon$ | «épsilon» | La **cadena vacía**: cero símbolos. No es «nada» ni el conjunto vacío | [[que-es-el-computo|Qué es el cómputo]] |
| $\lvert w\rvert$ | «longitud de doble u» | Cuántos símbolos tiene la cadena $w$ | [[que-es-el-computo|Qué es el cómputo]] |
| $\Sigma^*$ | «sigma estrella» | **Todas** las cadenas finitas sobre $\Sigma$, $\varepsilon$ incluida. El `*` es la *estrella de Kleene*, no multiplica | [[que-es-el-computo|Qué es el cómputo]] |
| $L \subseteq \Sigma^*$ | «ele contenido en sigma estrella» | Un **lenguaje**: cualquier subconjunto de $\Sigma^*$ | [[que-es-el-computo|Qué es el cómputo]] |
| $0^n1^n$ | «cero a la ene, uno a la ene» | **Repetición**, no potencia: $0^31^3 = 000111$ | [[que-es-el-computo|Qué es el cómputo]] |
| $\mathbb{N}$ | «los naturales» | $\{0, 1, 2, \dots\}$ — **con el cero**, en toda la unidad | [[que-es-el-computo|Qué es el cómputo]] |

## La máquina

| Símbolo | Se lee | Qué es | Se presenta en |
|---|---|---|---|
| $M$ | «eme» | Una máquina de Turing | [[maquina-de-turing|La máquina de Turing]] |
| $Q$ | «cu» | Su conjunto **finito** de estados | [[maquina-de-turing|La máquina de Turing]] |
| $\Gamma$ | «gamma» | El alfabeto de **cinta**: incluye a $\Sigma$ y al blanco | [[maquina-de-turing|La máquina de Turing]] |
| $\sqcup$ | «blanco» | El símbolo de casilla vacía. No está en $\Sigma$ | [[maquina-de-turing|La máquina de Turing]] |
| $\delta$ | «delta» | La **función de transición**: la tabla de reglas | [[maquina-de-turing|La máquina de Turing]] |
| $q_0$, $q_{\text{acc}}$, $q_{\text{rej}}$ | «cu cero, cu acc, cu rej» | Estado inicial, de aceptación y de rechazo | [[maquina-de-turing|La máquina de Turing]] |
| $\leftarrow$, $\rightarrow$ | «izquierda, derecha» | Hacia dónde se mueve el cabezal | [[maquina-de-turing|La máquina de Turing]] |
| $u\,q\,v$ | — | Una **configuración**: el estado va escrito justo antes del símbolo que se está leyendo | [[maquina-de-turing|La máquina de Turing]] |
| $L(M)$ | «ele de eme» | El conjunto de cadenas que $M$ **acepta** | [[maquina-de-turing|La máquina de Turing]] |

## Computabilidad

| Símbolo | Se lee | Qué es | Se presenta en |
|---|---|---|---|
| $\chi_L$ | «ji sub ele» | La **función característica** de $L$: $1$ dentro, $0$ fuera | [[computabilidad-y-decidibilidad|Computabilidad y decidibilidad]] |
| $\overline{L}$ | «ele barra» | El **complemento**: lo que no está en $L$ | [[computabilidad-y-decidibilidad|Computabilidad y decidibilidad]] |
| $\mathcal{P}(\Sigma^*)$ | «partes de sigma estrella» | **Todos** los lenguajes posibles | [[computabilidad-y-decidibilidad|Computabilidad y decidibilidad]] |
| $\subsetneq$ | «contenido estrictamente en» | Contenido, y **no** iguales | [[computabilidad-y-decidibilidad|Computabilidad y decidibilidad]] |
| $\langle M\rangle$ | «código de eme» | La máquina $M$ escrita como una cadena | [[todo-es-un-numero|Todo es un número]] |
| $\langle M, w\rangle$ | «código de eme coma doble u» | Una máquina **y** una entrada, juntas en una cadena | [[todo-es-un-numero|Todo es un número]] |
| $U$ | «u» | La **máquina universal**: corre a cualquier otra | [[todo-es-un-numero|Todo es un número]] |
| $\text{HALT}$ | «halt», el problema de la parada | El lenguaje de los pares $\langle M,w\rangle$ tales que $M$ se detiene con $w$ | [[problema-de-la-parada|El problema de la parada]] |

## Lógica

| Símbolo | Se lee | Qué es | Se presenta en |
|---|---|---|---|
| $F$ | «efe» | Un **sistema formal** cualquiera | [[sistemas-formales|Sistemas formales]] |
| PA | «pe a» | *Peano Arithmetic*, la aritmética de Peano de **primer orden** | [[sistemas-formales|Sistemas formales]] |
| $\varphi$ | «fi» | Una fórmula o enunciado cualquiera | [[sistemas-formales|Sistemas formales]] |
| $F \vdash \varphi$ | «efe demuestra fi» | Existe una demostración de $\varphi$ en $F$ | [[sistemas-formales|Sistemas formales]] |
| $\lnot\varphi$ | «no fi» | La **negación** de $\varphi$ | [[sistemas-formales|Sistemas formales]] |
| $\ulcorner\varphi\urcorner$ | «número de fi» | El número que codifica la fórmula $\varphi$ | [[sistemas-formales|Sistemas formales]] |
| $\text{NoPara}(x,y)$ | — | La oración que dice «el programa $x$ no termina con entrada $y$» | [[sistemas-formales|Sistemas formales]] |
| $\text{Con}(F)$ | «con de efe» | La oración que dice «$F$ es consistente» | [[teoremas-de-godel|Los teoremas de Gödel]] |
| $\blacksquare$ | — | Fin de la demostración | — |

## Tres palabras que se confunden

Y como cierre, las tres parejas donde el vocabulario engaña. Si te vas a llevar
algo de esta hoja, que sea esto:

| No confundir | con | Porque |
|---|---|---|
| **numerable** | **recursivamente enumerable** | *Todo* lenguaje es numerable. Casi ninguno es r.e. |
| **indecidible** (un lenguaje) | **indecidible en $F$** (una oración) | Lo primero es que ninguna máquina lo decide; lo segundo es que $F$ no demuestra ni la oración ni su negación |
| **indecidible** | **intratable** | Lo primero es imposible siempre; lo segundo es posible pero carísimo. Eso es [[complejidad|complejidad]], no computabilidad |
