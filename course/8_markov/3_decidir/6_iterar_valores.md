---
id: mkv-iterar-valores
title: "Iteración de valores"
nav_title: "Iteración de valores"
summary: "Resolver Bellman aplicando el máximo una y otra vez: la traza en el pasillo, cuándo converge, cuándo parar y un pasillo de 200 casillas."
status: ready
estimated_time: 30m
tags: [markov, decidir, iteracion-de-valores, algoritmo]
---

# Iteración de valores

**¿Cómo se resuelve una ecuación con un máximo y un ciclo?**

Al terminar tendrás:

- **Una traza a mano.** Correrás seis rondas en el pasillo mojado y verás a ${V^{(k)}}$ acercarse a ${(-5,-2)}$.
- **El algoritmo ITERACIÓN DE VALORES.** Seguirás su pseudocódigo y su gemelo Python, y justificarás su costo por ronda.
- **El teorema y su condición.** Aplicarás @mkv-c3-teo-iterar-valores y dirás qué significa ${V^{(k)}}$ cuando se arranca en 0.
- **Una regla de paro.** Convertirás un residuo en una cota del error, y darás un caso donde el error es 99 veces el residuo.
- **Un caso grande.** Resolverás un pasillo de 200 casillas sin revisar sus $2^{200}\approx1.6\times10^{60}$ políticas.

## Lo que traes

- **Punto fijo.** En [[mkv-max-y-punto-fijo|Lo que necesitas: máximo y punto fijo]] viste el máximo, el argmax (@mkv-c3-def-argmax) y qué pasa al iterar ${x\leftarrow f(x)}$ (@mkv-c3-def-punto-fijo).
- **Hacia atrás.** En [[mkv-la-escalera|De contar a decidir]], una pasada hacia atrás resolvió la escalera porque no tenía ciclos (@mkv-c3-teo-hacia-atras).
- **El modelo.** De [[mkv-el-mdp|El MDP]]: el MDP (@mkv-c3-def-mdp), la política (@mkv-c3-def-politica), el valor (@mkv-c3-def-valor) y terminar con probabilidad 1 (@mkv-c3-def-termina).
- **La ecuación.** En [[mkv-bellman|La ecuación de Bellman]] viste $Q$ (@mkv-c3-def-q), el óptimo (@mkv-c3-def-optimo), la ecuación con su condición (@mkv-c3-teo-bellman) y que la codiciosa de $V^*$ es óptima (@mkv-c3-teo-codiciosa).

> [!NOTE]
> **Por qué un algoritmo nuevo.** Evaluar una política es un sistema lineal: se despeja. La ecuación de Bellman tiene un máximo en cada renglón, así que no es lineal. Y el pasillo tiene lazos, así que la pasada hacia atrás de la escalera no sirve: $V(1)$ depende de sí mismo. La salida es la de @mkv-c3-def-punto-fijo: tomar el lado derecho como una regla y aplicarla una y otra vez.

---

## 1 · Iterar la ecuación de Bellman a mano

**Piensa: si no puedes despejar $V^*$, ¿qué haces con una estimación que no es la buena?**

Le aplicas el lado derecho de Bellman y obtienes otra estimación. Repetirlo es la **iteración de valores** (*value iteration*).

> **Dado:** un MDP finito $\langle\mathcal S,\mathcal A,P,r\rangle$ con terminales $\mathcal F$ de valor 0, que cumple la condición de @mkv-c3-teo-bellman, y una tolerancia $\mathrm{tol}>0$.
>
> **Encontrar:** una estimación de ${V^*(s)}$ para cada ${s\in\mathcal T}$ y una política codiciosa respecto a ella.

La ecuación, de @mkv-c3-teo-bellman, para cada ${s\in\mathcal T}$ y con ${V=0}$ en $\mathcal F$:

$$
\begin{aligned}
V(s)=\max_{a\in\mathcal A(s)}\Big[&r(s,a)\\
&+\sum_{s'}P(s'\mid s,a)\,V(s')\Big].
\end{aligned}
$$

Una **ronda** reemplaza el lado izquierdo por el derecho, en todos los estados a la vez. El superíndice $(k)$ cuenta rondas del algoritmo; en las clases 1 y 2, $k$ era el número de estados.

$$
\begin{aligned}
V^{(k+1)}(s)=\max_{a\in\mathcal A(s)}\Big[&r(s,a)\\
&+\sum_{s'}P(s'\mid s,a)\,V^{(k)}(s')\Big].
\end{aligned}
$$

> [!NOTE]
> **Qué cuenta la $k$: pasos que quedan.** Desde ${V^{(0)}=0}$, ${V^{(k)}(s)}$ es lo mejor desde $s$ si solo quedan $k$ pasos. Con ${k+1}$ pasos gastas uno (eliges $a$, pagas ${r(s,a)}$, caes en $s'$) y te quedan $k$: ${V^{(k)}(s')}$. Es la pasada hacia atrás de [[mkv-la-escalera|la escalera]], ahora con azar.
>
> **En la casilla 2 del pasillo.** Con 0 pasos no haces nada: ${V^{(0)}=(0,0)}$. Con uno, ${V^{(1)}(2)=\max(-3,-1)=-1}$: correr, porque si resbalas ya no quedan pasos. Con dos, ${V^{(2)}(2)=\max(-3,\,-1+\tfrac12(-1))=-\tfrac32}$. Al crecer $k$, el valor se acerca a ${V^*(2)=-2}$.

> [!WARNING]
> **Leer ${V^{(k)}}$ como el valor en el turno $k$ del robot.** La $k$ es la ronda del algoritmo, no el turno $t$ del robot; el turno sigue siendo $t$, como en $S_t$ y $A_t$.

- **Síncrona.** El lado derecho usa solo valores de la ronda $k$, aunque ya hayas calculado otro estado de la ronda ${k+1}$.

**En el juguete.** En el pasillo mojado, ${\mathcal T=\{1,2\}}$. Con $P_{\text{caminar}}$ y $P_{\text{correr}}$ de [[mkv-el-mdp|El MDP]], cada ronda es:

$$
\begin{aligned}
V^{(k+1)}(2)&=\max\big(-3,\ -1+\tfrac12V^{(k)}(2)\big),\\
V^{(k+1)}(1)&=\max\big(-3+V^{(k)}(2),\\
&\qquad -6+\tfrac12V^{(k)}(1)+\tfrac12V^{(k)}(2)\big).
\end{aligned}
$$

El primer término es caminar y el segundo, correr. La meta aporta 0. Desde ${V^{(0)}=(0,0)}$:

- **Ronda 1.** En 2: ${\max(-3,-1)=-1}$. En 1: ${\max(-3+0,\,-6)=-3}$. Queda ${V^{(1)}=(-3,-1)}$.
- **Ronda 2.** En 2: ${\max(-3,\,-1-\tfrac12)=-\tfrac32}$. En 1: ${\max(-3-1,\,-6-\tfrac32-\tfrac12)=-4}$.

- **Residuo.** ${\operatorname{res}^{(k)}=\max_s\lvert V^{(k)}(s)-V^{(k-1)}(s)\rvert}$: el mayor cambio que hizo la ronda $k$.

::: table {#mkv-c3-vi-tabla-traza title="Traza de la iteración de valores en el pasillo mojado"}
| $k$ | $V^{(k)}(1)$ | $V^{(k)}(2)$ | $\operatorname{res}^{(k)}$ |
|---|---|---|---|
| 0 | 0 | 0 | — |
| 1 | −3 | −1 | 3 |
| 2 | −4 | −3/2 | 1 |
| 3 | −9/2 | −7/4 | 1/2 |
| 4 | −19/4 | −15/8 | 1/4 |
| 5 | −39/8 | −31/16 | 1/8 |
| 6 | −79/16 | −63/32 | 1/16 |
:::

- **La fórmula.** ${V^{(k)}(2)=-2+2^{1-k}}$ para ${k\ge0}$, y ${V^{(k)}(1)=-5+2^{2-k}}$ para ${k\ge1}$.
- **Nunca llega.** La distancia a ${V^*=(-5,-2)}$ pasa de 5 a 2 en la ronda 1; desde ahí, cada ronda la corta a la mitad, y ninguna ronda finita la cierra. Es la telaraña de @mkv-c3-def-punto-fijo, ahora en dos estados.
- **La política sí llega.** En toda ronda, el máximo en 1 lo da caminar y el máximo en 2 lo da correr: la codiciosa ya es caminar–correr.

::: figure {#mkv-c3-fig-iterar-valores title="Los valores contra la ronda en el pasillo mojado"}
![Gráfica de V(1) y V(2) contra la ronda k, de 0 a 6. V(1) baja de 0 a −3, −4, −4.5 y sigue hacia la línea punteada en −5; V(2) baja de 0 a −1, −1.5, −1.75 y sigue hacia la línea punteada en −2. Ninguna curva toca su línea; desde la ronda 1, la distancia se corta a la mitad en cada ronda](../_assets/mkv-c3-iterar-valores.svg)
:::

> [!WARNING]
> **Actualizar en el lugar sin decirlo.** Si en la ronda 1 calculas primero ${V(2)=-1}$ y lo usas en seguida para 1, obtienes ${V(1)=-4}$, no $-3$. Esa variante también converge, pero su traza es otra.
> **En la versión síncrona, todo el lado derecho usa la ronda anterior.**

::: exercise {#mkv-c3-vi-ej-ronda-7 title="Haz la ronda 7"}
Con ${V^{(6)}=(-79/16,\,-63/32)}$ de la traza, calcula ${V^{(7)}}$ y ${\operatorname{res}^{(7)}}$. ¿Qué acción da el máximo en cada casilla?
:::

::: hint {#mkv-c3-vi-pista-ronda-7 of="mkv-c3-vi-ej-ronda-7" title="¿Qué valores entran al lado derecho?"}
¿Usas ${V^{(6)}}$ en los dos renglones, aunque ya tengas ${V^{(7)}(2)}$?
:::

::: answer {#mkv-c3-vi-resp-ronda-7 of="mkv-c3-vi-ej-ronda-7"}
En 2: ${\max(-3,\,-1-\tfrac{63}{64})=-\tfrac{127}{64}}$, con correr. En 1: caminar da ${-3-\tfrac{63}{32}=-\tfrac{159}{32}}$ y correr da ${-6-\tfrac{79}{32}-\tfrac{63}{64}=-\tfrac{605}{64}}$; gana caminar. Queda ${V^{(7)}=(-159/32,\,-127/64)}$ y ${\operatorname{res}^{(7)}=1/32}$, el cambio en la casilla 1. Coincide con la fórmula para ${k=7}$.
:::

A mano bastan dos estados; para muchos hace falta escribir la ronda como un procedimiento que además sepa parar.

---

## 2 · Calcular con ITERACIÓN DE VALORES

**Piensa: ¿qué necesita guardar un programa entre una ronda y la siguiente?**

Solo la estimación de la ronda anterior. Con ella arma la nueva, mide cuánto cambió y decide si sigue.

### El mapa de ITERACIÓN DE VALORES

- **Qué calcula:** las rondas ${V^{(1)},V^{(2)},\dots}$ desde ${V^{(0)}=0}$, y al final la política codiciosa de la última.
- **Qué guarda:** la estimación $V$ de la ronda anterior, la nueva $W$ y el residuo.
- **Cómo avanza:** en cada ronda, para cada estado de $\mathcal T$, toma el máximo sobre las acciones de ${r(s,a)}$ más lo que se espera de $V$ en el destino.
- **A qué converge y bajo qué condición:** a $V^*$, si se cumple la condición de @mkv-c3-teo-bellman (@mkv-c3-teo-iterar-valores). Para cuando el residuo baja de $\mathrm{tol}$.

::: figure {#mkv-c3-fig-flujo-valores title="Iteración de valores, en palabras"}
![Diagrama de flujo de la iteración de valores, en palabras. 1: Empieza con V = 0 en todos los estados. 2: Para cada estado no terminal, calcula el mejor «recompensa ahora más lo que se espera después» usando la V anterior. 3: Mide el residuo, el mayor cambio entre la V anterior y la nueva. 4: Reemplaza la V anterior por la nueva. 5, pregunta: ¿el residuo es a lo más tol? Si no, regresa al paso 2. Si sí, 6: en cada estado elige la acción que da ese máximo y devuelve V y la política](../_assets/mkv-c3-flujo-valores.svg)
:::

```text
INPUT   MDP finito ⟨𝒮, 𝒜, P, r⟩; meta 𝓕
        con valor 0; tol > 0.
OUTPUT  V ≈ V* en 𝒯 y su política
        codiciosa π.

 1 function ITERAR-VALORES(MDP, tol)
 2   V(s) ← 0 para todo s        (V⁽⁰⁾)
 3   repeat
 4     para cada s en 𝒯:
 5       W(s) ← max sobre a de r(s,a)
               + Σ_s' P(s'|s,a) V(s')
 6     res ← max_s |W(s) − V(s)|
 7     V ← W               (síncrona)
 8   until res ≤ tol
 9   π(s) ← la a que da el máximo de
            r(s,a) + Σ_s' P(s'|s,a) V(s'),
            con la V final
10   return V, π
```

**Gemelo Python.** Cada comentario numerado remite al pseudocódigo. `pasillo(n)` arma el pasillo de $n$ casillas: hay hueco en la casilla $i$ si ${i\equiv1\pmod 3}$, así que con ${n=2}$ es el juguete. Correr en un hueco cuesta 1 más el castigo de 10 con probabilidad $1/2$: ${-6}$ en promedio.

```python
from fractions import Fraction as F

ACCIONES = ("caminar", "correr")

def pasillo(n, castigo=10):
    """Casillas 1..n; la meta es n + 1."""
    P, r = {}, {}
    for i in range(1, n + 1):
        hueco = i % 3 == 1         # sin barandal
        P[i, "caminar"] = {i + 1: F(1)}
        r[i, "caminar"] = F(-3)
        P[i, "correr"] = {i: F(1, 2), i + 1: F(1, 2)}
        r[i, "correr"] = -1 - F(castigo, 2) * hueco
    return list(range(1, n + 1)), P, r

def q(P, r, V, s, a):              # la meta vale 0
    return r[s, a] + sum(p * V.get(t, 0)
                         for t, p in P[s, a].items())

def iterar_valores(S, P, r, tol, cero):
    V = {s: cero for s in S}                     # (2)
    traza = [V]
    while True:                                  # (3)
        W = {s: max(q(P, r, V, s, a)
                    for a in ACCIONES)
             for s in S}                         # (4)(5)
        res = max(abs(W[s] - V[s]) for s in S)   # (6)
        V = W                                    # (7)
        traza.append(V)
        if res <= tol:                           # (8)
            break
    pi = {s: max(ACCIONES,
                 key=lambda a: q(P, r, V, s, a))
          for s in S}                            # (9)
    return traza, pi                             # (10)

S, P, r = pasillo(2)
traza, pi = iterar_valores(S, P, r, F(1, 16), F(0))
for k, V in enumerate(traza):
    print(k, V[1], V[2])
print(pi)
# 0 0 0
# 1 -3 -1
# 2 -4 -3/2
# 3 -9/2 -7/4
# 4 -19/4 -15/8
# 5 -39/8 -31/16
# 6 -79/16 -63/32
# {1: 'caminar', 2: 'correr'}
```

**Cada pieza, en su línea:**

- **Línea 2.** `cero` decide la aritmética: `F(0)` da fracciones exactas, como en la traza; `0.0` da decimales, como en el pasillo grande.
- **Líneas 4 y 5.** `W` se arma completo desde `V` antes de reemplazarlo: eso la hace síncrona.
- **Línea 9.** Recalcula el máximo con la `V` final, no reusa el de la última ronda: las dos políticas pueden diferir. `max` con `key` devuelve la primera acción que alcanza el máximo: en un empate conserva caminar.
- **Dos atajos del pasillo.** Las acciones son las mismas en todo estado (`ACCIONES`, no ${\mathcal A(s)}$), y la función devuelve la traza entera en lugar de $V$: su último elemento es $V$.

::: exercise {#mkv-c3-vi-ej-tol title="Elige la tolerancia"}
Con ${\mathrm{tol}=1/16}$ la llamada para en la ronda 6. ¿Qué valores de `tol` la harían parar justo en la ronda 4?
:::

::: hint {#mkv-c3-vi-pista-tol of="mkv-c3-vi-ej-tol" title="¿Qué compara la línea 8?"}
¿Qué residuo tiene que pasar la prueba de la línea 8, y cuál tiene que fallarla?
:::

::: answer {#mkv-c3-vi-resp-tol of="mkv-c3-vi-ej-tol"}
Para en la ronda 4 si ${\operatorname{res}^{(4)}=1/4\le\mathrm{tol}}$ y ${\operatorname{res}^{(3)}=1/2>\mathrm{tol}}$: cualquier ${\mathrm{tol}}$ con ${1/4\le\mathrm{tol}<1/2}$.
:::

### Lo que garantiza y cuánto cuesta

::: theorem {#mkv-c3-teo-iterar-valores title="La iteración de valores converge al valor óptimo"}
Sea un MDP finito con terminales $\mathcal F$ de valor 0.

**Condición.** La de @mkv-c3-teo-bellman: existe una política que termina con probabilidad 1, y toda política estacionaria que no termina vale $-\infty$ en algún estado.

Entonces, desde cualquier ${V^{(0)}}$ finito, ${V^{(k)}(s)\to V^*(s)}$ para todo ${s\in\mathcal T}$. Y tras un número finito de rondas, toda política codiciosa de ${V^{(k)}}$ es óptima.

Si además ${V^{(0)}=0}$ y ${r\le0}$, entonces ${V^{(k)}(s)}$ es lo mejor que se espera cobrar en a lo más $k$ pasos, y baja monótona: ${V^{(k+1)}(s)\le V^{(k)}(s)}$.

**Lectura.** Es el recuadro «Qué cuenta la $k$» de la sección 1: cada ronda agrega un paso de futuro; con suficientes pasos, lo que queda después pesa cada vez menos.

**Casos nulos.** Sin ciclos, como en la escalera, ${V^{(k)}=V^*}$ exacto a más tardar cuando $k$ alcanza el camino más largo: 5 rondas desde el escalón 0. Si toda acción lleva directo a $\mathcal F$, basta una ronda.
:::

::: proof {#mkv-c3-vi-dem-iterar-valores of="mkv-c3-teo-iterar-valores"}
**Lo mejor en $k$ pasos.** Por inducción. Con 0 pasos no se cobra nada: ${V^{(0)}=0}$. Con ${k+1}$ pasos, condiciona en el primero (@mkv-c2-teo-primer-paso): cobras ${r(s,a)}$ y desde donde caes te quedan $k$ pasos, que valen a lo más ${V^{(k)}}$. Elegir la mejor primera acción es el máximo de la ronda.

**Monótona.** Una ronda respeta el orden: si ${U\le W}$ en todo estado, la ronda desde $U$ da a lo más la ronda desde $W$, porque las probabilidades no son negativas. Como ${r\le0}$, ${V^{(1)}\le0=V^{(0)}}$; aplicando la ronda a los dos lados, ${V^{(k+1)}\le V^{(k)}}$ para todo $k$.

**Converge.** Para el caso general, la demostración está en Bertsekas y Tsitsiklis, «An analysis of stochastic shortest path problems» (*Mathematics of Operations Research*, 1991). Cuando toda política termina, la sección 3 da una prueba completa: la suma de los residuos es finita.

**La política.** Hay un número finito de acciones. Una acción que no da el máximo en la ecuación de Bellman queda abajo de él por una distancia fija; cuando ${V^{(k)}}$ está más cerca que eso de $V^*$, ya no puede ganar. Lo que sí gana da una codiciosa de $V^*$, óptima por @mkv-c3-teo-codiciosa.
:::

- **Número que da.** En el pasillo mojado, ${V^{(6)}=(-79/16,\,-63/32)}$, a $1/16$ de ${V^*=(-5,-2)}$; la codiciosa es caminar–correr desde la ronda 0.
- **Costo por ronda.** Cada estado recorre cada acción y cada destino: del orden de ${\lvert\mathcal T\rvert\cdot\lvert\mathcal A\rvert\cdot\lvert\mathcal S\rvert}$ operaciones. Si cada acción tiene pocos destinos, como en el pasillo, es del orden de ${\lvert\mathcal T\rvert\cdot\lvert\mathcal A\rvert}$.
- **Número de rondas.** Lo decide $\mathrm{tol}$, no el número de políticas. Con ciclos no hay garantía de llegar exacto: en el pasillo mojado, desde 0, ninguna ronda finita da $V^*$.
- **Supuestos.** El MDP es finito y conocido: $P$ y $r$ están en la mesa.

El teorema dice que converge, pero no cuándo parar. Para eso hay que leer el residuo.

---

## 3 · Decidir cuándo parar

**Piensa: el algoritmo para cuando el residuo es chico; ¿garantiza eso que el error es chico?**

No por sí solo. Un residuo chico dice que la última ronda movió poco, no que falta poco. Hace falta un factor que traduzca uno en el otro.

::: figure {#mkv-c3-fig-residuo title="El residuo por ronda, en escala logarítmica"}
![Gráfica en escala logarítmica del residuo del pasillo mojado contra la ronda k: 3 en la ronda 1, y desde ahí 1, 1/2, 1/4, 1/8 y 1/16. Desde la ronda 2 los puntos caen sobre una recta: el residuo se divide entre 2 en cada ronda. Una línea horizontal marca tol](../_assets/mkv-c3-residuo.svg)
:::

**En el juguete.** La distancia a $V^*$ en la ronda $k$ es ${\max(2^{2-k},2^{1-k})=2^{2-k}}$, y el residuo también es $2^{2-k}$ desde ${k\ge2}$. Aquí error y residuo coinciden. Eso es suerte del juguete.

::: theorem {#mkv-c3-vi-teo-cota title="Una cota del error con el residuo"}
**Condición.** Existen un número de pasos $m$ y una probabilidad ${\beta<1}$ tales que, con **cualquier** sucesión de acciones y desde cualquier estado de $\mathcal T$, la probabilidad de seguir sin terminar tras $m$ pasos es a lo más $\beta$. Esta $m$ no es el tiempo medio $m(s)$ de la clase 2, y $\beta$ no es la de alfa-beta.

Entonces, en toda ronda $k$, ${\max_s\lvert V^*(s)-V^{(k)}(s)\rvert\le\tfrac{m}{1-\beta}\operatorname{res}^{(k)}}$.

**Lectura.** Si el residuo es a lo más $\mathrm{tol}$, el error es a lo más ${\tfrac{m}{1-\beta}\,\mathrm{tol}}$. Para garantizar un error ${\varepsilon}$, se pide ${\mathrm{tol}=\tfrac{1-\beta}{m}\,\varepsilon}$.

**Casos nulos.** Si toda acción termina en un paso, ${m=1}$ y ${\beta=0}$: el error es a lo más el residuo.
:::

::: proof {#mkv-c3-vi-dem-cota of="mkv-c3-vi-teo-cota"}
**Una ronda no agranda diferencias.** Para dos estimaciones $U$ y $W$, la diferencia de sus rondas en $s$ es a lo más ${\max_a\sum_{s'}P(s'\mid s,a)\lvert U(s')-W(s')\rvert}$. Las probabilidades suman a lo más 1 y en la meta las dos valen 0: queda a lo más ${\max\lvert U-W\rvert}$. Aplicado a ${V^{(k)}}$ y ${V^{(k-1)}}$, cada residuo es a lo más el anterior.

**$m$ rondas la encogen por $\beta$.** Tras $m$ rondas, la diferencia en $s$ es a lo más un promedio de ${\lvert U-W\rvert}$ sobre donde quedas tras $m$ pasos sin terminar. Eso pesa a lo más $\beta$. Entonces ${\operatorname{res}^{(k+jm+i)}\le\beta^j\operatorname{res}^{(k)}}$ para ${1\le i\le m}$.

**Sumar.** Como ${V^{(k)}\to V^*}$, el error es a lo más la suma de los residuos que faltan. En bloques de $m$:

$$
\begin{aligned}
\sum_{\ell>k}\operatorname{res}^{(\ell)}
&\le m\,\operatorname{res}^{(k)}\,(1+\beta+\beta^2+\cdots)\\
&=\frac{m}{1-\beta}\operatorname{res}^{(k)}.
\end{aligned}
$$

La misma suma finita prueba que ${V^{(k)}}$ converge cuando toda política termina.
:::

**En el juguete.** Con cualquier sucesión de acciones, desde la casilla 1 la probabilidad de no haber terminado tras 3 pasos es a lo más $1/2$. Con ${m=3}$ y ${\beta=1/2}$, el factor es ${3/(1/2)=6}$: el error es a lo más 6 veces el residuo. Con ${m=2}$ el peor caso es ${\beta=3/4}$ y el factor sube a 8. La cota es holgada, pero segura.

> [!TIP]
> **Ejemplo y contraejemplo de «el error es igual al residuo».**
>
> - **Lo cumple:** en el pasillo mojado, el error desde la ronda 2 es igual a ${\operatorname{res}^{(k)}}$; un residuo de $1/16$ deja un error de $1/16$.
> - **No lo cumple:** un estado con un lazo que lo regresa a sí mismo con probabilidad $99/100$, con ${r=-1}$ y la meta con $1/100$. Ahí ${V^*=-100}$; desde 0, ${V^{(k)}=-100\,(1-0.99^k)}$, el residuo es $0.99^{k-1}$ y el error es **99 veces el residuo**. Un residuo de 0.001 esconde un error de 0.099. La condición de la cota sí se cumple, con factor 100.

::: figure {#mkv-c3-fig-ej-paro title="Residuo chico no es error chico"}
![Dos paneles con escala logarítmica, error y residuo contra la ronda. Arriba, marcado como cumple, el pasillo mojado: desde la ronda 2 las curvas de error y de residuo van encimadas, el error es igual al residuo. Abajo, marcado como no cumple, el estado con lazo 99/100 y recompensa −1: las dos curvas bajan muy despacio y la del error va siempre 99 veces arriba de la del residuo. Pie: parar con residuo chico no garantiza error chico sin el factor de la cota](../_assets/mkv-c3-ej-paro.svg)
:::

> [!WARNING]
> **Parar con $\mathrm{tol}$ y reportar $\mathrm{tol}$ como error.** En el lazo, ${\mathrm{tol}=0.001}$ para en la ronda 689 con un error de 0.0983, no de 0.001.
> **El error garantizado es ${\tfrac{m}{1-\beta}\,\mathrm{tol}}$: a mayor probabilidad de no terminar, más rondas hacen falta.**

::: exercise {#mkv-c3-vi-ej-lazo title="Aplica la cota al lazo"}
En el estado con lazo $99/100$, ¿qué $m$ y qué $\beta$ cumplen la condición de la cota? ¿Qué factor da, y qué tan cerca queda del 99 real?
:::

::: hint {#mkv-c3-vi-pista-lazo of="mkv-c3-vi-ej-lazo" title="¿Cuántas acciones hay para elegir?"}
Si hay una sola acción, ¿cuál es la probabilidad de seguir sin terminar tras un paso?
:::

::: answer {#mkv-c3-vi-resp-lazo of="mkv-c3-vi-ej-lazo"}
Hay una sola acción, así que basta ${m=1}$ con ${\beta=99/100}$. El factor es ${1/(1/100)=100}$: el error es a lo más 100 veces el residuo. El real es 99, así que aquí la cota es casi exacta. En el pasillo mojado, en cambio, da 6 contra un factor real de 1.
:::

Con la regla de paro completa, falta probar el algoritmo donde enumerar políticas es imposible.

---

## 4 · Comprobar en un pasillo de 200 casillas

**Piensa: con $2^{200}$ políticas, ¿cómo encuentras la mejor sin revisarlas?**

No las revisas. La iteración de valores trabaja con 200 números por ronda, no con políticas.

**El caso grande.** El PASILLO tiene casillas 1 a 200 y la meta en 201. Hay hueco sin barandal en la casilla $i$ si ${i\equiv1\pmod3}$, y barandal en las demás. Caminar cuesta 3; correr cuesta 1, resbala con $1/2$ y en un hueco suma el castigo de 10. Son las reglas del pasillo mojado, repetidas.

```python
S, P, r = pasillo(200)
traza, pi = iterar_valores(S, P, r, 1e-9, 0.0)
print(len(traza) - 1, round(traza[-1][1]))
print(all(pi[i] == ("caminar" if i % 3 == 1
                    else "correr") for i in S))
# 451 -467
# True
```

- **Lectura.** Con ${\mathrm{tol}=10^{-9}}$, el algoritmo para tras 451 rondas, con ${V^{(451)}(1)\approx-467}$; el valor óptimo exacto es ${V^*(1)=-467}$.
- **La política.** El `True` dice que la codiciosa camina junto a cada hueco y corre junto a cada barandal. Nadie le dio esa regla al algoritmo: salió del máximo.
- **El costo.** Cada ronda hace 200 casillas × 2 acciones × a lo más 2 destinos. Enumerar $2^{200}\approx1.6\times10^{60}$ políticas, en cambio, no termina en ninguna computadora.

::: figure {#mkv-c3-fig-pasillo-largo title="La política y el valor óptimos en el pasillo de 200 casillas"}
![Arriba, una franja de 200 casillas coloreada por la acción que elige la iteración de valores: caminar en las casillas con hueco, 1, 4, 7 y así cada tres, y correr en las de barandal. Abajo, el valor óptimo de cada casilla: sube en escalones desde la casilla 1 hasta 0 en la meta, 201, con un escalón más alto en cada casilla con hueco](../_assets/mkv-c3-pasillo-largo.svg)
:::

**Lo que tarda.** Como en el juguete, la codiciosa es óptima desde la ronda 0: la decisión es local, hueco o barandal. Lo que tarda son los **valores**: la información de la meta avanza a lo más una casilla por ronda, así que las primeras casillas tardan en «verla».

::: exercise {#mkv-c3-vi-ej-200 title="Cuenta las rondas mínimas"}
Explica por qué, en el pasillo de 200 casillas, el residuo es al menos 1 en cada ronda ${k\le200}$. ¿Qué dice eso de las rondas necesarias con ${\mathrm{tol}=10^{-9}}$?
:::

::: hint {#mkv-c3-vi-pista-200 of="mkv-c3-vi-ej-200" title="¿Llegas a la meta en pocos pasos?"}
Lee ${V^{(k)}(1)}$ como lo mejor en $k$ pasos. Desde la casilla 1, ¿cuántos pasos necesitas como mínimo para llegar a 201, y cuánto cuesta, como mínimo, cada paso?
:::

::: answer {#mkv-c3-vi-resp-200 of="mkv-c3-vi-ej-200"}
Desde la casilla 1 hacen falta al menos 200 pasos para llegar a la meta, porque cada paso avanza a lo más una casilla. Con ${k\le200}$ pasos, los primeros ${k-1}$ nunca terminan y cada uno cuesta al menos 1.

Toma el mejor plan de $k$ pasos: sus primeros ${k-1}$ pasos valen a lo más ${V^{(k-1)}(1)}$, y el último cuesta al menos 1. Entonces ${V^{(k)}(1)\le V^{(k-1)}(1)-1}$ y ${\operatorname{res}^{(k)}\ge1}$. Con ${\mathrm{tol}=10^{-9}}$, el algoritmo hace más de 200 rondas.
:::

Ahora cambia el punto de partida y mira qué del teorema se sostiene.

---

## Ejercicios

::: exercise {#mkv-c3-vi-ej-arranque title="Arranca desde una estimación equivocada"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Usa el pasillo mojado de dos casillas. **Cambia una idea:** el punto de partida. En lugar de ${V^{(0)}=(0,0)}$, empieza en ${V^{(0)}=(-8,-8)}$, una estimación demasiado pesimista.

1. **Traza.** Corre tres rondas síncronas y escribe ${V^{(1)}}$, ${V^{(2)}}$ y ${V^{(3)}}$.
2. **¿Monótona?** ¿Los valores bajan, suben o ninguna de las dos? ¿Contradice eso a @mkv-c3-teo-iterar-valores?
3. **La codiciosa.** Escribe la codiciosa de ${V^{(0)}}$ y la de ${V^{(1)}}$. ¿Cuál es óptima?
4. **Paro.** Calcula ${\operatorname{res}^{(3)}}$ y el error en la ronda 3. ¿Lo respeta la cota con ${m=3}$, ${\beta=1/2}$?
5. **Explica.** ¿Por qué la cota no depende del punto de partida?
:::

::: hint {#mkv-c3-vi-pista-arranque-1 of="mkv-c3-vi-ej-arranque" title="Pista 1 · ¿Qué entra en cada renglón de la ronda?"}
Escribe los dos renglones de la ronda del juguete con los números de ${V^{(0)}}$. En la casilla 2 caminar lleva a la meta, que vale 0 aunque arranques en $-8$. ¿Qué acción da el máximo en cada renglón?
:::

::: hint {#mkv-c3-vi-pista-arranque-2 of="mkv-c3-vi-ej-arranque" title="Pista 2 · ¿Cómo sabes que tu traza va bien?"}
¿Se acerca a ${(-5,-2)}$? ¿Tu residuo de la ronda 1 sale del cambio en la casilla 2? ¿La condición de la cota habla de valores o solo de probabilidades?
:::

::: answer {#mkv-c3-vi-resp-arranque of="mkv-c3-vi-ej-arranque" title="Respuesta · Desde una estimación equivocada"}
**1. Traza.**

- **Ronda 1.** En 2: ${\max(-3,\,-1-4)=-3}$. En 1: ${\max(-3-8,\,-6-4-4)=-11}$. Queda ${V^{(1)}=(-11,-3)}$, con ${\operatorname{res}^{(1)}=5}$, el cambio en la casilla 2.
- **Ronda 2.** En 2: ${\max(-3,\,-1-\tfrac32)=-\tfrac52}$. En 1: ${\max(-3-3,\,-6-\tfrac{11}2-\tfrac32)=-6}$. Queda ${V^{(2)}=(-6,-5/2)}$.
- **Ronda 3.** En 2: ${\max(-3,\,-1-\tfrac54)=-\tfrac94}$. En 1: ${\max(-3-\tfrac52,\,-6-3-\tfrac54)=-\tfrac{11}2}$. Queda ${V^{(3)}=(-11/2,-9/4)}$.

**2. Ninguna de las dos.** ${V(2)}$ sube: $-8$, $-3$, $-5/2$, $-9/4$. ${V(1)}$ primero baja a $-11$, porque usa el $-8$ viejo de la casilla 2, y luego sube. No contradice el teorema: la monotonía solo se promete desde ${V^{(0)}=0}$ con ${r\le0}$; la convergencia, desde cualquier arranque finito.

**3. La codiciosa.** Con ${V^{(0)}=(-8,-8)}$, en 1 caminar da $-11$ contra $-14$, y en 2 caminar da $-3$ contra $-5$: caminar–caminar, que no es óptima. Es el contraejemplo de la codiciosa de [[mkv-bellman|La ecuación de Bellman]]. Con ${V^{(1)}=(-11,-3)}$, en 2 correr da $-5/2$ contra $-3$, y en 1 caminar da $-6$ contra $-13$: caminar–correr, la óptima.

**4. Paro.** ${\operatorname{res}^{(3)}=\max(\tfrac12,\tfrac14)=\tfrac12}$. El error es ${\max(\lvert-5+\tfrac{11}2\rvert,\lvert-2+\tfrac94\rvert)=\tfrac12}$. La cota da ${6\cdot\tfrac12=3\ge\tfrac12}$: se cumple.

**5. Explica.** $m$ y $\beta$ hablan solo de las probabilidades de terminar, y la prueba compara dos rondas cualesquiera. El arranque cambia los residuos, pero no el factor que los traduce en error.
:::

**Punto de control:** deberías poder escribir una ronda síncrona de la iteración de valores y correrla a mano en un MDP chico. También, decir qué significa ${V^{(k)}}$ desde 0, aplicar @mkv-c3-teo-iterar-valores con su condición, y traducir un residuo en una cota del error con $m$ y $\beta$.

---

## Lo que hay que llevarse

- **La idea.** No se despeja $V^*$: se aplica el lado derecho de Bellman una y otra vez, en todos los estados con la ronda anterior.
- **El significado.** Desde 0, ${V^{(k)}(s)}$ es lo mejor en $k$ pasos y baja monótona hacia $V^*$.
- **El juguete.** ${V^{(k)}(1)=-5+2^{2-k}}$ y ${V^{(k)}(2)=-2+2^{1-k}}$: se acerca a ${(-5,-2)}$ sin llegar; la codiciosa es caminar–correr desde la ronda 0.
- **El teorema.** Bajo la condición de @mkv-c3-teo-bellman converge desde cualquier arranque, y tras rondas finitas la codiciosa es óptima (@mkv-c3-teo-iterar-valores).
- **Cuándo parar.** El error es a lo más ${\tfrac{m}{1-\beta}\operatorname{res}^{(k)}}$: factor 6 en el juguete. En el lazo $99/100$ el error real es 99 veces el residuo.
- **El caso grande.** En el pasillo de 200 casillas, 451 rondas dan ${V^{(451)}(1)\approx V^*(1)=-467}$ y la regla local, sin revisar $2^{200}$ políticas.

Los valores nunca llegan, pero la política llegó desde el principio. ¿Se puede llegar en un número finito de rondas?

Continúa con [[mkv-iterar-politicas|Iteración de políticas]].
