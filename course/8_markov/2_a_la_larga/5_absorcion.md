---
id: mkv-absorcion
title: "Cuánto falta para terminar: serpientes y escaleras"
nav_title: "Cuánto falta: serpientes y escaleras"
summary: "¿Cuántos turnos dura, en promedio, una partida de serpientes y escaleras? El tiempo medio de llegada resuelve un sistema lineal que sale de condicionar en el primer paso; a mano en un tablero chico, con el algoritmo TIEMPO MEDIO DE LLEGADA en uno de 100 casillas y con 10 000 partidas simuladas."
status: ready
estimated_time: 27m
tags: [markov, absorcion, algoritmo, simulacion]
---

# Cuánto falta para terminar: serpientes y escaleras

**¿Cuántos turnos dura, en promedio, una partida de serpientes y escaleras?**

Al terminar tendrás:

- **Un modelo.** Escribirás un tablero como cadena, con estados al final de cada turno.
- **El teorema y su condición.** Aplicarás @mkv-c2-teo-absorcion y darás un tablero donde falla.
- **Una cuenta a mano.** Resolverás el tablero chico: ${m(0)=3}$ turnos.
- **El algoritmo TIEMPO MEDIO DE LLEGADA.** Seguirás pseudocódigo y Python, y justificarás su costo.
- **Una comprobación.** Compararás el valor calculado, ${m(0)\approx55.668}$ turnos, con 10 000 partidas simuladas.

## Lo que traes

- **Esperanza y primer paso.** [[mkv-algebra-y-limites|Lo que necesitas de álgebra y límites]] presenta el valor esperado (@mkv-c2-def-esperanza) y la regla de condicionar en el primer paso (@mkv-c2-teo-primer-paso).
- **Sistemas y caminos.** De la misma página: resolver un sistema lineal (@mkv-c2-def-sistema) y alcanzar un estado por un camino (@mkv-c2-def-alcanzar).
- **Clasificar.** En [[mkv-clasificar-estados|Clasificar los estados]] viste qué es un estado transitorio (@mkv-c2-def-transitorio) y una clase cerrada (@mkv-c2-def-clase-cerrada).
- **Simular.** De la clase 1: MUESTREAR-FILA, el promedio de réplicas independientes (@mkv-c1-teo-promedio) y el error estándar (@mkv-c1-error-estandar).

> **Modelo.** Cadenas finitas y homogéneas. En [[mkv-olvida-su-inicio|¿Olvida su inicio?]] preguntamos dónde está la cadena a la larga; aquí, cuánto tarda en llegar a un lugar.

---

## 1 · Modelar la partida como cadena

**Piensa: en serpientes y escaleras, ¿qué es un estado?**

La casilla donde queda la ficha **al final** del turno. Un tablero general tiene casillas ${0,\dots,n}$, salida 0 y meta $n$. Cada turno se tira un dado justo de $d$ caras y se avanza lo que salga.

- **Saltos.** Caer en la base de una escalera te sube a su punta; caer en la cabeza de una serpiente te baja a su cola.
- **Pasarse.** Si la tirada te lleva más allá de $n$, llegas a $n$. Es una regla nuestra; hay tableros que exigen tirada exacta.
- **Estados.** Las bases de escaleras y serpientes **no** son estados: nadie termina un turno ahí. Es una decisión de modelado, como elegir V y C en la clase 1.
- **Meta.** Desde $n$ la cadena se queda: ${P_{nn}=1}$.

Con eso, la casilla al final de cada turno es una cadena de Markov: la siguiente depende solo de la actual y del dado. Lo que nos importa es cuándo llega a la meta.

::: definition {#mkv-c2-ab-def-llegada title="Tiempo de llegada y tiempo medio"}
- **Qué es:** dado un conjunto objetivo ${A\subseteq\mathcal S}$ no vacío, el **tiempo de llegada** es el primer paso en que la cadena está en $A$:

$$
\tau_A=\min\{t\ge0:\ S_t\in A\}.
$$

- **Cómo se calcula:** si la cadena nunca entra en $A$, ${\tau_A=\infty}$. $E_s$ y $\Pr_s$ son esperanza y probabilidad al empezar en $s$, con ${\mu_0=\mathbf e_s}$ (@mkv-c2-def-esperanza). El **tiempo medio** desde $s$ es

$$
m(s)=E_s[\tau_A].
$$

- **Qué significa:** $m(s)$ cuenta transiciones, no casillas. En el tablero, una transición es un turno.
- **Qué no es:** no es el número de turnos de una partida concreta, que es aleatorio. Es su promedio.
:::

- **Notación.** $\mathcal T$ son los estados fuera de $A$ y $P_{\mathcal T}$ es $P$ restringida a sus filas y columnas. Los libros escriben $Q$; aquí $Q$ queda libre para refuerzo.
- **Paso 0.** Si ${s\in A}$, entonces ${\tau_A=0}$ y ${m(s)=0}$.

**En el juguete.** El tablero chico tiene casillas 0 a 5 y $A=\{5\}$. En vez de dado hay una moneda: avanzas 1 o 2, cada uno con probabilidad $1/2$. La escalera va de 2 a 4 y la serpiente, de 3 a 1.

::: figure {#mkv-c2-ab-fig-tablero title="El tablero chico y su cadena: cuatro estados reales"}
![Arriba, el tablero de seis casillas, de 0 a 5, con salida en 0 y meta en 5; una escalera sube de 2 a 4 y una serpiente baja de 3 a 1. Abajo, el grafo de los estados reales 0, 1, 4 y 5: de 0 a 1 con 1/2 y a 4 con 1/2; de 1 a sí misma con 1/2 y a 4 con 1/2; de 4 a 5 con 1; 5 se queda con 1. Las casillas 2 y 3 no son estados](../_assets/mkv-c2-tablero-chico.svg)
:::

- **Desde 0.** Con 1 llegas a 1; con 2 caes en la escalera y subes a 4.
- **Desde 1.** Con 1 caes en 2 y subes a 4; con 2 caes en 3 y bajas a 1.
- **Desde 4.** Con 1 llegas a 5; con 2 te pasas y también llegas.

En el orden 0, 1, 4, 5, fila = desde dónde y columna = hacia dónde:

$$
P=\begin{pmatrix}
0&1/2&1/2&0\\
0&1/2&1/2&0\\
0&0&0&1\\
0&0&0&1
\end{pmatrix},
$$

$$
P_{\mathcal T}=\begin{pmatrix}
0&1/2&1/2\\
0&1/2&1/2\\
0&0&0
\end{pmatrix}.
$$

- **Lectura.** $P_{\mathcal T}$ quita la fila y la columna de 5. Sus filas suman **a lo más** 1: lo que falta es la probabilidad de llegar a la meta en ese turno.

**El caso grande.** Nuestro tablero de 100 casillas usa un dado de 6, ocho escaleras y ocho serpientes. No es un tablero histórico: lo fijamos para esta clase. Quedan 85 estados reales: 101 casillas menos 16 bases.

> **Una nota de historia.** El juego viene, hasta donde se sabe, de una familia de juegos de dados de la India, como el *gyan chaupar* o *moksha patam*. En Inglaterra se conserva un tablero de F. H. Ayres, Londres, 1892. Milton Bradley lo publicó en Estados Unidos en 1943 como *Chutes and Ladders*.

> [!WARNING]
> **Contar las casillas 2 y 3 como estados.** Al caer en 3 bajas a 1 en el mismo turno; si 3 fuera estado, el turno se partiría en dos.
> **Los estados son las casillas donde se puede terminar un turno: 0, 1, 4 y 5.**

::: exercise {#mkv-c2-ab-ej-minimo title="Cuenta la partida más corta"}
En el tablero chico, ¿cuántos turnos dura la partida más corta? ¿Con qué probabilidad ocurre?
:::

::: hint {#mkv-c2-ab-pista-minimo of="mkv-c2-ab-ej-minimo" title="¿Desde qué estado se llega a 5?"}
¿Qué estado tiene una flecha a 5, y cómo llegas a él desde 0 lo antes posible?
:::

::: answer {#mkv-c2-ab-resp-minimo of="mkv-c2-ab-ej-minimo"}
Dos turnos: 0 → 4 (sale 2 y subes por la escalera) y 4 → 5. Ocurre con probabilidad ${\tfrac12\cdot1=\tfrac12}$. En un turno no se puede, porque desde 0 no hay flecha a 5.
:::

Ya tenemos la cadena; falta una ecuación que dé $m(0)$ sin recorrer todas las partidas posibles.

---

## 2 · Plantear el tiempo medio con el primer paso

**Piensa: ¿qué relación hay entre $m(0)$ y el tiempo medio desde las casillas a donde puedes ir?**

Un turno se gasta siempre; después falta, en promedio, lo que falte desde donde caíste. Eso es condicionar en el primer paso, y da un sistema lineal.

::: theorem {#mkv-c2-teo-absorcion title="El tiempo medio de llegada resuelve un sistema lineal"}
Sea una cadena finita y homogénea con estados $\mathcal S$, un conjunto objetivo ${A\subseteq\mathcal S}$ no vacío y ${\mathcal T=\mathcal S\setminus A}$.

**Condición.** Desde todo ${s\in\mathcal T}$, ${\Pr_s(\tau_A<\infty)=1}$. En cadenas finitas equivale a que desde cada ${s\in\mathcal T}$ haya un camino hacia $A$ (@mkv-c2-def-alcanzar), y también a que ${I-P_{\mathcal T}}$ sea invertible.

Entonces ${m(s)<\infty}$ para todo ${s\in\mathcal T}$, y el vector columna $m$ sobre $\mathcal T$ es la **única** solución de

$$
\begin{aligned}
m(s)&=1+\sum_{s'\in\mathcal T}P_{ss'}\,m(s'),
\quad s\in\mathcal T,\\
m&=\mathbf 1+P_{\mathcal T}\,m,\\
(I-P_{\mathcal T})\,m&=\mathbf 1,
\end{aligned}
$$

con ${m(s)=0}$ en $A$. Las dimensiones son ${\lvert\mathcal T\rvert\times\lvert\mathcal T\rvert}$ por ${\lvert\mathcal T\rvert\times1}$.

**Lectura.** El 1 es el turno que se gasta; la suma promedia lo que falta desde cada destino. Los destinos en $A$ no aportan: ahí ya no falta nada.

**Casos nulos.** Si ${s\in A}$, ${m(s)=0}$. Si toda flecha de $s$ va a $A$, ${m(s)=1}$.
:::

- **Suficiente y necesaria.** Sin la condición, algún $m(s)$ vale $\infty$ y ${I-P_{\mathcal T}}$ es singular. Los estados que no pueden caer en la trampa conservan un tiempo finito, pero el sistema ya no lo entrega.
- **Cómo revisarla.** Basta mirar el grafo: ninguna clase cerrada (@mkv-c2-def-clase-cerrada) puede quedar dentro de $\mathcal T$. Si cada estado de $A$ es absorbente, la condición dice que todos los de $\mathcal T$ son transitorios (@mkv-c2-def-transitorio).

::: proof {#mkv-c2-ab-dem-absorcion of="mkv-c2-teo-absorcion"}
**Finito.** Desde cada ${s\in\mathcal T}$ hay un camino a $A$ de a lo más $\lvert\mathcal T\rvert$ pasos. Sea ${\delta>0}$ la menor probabilidad de esos caminos. Cada bloque de $\lvert\mathcal T\rvert$ pasos llega a $A$ con probabilidad al menos $\delta$, así que ${\Pr_s(\tau_A>j\lvert\mathcal T\rvert)\le(1-\delta)^j}$. Con ${E[\tau]=\sum_{t\ge0}\Pr(\tau>t)}$, que usamos sin demostración:

$$
m(s)\le\lvert\mathcal T\rvert\sum_{j\ge0}(1-\delta)^j=\frac{\lvert\mathcal T\rvert}{\delta}.
$$

**La ecuación.** Sea ${s\in\mathcal T}$; por @mkv-c2-teo-primer-paso,

$$
m(s)=\sum_{s'\in\mathcal S}P_{ss'}\,E_s[\tau_A\mid S_1=s'].
$$

Como ${s\notin A}$, ${\tau_A\ge1}$. Dado ${S_1=s'}$, por Markov y homogeneidad lo que sigue es la cadena empezando en $s'$: ${E_s[\tau_A\mid S_1=s']=1+m(s')}$. Las filas suman 1 y ${m(s')=0}$ en $A$; queda la ecuación del teorema.

**Única.** Si $m$ y $m'$ la resuelven, su diferencia ${x=m-m'}$ cumple ${x=P_{\mathcal T}x}$, y por tanto ${x=P_{\mathcal T}^{\,t}x}$ para todo $t$. La entrada ${(P_{\mathcal T}^{\,t})_{ss'}}$ es la probabilidad de estar en $s'$ en el paso $t$ sin haber tocado $A$: a lo más ${\Pr_s(\tau_A>t)\to0}$. Entonces ${x=0}$, y ${I-P_{\mathcal T}}$ es invertible.
:::

**Contraejemplo: un pozo.** Cambia el tablero chico: la casilla 4 es un pozo y quien cae ahí no sale. Ahora $\{4\}$ es una clase cerrada fuera de $A$.

$$
m(4)=1+m(4)
\quad\Longrightarrow\quad 0=1.
$$

- **Qué se rompe.** Ninguna partida termina: desde 0 y desde 1 se cae en 4 tarde o temprano. ${m=\infty}$ y la fila de 4 en ${I-P_{\mathcal T}}$ queda en ceros.

**En el juguete.** La condición se cumple: desde 0, 1 y 4 hay camino a 5. Con ${P_{\mathcal T}}$ de la sección 1:

$$
\begin{aligned}
m(4)&=1,\\
m(1)&=1+\tfrac12m(1)+\tfrac12m(4),\\
m(0)&=1+\tfrac12m(1)+\tfrac12m(4).
\end{aligned}
$$

- **De abajo hacia arriba.** ${m(4)=1}$. Despejar en la segunda da ${\tfrac12m(1)=\tfrac32}$, es decir ${m(1)=3}$. La tercera da ${m(0)=1+\tfrac32+\tfrac12=3}$.
- **Respuesta.** Una partida del tablero chico dura, en promedio, **3 turnos**.
- **Una coincidencia que no lo es.** ${m(0)=m(1)}$ porque las filas de 0 y de 1 son iguales: la serpiente te regresa a un estado con el mismo futuro que la salida.

**El caso grande.** El tablero de 100 da 84 ecuaciones con 84 incógnitas, una por estado fuera de la meta. Cada una tiene hasta seis términos y las serpientes las encadenan en ciclos. A mano no; lo resuelve un algoritmo.

> [!WARNING]
> **Olvidar el 1.** ${m=P_{\mathcal T}m}$ tiene la solución ${m=0}$, que diría que la partida no dura nada.
> **Cada ecuación suma el turno que se gasta: ${m=\mathbf 1+P_{\mathcal T}m}$.**

::: exercise {#mkv-c2-ab-ej-sin-serpiente title="Quita la serpiente"}
Quita la serpiente del tablero chico y deja la escalera. ¿Qué casillas son estados ahora? Calcula $m(0)$. ¿Cuánto alarga la partida la serpiente?
:::

::: hint {#mkv-c2-ab-pista-sin-serpiente of="mkv-c2-ab-ej-sin-serpiente" title="¿Qué casilla se vuelve estado?"}
¿Dónde terminas ahora un turno al caer en 3? ¿Desde qué estado conviene empezar a despejar?
:::

::: answer {#mkv-c2-ab-resp-sin-serpiente of="mkv-c2-ab-ej-sin-serpiente"}
Los estados son 0, 1, 3, 4 y 5: la casilla 3 ya es estado. De abajo hacia arriba:

$$
\begin{aligned}
m(4)&=1,\\
m(3)&=1+\tfrac12m(4)=\tfrac32,\\
m(1)&=1+\tfrac12m(4)+\tfrac12m(3)=\tfrac94,\\
m(0)&=1+\tfrac12m(1)+\tfrac12m(4)=\tfrac{21}{8}.
\end{aligned}
$$

Sin serpiente, ${m(0)=21/8=2.625}$. La serpiente alarga la partida en ${3-21/8=3/8}$ de turno, en promedio.
:::

Con 84 incógnitas hace falta un procedimiento que arme el sistema y lo resuelva solo.

---

## 3 · Calcular con TIEMPO MEDIO DE LLEGADA

**Piensa: ¿qué necesita un programa para pasar de $P$ y $A$ a $m$?**

Separar los estados fuera de $A$, armar ${I-P_{\mathcal T}}$ y resolver el sistema con el lado derecho lleno de unos. La eliminación de Gauss hace el último paso: despeja una incógnita y la sustituye en las demás ecuaciones, como en los sistemas de @mkv-c2-def-sistema. De paso, revisa la condición.

> **Dado:** una cadena finita y homogénea con matriz $P$ de ${k\times k}$ y un conjunto objetivo $A$ no vacío.
>
> **Encontrar:** ${m(s)=E_s[\tau_A]}$ para cada ${s\in\mathcal T}$, o avisar que algún estado de $\mathcal T$ no llega a $A$.

### El mapa de TIEMPO MEDIO DE LLEGADA

- **Qué calcula:** la solución de ${(I-P_{\mathcal T})m=\mathbf 1}$, que por @mkv-c2-teo-absorcion es el tiempo medio.
- **Qué guarda:** la lista $\mathcal T$, la matriz ${I-P_{\mathcal T}}$ con el vector de unos pegado como última columna.
- **Cómo avanza:** columna por columna, busca un pivote distinto de cero y elimina esa incógnita de las demás filas.
- **Qué devuelve al terminar:** $m$ sobre $\mathcal T$, o FALLA si alguna columna se queda sin pivote.

::: figure {#mkv-c2-ab-fig-flujo title="El tiempo medio de llegada, en palabras"}
![Diagrama de flujo del tiempo medio de llegada, en palabras: separa los estados fuera de A; arma la matriz P restringida a ellos; forma I menos esa matriz y pega una columna de unos; elimina columna por columna; un rombo pregunta si la columna tiene pivote distinto de cero; si no, falla: algún estado no llega a A; si sí, sigue con la siguiente columna; al terminar devuelve m, con m igual a 0 en A](../_assets/mkv-c2-flujo-absorcion.svg)
:::

```text
INPUT   P, de k×k, estocástica por
        filas; A, conjunto objetivo
        no vacío.
OUTPUT  m(s) = E_s[τ_A] para cada s
        fuera de A, o FALLA.

 1 function TIEMPO-MEDIO(P, A)
 2   𝒯 ← estados fuera de A, en orden
 3   P_𝒯 ← P en filas y columnas de 𝒯
 4   M ← I − P_𝒯
 5   b ← vector de |𝒯| unos
 6   resolver M m = b por eliminación
 7     si una columna no tiene pivote:
         return FALLA
 8   return m          (m = 0 en A)
```

**Gemelo Python.** Cada comentario numerado remite al pseudocódigo. `resolver` es la eliminación de la línea 6, con fracciones exactas; `tablero` arma $P$ con las reglas de la sección 1.

```python
from fractions import Fraction as F

def resolver(M, b):              # (6) eliminación exacta
    k = len(b)
    M = [list(f) + [c] for f, c in zip(M, b)]
    for c in range(k):
        p = next((r for r in range(c, k)
                  if M[r][c] != 0), None)
        if p is None:
            return None          # (7) sin pivote
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [x / piv for x in M[c]]
        for r in range(k):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y
                        for x, y in zip(M[r], M[c])]
    return [M[r][k] for r in range(k)]

def tiempo_medio(P, A):                    # (1)
    T = [s for s in range(len(P))
         if s not in A]                    # (2)
    PT = [[P[i][j] for j in T] for i in T] # (3)
    k = len(T)
    M = [[(i == j) - PT[i][j]
          for j in range(k)]
         for i in range(k)]                # (4)
    b = [F(1)] * k                         # (5)
    m = resolver(M, b)                     # (6)
    if m is None:
        return None                        # (7) FALLA
    return dict(zip(T, m))                 # (8)

def tablero(n, caras, saltos):
    estados = [c for c in range(n + 1)
               if c not in saltos]
    pos = {c: i for i, c in enumerate(estados)}
    P = [[F(0)] * len(estados) for _ in estados]
    for c in estados:
        if c == n:                     # la meta se queda
            P[pos[c]][pos[c]] = F(1)
            continue
        for d in range(1, caras + 1):
            llega = min(c + d, n)      # pasarse = llegar
            llega = saltos.get(llega, llega)
            P[pos[c]][pos[llega]] += F(1, caras)
    return estados, P

est, P = tablero(5, 2, {2: 4, 3: 1})
m = tiempo_medio(P, {est.index(5)})
print({est[s]: v for s, v in m.items()})
# {0: Fraction(3, 1), 1: Fraction(3, 1), 4: Fraction(1, 1)}

cien = {3: 22, 8: 30, 17: 45, 28: 55, 36: 57,
        51: 72, 63: 81, 71: 92,           # escaleras
        33: 6, 47: 26, 49: 11, 62: 19, 64: 42,
        87: 24, 95: 56, 98: 78}           # serpientes
est, P = tablero(100, 6, cien)
m = tiempo_medio(P, {est.index(100)})
print(len(est), round(float(m[0]), 3))
# 85 55.668
```

**Cada pieza, en su línea:**

- **Línea 4.** `(i == j)` vale 1 en la diagonal y 0 fuera: es la identidad sin escribirla.
- **Líneas 6 y 7.** Con fracciones, «sin pivote» es exacto: un cero es un cero, no un redondeo.
- **Línea 8.** Las llaves son índices de $P$; el `print` las traduce a casillas.

**Cómo leer la traza.** Corremos el tablero chico. Cada renglón dice qué deja la línea indicada.

**Tramo único · Del tablero chico a m**

| Línea | Qué queda |
|---|---|
| 2 | 𝒯 = 0, 1, 4 |
| 3 | P_𝒯: filas (0, ½, ½), (0, ½, ½), (0, 0, 0) |
| 4 | M: filas (1, −½, −½), (0, ½, −½), (0, 0, 1) |
| 6 | m = (3, 3, 1); pivotes 1, ½, 1, ninguno es cero |

- **Línea 6.** Hace en orden lo que hicimos a mano de abajo hacia arriba.
- **Número que da.** En el tablero de 100, ${m(0)\approx55.668}$ turnos. Exacto es una fracción de 62 dígitos en el numerador.

::: exercise {#mkv-c2-ab-ej-pozo title="Corre el algoritmo en el tablero con pozo"}
En el tablero chico con pozo en 4, ¿cómo queda la fila de 4 en $M$ de la línea 4? ¿Qué devuelve TIEMPO-MEDIO y en qué línea?
:::

::: hint {#mkv-c2-ab-pista-pozo of="mkv-c2-ab-ej-pozo" title="¿Qué fila tiene ahora el pozo en la matriz de transición?"}
¿Cuánto vale ${P_{44}}$ con el pozo, y qué le hace la resta de la línea 4?
:::

::: answer {#mkv-c2-ab-resp-pozo of="mkv-c2-ab-ej-pozo"}
Con el pozo, la fila de 4 en $P_{\mathcal T}$ es ${(0,0,1)}$ y en $M$ queda ${(0,0,0)}$. Al llegar a la columna de 4 no hay pivote distinto de cero: la línea 7 devuelve FALLA. Es la clase cerrada fuera de $A$ que prohíbe la condición.
:::

### Lo que garantiza y cuánto cuesta

- **Propiedades:** termina siempre, tras $\lvert\mathcal T\rvert$ columnas. Devuelve FALLA exactamente cuando ${I-P_{\mathcal T}}$ es singular.
- **Número que da:** 3 turnos en el tablero chico; ${\approx55.668}$ en el de 100.
- **Garantía:** si no falla, por @mkv-c2-teo-absorcion devuelve ${E_s[\tau_A]}$ desde cada estado de $\mathcal T$. Con fracciones es exacto; con decimales, `numpy.linalg.solve` da lo mismo con redondeo.
- **Costo:** armar $M$ toma ${\lvert\mathcal T\rvert^2}$; la eliminación, del orden de ${\lvert\mathcal T\rvert^3}$ operaciones. En el tablero de 100, ${84^3\approx6\times10^5}$.
- **Supuestos:** $P$ es fija, sus filas suman 1 y $A$ no es vacío.

El algoritmo confía en el álgebra; la simulación comprueba el número jugando.

---

## 4 · Simular partidas para comprobar

**Piensa: ¿cómo compruebas 55.668 turnos sin repetir la eliminación?**

Jugando muchas partidas independientes y promediando sus turnos. Cada réplica empieza en 0, sortea cada turno con MUESTREAR-FILA y para al llegar a la meta. Por @mkv-c1-teo-promedio, con probabilidad 1:

$$
\frac{1}{n}\sum_{r=1}^{n}(\text{turnos de la réplica }r)
\xrightarrow[n\to\infty]{}m(0).
$$

- **Ruido.** Ahora promediamos turnos, no ceros y unos, así que ${\sqrt{p(1-p)}}$ de @mkv-c1-error-estandar ya no sirve. Si $x_r$ son los turnos de la réplica $r$ y ${\bar x=\frac1n\sum_r x_r}$, la dispersión es ${s=\sqrt{\frac{1}{n-1}\sum_r(x_r-\bar x)^2}}$ (con ${n\ge2}$), y el error estándar del promedio es ${s/\sqrt n}$.
- **Por qué termina.** Por la condición del teorema, cada réplica llega a la meta con probabilidad 1. En el tablero con pozo, la simulación no pararía nunca.

**En el juguete.** Con ${n=10\,000}$ partidas y semilla 2041, el promedio fue 3.0048, con error estándar 0.0143. La diferencia con 3 es 0.0048, un tercio de error estándar.

**El caso grande.** En el tablero de 100, con ${n=10\,000}$ partidas y semilla 2038:

| Cantidad | Turnos |
|---|---|
| m(0), TIEMPO-MEDIO | 55.668 |
| Promedio de 10 000 partidas | 56.008 |
| Error estándar | 0.428 |
| Diferencia | 0.340 |

- **Lectura.** La diferencia es 0.79 errores estándar: el tamaño que anticipa el ruido.
- **Dispersión.** El error estándar es treinta veces el del juguete con el mismo $n$: las partidas del tablero de 100 varían mucho más entre sí.

> [!WARNING]
> **Confundir el promedio con la partida típica.** 55.668 es la media de muchas partidas, no lo que dura una.
> **Una partida concreta puede durar mucho menos o mucho más; $m(0)$ solo fija el promedio.**

::: exercise {#mkv-c2-ab-ej-menos-partidas title="Predice el error con menos partidas"}
Repites la simulación del tablero de 100 con 2500 partidas. ¿Qué error estándar esperas, aproximadamente?
:::

::: hint {#mkv-c2-ab-pista-menos-partidas of="mkv-c2-ab-ej-menos-partidas" title="¿Cómo cambia el error con n?"}
¿Entre qué raíz se divide la dispersión, y cuántas veces más chico es $n$?
:::

::: answer {#mkv-c2-ab-resp-menos-partidas of="mkv-c2-ab-ej-menos-partidas"}
El error estándar cambia como ${1/\sqrt n}$. Con cuatro veces menos partidas, se multiplica por ${\sqrt4=2}$: cerca de ${2\cdot0.428\approx0.86}$ turnos.
:::

**Lo que no generaliza.** En el tablero chico se despeja de abajo hacia arriba porque la única vuelta atrás es un lazo en 1. Con serpientes largas, las ecuaciones se encadenan en ciclos y hay que resolverlas juntas: eso hace la eliminación.

Aplica el planteamiento a un tablero distinto.

---

## Ejercicios

::: exercise {#mkv-c2-ab-ej-siete title="Resuelve un tablero de siete casillas"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Un tablero tiene casillas 0 a 6, salida 0 y meta 6. Se tira la misma moneda: avanzas 1 o 2 con probabilidad $1/2$; si te pasas de 6, llegas a 6. **Cambia una idea:** el tablero crece y cambian los saltos. Hay una escalera de 1 a 3 y una serpiente de 5 a 4.

1. **Modela.** ¿Qué casillas son estados reales? Escribe las flechas con sus probabilidades.
2. **Revisa la condición.** ¿Hay camino a la meta desde cada estado?
3. **Plantea y resuelve.** Escribe ${m=\mathbf 1+P_{\mathcal T}m}$ y calcula $m(0)$.
4. **Cambia una regla.** La serpiente de 5 ahora baja a 0. Recalcula $m(0)$; puedes usar el Python de la sección 3.
5. **Explica.** ¿Por qué el inciso 4 ya no se despeja de abajo hacia arriba?
:::

::: hint {#mkv-c2-ab-pista-siete-1 of="mkv-c2-ab-ej-siete" title="Pista 1 · ¿Dónde puede terminar un turno?"}
¿Qué casillas son base de un salto? Para cada estado, ¿a qué casilla te lleva cada cara de la moneda después de aplicar los saltos?
:::

::: hint {#mkv-c2-ab-pista-siete-2 of="mkv-c2-ab-ej-siete" title="Pista 2 · ¿Tus números tienen sentido?"}
¿Suma 1 cada fila de tu $P$? ¿Tu $m$ más chico es el del estado más cercano a la meta? ¿Es $m(0)$ al menos el número mínimo de turnos?
:::

::: answer {#mkv-c2-ab-resp-siete of="mkv-c2-ab-ej-siete" title="Respuesta · El tablero de siete casillas"}
**1. Estados.** Las bases 1 y 5 no son estados; quedan 0, 2, 3, 4 y 6. Las flechas:

- **Desde 0:** a 3 (sale 1, escalera) y a 2, con $1/2$ cada una.
- **Desde 2:** a 3 y a 4, con $1/2$ cada una.
- **Desde 3:** con 1 llegas a 4; con 2 caes en 5 y bajas a 4. Va a 4 con 1.
- **Desde 4:** con 1 caes en 5 y vuelves a 4; con 2 llegas a 6.

**2. Condición.** Desde 0, 2 y 3 se llega a 4, y desde 4 a 6. No hay clase cerrada fuera de la meta.

**3. Resolver.** De abajo hacia arriba:

$$
\begin{aligned}
m(4)&=1+\tfrac12m(4)\ \Rightarrow\ m(4)=2,\\
m(3)&=1+m(4)=3,\\
m(2)&=1+\tfrac12m(3)+\tfrac12m(4)=\tfrac72,\\
m(0)&=1+\tfrac12m(3)+\tfrac12m(2)=\tfrac{17}{4}.
\end{aligned}
$$

**4. Serpiente a 0.** Ahora desde 3 se va a 4 o a 0, y desde 4 a 0 o a 6, con $1/2$ cada uno. El sistema da ${m=(46/5,\ 8,\ 42/5,\ 28/5)}$ en el orden 0, 2, 3, 4: ${m(0)=46/5=9.2}$ turnos.

**5. Ciclos.** $m(4)$ depende de $m(0)$, y $m(0)$ depende de $m(4)$ a través de 2 y 3. Ninguna ecuación tiene una sola incógnita: hay que resolverlas juntas, como hace la eliminación.
:::

**Punto de control:** deberías poder modelar un tablero como cadena con estados al final del turno. También, plantear ${(I-P_{\mathcal T})m=\mathbf 1}$, revisar su condición en el grafo, correr TIEMPO MEDIO DE LLEGADA y comparar su resultado con partidas simuladas.

---

## Lo que hay que llevarse

- **El modelo.** Estado = casilla al final del turno; las bases de saltos no son estados. El tablero chico tiene 4 estados; el de 100, 85.
- **El teorema.** ${m=\mathbf 1+P_{\mathcal T}m}$, con ${m=0}$ en $A$, si desde todo estado fuera de $A$ se llega a $A$ con probabilidad 1 (@mkv-c2-teo-absorcion).
- **La condición.** En finitas equivale a que ${I-P_{\mathcal T}}$ sea invertible. Un pozo fuera de la meta la rompe: ${m=\infty}$.
- **A mano.** El tablero chico dura en promedio ${m(0)=3}$ turnos; sin serpiente, $21/8$.
- **El algoritmo.** TIEMPO MEDIO DE LLEGADA arma ${I-P_{\mathcal T}}$ y elimina; cuesta del orden de ${\lvert\mathcal T\rvert^3}$ y falla exactamente cuando la condición falla.
- **La simulación.** En el tablero de 100: ${\approx55.668}$ calculados contra 56.008 simulados, con error estándar 0.428.

Continúa con [[mkv-pagerank|PageRank]].
