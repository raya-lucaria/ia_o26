---
id: mkv-evaluar-politica
title: "Evaluar una política"
nav_title: "Evaluar una política"
summary: "Si fijas la política, su valor resuelve un sistema lineal; a mano en el pasillo, con el algoritmo EVALUAR-POLÍTICA para las cuatro políticas y simulando 10 000 episodios."
status: ready
estimated_time: 28m
tags: [markov, decidir, evaluacion, algoritmo, simulacion]
---

# Evaluar una política

**Si fijamos la política, ¿cuánto vale?**

Al terminar tendrás:

- **El teorema y su condición.** Escribirás ${V_\pi=r_\pi+P_{\pi,\mathcal T}V_\pi}$ y dirás cuándo tiene solución única.
- **Una cuenta a mano.** Evaluarás caminar–correr en el pasillo: ${(V(1),V(2))=(-5,-2)}$.
- **El algoritmo EVALUAR-POLÍTICA.** Seguirás pseudocódigo y Python, y justificarás su costo.
- **Las cuatro políticas.** Las compararás casilla por casilla en una tabla y en el plano.
- **Una comprobación.** Contrastarás −5 con 10 000 episodios simulados.

## Lo que traes

- **El MDP y la política.** En [[mkv-el-mdp|El proceso de decisión de Markov]] viste el MDP (@mkv-c3-def-mdp), la política (@mkv-c3-def-politica) y la cadena que elige (@mkv-c3-def-cadena-politica).
- **Valor y terminar.** De la misma página: el retorno y el valor (@mkv-c3-def-valor), y terminar con probabilidad 1 (@mkv-c3-def-termina).
- **El tiempo medio de llegada.** En [[mkv-absorcion|Cuánto falta para terminar]] resolviste ${(I-P_{\mathcal T})m=\mathbf 1}$ (@mkv-c2-teo-absorcion).
- **Primer paso y sistemas.** En [[mkv-algebra-y-limites|Lo que necesitas de álgebra y límites]] viste condicionar en el primer paso (@mkv-c2-teo-primer-paso) y resolver un sistema lineal (@mkv-c2-def-sistema).
- **Simular.** De la clase 1: MUESTREAR-FILA, el promedio de réplicas (@mkv-c1-teo-promedio) y el error estándar (@mkv-c1-error-estandar).

> [!NOTE]
> **Por qué evaluamos antes de elegir.** El pasillo tiene cuatro políticas, y para compararlas hace falta un número por casilla para cada una.
> Una política fija convierte el MDP en una cadena de Markov con costos. Su valor sale con el mismo truco que el tiempo medio de llegada: lo que pagas ahora más lo que falta.

**El problema, en general.** Sirve para cualquier MDP finito y cualquier política fija.

> **Dado:** un MDP finito $\langle\mathcal S,\mathcal A,P,r\rangle$ con terminales $\mathcal F$ y una política fija $\pi$. De ahí salen las tres piezas que se usan: los estados sin terminar $\mathcal T$, la matriz $P_{\pi,\mathcal T}$ y el vector $r_\pi$.
>
> **Encontrar:** ${V_\pi(s)=E^\pi_s[G_0]}$ para cada ${s\in\mathcal T}$, o avisar que desde algún estado la política no termina.

$V_\pi(s)$ responde una sola pregunta: **cuánto vale estar en $s$ si sigo $\pi$**.

::: table {#mkv-c3-ev-tabla-piezas title="Las piezas de evaluar una política"}
| Símbolo | Qué es | Tamaño | En el pasillo con caminar–correr |
|---|---|---|---|
| $\mathcal T$ | Los estados que aún no terminan | $k=\lvert\mathcal T\rvert$ estados | $\{1,2\}$, en el orden 1, 2 |
| $\pi$ | La acción elegida en cada estado | una acción por estado | caminar en 1, correr en 2 |
| $P_{\pi,\mathcal T}$ | Fila $s$ de $P_{\pi(s)}$, solo columnas de $\mathcal T$ | $k\times k$ | fila 1 de $P_{\text{caminar}}$, fila 2 de $P_{\text{correr}}$ |
| $r_\pi$ | La recompensa $r(s,\pi(s))$ de cada estado | $k\times1$ | $-3$ en 1, $-1$ en 2 |
| $V_\pi$ | La incógnita: el valor desde cada estado | $k\times1$ | $V(1)$ y $V(2)$ |
| $I$ | La matriz identidad | $k\times k$ | la identidad de $2\times2$ |
:::

**El mismo problema, en el pasillo.** Las mismas piezas, con números.

> **Dado:** el pasillo con la política caminar–correr. La política elige filas: la 1 de $P_{\text{caminar}}$ y la 2 de $P_{\text{correr}}$. Restringidas a ${\mathcal T=\{1,2\}}$:
>
> $$
> \begin{aligned}
> P_{\pi,\mathcal T}&=\begin{pmatrix}0&1\\0&1/2\end{pmatrix},\\
> r_\pi&=\begin{pmatrix}-3\\-1\end{pmatrix}.
> \end{aligned}
> $$
>
> **Encontrar:** $V(1)$ y $V(2)$: cuánto vale cada casilla si caminas en 1 y corres en 2.

- **Lectura.** La fila 2 suma $1/2$: la otra mitad es llegar a la meta.

---

## 1 · Plantear el valor con el primer paso

**Piensa: ¿qué relación hay entre $V_\pi(1)$ y el valor de las casillas a donde te lleva la acción?**

Pagas $r(1,\pi(1))$ en este paso; después te falta, en promedio, el valor de donde caigas. Es el sistema de @mkv-c2-teo-absorcion con $r_\pi$ en el lugar del 1.

::: theorem {#mkv-c3-teo-evaluar title="El valor de una política resuelve un sistema lineal"}
Sea un MDP finito $\langle\mathcal S,\mathcal A,P,r\rangle$ con terminales $\mathcal F$, ${\mathcal T=\mathcal S\setminus\mathcal F}$, y una política $\pi$.

**Condición.** La política termina con probabilidad 1 **desde todo** ${s\in\mathcal T}$ (@mkv-c3-def-termina). En MDP finitos equivale a que ${I-P_{\pi,\mathcal T}}$ sea invertible.

Entonces $V_\pi(s)$ es finito para todo ${s\in\mathcal T}$, y el vector columna $V_\pi$ sobre $\mathcal T$ es la **única** solución de

$$
\begin{aligned}
V_\pi(s)&=r(s,\pi(s))\\
&\quad+\sum_{s'\in\mathcal T}P(s'\mid s,\pi(s))\,V_\pi(s'),\\
&\quad\text{para cada } s\in\mathcal T,\\
V_\pi&=r_\pi+P_{\pi,\mathcal T}\,V_\pi,\\
(I-P_{\pi,\mathcal T})\,V_\pi&=r_\pi,
\end{aligned}
$$

con ${V_\pi(s)=0}$ en $\mathcal F$.

**Lectura.** El primer término es lo que pagas en este paso; la suma promedia lo que falta desde cada destino. Los destinos en $\mathcal F$ no aportan: ahí ya no se paga nada.

**Casos nulos.** Si ${s\in\mathcal F}$, ${V_\pi(s)=0}$. Si $\pi(s)$ lleva seguro a $\mathcal F$, ${V_\pi(s)=r(s,\pi(s))}$.
:::

::: proof {#mkv-c3-ev-dem-evaluar of="mkv-c3-teo-evaluar"}
Con $\pi$ fija, $P_\pi$ es una cadena finita y homogénea, y la condición es la de @mkv-c2-teo-absorcion con ${A=\mathcal F}$.

**Finito.** Cada paso paga a lo más ${c=\max_{s,a}\lvert r(s,a)\rvert}$ en promedio, y hay $\tau_{\mathcal F}$ pasos. La demostración de @mkv-c2-teo-absorcion da ${E^\pi_s[\tau_{\mathcal F}]<\infty}$, así que ${\lvert V_\pi(s)\rvert\le c\,E^\pi_s[\tau_{\mathcal F}]<\infty}$.

**La ecuación.** Si ${s\in\mathcal T}$, el retorno se parte en ${G_0=r_1+G_1}$, con $G_1$ lo que se paga desde $S_1$. Por linealidad de la esperanza, ${V_\pi(s)=E^\pi_s[r_1]+E^\pi_s[G_1]}$. El primer término es $r(s,\pi(s))$. Por @mkv-c2-teo-primer-paso y Markov, el segundo es ${\sum_{s'}P(s'\mid s,\pi(s))\,V_\pi(s')}$, y los $s'$ en $\mathcal F$ valen 0.

**Única.** Es el argumento de @mkv-c2-teo-absorcion: la diferencia $x$ de dos soluciones cumple ${x=P_{\pi,\mathcal T}^{\,t}x}$ para todo $t$, y ${P_{\pi,\mathcal T}^{\,t}\to0}$.
:::

- **Suficiente y necesaria.** Si desde algún estado la política no termina, ${I-P_{\pi,\mathcal T}}$ es singular y el sistema deja de dar un único vector.
- **Cómo revisarla.** Como en 8.2.5: en el grafo de $P_\pi$, ninguna clase cerrada puede quedar dentro de $\mathcal T$.

> [!TIP]
> **Ejemplo y contraejemplo.**
>
> - **Lo cumple:** caminar–correr. ${I-P_{\pi,\mathcal T}=\begin{pmatrix}1&-1\\0&1/2\end{pmatrix}}$ es invertible, y la única solución es ${(V(1),V(2))=(-5,-2)}$.
> - **No lo cumple:** agrega «esperar» gratis, que te deja en tu casilla con ${r=0}$. Con esperar siempre, ${P_{\pi,\mathcal T}=I}$ e ${I-P_{\pi,\mathcal T}=0}$. La ecuación queda ${V_\pi=V_\pi}$: cualquier vector la cumple, y no hay solución única.

::: figure {#mkv-c3-fig-ej-evaluar title="Ejemplo y contraejemplo: evaluar una política"}
![Dos cadenas de una política en el pasillo, cada una con su grafo y su matriz. Arriba, la que cumple: caminar–correr; de 1 a 2 con 1, lazo en 2 con 1/2 y de 2 a la meta con 1/2; I − P_π,𝒯 = (1, −1; 0, 1/2) es invertible y la solución es (−5, −2). Abajo, la que no: esperar siempre, gratis; lazo en 1 con 1 y lazo en 2 con 1, ninguna flecha a la meta; I − P_π,𝒯 = 0 y el sistema no tiene solución única.](../_assets/mkv-c3-ej-evaluar.svg)
:::

- **Qué valor tiene esperar siempre.** Nunca termina y nunca paga: su retorno es 0 en cada episodio. El sistema no lo distingue de ningún otro vector, porque la condición falla.

> [!WARNING]
> **Evaluar sin revisar la condición.** Un programa con decimales puede devolver números aunque ${I-P_{\pi,\mathcal T}}$ sea casi singular.
> **Antes de leer el resultado, revisa que desde cada estado la política llegue a $\mathcal F$.**

::: exercise {#mkv-c3-ev-ej-desde-todo title="¿Basta con que termine desde una casilla?"}
Con esperar gratis disponible, toma la política que espera en 1 y camina en 2. ¿Cumple la condición de @mkv-c3-teo-evaluar? ¿Qué dice el sistema de $V(1)$ y de $V(2)$?
:::

::: hint {#mkv-c3-ev-pista-desde-todo of="mkv-c3-ev-ej-desde-todo" title="¿Desde cuál casilla se llega a la meta?"}
¿A dónde lleva la fila de 1 y a dónde la de 2? Escribe las dos ecuaciones y mira cuál tiene a su incógnita de los dos lados.
:::

::: answer {#mkv-c3-ev-resp-desde-todo of="mkv-c3-ev-ej-desde-todo"}
No la cumple: desde 2 se llega a la meta, pero desde 1 nunca se sale. Las ecuaciones son ${V(1)=0+V(1)}$ y ${V(2)=-3}$. La segunda fija ${V(2)=-3}$; la primera la cumple cualquier $V(1)$, así que no hay solución única. La condición pide terminar **desde todo** estado, no desde alguno.
:::

Con el teorema en mano, el pasillo se evalúa con dos ecuaciones.

---

## 2 · Evaluar caminar–correr a mano

**Piensa: ¿cuál de las dos ecuaciones tiene una sola incógnita?**

Usa $P_{\pi,\mathcal T}$ y $r_\pi$ del planteamiento. La condición se cumple: desde 1 se llega a 2, y desde 2 a la meta.

El sistema, renglón por renglón:

$$
\begin{aligned}
V(2)&=-1+\tfrac12V(2),\\
V(1)&=-3+V(2).
\end{aligned}
$$

- **De abajo hacia arriba.** La primera da ${\tfrac12V(2)=-1}$, es decir ${V(2)=-2}$. La segunda da ${V(1)=-3-2=-5}$.
- **Lectura del −2.** En la casilla 2 corres hasta llegar. Cada intento cuesta 1 y llega con $1/2$: en promedio son dos intentos.
- **Lectura del −5.** Caminar de 1 a 2 cuesta 3 seguro; luego faltan los 2 de la casilla 2.

Las otras tres políticas salen igual, y la sección 3 las calcula todas.

::: exercise {#mkv-c3-ev-ej-correr-caminar title="Evalúa correr–caminar a mano"}
Escribe $P_{\pi,\mathcal T}$ y $r_\pi$ de correr–caminar, y resuelve el sistema. ¿Por qué $V(2)$ no depende de lo que hagas en 1?
:::

::: hint {#mkv-c3-ev-pista-correr-caminar of="mkv-c3-ev-ej-correr-caminar" title="¿Qué fila usa cada casilla?"}
¿De qué matriz sale la fila de 1 y de cuál la de 2? ¿Cuál de las dos ecuaciones tiene una sola incógnita?
:::

::: answer {#mkv-c3-ev-resp-correr-caminar of="mkv-c3-ev-ej-correr-caminar"}
La fila 1 sale de $P_{\text{correr}}$ y la fila 2 de $P_{\text{caminar}}$:

$$
P_{\pi,\mathcal T}=\begin{pmatrix}1/2&1/2\\0&0\end{pmatrix},
$$

$$
r_\pi=\begin{pmatrix}-6\\-3\end{pmatrix}.
$$

Entonces ${V(2)=-3}$ y ${V(1)=-6+\tfrac12V(1)+\tfrac12(-3)}$, que da ${\tfrac12V(1)=-\tfrac{15}{2}}$ y ${V(1)=-15}$. $V(2)$ no depende de 1 porque desde 2 nunca se regresa a 1: la fila 2 no tiene nada en la columna 1.
:::

Con más casillas o más políticas, conviene que un programa arme y resuelva el sistema.

---

## 3 · Calcular con EVALUAR-POLÍTICA

**Piensa: ¿qué cambia respecto a TIEMPO MEDIO DE LLEGADA?**

Solo dos cosas. Antes de armar la matriz, la política elige una fila por estado. Y el lado derecho es $r_\pi$, no un vector de unos. La eliminación es la misma.

### El mapa de EVALUAR-POLÍTICA

- **Qué calcula:** la solución de ${(I-P_{\pi,\mathcal T})V_\pi=r_\pi}$, que por @mkv-c3-teo-evaluar es el valor de $\pi$.
- **Qué guarda:** la matriz ${I-P_{\pi,\mathcal T}}$ con $r_\pi$ pegado como última columna.
- **Cómo avanza:** primero copia la fila de la acción elegida en cada estado; después elimina columna por columna.
- **Qué devuelve al terminar:** $V_\pi$ sobre $\mathcal T$, o FALLA si alguna columna se queda sin pivote.

::: figure {#mkv-c3-fig-flujo-evaluar title="Evaluar una política, en palabras"}
![Diagrama de flujo de evaluar una política, en palabras. 1: Para cada estado sin terminar, toma la acción que elige la política. 2: Copia su fila de P y su recompensa r. 3: Arma el sistema (I − P_π,𝒯) V = r_π. 4, pregunta: ¿tiene solución única? Si sí, 5: resuélvelo y devuelve V, con V = 0 en la meta. Si no es única, 6: avisa que desde algún estado la política no termina. Cada renglón dice: lo que pagas ahora más lo que falta desde donde caes.](../_assets/mkv-c3-flujo-evaluar.svg)
:::

```text
INPUT   un MDP finito: 𝒯, P(s'|s,a),
        r(s,a); una política π.
OUTPUT  V_π(s) para cada s en 𝒯,
        o FALLA.

 1 function EVALUAR-POLÍTICA(MDP, π)
 2   for s in 𝒯, en orden
 3     a ← π(s)
 4     fila s de P_π,𝒯 ← P(·|s,a)
         en las columnas de 𝒯
 5     r_π(s) ← r(s,a)
 6   M ← I − P_π,𝒯
 7   resolver M V = r_π por eliminación
 8     si una columna no tiene pivote:
         return FALLA
 9   return V          (V = 0 en ℱ)
```

**Gemelo Python.** Cada comentario numerado remite al pseudocódigo. `resolver` es la eliminación de 8.2.5, sin cambios. El MDP es un diccionario: `P[(s, a)]` da los destinos con su probabilidad y `r[(s, a)]` la recompensa esperada.

```python
from fractions import Fraction as F

def resolver(M, b):              # (7) eliminación exacta
    k = len(b)
    M = [list(f) + [c] for f, c in zip(M, b)]
    for c in range(k):
        p = next((r for r in range(c, k)
                  if M[r][c] != 0), None)
        if p is None:
            return None          # (8) sin pivote
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [x / piv for x in M[c]]
        for r in range(k):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y
                        for x, y in zip(M[r], M[c])]
    return [M[r][k] for r in range(k)]

def evaluar_politica(mdp, pol):
    T = mdp["estados"]
    PT, rp = [], []
    for s in T:                            # (2)
        a = pol[s]                         # (3)
        fila = mdp["P"][(s, a)]
        PT.append([fila.get(j, F(0))
                   for j in T])            # (4)
        rp.append(mdp["r"][(s, a)])        # (5)
    k = len(T)
    M = [[(i == j) - PT[i][j]
          for j in range(k)]
         for i in range(k)]                # (6)
    V = resolver(M, rp)                    # (7)
    if V is None:
        return None                        # (8) FALLA
    return dict(zip(T, V))                 # (9)

mitad = F(1, 2)
pasillo = {
    "estados": [1, 2],
    "P": {(1, "caminar"): {2: F(1)},
          (1, "correr"): {1: mitad, 2: mitad},
          (2, "caminar"): {"meta": F(1)},
          (2, "correr"): {2: mitad, "meta": mitad}},
    "r": {(1, "caminar"): F(-3),
          (1, "correr"): F(-6),
          (2, "caminar"): F(-3),
          (2, "correr"): F(-1)},
}
for a1 in ("caminar", "correr"):
    for a2 in ("caminar", "correr"):
        V = evaluar_politica(pasillo,
                             {1: a1, 2: a2})
        print(f"{a1}–{a2}: {V[1]}, {V[2]}")
# caminar–caminar: -6, -3
# caminar–correr: -5, -2
# correr–caminar: -15, -3
# correr–correr: -14, -2
```

**Cada pieza, en su línea:**

- **Línea 4.** `fila.get(j, F(0))` pone 0 donde la acción no lleva; la meta no tiene columna, así que su probabilidad queda fuera, como en $P_{\pi,\mathcal T}$.
- **Línea 5.** `r[(s, a)]` es la recompensa esperada: en la casilla 1, correr vale ${-1-\tfrac12\cdot10=-6}$.
- **Líneas 7 y 8.** Con fracciones, «sin pivote» es exacto: la condición falla o no falla, sin redondeo.

**Las cuatro políticas.** El ciclo final evalúa las ${2\cdot2=4}$ políticas del pasillo:

::: table {#mkv-c3-ev-tabla-cuatro title="El valor de las cuatro políticas del pasillo"}
| Política | V(1) | V(2) |
|---|---:|---:|
| caminar–caminar | −6 | −3 |
| caminar–correr | −5 | −2 |
| correr–caminar | −15 | −3 |
| correr–correr | −14 | −2 |
:::

::: figure {#mkv-c3-fig-cuatro-politicas-plano title="Las cuatro políticas en el plano V(1)–V(2)"}
![Plano con V(1) en el eje horizontal y V(2) en el vertical. Cuatro puntos: caminar–caminar en (−6, −3), caminar–correr en (−5, −2), correr–caminar en (−15, −3) y correr–correr en (−14, −2). Caminar–correr queda a la derecha de las otras tres y a la altura máxima, empatada con correr–correr.](../_assets/mkv-c3-cuatro-politicas-plano.svg)
:::

- **Columna V(2).** Solo depende de la acción en 2: −3 si caminas, −2 si corres. Desde 2 nunca se regresa a 1.
- **Columna V(1).** Depende de las dos acciones. Correr en 1 sale caro: el castigo de 10 llega con $1/2$ en cada intento.
- **Una sola alcanza el máximo en las dos.** Caminar–correr tiene el valor más alto en la casilla 1 **y** empata el más alto en la casilla 2 con correr–correr. En la figura, es el punto de la fila de arriba que queda más a la derecha.

::: exercise {#mkv-c3-ev-ej-esperar title="Corre el algoritmo con esperar siempre"}
Agrega al pasillo «esperar» gratis y evalúa esperar siempre con EVALUAR-POLÍTICA. ¿Cómo queda $M$ en la línea 6, y qué devuelve el algoritmo, en qué línea?
:::

::: hint {#mkv-c3-ev-pista-esperar of="mkv-c3-ev-ej-esperar" title="¿Qué fila copia la línea 4?"}
¿A dónde lleva esperar desde 1 y desde 2, y qué le hace la resta de la línea 6 a esas filas?
:::

::: answer {#mkv-c3-ev-resp-esperar of="mkv-c3-ev-ej-esperar"}
Esperar deja a cada casilla en su lugar, así que ${P_{\pi,\mathcal T}=I}$ y ${M=I-I}$ es la matriz de ceros. En la primera columna no hay pivote distinto de cero: la línea 8 devuelve FALLA. Es la condición de @mkv-c3-teo-evaluar que falla, no un error del programa.
:::

### Lo que garantiza y cuánto cuesta

- **Propiedades:** termina siempre, tras $\lvert\mathcal T\rvert$ columnas. Devuelve FALLA exactamente cuando ${I-P_{\pi,\mathcal T}}$ es singular.
- **Número que da:** ${(V(1),V(2))=(-5,-2)}$ para caminar–correr.
- **Garantía:** si no falla, por @mkv-c3-teo-evaluar devuelve $V_\pi(s)$ desde cada estado de $\mathcal T$. Con fracciones es exacto.
- **Costo:** copiar las filas toma ${\lvert\mathcal T\rvert^2}$; la eliminación, del orden de ${\lvert\mathcal T\rvert^3}$ operaciones. Es por política: evaluarlas todas multiplica por ${\prod_{s\in\mathcal T}\lvert\mathcal A(s)\rvert}$.
- **Supuestos:** el MDP es finito, $P$ y $r$ se conocen, y la política es determinista y estacionaria.

El álgebra dice −5; falta comprobarlo con episodios.

---

## 4 · Simular episodios para comprobar

**Piensa: ¿cómo compruebas ${V_\pi(1)=-5}$ sin resolver nada?**

Corriendo muchos episodios independientes desde 1 con caminar–correr y promediando sus retornos. Cada episodio sortea el siguiente estado con MUESTREAR-FILA y para al llegar a la meta. Por la condición, cada episodio termina con probabilidad 1.

- **El promedio.** Los retornos de los episodios son independientes, con la misma distribución y esperanza $V_\pi(1)$. Por la ley de los grandes números, la extensión de @mkv-c1-teo-promedio que ya usamos en 8.2.5, su promedio tiende a $V_\pi(1)$.
- **El ruido.** Como en 8.2.5, el error estándar es ${s/\sqrt n}$, con $s$ la dispersión de los retornos.
- **Qué se suma.** El programa suma $r(s,a)$ en cada paso. Para caminar y para correr en 2 es lo que de verdad se paga; correr en 1 tendría que sortear además el castigo.

```python
import math, random, statistics

def muestrear_fila(fila, u):
    suma = 0
    for i, p in enumerate(fila):
        suma += p
        if u < suma:
            return i
    return max(i for i, p in enumerate(fila)
               if p > 0)

def simular(mdp, pol, inicio, n, semilla):
    rng = random.Random(semilla)
    retornos = []
    for _ in range(n):
        s, G = inicio, 0
        while s != "meta":
            a = pol[s]
            G += mdp["r"][(s, a)]
            destinos = list(mdp["P"][(s, a)])
            fila = [float(p) for p in
                    mdp["P"][(s, a)].values()]
            u = rng.random()
            s = destinos[muestrear_fila(fila, u)]
        retornos.append(int(G))
    return retornos

G = simular(pasillo, {1: "caminar", 2: "correr"},
            1, 10_000, 2044)
ee = statistics.stdev(G) / math.sqrt(len(G))
print(round(statistics.fmean(G), 4), round(ee, 4))
# -5.0074 0.0143
```

**En el juguete.** Con ${n=10\,000}$ episodios y semilla 2044, el promedio fue −5.0074, con error estándar 0.0143: la diferencia con −5 es la mitad de un error estándar. El valor calculado es −5.

::: figure {#mkv-c3-fig-simular-politica title="Los retornos de 10 000 episodios de caminar–correr"}
![Histograma de los retornos de 10 000 episodios de caminar–correr desde la casilla 1, semilla 2044. Las barras están en −4, −5, −6, −7 y siguen hacia la izquierda; cada una mide cerca de la mitad de la anterior, y la de −4 tiene cerca de la mitad de los episodios. Una línea vertical marca el valor calculado, −5, y otra el promedio simulado.](../_assets/mkv-c3-simular-politica.svg)
:::

- **Lectura.** El retorno es −3 por caminar y −1 por cada intento de correr. Ningún episodio paga menos de 4, y la mitad paga justo 4.
- **El promedio no es lo típico.** El retorno más frecuente es −4, pero los episodios largos jalan la media hasta −5.

> [!WARNING]
> **Leer $V_\pi(1)$ como lo que pagará un episodio.** −5 es el promedio de muchos episodios; el que tuvo suerte en el primer intento paga 4, no 5.
> **El valor fija la media del retorno, no su valor en un episodio concreto.**

::: exercise {#mkv-c3-ev-ej-histograma title="Lee el histograma sin simular"}
Con caminar–correr desde 1, ¿con qué probabilidad el retorno es −4? ¿Y −5? ¿Qué regla siguen las alturas de las barras?
:::

::: hint {#mkv-c3-ev-pista-histograma of="mkv-c3-ev-ej-histograma" title="¿Cuántos intentos de correr hace cada episodio?"}
¿Cuánto paga un episodio que llega a la meta en el primer intento desde 2, y con qué probabilidad pasa eso?
:::

::: answer {#mkv-c3-ev-resp-histograma of="mkv-c3-ev-ej-histograma"}
Un episodio con $j$ intentos de correr paga ${3+j}$. Llega en el primer intento con $1/2$, así que el retorno es −4 con $1/2$. Llega en el segundo con ${\tfrac12\cdot\tfrac12=\tfrac14}$: retorno −5 con $1/4$. En general, el retorno es ${-3-j}$ con probabilidad $(1/2)^j$: cada barra mide la mitad de la anterior.
:::

Cambia una regla del pasillo y evalúa de nuevo.

---

## Ejercicios

::: exercise {#mkv-c3-ev-ej-rampa title="Evalúa el pasillo con rampa"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

El pasillo es el mismo, con los mismos costos. **Cambia una idea:** el piso de la casilla 2 está inclinado. Si corres en 2 y resbalas, ya no te quedas: regresas a la casilla 1. Todo lo demás sigue igual.

1. **Modela.** Escribe la nueva fila 2 de $P_{\text{correr}}$ y revisa que sume 1.
2. **Revisa la condición.** ¿Caminar–correr termina con probabilidad 1 desde las dos casillas?
3. **Plantea y resuelve.** Escribe ${V_\pi=r_\pi+P_{\pi,\mathcal T}V_\pi}$ para caminar–correr y calcula $V(1)$ y $V(2)$.
4. **Evalúa las otras tres.** Puedes usar el Python de la sección 3, cambiando una línea del diccionario.
5. **Explica.** ¿Por qué el inciso 3 ya no se despeja de abajo hacia arriba? ¿Qué política tiene ahora el valor más alto en cada casilla?
:::

::: hint {#mkv-c3-ev-pista-rampa-1 of="mkv-c3-ev-ej-rampa" title="Pista 1 · ¿A dónde lleva cada resbalón?"}
¿Qué destinos tiene correr en 2 ahora, y con qué probabilidad? ¿Desde qué casilla se puede llegar a la meta?
:::

::: hint {#mkv-c3-ev-pista-rampa-2 of="mkv-c3-ev-ej-rampa" title="Pista 2 · ¿Tus números tienen sentido?"}
¿Suma a lo más 1 cada fila de tu $P_{\pi,\mathcal T}$? ¿Es tu $V(1)$ menor que tu $V(2)$, si desde 1 primero hay que pasar por 2? ¿Coinciden las políticas que no corren en 2 con la tabla de la sección 3?
:::

::: answer {#mkv-c3-ev-resp-rampa of="mkv-c3-ev-ej-rampa" title="Respuesta · El pasillo con rampa"}
**1. La fila.** Correr en 2 va a 1 con $1/2$ y a la meta con $1/2$; suma 1. En el diccionario: `(2, "correr"): {1: mitad, "meta": mitad}`.

**2. Condición.** Sí. Desde 1 se camina a 2, y desde 2 se llega a la meta con $1/2$ en cada intento. No hay clase cerrada dentro de $\{1,2\}$.

**3. Resolver.** Con caminar–correr:

$$
\begin{aligned}
P_{\pi,\mathcal T}&=\begin{pmatrix}0&1\\1/2&0\end{pmatrix},\\
V(1)&=-3+V(2),\\
V(2)&=-1+\tfrac12V(1).
\end{aligned}
$$

Sustituir la primera en la segunda da ${V(2)=-\tfrac52+\tfrac12V(2)}$: ${V(2)=-5}$ y ${V(1)=-8}$.

**4. Las cuatro.**

- **Caminar–caminar:** $(-6,-3)$, igual que antes, porque no corre en 2.
- **Caminar–correr:** $(-8,-5)$.
- **Correr–caminar:** $(-15,-3)$, igual que antes.
- **Correr–correr:** $(-26,-14)$.

**5. Ciclos y ganadora.** $V(1)$ depende de $V(2)$ y $V(2)$ de $V(1)$: ninguna ecuación tiene una sola incógnita, y hay que resolverlas juntas. Ahora caminar–caminar alcanza el máximo en las dos casillas (en la 2 empata con correr–caminar): la rampa vuelve caro correr en 2.
:::

**Punto de control:** deberías poder armar $P_{\pi,\mathcal T}$ y $r_\pi$ eligiendo filas, revisar la condición en el grafo y resolver ${(I-P_{\pi,\mathcal T})V_\pi=r_\pi}$. También, correr EVALUAR-POLÍTICA y comparar su resultado con episodios simulados.

---

## Lo que hay que llevarse

- **El teorema.** ${V_\pi=r_\pi+P_{\pi,\mathcal T}V_\pi}$, con ${V_\pi=0}$ en $\mathcal F$, si la política termina con probabilidad 1 desde todo estado (@mkv-c3-teo-evaluar).
- **La condición.** En MDP finitos equivale a que ${I-P_{\pi,\mathcal T}}$ sea invertible. Esperar siempre, gratis, la rompe: ${I-P_{\pi,\mathcal T}=0}$.
- **A mano.** Caminar–correr vale ${(V(1),V(2))=(-5,-2)}$; correr–caminar, $(-15,-3)$.
- **El algoritmo.** EVALUAR-POLÍTICA elige filas, arma ${I-P_{\pi,\mathcal T}}$ y elimina; cuesta del orden de ${\lvert\mathcal T\rvert^3}$ por política.
- **Las cuatro.** caminar–caminar $(-6,-3)$, caminar–correr $(-5,-2)$, correr–caminar $(-15,-3)$, correr–correr $(-14,-2)$. Caminar–correr alcanza el máximo en las dos casillas.
- **La simulación.** −5 calculado contra −5.0074 simulado, con error estándar 0.0143.

Evaluar las cuatro funcionó porque eran cuatro. ¿Y si en lugar de fijar la acción la elegimos?

Continúa con [[mkv-bellman|La ecuación de Bellman]].
