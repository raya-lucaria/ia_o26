---
id: mkv-mdp-lineal
title: "El MDP como programa lineal"
nav_title: "Como programa lineal"
summary: "Bellman como un programa lineal: minimizar la suma de los valores sujeta a una desigualdad por estado y acción, resuelto con linprog."
status: ready
estimated_time: 18m
tags: [markov, decidir, programacion-lineal, optimizacion]
---

# El MDP como programa lineal

**¿Se puede resolver la ecuación de Bellman con un solver de programación lineal, como los de la unidad 6?**

Al terminar tendrás:

- **Un modelo.** Cambiarás cada máximo de Bellman por una desigualdad por estado y acción.
- **El teorema y su condición.** Aplicarás @mkv-c3-teo-lineal: el mínimo de la suma es $V^*$.
- **Una cuenta a mano.** Dibujarás la región del pasillo y encontrarás su mínimo, ${V^*=(-5,-2)}$.
- **El algoritmo PL-BELLMAN.** Armarás las restricciones y llamarás a `linprog` sin cotas.
- **Una lectura de la política.** Sacarás $\pi^*$ de las restricciones que quedan con igualdad.

## Lo que traes

**Qué V usa esta página.** $V(s)$ a secas es la **incógnita** del programa lineal: unos números por encontrar. $V^*$ es el óptimo, y el teorema dice que la solución es $V^*$. $V_\pi$ aparece solo al evaluar una política fija.

- **El óptimo.** $V^*(s)$ es lo que vale $s$ con la mejor política. $Q^*(s,a)$ es lo que vale empezar con $a$ y seguir óptimo (@mkv-c3-def-q, @mkv-c3-def-optimo).
- **Bellman.** En [[mkv-bellman|La ecuación de Bellman]] buscábamos números $V(s)$ con ${V(s)=\max_a(\text{lado derecho})}$. Bajo las condiciones de @mkv-c3-teo-bellman, la única solución es $V^*$. El lado derecho de $(s,a)$ es ${r(s,a)+\sum_{s'}P(s'\mid s,a)V(s')}$.
- **Evaluar.** Si una política fija $\pi$ termina con probabilidad 1, su valor $V_\pi$ es la única solución de ${V_\pi=r_\pi+P_{\pi,\mathcal T}V_\pi}$ (@mkv-c3-teo-evaluar).
- **El pasillo.** En [[mkv-el-mdp|El proceso de decisión de Markov]]: caminar cuesta 3; correr cuesta 1 y resbala con $1/2$; en la casilla 1 resbalar cuesta 10 más.
- **Programación lineal.** En [[patrones-lineales|Patrones lineales]] viste `linprog`, que minimiza, y su convención de signos (@opt-signos). Un punto factible cumple todas las restricciones (@opt-factible).

> [!NOTE]
> **Por qué nos importa.** Iterar valores da aproximaciones $V^{(k)}$ que se acercan a $V^*$ sin llegar. Iterar políticas resuelve un sistema por ronda. Un programa lineal (*linear program*) deja el trabajo a un solver ya hecho. El solver entrega $V^*$ de una vez.

---

## 1 · Escribir Bellman con desigualdades

**Piensa: ¿qué dice ${x=\max(a,b)}$ en términos de desigualdades?**

Dice tres cosas:

- $x$ es mayor o igual que $a$: ${x\ge a}$.
- $x$ es mayor o igual que $b$: ${x\ge b}$.
- $x$ toca a alguna de las dos.

Las dos primeras son lineales; la tercera no. El truco: quedarse con las lineales y recuperar la tercera minimizando.

> **Dado:** un MDP finito con terminales $\mathcal F$ y no terminales $\mathcal T$ que cumple las condiciones de @mkv-c3-teo-bellman.
>
> **Encontrar:** $V^*$ sobre $\mathcal T$ como solución de un programa lineal.

::: theorem {#mkv-c3-teo-lineal title="El valor óptimo es el mínimo de un programa lineal"}
Sea un MDP $\langle\mathcal S,\mathcal A,P,r\rangle$. Las incógnitas son números $V(s)$, uno por estado, con ${V=0}$ en $\mathcal F$. El programa lineal es

$$
\begin{aligned}
\text{minimizar}\quad&\sum_{s\in\mathcal T}V(s)\\
\text{sujeto a}\quad&V(s)\ge r(s,a)\\
&\qquad+\sum_{s'\in\mathcal T}P(s'\mid s,a)\,V(s')\\
&\text{para todo }s\in\mathcal T,\ a\in\mathcal A(s).
\end{aligned}
$$

Las variables son los $V(s)$ con ${s\in\mathcal T}$. No tienen signo fijo.

**Condición.** Las de @mkv-c3-teo-bellman:

- estados y acciones finitos;
- terminales con valor 0;
- alguna política que termina;
- toda política estacionaria que no termina vale $-\infty$ en algún estado.

Entonces el óptimo $V^*$ es la **única** solución óptima del programa.

**Lectura.** Todo punto factible queda arriba de $V^*$ en cada estado. Por eso minimizar la suma lo empuja hasta $V^*$. Cualquier suma con pesos positivos daría lo mismo.

**Casos nulos.** Si cada estado tiene una sola acción, hay una sola política $\pi$. Entonces el mínimo es su valor $V_\pi$, el de @mkv-c3-teo-evaluar.
:::

::: proof {#mkv-c3-lp-dem-lineal of="mkv-c3-teo-lineal"}
**Factible.** $V^*$ es el máximo de los lados derechos. Así que es mayor o igual que cada uno.

**Abajo no hay nada.** Sea $V$ un punto factible cualquiera: números que cumplen todas las restricciones.

- Sea $\pi^*$ la codiciosa de $V^*$ (@mkv-c3-teo-codiciosa). Por la condición, $\pi^*$ termina.
- Por @mkv-c3-teo-evaluar, ${V^*=r_{\pi^*}+P_{\pi^*,\mathcal T}V^*}$.
- Las restricciones con ${a=\pi^*(s)}$ dicen ${V\ge r_{\pi^*}+P_{\pi^*,\mathcal T}V}$.
- Restando, la diferencia cumple ${V-V^*\ge P_{\pi^*,\mathcal T}(V-V^*)}$.
- Las entradas de esa matriz son ${\ge0}$. Así que la desigualdad se conserva al multiplicar: ${V-V^*\ge P_{\pi^*,\mathcal T}^{\,t}(V-V^*)}$ para todo $t$.
- Como $\pi^*$ termina, ${P_{\pi^*,\mathcal T}^{\,t}\to0}$. Queda ${V-V^*\ge0}$.

**Única.** Si un punto factible $V$ no es $V^*$, alguna coordenada es estrictamente mayor. Su suma también lo es.
:::

- **Por qué minimizar.** Maximizar no tiene sentido: la región no tiene techo. Si un punto $V$ es factible, ${V+1}$ también lo es. La razón: las probabilidades hacia $\mathcal T$ suman a lo más 1.
- **Una región que ya viste.** Es el conjunto de soluciones de Bellman con esperar gratis, de [[mkv-bellman|La ecuación de Bellman]]. Ahí la incógnita cumplía ${V(s)=\max(\dots,V(s))}$. Eso solo dice que $V(s)$ es mayor o igual que cada lado derecho. El programa busca la esquina más baja de esa región.
- **Dónde está la acción.** En el óptimo $V^*$, la restricción de $(s,a)$ queda con igualdad justo cuando $a$ es óptima en $s$. Su lado derecho vale $Q^*(s,a)$.

**En el juguete.** Buscamos dos números, $V(1)$ y $V(2)$. Hay cuatro restricciones, una por par:

$$
\begin{aligned}
\text{(1, caminar)}\quad&V(1)\ge-3+V(2),\\
\text{(1, correr)}\quad&V(1)\ge-6+\tfrac12V(1)\\
&\qquad+\tfrac12V(2),\\
\text{(2, caminar)}\quad&V(2)\ge-3,\\
\text{(2, correr)}\quad&V(2)\ge-1+\tfrac12V(2).
\end{aligned}
$$

- **Despejar.** La segunda es ${V(1)\ge V(2)-12}$ y la cuarta es ${V(2)\ge-2}$.
- **Las que mandan.** ${V(2)\ge-2}$ hace sobrar a ${V(2)\ge-3}$. Y ${V(1)\ge V(2)-3}$ hace sobrar a ${V(1)\ge V(2)-12}$.
- **El mínimo.** Bajar $V(2)$ hasta $-2$ y luego $V(1)$ hasta ${-2-3=-5}$. La suma mínima es $-7$, en ${(-5,-2)}$. Ese punto es el óptimo: ${V^*=(-5,-2)}$.
- **La política.** Quedan con igualdad (1, caminar) y (2, correr): es caminar–correr, la óptima.

::: figure {#mkv-c3-fig-region-lp title="La región del pasillo y su mínimo"}
![El plano con V(1) y V(2) en los ejes y cuatro rectas rotuladas: V(1) = V(2) − 3 (caminar en 1), V(1) = V(2) − 12 (correr en 1), V(2) = −3 (caminar en 2) y V(2) = −2 (correr en 2). La región factible queda arriba de V(2) = −2 y a la derecha de V(1) = V(2) − 3, sin techo. Las curvas de nivel de V(1) + V(2) bajan hasta la esquina (−5, −2), marcada como el óptimo, donde se cruzan las rectas de caminar en 1 y correr en 2](../_assets/mkv-c3-region-lp.svg)
:::

> [!TIP]
> **Ejemplo y contraejemplo.**
>
> - **Lo cumple:** en el pasillo, el mínimo del programa es ${(-5,-2)=V^*}$.
> - **No lo cumple:** con esperar gratis falla la condición de [[mkv-bellman|La ecuación de Bellman]]. La región no cambia y el mínimo sigue en ${(-5,-2)}$. Pero ahora el óptimo es ${V^*=(0,0)}$: esperar siempre no cuesta nada.

::: figure {#mkv-c3-fig-ej-lineal title="El programa lineal acierta solo con la condición"}
![Dos paneles. Arriba, con marca de cumple: el pasillo con caminar y correr; su región en el plano V(1)–V(2) tiene la esquina mínima en (−5, −2), que es V*. Abajo, con marca de no cumple: el pasillo con la acción esperar gratis, que deja al robot en su casilla con recompensa 0; su restricción V(s) ≥ V(s) no recorta nada, la región es la misma y el mínimo sigue en (−5, −2), mientras que V* = (0, 0). Pie: esperar siempre no termina y no vale −∞, así que el mínimo deja de ser V*](../_assets/mkv-c3-ej-lineal.svg)
:::

::: exercise {#mkv-c3-lp-ej-apretadas title="Cuáles quedan con igualdad"}
En el óptimo ${V^*=(-5,-2)}$, calcula el lado derecho de cada una de las cuatro restricciones originales, sin despejar. ¿Cuáles se cumplen con igualdad y qué nombre tienen esos cuatro números?
:::

::: hint {#mkv-c3-lp-pista-apretadas of="mkv-c3-lp-ej-apretadas" title="¿Qué es un lado derecho evaluado en V*?"}
¿Qué cuenta ${r(s,a)+\sum_{s'}P(s'\mid s,a)V^*(s')}$: empezar con $a$ y después qué?
:::

::: answer {#mkv-c3-lp-resp-apretadas of="mkv-c3-lp-ej-apretadas"}
Los lados derechos son:

- **(1, caminar):** ${-3+(-2)=-5}$, igual a ${V^*(1)=-5}$.
- **(1, correr):** ${-6+\tfrac12(-5)+\tfrac12(-2)=-9.5}$, menor que $-5$.
- **(2, caminar):** $-3$, menor que ${V^*(2)=-2}$.
- **(2, correr):** ${-1+\tfrac12(-2)=-2}$, igual a $V^*(2)$.

Son los $Q^*(s,a)$. Con igualdad quedan caminar en 1 y correr en 2.

Ojo: en la forma despejada, la holgura de (1, correr) parece de 9 y no de 4.5. Es porque despejar multiplicó por 2.
:::

Falta pasarle esto a `linprog` sin que se pierda un signo.

---

## 2 · Resolver con PL-BELLMAN

**Piensa: `linprog` solo acepta restricciones con $\le$. ¿Cómo se escribe ${V(s)\ge r(s,a)+\dots}$?**

Se pasa todo a la izquierda y se cambia el signo, como pide @opt-signos. La incógnita sigue siendo $V$:

$$
\sum_{s'\in\mathcal T}P(s'\mid s,a)\,V(s')-V(s)\le-r(s,a).
$$

Cada par $(s,a)$ da un renglón. Es la fila de $P_a$ en las columnas de $\mathcal T$, con 1 menos en la columna de $s$.

### El mapa de PL-BELLMAN

- **Qué calcula:** el mínimo del programa de @mkv-c3-teo-lineal, que es el óptimo $V^*$.
- **Qué guarda:** una matriz con un renglón por par $(s,a)$ y una columna por estado de $\mathcal T$. También el vector de los $-r(s,a)$.
- **Cómo avanza:** arma los renglones uno por uno. Después `linprog` busca la esquina más baja de la región.
- **Qué devuelve al terminar:** $V^*$ sobre $\mathcal T$, o FALLA si el solver no encuentra un mínimo.
- **La V del pseudocódigo:** en las líneas 4 a 6, V es la incógnita; lo que devuelve la línea 8 ya es $V^*$.

```text
INPUT   𝒯, estados no terminales; para
        cada s en 𝒯 y a en 𝒜(s): r(s,a)
        y la fila P(·|s,a).
OUTPUT  V* sobre 𝒯, o FALLA.

 1 function PL-BELLMAN(𝒯, 𝒜, P, r)
 2   para cada s en 𝒯:
 3     para cada a en 𝒜(s):
 4       fila ← P(·|s,a) en 𝒯, menos 1
           en la columna de s
           (V = 0 en 𝓕)
 5       agregar  fila · V ≤ −r(s,a)
 6   V* ← linprog: minimizar la
       suma de V, sin cotas en
       las variables
 7   si no hay mínimo: return FALLA
 8   return V*
```

**Gemelo Python.** Cada comentario numerado remite al pseudocódigo. El MDP es el diccionario de [[mkv-el-mdp|El MDP]], y `armar_pasillo` la de [[mkv-iterar-valores|Iteración de valores]]. `n` es el número de estados de $\mathcal T$.

```python
from fractions import Fraction as F
from scipy.optimize import linprog

def armar_pasillo(n=2, castigo=10):
    """Casillas 1..n y la meta; hueco si i % 3 == 1."""
    h = F(1, 2)
    mdp = {"estados": list(range(1, n + 1)),
           "acciones": {}, "P": {}, "r": {}}
    for i in mdp["estados"]:
        sig = i + 1 if i < n else "meta"
        hueco = i % 3 == 1               # sin barandal
        mdp["acciones"][i] = ["caminar", "correr"]
        mdp["P"][(i, "caminar")] = {sig: F(1)}
        mdp["r"][(i, "caminar")] = F(-3)
        mdp["P"][(i, "correr")] = {i: h, sig: h}
        mdp["r"][(i, "correr")] = -1 - h * castigo * hueco
    return mdp

def pl_bellman(mdp):                     # (1)
    T = mdp["estados"]
    n = len(T)
    pos = {s: i for i, s in enumerate(T)}
    A, b = [], []
    for s in T:                          # (2)
        for a in mdp["acciones"][s]:     # (3)
            fila = [0.0] * n
            for s2, p in mdp["P"][(s, a)].items():
                if s2 in pos:            # (4) V = 0 en F
                    fila[pos[s2]] += float(p)
            fila[pos[s]] -= 1
            A.append(fila)               # (5)
            b.append(-float(mdp["r"][(s, a)]))
    res = linprog([1] * n, A_ub=A, b_ub=b,
        bounds=(None, None))             # (6)
    if res.status != 0:
        return None                      # (7) FALLA
    return dict(zip(T, res.x))           # (8) V*

pasillo = armar_pasillo(2)
V_estrella = pl_bellman(pasillo)
print([round(float(v), 6) for v in V_estrella.values()])
# [-5.0, -2.0]
```

**Cada pieza, en su línea:**

- **Línea 4.** La meta no tiene columna. Su valor es 0 y no aporta. Por eso la fila suma menos de 1 en $\mathcal T$.
- **Línea 6.** `[1] * n` pide minimizar la suma de las incógnitas $V(s)$. `bounds=(None, None)` quita la cota que `linprog` pone por omisión.
- **Línea 7.** `status` vale 0 solo si encontró un mínimo. Maximizar, por ejemplo, devuelve «no acotado».

> [!WARNING]
> **Olvidar `bounds=(None, None)`.** Por omisión `linprog` exige que las incógnitas cumplan ${V\ge0}$. Aquí las recompensas son negativas. El solver devuelve un número que no es $V^*$, sin quejarse.
> **Los valores pueden ser negativos: las variables van sin cota.**

### Lo que garantiza y cuánto cuesta

- **Propiedades:** arma un renglón por par $(s,a)$ y una variable por estado de $\mathcal T$. El resto lo hace el solver.
- **Número que da:** ${V^*=(-5,-2)}$ en el pasillo de dos casillas, con suma $-7$.
- **Garantía:** bajo las condiciones de @mkv-c3-teo-bellman, devuelve $V^*$ por @mkv-c3-teo-lineal, con el redondeo del solver. La política sale de las restricciones con igualdad. También sale de la codiciosa de $V^*$ (@mkv-c3-teo-codiciosa).
- **Costo:** el programa tiene $\lvert\mathcal T\rvert$ variables y ${\sum_s\lvert\mathcal A(s)\rvert}$ restricciones. No enumera políticas. Crece con estados y acciones, no con su producto.
- **Supuestos:** se conocen $P$ y $r$, y las condiciones se cumplen. Si no, el solver puede devolver un número que no es $V^*$ sin avisar.

**El caso grande.** En el pasillo de 200 casillas hay 200 variables y 400 restricciones, frente a $2^{200}\approx1.6\times10^{60}$ políticas deterministas. PL-BELLMAN da ${V^*(1)=-467}$, el mismo valor que iterar valores y que iterar políticas.

```python
largo = armar_pasillo(200)
V_estrella = pl_bellman(largo)
print(round(float(V_estrella[1]), 6))
# -467.0
```

> **Una nota de historia.** Manne (1960) planteó un proceso de decisión de Markov como programa lineal; d'Epenoux (1963) lo extendió al caso con descuento.

::: exercise {#mkv-c3-lp-ej-cotas title="Predice lo que devuelve sin cotas libres"}
Quita `bounds=(None, None)` de la línea 6 y corre el pasillo. ¿Qué devuelve `pl_bellman`, y por qué `status` vale 0?
:::

::: hint {#mkv-c3-lp-pista-cotas of="mkv-c3-lp-ej-cotas" title="¿Qué región queda con V ≥ 0?"}
¿Cumple ${(0,0)}$ las cuatro restricciones? ¿Hay algún punto con ${V\ge0}$ y suma menor?
:::

::: answer {#mkv-c3-lp-resp-cotas of="mkv-c3-lp-ej-cotas"}
Devuelve ${(0,0)}$ con `status` 0, y ${(0,0)}$ no es $V^*$. El punto cumple las cuatro restricciones. Con las incógnitas obligadas a ${V\ge0}$, ninguna suma baja de 0. Para el solver es un mínimo legítimo. El error está en el modelo, no en el solver.
:::

Con el modelo y el código en la mano, cambia un número del pasillo.

---

## Ejercicios

::: exercise {#mkv-c3-lp-ej-rampa title="El pasillo con rampa, como programa lineal"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Es el pasillo con rampa de [[mkv-evaluar-politica|Evaluar una política]]: los mismos costos, pero si corres en 2 y resbalas, regresas a la casilla 1. Ahí lo resolviste evaluando las cuatro políticas. Ahora resuélvelo con un solo programa lineal.

1. **Plantea.** Escribe las cuatro restricciones del programa y despéjalas.
2. **Resuelve a mano.** Encuentra el mínimo de ${V(1)+V(2)}$ en la región.
3. **Lee la política.** ¿Qué restricciones quedan con igualdad, y qué política es?
4. **Corre.** Cambia un solo destino del `pasillo` en el Python y comprueba tu resultado.
5. **Compara.** ¿Coincide con la tabla de las cuatro políticas con rampa? ¿Por qué la restricción de (2, correr) no queda con igualdad?
:::

::: hint {#mkv-c3-lp-pista-rampa-1 of="mkv-c3-lp-ej-rampa" title="Pista 1 · ¿Qué cambia en las cuatro restricciones?"}
¿Cuál de las cuatro restricciones es la única que cambia? ¿Qué incógnitas aparecen ahora en ella?
:::

::: hint {#mkv-c3-lp-pista-rampa-2 of="mkv-c3-lp-ej-rampa" title="Pista 2 · ¿Tu respuesta tiene sentido?"}
¿Tu punto cumple las cuatro restricciones, incluida la que cambió? ¿Coincide con el valor $V_\pi$ que calculaste para esa política con rampa?
:::

::: answer {#mkv-c3-lp-resp-rampa of="mkv-c3-lp-ej-rampa" title="Respuesta · El pasillo con rampa"}
**1. Plantear.** Solo cambia (2, correr): al resbalar cae en 1, no en 2.

$$
\begin{aligned}
\text{(1, caminar)}\quad&V(1)\ge V(2)-3,\\
\text{(1, correr)}\quad&V(1)\ge V(2)-12,\\
\text{(2, caminar)}\quad&V(2)\ge-3,\\
\text{(2, correr)}\quad&V(2)\ge-1+\tfrac12V(1).
\end{aligned}
$$

La última tiene a las dos incógnitas: ya no se despeja sola.

**2. Resolver.** Las dos de caminar dan ${V(2)\ge-3}$ y ${V(1)\ge V(2)-3\ge-6}$. Ningún punto factible baja de $(-6,-3)$. Ese punto cumple también (2, correr): ${-3\ge-1+\tfrac12(-6)=-4}$. El mínimo es ${V^*=(-6,-3)}$, con suma $-9$.

**3. La política.** Quedan con igualdad (1, caminar) y (2, caminar): caminar–caminar.

**4. Correr.** Después de `pasillo = armar_pasillo(2)`, cambia la fila de correr en la casilla 2: `pasillo["P"][(2, "correr")] = {1: F(1, 2), "meta": F(1, 2)}`. Imprime `[-6.0, -3.0]`.

**5. Comparar.** Coincide: con rampa, caminar–caminar vale $(-6,-3)$ y gana en las dos casillas. La restricción de (2, correr) vale $-4$ en el óptimo, menos que ${V^*(2)=-3}$. Ese $-4$ es $Q^*(2,\text{correr})$: correr en 2 es peor que caminar.
:::

**Punto de control:** deberías poder:

- escribir el programa lineal de un MDP y despejar sus restricciones;
- encontrar su mínimo, $V^*$, a mano en dos variables;
- pasarlo a `linprog` con los signos y las cotas correctos;
- leer la política de las restricciones con igualdad.

---

## Lo que hay que llevarse

- **El programa.** Las incógnitas son los $V(s)$. Minimizar ${\sum_s V(s)}$ sujeto a ${V(s)\ge r(s,a)+\sum_{s'}P(s'\mid s,a)V(s')}$ para todo par, con ${V=0}$ en $\mathcal F$.
- **El teorema.** Bajo las condiciones de Bellman, el mínimo es $V^*$ y es único (@mkv-c3-teo-lineal). Maximizar no tiene sentido: la región no tiene techo.
- **A mano.** En el pasillo, la región tiene su esquina más baja en ${V^*=(-5,-2)}$, con suma $-7$.
- **La política.** Las restricciones con igualdad son las de caminar en 1 y correr en 2: sus lados derechos son los $Q^*$.
- **El código.** `linprog` con `A_ub` de signo cambiado y `bounds=(None, None)`. Sin las cotas libres devuelve ${(0,0)}$, que no es $V^*$, sin avisar.
- **La condición.** Con esperar gratis la región no cambia. El mínimo sigue en ${(-5,-2)}$, pero el óptimo pasa a ser ${V^*=(0,0)}$.
- **El tamaño.** Una variable por estado y una restricción por par: 200 y 400 en el pasillo largo.

¿Cuál de los tres caminos usar?

Continúa con [[mkv-resumen-decidir|Resumen de la clase: el formulario]].
