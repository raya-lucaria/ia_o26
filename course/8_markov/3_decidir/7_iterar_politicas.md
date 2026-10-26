---
id: mkv-iterar-politicas
title: "Iteración de políticas"
nav_title: "Iteración de políticas"
summary: "Evaluar y mejorar hasta que la política no cambie: termina en un número finito de rondas si se conserva la acción en los empates."
status: ready
estimated_time: 22m
tags: [markov, decidir, iteracion-de-politicas, algoritmo]
---

# Iteración de políticas

**¿Se puede llegar a la política óptima en un número finito de rondas?**

Al terminar tendrás:

- **Una ronda a mano.** Evaluarás caminar–caminar en el pasillo, la mejorarás y llegarás a caminar–correr, con valores $(-5,-2)$.
- **Un teorema con su condición.** Sabrás por qué el valor nunca baja y por qué el algoritmo termina.
- **Un contraejemplo.** Verás que, si la mejora cambia de acción en un empate, las políticas alternan para siempre.
- **El algoritmo ITERACIÓN DE POLÍTICAS.** Seguirás pseudocódigo y Python exacto con fracciones.
- **Una comparación.** Contarás sus rondas contra las de iteración de valores en un pasillo de 200 casillas.

## Lo que traes

- **El MDP y sus políticas.** En [[mkv-el-mdp|El MDP]] viste el MDP (@mkv-c3-def-mdp), la política (@mkv-c3-def-politica), la cadena que elige (@mkv-c3-def-cadena-politica) y qué es terminar con probabilidad 1 (@mkv-c3-def-termina).
- **Evaluar.** En [[mkv-evaluar-politica|Evaluar una política]], si $\pi$ termina, $V_\pi=r_\pi+P_{\pi,\mathcal T}V_\pi$ tiene una sola solución (@mkv-c3-teo-evaluar).
- **Bellman.** En [[mkv-bellman|La ecuación de Bellman]] viste el valor de acción (@mkv-c3-def-q), el óptimo (@mkv-c3-def-optimo), la ecuación con su condición (@mkv-c3-teo-bellman) y la codiciosa (@mkv-c3-teo-codiciosa).
- **Iteración de valores.** En [[mkv-iterar-valores|Iteración de valores]] el pasillo nunca llega en rondas finitas: ${V^{(k)}(2)=-2+2^{1-k}}$ (@mkv-c3-teo-iterar-valores).

> [!NOTE]
> **Por qué otro algoritmo.** Iteración de valores se acerca a $V^*$ sin tocarlo, y hay que decidir cuándo parar. Pero el pasillo tiene solo cuatro políticas. Si buscamos entre políticas en lugar de entre números, la búsqueda es finita. Falta que no dé vueltas.

---

## 1 · Evaluar y mejorar, a mano

**Piensa: si ya sabes cuánto vale una política, ¿cómo encuentras una mejor?**

En cada casilla pruebas cada acción una vez y después sigues con la política vieja. Si alguna da más, la cambias: es la codiciosa de @mkv-c3-teo-codiciosa con ${U=V_\pi}$.

> **Dado:** un MDP finito que cumple las condiciones de @mkv-c3-teo-bellman y una política $\pi_0$ que termina con probabilidad 1.
>
> **Encontrar:** una política óptima $\pi^*$ y su valor ${V^*=V_{\pi^*}}$, en un número finito de rondas.

Una **ronda** tiene dos pasos:

- **Evaluar.** Resolver ${V_\pi=r_\pi+P_{\pi,\mathcal T}V_\pi}$. Por @mkv-c3-teo-evaluar tiene una sola solución si $\pi$ termina.
- **Mejorar.** En cada ${s\in\mathcal T}$, elegir una acción que maximice ${Q_\pi(s,a)=r(s,a)+\sum_{s'}P(s'\mid s,a)V_\pi(s')}$. Si la acción actual empata con el máximo, se conserva.

Si la mejora no cambia nada, el algoritmo para. En inglés se llama *policy iteration*.

**En el juguete.** Empezamos con caminar–caminar. Caminar avanza seguro y cuesta 3, así que ${V_\pi(2)=-3}$ y ${V_\pi(1)=-3+V_\pi(2)=-6}$.

**Mejorar en la casilla 2.** Correr cuesta 1 y se queda en 2 con $1/2$:

$$
\begin{aligned}
Q_\pi(2,\text{caminar})&=-3+0=-3,\\
Q_\pi(2,\text{correr})&=-1+\tfrac12(-3)+\tfrac12(0)=-\tfrac52.
\end{aligned}
$$

Correr gana: $-5/2>-3$.

**Mejorar en la casilla 1.** Correr cuesta $-6$ por el hueco:

$$
\begin{aligned}
Q_\pi(1,\text{caminar})&=-3+(-3)=-6,\\
Q_\pi(1,\text{correr})&=-6+\tfrac12(-6)+\tfrac12(-3)=-\tfrac{21}2.
\end{aligned}
$$

Caminar gana. La política nueva es caminar–correr.

**Segunda ronda.** Evaluar caminar–correr da ${V(2)=-1+\tfrac12V(2)}$, o sea ${V(2)=-2}$, y ${V(1)=-3+V(2)=-5}$. Mejorar:

- **Casilla 2.** Caminar da $-3$; correr da ${-1+\tfrac12(-2)=-2}$. Se queda correr.
- **Casilla 1.** Caminar da ${-3-2=-5}$; correr da ${-6+\tfrac12(-5)+\tfrac12(-2)=-\tfrac{19}2}$. Se queda caminar.

Nada cambió: el algoritmo para con caminar–correr y ${(V(1),V(2))=(-5,-2)}$. Es $\pi^*$ y es $V^*$, exactos, en dos rondas. La segunda solo confirma.

> [!WARNING]
> **Mejorar con el valor de la acción, no con el costo inmediato.** En la casilla 2, caminar cuesta 3 y correr 1, pero eso no basta: correr puede repetir el turno.
> **Se compara $Q_\pi(s,a)$, que suma el costo de ahora y el valor de donde caes.**

::: exercise {#mkv-c3-pi-ej-correr title="Empieza corriendo"}
Corre una ronda desde correr–correr, cuyo valor es ${(-14,-2)}$. ¿Qué política sale de la mejora?
:::

::: hint {#mkv-c3-pi-pista-correr of="mkv-c3-pi-ej-correr" title="¿Qué acción gana en la casilla 1?"}
¿Cuánto vale caminar desde 1 si después sigues con un ${V(2)=-2}$? ¿Y correr, si ${V(1)=-14}$?
:::

::: answer {#mkv-c3-pi-resp-correr of="mkv-c3-pi-ej-correr"}
En la casilla 2, caminar da $-3$ y correr ${-1+\tfrac12(-2)=-2}$: se queda correr. En la casilla 1, caminar da ${-3-2=-5}$ y correr ${-6+\tfrac12(-14)+\tfrac12(-2)=-14}$: cambia a caminar. Sale caminar–correr, también en una sola mejora.
:::

Dos arranques distintos llegaron en una mejora. ¿Pasa siempre que el algoritmo termina?

---

## 2 · Por qué termina

**Piensa: ¿qué impide que la mejora regrese a una política que ya visitó?**

Que el valor sube en cada cambio: no puede volver a una política de valor menor. Y hay un número finito de políticas.

::: theorem {#mkv-c3-teo-iterar-politicas title="Iteración de políticas mejora y termina"}
Sea un MDP finito y sean $\pi_0,\pi_1,\dots$ las políticas que produce iteración de políticas.

**Condición.** El MDP cumple las condiciones de @mkv-c3-teo-bellman. La política inicial $\pi_0$ termina con probabilidad 1 desde todo ${s\in\mathcal T}$ (@mkv-c3-def-termina). En cada mejora, si $\pi_k(s)$ empata con el máximo, se conserva.

Entonces:

1. Cada $\pi_k$ termina con probabilidad 1, así que cada evaluación tiene una sola solución.
2. ${V_{\pi_{k+1}}(s)\ge V_{\pi_k}(s)}$ para todo $s$, con desigualdad estricta en toda casilla donde la acción cambió.
3. Ninguna política se repite: el algoritmo para tras a lo más ${\prod_{s\in\mathcal T}\lvert\mathcal A(s)\rvert}$ rondas.
4. La política con que para es óptima, y su valor es $V^*$.

**Lectura.** Probar otra acción un paso y luego seguir igual nunca pierde valor.

**Casos nulos.** Si $\pi_0$ ya es óptima, basta una ronda. Si cada casilla tiene una sola acción, también.
:::

::: proof {#mkv-c3-pi-dem-iterar-politicas of="mkv-c3-teo-iterar-politicas"}
Sea $\pi$ una política que termina y $\pi'$ su mejora. Como $\pi'(s)$ maximiza y $\pi(s)$ es una de las opciones,

$$
\begin{aligned}
r_{\pi'}+P_{\pi',\mathcal T}V_\pi\ &\ge\ r_\pi+P_{\pi,\mathcal T}V_\pi\\
&=V_\pi,
\end{aligned}
$$

entrada por entrada. $P_{\pi',\mathcal T}$ no tiene entradas negativas, así que la desigualdad se puede aplicar $n$ veces:

$$
\begin{aligned}
V_\pi\ &\le\ \sum_{t=0}^{n-1}P_{\pi',\mathcal T}^{\,t}\,r_{\pi'}\\
&\quad+P_{\pi',\mathcal T}^{\,n}\,V_\pi.
\end{aligned}
$$

La suma es lo que se espera recibir en los primeros $n$ pasos con $\pi'$. El último término está acotado por ${\max_s\lvert V_\pi(s)\rvert}$.

- **Termina.** Si $\pi'$ no terminara, la condición de @mkv-c3-teo-bellman diría que vale $-\infty$ en algún estado. Pero la desigualdad acota sus sumas por abajo, para todo $n$. Entonces $\pi'$ termina.
- **No baja.** Como $\pi'$ termina, ${P_{\pi',\mathcal T}^{\,n}\to0}$ y queda ${V_\pi\le V_{\pi'}}$.
- **Sube donde cambia.** Por la regla de empates, si la acción cambió en $s$ es porque ${Q_\pi(s,\pi'(s))>V_\pi(s)}$. Con ${V_{\pi'}\ge V_\pi}$, ${V_{\pi'}(s)\ge Q_\pi(s,\pi'(s))>V_\pi(s)}$.
- **Para.** El valor crece estrictamente en cada cambio, así que ninguna política se repite. Hay ${\prod_s\lvert\mathcal A(s)\rvert}$ políticas.
- **Óptima.** Al parar, $\pi(s)$ alcanza el máximo en cada $s$: ${V_\pi(s)=\max_aQ_\pi(s,a)}$. Es una solución de Bellman, y por @mkv-c3-teo-bellman es $V^*$.
:::

- **La política inicial importa.** Una $\pi_0$ que no termina no se puede evaluar: ${I-P_{\pi,\mathcal T}}$ es singular, como en esperar siempre de @mkv-c3-teo-evaluar.
- **La regla de empates importa.** Sin ella, la acción puede cambiar sin que el valor suba, y el argumento de «no se repite» se cae.

**En el juguete.** Hay ${2\cdot2=4}$ políticas, así que a lo más 4 rondas. Desde caminar–caminar el valor sube de ${(-6,-3)}$ a ${(-5,-2)}$, estricto en las dos casillas aunque la acción cambió solo en la 2. Usó 2 rondas.

> [!TIP]
> **Ejemplo y contraejemplo.** Cambia el pasillo: caminar en la casilla 2 cuesta 2, no 3. Ahora caminar y correr empatan ahí: correr da ${-1+\tfrac12(-2)=-2}$, igual que caminar.
> - **Lo cumple:** conservar en empate. Desde caminar–caminar, con valor ${(-5,-2)}$, la casilla 2 empata y se queda caminar. Para en una ronda.
> - **No lo cumple:** cambiar en empate. Caminar–caminar pasa a caminar–correr, que vale lo mismo, ${(-5,-2)}$, y en la siguiente ronda regresa. Alterna para siempre.

::: figure {#mkv-c3-fig-ej-empates title="Conservar o cambiar en un empate"}
![Dos paneles con el pasillo donde caminar en la casilla 2 cuesta 2. Arriba, marcado como cumple: conservar en empate; desde caminar–caminar, con valor (−5, −2), en la casilla 2 caminar y correr empatan en −2, se conserva caminar y el algoritmo para en una ronda. Abajo, marcado como no cumple: cambiar en empate; caminar–caminar pasa a caminar–correr y regresa, las dos con valor (−5, −2), en un ciclo que no termina. Debajo de cada grafo, las matrices de caminar y de correr. Pie: sin la regla de empates, la política cambia sin que el valor suba](../_assets/mkv-c3-ej-empates.svg)
:::

Las dos son óptimas: el algoritmo encontró el óptimo, pero nunca se entera de que ya llegó. Sutton y Barto lo dejan como el ejercicio 4.4 de su libro (2.ª ed., 2018).

::: exercise {#mkv-c3-pi-ej-cota title="Cuenta la cota"}
Un MDP tiene 5 estados no terminales con 3 acciones cada uno. ¿Cuántas rondas, a lo más, garantiza el teorema?
:::

::: hint {#mkv-c3-pi-pista-cota of="mkv-c3-pi-ej-cota" title="¿Cuántas políticas hay?"}
¿Cuántas acciones puedes elegir en cada estado, y cómo se combinan entre estados?
:::

::: answer {#mkv-c3-pi-resp-cota of="mkv-c3-pi-ej-cota"}
Hay ${3^5=243}$ políticas, así que a lo más 243 rondas. Es una cota de peor caso: suelen bastar pocas.
:::

Falta escribirlo para que lo haga un programa.

---

## 3 · Calcular con ITERACIÓN DE POLÍTICAS

**Piensa: ¿qué necesita guardar el programa entre una ronda y la siguiente?**

Solo la política actual: el valor se recalcula exacto en cada ronda.

### El mapa de ITERACIÓN DE POLÍTICAS

- **Qué calcula:** una política óptima y su valor.
- **Qué guarda:** la política actual $\pi$ y su valor $V_\pi$.
- **Cómo avanza:** evalúa $\pi$ con un sistema lineal y la reemplaza por su codiciosa, conservando la acción en los empates.
- **Qué devuelve al terminar:** $\pi^*$ y $V^*$, exactos, cuando una mejora no cambia nada.

::: figure {#mkv-c3-fig-flujo-politicas title="Iteración de políticas, en palabras"}
![Diagrama de flujo de iteración de políticas, en palabras. 1: Empieza con una política que termina. 2: Evalúala: resuelve el sistema lineal de su valor. 3: En cada casilla, prueba cada acción un paso y luego sigue con la política. 4: Quédate con la mejor; si la actual empata, consérvala. 5, pregunta: ¿cambió alguna casilla? Si sí, regresa al paso 2 con la política nueva. Si no, 6: devuelve la política y su valor](../_assets/mkv-c3-flujo-politicas.svg)
:::

```text
INPUT   un MDP finito con las condiciones
        de Bellman; π₀, que termina.
OUTPUT  π*, una política óptima, y V*.

 1 function ITERAR-POLÍTICAS(MDP, π₀)
 2   π ← π₀
 3   repetir
 4     V ← EVALUAR-POLÍTICA(MDP, π)
 5     para cada s en 𝒯:
 6       Q(a) ← r(s,a) + Σ P(s'|s,a) V(s')
 7       si π(s) alcanza el máximo de Q:
           π'(s) ← π(s)
         si no: π'(s) ← un a que maximiza Q
 8     si π' = π: return π, V
 9     π ← π'
```

**Gemelo Python.** Cada comentario numerado remite al pseudocódigo. `resolver` es la eliminación exacta de [[mkv-absorcion|Cuánto falta para terminar]]; `evaluar` arma ${I-P_{\pi,\mathcal T}}$ y $r_\pi$ como en @mkv-c3-teo-evaluar. Un MDP es un diccionario: estado, acción, recompensa y destinos; la meta no es llave y vale 0.

```python
from fractions import Fraction as F
from itertools import count

def resolver(M, b):              # eliminación exacta
    k = len(b)
    M = [list(f) + [c] for f, c in zip(M, b)]
    for c in range(k):
        p = next((r for r in range(c, k)
                  if M[r][c] != 0), None)
        if p is None:
            return None          # singular
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [x / piv for x in M[c]]
        for r in range(k):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y
                        for x, y in zip(M[r], M[c])]
    return [M[r][k] for r in range(k)]

def evaluar(mdp, pol):                     # (4)
    pos = {s: i for i, s in enumerate(mdp)}
    k = len(mdp)
    M = [[F(0)] * k for _ in mdp]
    b = [F(0)] * k
    for s, i in pos.items():
        r, P = mdp[s][pol[s]]
        M[i][i] += 1
        b[i] = F(r)
        for t, p in P.items():
            if t in pos:                   # meta: V = 0
                M[i][pos[t]] -= p
    V = resolver(M, b)
    if V is None:
        raise ValueError("π no termina")
    return dict(zip(mdp, V))

def q(mdp, V, s, a):                       # (6)
    r, P = mdp[s][a]
    return r + sum(p * V.get(t, 0)
                   for t, p in P.items())

def mejorar(mdp, V, pol, conservar):       # (5)
    nueva = {}
    for s in mdp:
        qs = {a: q(mdp, V, s, a) for a in mdp[s]}
        top = max(qs.values())
        empate = [a for a in qs if qs[a] == top]
        if conservar and pol[s] in empate:
            nueva[s] = pol[s]              # (7)
        else:
            otra = [a for a in empate if a != pol[s]]
            nueva[s] = (otra or empate)[0]
    return nueva

def iterar_politicas(mdp, pol, conservar=True,
                     max_rondas=None):     # (1)
    rondas = (count(1) if max_rondas is None
              else range(1, max_rondas + 1))
    for ronda in rondas:                   # (3)
        V = evaluar(mdp, pol)              # (4)
        nueva = mejorar(mdp, V, pol,
                        conservar)         # (5)
        if nueva == pol:                   # (8)
            return pol, V, ronda
        pol = nueva                        # (9)
    return None                 # tope sin parar

def pasillo(n=2, caminar=3):
    """Casillas 1..n, meta n+1; hueco si i % 3 == 1.
    caminar: costo de caminar solo en la casilla n."""
    mdp, h = {}, F(1, 2)
    for i in range(n, 0, -1):     # de la meta hacia atrás
        sig = i + 1 if i < n else "meta"
        mal = -6 if i % 3 == 1 else -1
        cam = -caminar if i == n else -3
        mdp[i] = {"caminar": (cam, {sig: F(1)}),
                  "correr": (mal, {i: h, sig: h})}
    return mdp

J2 = pasillo()
for ini in ("caminar", "correr"):
    pol, V, k = iterar_politicas(J2, {1: ini, 2: ini})
    print(ini, "->", pol[1], pol[2],
          V[1], V[2], "rondas:", k)
# caminar -> caminar correr -5 -2 rondas: 2
# correr -> caminar correr -5 -2 rondas: 2

EMP = pasillo(caminar=2)       # caminar en 2 cuesta 2
cc = {1: "caminar", 2: "caminar"}
print(iterar_politicas(EMP, cc)[2])
print(iterar_politicas(EMP, cc, conservar=False,
                       max_rondas=50))
# 1
# None
```

**Cada pieza, en su línea:**

- **Línea 4.** `evaluar` lanza un error si $\pi$ no termina: la eliminación se queda sin pivote. Por eso $\pi_0$ debe terminar.
- **Línea 7.** `conservar=True` es la regla de empates del teorema. Con `False`, el empate se rompe hacia la otra acción.
- **Línea 8.** Comparar políticas es exacto; no hay tolerancia, porque las fracciones no redondean. Además de $\pi$ y $V$, el Python devuelve cuántas rondas usó.
- **`max_rondas`.** Por omisión no hay tope: con `conservar=True` el teorema garantiza que para. Con tope, si se agota, devuelve `None`, sin garantía.
- **`pasillo`.** Recorre las casillas de la meta hacia atrás: la eliminación casi no rellena y 200 casillas tardan menos de un segundo.

**Cómo leer la traza.** Corremos el pasillo desde caminar–caminar. Cada renglón dice qué deja la línea indicada.

**Tramo único · De caminar–caminar a caminar–correr**

| Ronda | Línea | Qué queda |
|---|---|---|
| 1 | 4 | V = (−6, −3) |
| 1 | 6 | en 2: −3 contra −5/2; en 1: −6 contra −21/2 |
| 1 | 9 | π = caminar–correr |
| 2 | 4 | V = (−5, −2) |
| 2 | 8 | sin cambios: devuelve π y V |

- **Contraejemplo, en código.** Con caminar a costo 2, `conservar=True` para en la ronda 1. Con `False` y un tope de 50 rondas, lo agota y devuelve `None`.

::: exercise {#mkv-c3-pi-ej-sin-conservar title="Rompe el empate al revés"}
En el pasillo original, donde caminar en 2 cuesta 3, corres `iterar_politicas(J2, cc, conservar=False)`. ¿Para? ¿Con qué política?
:::

::: hint {#mkv-c3-pi-pista-sin-conservar of="mkv-c3-pi-ej-sin-conservar" title="¿Hay algún empate en el pasillo original?"}
Revisa las cuentas de la sección 1: ¿alguna comparación dio dos números iguales?
:::

::: answer {#mkv-c3-pi-resp-sin-conservar of="mkv-c3-pi-ej-sin-conservar"}
Sí para, en 2 rondas, con caminar–correr. En el pasillo original nunca hay empate: la regla solo decide cuando dos acciones dan exactamente lo mismo.
:::

### Lo que garantiza y cuánto cuesta

- **Propiedades:** el valor nunca baja y sube estrictamente donde la acción cambia (@mkv-c3-teo-iterar-politicas).
- **Número que da:** caminar–correr con ${(-5,-2)}$ en el pasillo, en 2 rondas desde caminar–caminar o desde correr–correr.
- **Garantía:** para en a lo más ${\prod_s\lvert\mathcal A(s)\rvert}$ rondas y devuelve $V^*$ exacto, sin tolerancia ni cota de paro.
- **Costo por ronda:** evaluar resuelve un sistema de ${\lvert\mathcal T\rvert}$ incógnitas, del orden de ${\lvert\mathcal T\rvert^3}$; mejorar calcula un $Q$ por cada par estado–acción.
- **Supuestos:** las condiciones de @mkv-c3-teo-bellman, una $\pi_0$ que termina y la regla de empates.

Cada ronda cuesta más que una de iteración de valores. ¿Cuántas hacen falta?

> **Una nota de historia.** El algoritmo lleva el nombre de Ronald A. Howard, que lo presentó en *Dynamic Programming and Markov Processes* (Technology Press del MIT y Wiley, 1960).

---

## 4 · Comparar con iteración de valores en el PASILLO

**Piensa: en un pasillo de 200 casillas, ¿cuántas rondas necesita cada algoritmo?**

Iteración de políticas, muy pocas: cada mejora corrige todas las casillas a la vez. El pasillo grande tiene casillas 1 a 200 y meta 201, con hueco sin barandal en cada casilla ${i\equiv1\pmod3}$.

- **Políticas.** Hay $2^{200}\approx1.6\times10^{60}$ políticas. La cota del teorema no ayuda.
- **Primera mejora.** Con caminar siempre, ${V(i)=V(i+1)-3}$, así que ${V(1)=-600}$. Junto a un barandal, correr da ${-1+\tfrac12V(i)+\tfrac12V(i+1)=V(i+1)-\tfrac52}$, mejor que caminar. Junto a un hueco, correr da ${V(i+1)-\tfrac{15}2}$, peor.
- **Resultado.** Una sola mejora ya encuentra la regla local: caminar junto al hueco, correr junto al barandal.

```python
largo = pasillo(n=200)
siempre = {i: "caminar" for i in largo}
pol, V, k = iterar_politicas(largo, siempre)
print(k, pol[1], pol[2])
print(V[1])
# 2 caminar correr
# -467
```

**El número que da.** Iteración de políticas usa 2 rondas desde caminar siempre (una mejora y una que confirma) y da ${V^*(1)=-467}$ exacto. Iteración de valores necesita 451 rondas para bajar el residuo a $10^{-9}$, y aun así da un valor aproximado.

::: figure {#mkv-c3-fig-rondas-politicas title="Una mejora basta para llegar"}
![Iteración de políticas en el pasillo de dos casillas. Desde caminar–caminar, con V = (−6, −3), y desde correr–correr, con V = (−14, −2), una mejora llega a caminar–correr, con V = (−5, −2), y la siguiente no cambia nada. Abajo, el pasillo de 200 casillas: valores, 451 rondas hasta residuo de 10⁻⁹; políticas, 1 mejora desde caminar siempre](../_assets/mkv-c3-rondas-politicas.svg)
:::

- **Por qué tan pocas.** El valor de una política ya trae el futuro entero, no $k$ pasos. La mejora decide con información completa.
- **Por qué no siempre conviene.** Cada ronda resuelve un sistema de 200 incógnitas, barato aquí porque cada casilla apunta solo a sí misma y a la siguiente.

::: exercise {#mkv-c3-pi-ej-sin-castigo title="Quita el castigo del pasillo grande"}
En el pasillo de 200 casillas, caer al hueco ya no cuesta nada más: correr cuesta 1 en todas las casillas. Desde caminar siempre, ¿qué hace la primera mejora?
:::

::: hint {#mkv-c3-pi-pista-sin-castigo of="mkv-c3-pi-ej-sin-castigo" title="¿Qué cambia junto al hueco?"}
Con caminar siempre, ¿cuánto da correr junto a un hueco si cuesta 1 en vez de 6?
:::

::: answer {#mkv-c3-pi-resp-sin-castigo of="mkv-c3-pi-ej-sin-castigo"}
Junto a un hueco, correr da ahora ${-1+\tfrac12V(i)+\tfrac12V(i+1)=V(i+1)-\tfrac52}$, como junto al barandal. La primera mejora cambia todas las casillas a correr. Con correr siempre, ${V(i)=V(i+1)-2}$, y caminar daría ${V(i+1)-3}$: la segunda ronda no cambia nada y el algoritmo para.
:::

Aplica la ronda a mano a un pasillo distinto.

---

## Ejercicios

::: exercise {#mkv-c3-pi-ej-sin-hueco title="El pasillo sin castigo"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Toma el pasillo de dos casillas. **Cambia una idea:** el hueco de la casilla 1 ya no castiga; si resbalas ahí, solo pierdes el turno, como en la 2.

1. **Escribe el MDP.** ¿Cuánto vale ahora $r(1,\text{correr})$? Lo demás no cambia.
2. **Evalúa.** Calcula el valor de caminar–caminar.
3. **Mejora.** Calcula $Q_\pi(s,a)$ en las dos casillas. ¿Qué política sale? ¿Cuántas casillas cambiaron?
4. **Termina.** Evalúa la nueva política y mejora otra vez. ¿Cuántas rondas usó el algoritmo? ¿Cuánto vale $V^*$?
5. **Pon el castigo en 1.** Con castigo 1, ${r(1,\text{correr})=-\tfrac32}$. Repite desde caminar–caminar conservando en empate. ¿Dónde aparece un empate y qué política devuelve?
:::

::: hint {#mkv-c3-pi-pista-sin-hueco-1 of="mkv-c3-pi-ej-sin-hueco" title="Pista 1 · ¿Qué cuenta hace cada ronda?"}
¿Cuál es el sistema de dos ecuaciones de la política actual? Con su solución, ¿cuánto da cada acción en cada casilla si después sigues con esa política?
:::

::: hint {#mkv-c3-pi-pista-sin-hueco-2 of="mkv-c3-pi-ej-sin-hueco" title="Pista 2 · ¿Tus valores tienen sentido?"}
¿El valor de cada política nueva es al menos el de la anterior, casilla por casilla? ¿Concuerda tu respuesta del inciso 5 con la frontera «correr en 1 conviene si el castigo es menor que 1»?
:::

::: answer {#mkv-c3-pi-resp-sin-hueco of="mkv-c3-pi-ej-sin-hueco" title="Respuesta · El pasillo sin castigo"}
**1. El MDP.** Sin castigo, correr en 1 solo tarda: ${r(1,\text{correr})=-1}$.

**2. Evaluar.** Caminar–caminar no cambia: ${(V(1),V(2))=(-6,-3)}$.

**3. Mejorar.**

$$
\begin{aligned}
Q_\pi(2,\text{caminar})&=-3,\\
Q_\pi(2,\text{correr})&=-\tfrac52,\\
Q_\pi(1,\text{caminar})&=-6,\\
Q_\pi(1,\text{correr})&=-1+\tfrac12(-6)+\tfrac12(-3)\\
&=-\tfrac{11}2.
\end{aligned}
$$

Correr gana en las dos: sale correr–correr. Cambiaron las dos casillas en una sola mejora.

**4. Terminar.** Correr–correr da ${V(2)=-2}$ y ${V(1)=-1+\tfrac12V(1)-1}$, o sea ${V(1)=-4}$. Mejorar: en 2, $-3$ contra $-2$; en 1, ${-3-2=-5}$ contra ${-1-2-1=-4}$. Nada cambia. Usó 2 rondas y ${V^*=(-4,-2)}$.

**5. Castigo 1.** En la ronda 1, en la casilla 1 caminar da $-6$ y correr ${-\tfrac32-3-\tfrac32=-6}$: empatan, y se conserva caminar. La casilla 2 pasa a correr. En la ronda 2, con ${(-5,-2)}$, caminar da $-5$ y correr ${-\tfrac32-\tfrac52-1=-5}$: otro empate, se conserva caminar. Devuelve caminar–correr con ${(-5,-2)}$. Es la frontera: con castigo 1 las dos acciones valen lo mismo en la casilla 1.
:::

**Punto de control:** deberías poder correr una ronda de iteración de políticas a mano, decir por qué el valor no baja y por qué el algoritmo para, y explicar qué hace la regla de empates.

---

## Lo que hay que llevarse

- **La ronda.** Evaluar con un sistema lineal (@mkv-c3-teo-evaluar) y mejorar con la codiciosa de $V_\pi$, conservando la acción en los empates.
- **En el juguete.** Desde caminar–caminar, ${(-6,-3)}$, o desde correr–correr, ${(-14,-2)}$, una mejora llega a caminar–correr, ${(-5,-2)}$. Una segunda ronda lo confirma.
- **El teorema.** Con las condiciones de Bellman, una $\pi_0$ que termina y la regla de empates, el valor no baja y el algoritmo para con $\pi^*$ en a lo más ${\prod_s\lvert\mathcal A(s)\rvert}$ rondas (@mkv-c3-teo-iterar-politicas).
- **Los empates.** Si la mejora cambia en empate, puede alternar para siempre entre dos políticas del mismo valor.
- **El costo.** Rondas caras y pocas: en el PASILLO, 2 rondas contra 451 de iteración de valores.

Evaluar es un sistema lineal y mejorar es un máximo; las dos piezas juntas suenan a optimización. ¿Es esto un problema de optimización como los de la unidad 6?

Continúa con [[mkv-mdp-lineal|El MDP como programa lineal]].
