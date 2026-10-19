---
id: notacion-markov
title: Toda la notación, en una hoja
nav_title: Notación
summary: "Cada símbolo y cada término que usa la unidad de cadenas de Markov, cómo se lee, qué significa y en qué página se presentó."
status: ready
estimated_time: 5m
tags: [markov, referencia, notacion]
---

# Toda la notación, en una hoja

Todos los símbolos están definidos en su página. Si encuentras uno a media
lectura y no recuerdas qué era, búscalo aquí en vez de retroceder.

**Cómo leer la última columna:** dice en qué página se **presentó** el
símbolo. Si algo te resulta opaco, vuelve a esa página.

**Dos convenciones valen en toda la unidad.** Mayúscula para lo que todavía
es azar ($S_t$) y minúscula para un valor concreto ($s$). Lo exacto va sin
gorro; lo que se estima con datos lleva gorro, como $\widehat P$.

## Probabilidad

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $\Pr(A)$ | «probabilidad de a». Qué tan probable es el evento $A$, entre 0 y 1 | Lo que necesitas de probabilidad |
| $\widehat{\Pr}(A)$ | «probabilidad estimada de a». La frecuencia con que $A$ ocurrió en los datos | Lo que necesitas de probabilidad |
| $A\cap B$ | «a y be». El evento de que ocurran los dos | Lo que necesitas de probabilidad |
| $\Pr(A\mid B)$ | «probabilidad de a dado be». La probabilidad de $A$ si ya sabes que ocurrió $B$: $\Pr(A\cap B)/\Pr(B)$, definida solo si $\Pr(B)>0$ | Lo que necesitas de probabilidad |
| $\Pr(S_0=a, S_1=b)$ | La coma se lee «y»: que ocurran las dos cosas | Lo que necesitas de probabilidad |
| $n$ | «ene». El número de réplicas de una simulación | Lo que necesitas de probabilidad |

## La cadena

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $t$ | «te». El paso: $t=0,1,2,\dots$ Los libros de cadenas usan $n$; aquí $t$, como en agentes | Lo que necesitas de probabilidad |
| $S_t$ | «ese sub te». El estado en el paso $t$, **todavía aleatorio** | Lo que necesitas de probabilidad |
| $s$, $s'$ | «ese», «ese prima». Valores concretos de un estado: de dónde sales y a dónde llegas | El problema de Markov |
| $\mathcal S$ | «ese caligráfica». El conjunto de estados posibles | El problema de Markov |
| $k$ | «ka». El número de estados: $k=\lvert\mathcal S\rvert$ | El problema de Markov |
| V, C | «ve», «ce». Los dos estados del juguete: vocal y consonante, en ese orden | El problema de Markov |
| $P$ | «pe». La matriz de transición, $k\times k$: fila = desde, columna = hacia; cada fila suma 1. No es la clase P de complejidad | El problema de Markov |
| $P(s'\mid s)$, $P_{ss'}$ | «pe de ese prima dado ese». La entrada de la fila $s$ y columna $s'$: $\Pr(S_{t+1}=s'\mid S_t=s)$ | El problema de Markov |
| $\mu_0$ | «mu cero». La distribución del estado inicial, un vector fila que suma 1. No es el $\mu$ de KKT | El problema de Markov |
| $\mu_t$ | «mu sub te». La distribución del estado en el paso $t$: $\mu_t(s)=\Pr(S_t=s)$ | Predecir |
| $j$ | «jota». Índice de un producto o una suma: $\prod_{j=0}^{t-1}$ | El problema de Markov |
| $u$ | «u». Un número uniforme en $[0,1)$ con que MUESTREAR-FILA elige el siguiente estado | El problema de Markov |
| $\ell$, $q$ | «ele», «cu». La longitud de una racha de consonantes y la probabilidad de seguir en consonante | El problema de Markov |
| $T$ | «te mayúscula». El largo de una trayectoria, en pasos | Ajustar contando |

## Ajustar desde datos

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $N(s,s')$ | «ene de ese, ese prima». Cuántas veces, en los datos, a $s$ le sigue $s'$ | Ajustar contando |
| $N(s)$ | «ene de ese». Las salidas observadas de $s$: $\sum_{s'}N(s,s')$. La última letra no cuenta: no tiene sucesor | Ajustar contando |
| $\widehat P$ | «pe gorro». La matriz estimada: $\widehat P(s'\mid s)=N(s,s')/N(s)$ | Ajustar contando |
| $\mathcal L(P)$ | «ele caligráfica de pe». La verosimilitud: la probabilidad de los datos observados como función de $P$, condicionada al primer estado | Ajustar contando |
| $\Sigma$ | «sigma mayúscula». El alfabeto: los símbolos que pueden seguir. Con las 27 letras y el espacio, $\lvert\Sigma\rvert=28$. En los juguetes son los estados: $\lvert\Sigma\rvert=k$ | Ajustar contando |
| $z$ | «zeta». Un símbolo de $\Sigma$: el que sigue a un contexto. Al agregarlo, el contexto se desliza | Ajustar contando |
| $\widetilde p$ | «pe tilde». La estimación suavizada (Laplace): $\widetilde p(z\mid s)=\frac{N(s,z)+1}{N(s)+\lvert\Sigma\rvert}$. No garantiza maximizar la verosimilitud | Ajustar contando |
| memoria $h$ | «memoria hache». Cuántos símbolos anteriores forman el estado. Memoria 0, 1, 2 = unigrama, bigrama, trigrama. No es la profundidad de UCT | Ajustar contando |

## Términos

| Término | Qué significa aquí | Se presenta en |
|---|---|---|
| Trayectoria | La secuencia de estados $S_0,\dots,S_T$; un texto es una trayectoria observada | El problema de Markov |
| Réplica | Una trayectoria simulada, independiente de las demás | El problema de Markov |
| Salidas | Las transiciones que parten de un estado, $N(s)$; la última letra no tiene salida | Ajustar contando |
| Verosimilitud | La probabilidad de los datos observados vista como función de $P$ | Ajustar contando |
| Cero estructural | Una transición imposible por las reglas o la normalización: dos espacios seguidos | Ajustar contando |
| Transición no observada | Un par con conteo 0 que sí podría ocurrir: q→a | Ajustar contando |
| Estado sin observaciones | Un estado con $N(s)=0$: los datos no determinan su fila. La «k» en el *Quijote* | Ajustar contando |
| Contexto | Los $h$ símbolos anteriores, que forman el estado con memoria $h$ | Ajustar contando |
| Suavizado aditivo de conteos | Sumar 1 a cada conteo por símbolo siguiente antes de dividir (Laplace) | Ajustar contando |
| Memoria 0, 1, 2 | Unigrama, bigrama, trigrama. Shannon los numera uno arriba: su «primer orden» es memoria 0 | Ajustar contando |

## En las figuras

- **Los estados:** V es un círculo azul con la letra V, y C un cuadrado
  amarillo con la C. La forma y la letra bastan; el color solo ayuda.
- **Las simulaciones:** el punto con línea es la mediana de las réplicas, y
  la franja va del 5 % al 95 % de ellas.
- **Diagramas «…, en palabras»:** cajas con verbos, rombos con una
  pregunta y una salida marcada con borde de otro color.

## Avisos de letras

- **$\pi$ no aparece en esta unidad con el sentido de los libros de cadenas.**
  Ahí la usan para otra cosa; aquí, como en agentes, $\pi$ queda para la
  política.
- **$\mu$** es una distribución sobre estados, como en el libro de Sutton y
  Barto; no es el multiplicador de KKT de optimización.
- **$T$** es el largo de una trayectoria, en pasos, como el $T$ de un
  episodio en Sutton y Barto. No es la transición $T(s,a)$ de juegos: aquí
  la transición es $P$.
- **$k$** es el número de estados. No son las simulaciones por jugada de
  Monte Carlo plano en juegos.
- **$N(s)$** cuenta **salidas**, no visitas como en juegos: la última letra
  aparece pero no sale.
- **$P$** es la matriz de transición, la misma $P$ de
  $\langle S,A,P,R,\gamma\rangle$ en agentes; no es la clase P de
  complejidad.
