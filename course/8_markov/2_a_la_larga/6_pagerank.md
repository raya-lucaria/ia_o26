---
id: mkv-pagerank
title: "PageRank: el navegante al azar"
nav_title: "PageRank"
summary: "Si solo conoces los enlaces entre páginas, ¿cuál es la más importante? Un navegante al azar vuelve la web una cadena; dos arreglos le dan una sola estacionaria, que se calcula a mano, con la iteración de potencias sin armar la matriz y simulando al navegante."
status: ready
estimated_time: 32m
tags: [markov]
---

# PageRank: el navegante al azar

**Si de una web solo conoces quién enlaza a quién, ¿cómo ordenas sus páginas por importancia?**

Al terminar tendrás:

- **La cadena del navegante.** Convertirás una lista de enlaces en una matriz de transición y verás dónde falla.
- **Los dos arreglos.** Construirás $\overline P$ y la matriz de Google $G$, y explicarás qué condición arregla cada uno.
- **El teorema.** Aplicarás @mkv-c2-teo-pagerank para garantizar una sola estacionaria y la convergencia.
- **El algoritmo.** Correrás PAGERANK, la iteración de potencias sin armar $G$, y justificarás su costo.
- **Una comprobación.** Compararás la fracción del tiempo de un navegante simulado con la cuenta exacta.

## Lo que traes

- **La estacionaria.** Una fila $\mu$ con ${\mu P=\mu}$, que suma 1 (@mkv-c2-def-estacionaria). Es única si hay una sola clase cerrada (@mkv-c2-teo-unica).
- **La convergencia.** Con una sola clase cerrada aperiódica, ${\mu_0P^t\to\mu}$ desde todo $\mu_0$ (@mkv-c2-teo-converge). La fracción del tiempo tiende a $\mu(s)$ (@mkv-c2-teo-ergodico).
- **Las clases.** En [[mkv-clasificar-estados|Clasificar los estados]], una clase cerrada no deja salir; un lazo ${P_{ss}>0}$ basta para que sea aperiódica.
- **La iteración de potencias.** En [[mkv-olvida-su-inicio|¿Olvida su inicio?]], multiplicar ${\mu\leftarrow\mu P}$ hasta que la distancia ${\lVert\cdot\rVert_1}$ entre dos vectores seguidos baja de $\mathrm{tol}$, con un tope de pasos.

> **Modelo y datos.** Una web finita de $k$ páginas, con enlaces fijos. No leemos el texto de las páginas: solo los enlaces.

---

## 1 · Convertir los enlaces en una cadena

**Piensa: ¿qué tiene que ver un navegante distraído con la importancia de una página?**

Imagina a alguien que, en cada paso, sigue al azar uno de los enlaces de la página donde está. A la larga, pasa más tiempo en las páginas a las que llegan muchos caminos. Esa fracción del tiempo es la medida de importancia.

::: definition {#mkv-c2-pr-def-navegante title="La cadena del navegante"}
- **Qué es:** la cadena cuyos estados son las $k$ páginas y que, desde $s$, sigue uno de sus enlaces con la misma probabilidad.
- **Cómo se calcula:** sea $\operatorname{salidas}(s)$ el conjunto de páginas a las que enlaza $s$. Si no es vacío, ${P_{ss'}=1/\lvert\operatorname{salidas}(s)\rvert}$ cuando $s'$ está en él, y 0 si no.
- **Qué significa:** la fila de $s$ reparte su peso por igual entre sus enlaces; la importancia se lee en la estacionaria.
- **Qué no es:** no cuenta enlaces recibidos. Un enlace de una página muy visitada pesa más que uno de una página olvidada.
:::

- **Lectura de ${\lvert\operatorname{salidas}(s)\rvert}$.** Es cuántas páginas distintas enlaza $s$; repetir un enlace no lo cuenta dos veces.
- **El hueco.** Si $s$ no enlaza a nadie, la fórmula no da nada: la fila de $s$ queda en ceros y no suma 1.

**En el juguete.** La web de @mkv-c2-fig-web-juguete tiene cuatro páginas. Los enlaces son A→B, A→C, B→C, C→A y C→D; de D no sale ninguno. La figura ya muestra el PageRank: el resultado que buscamos.

::: figure {#mkv-c2-fig-web-juguete title="Una web de cuatro páginas; D no enlaza a nadie"}
![Web de juguete con cuatro páginas A, B, C y D. Flechas: de A a B y de A a C; de B a C; de C a A y de C a D. D, con borde punteado, no tiene enlaces de salida. Junto a cada página, su PageRank con α = 0.85 y salto uniforme: A = 1429/6107 ≈ 0.234, B = 1140/6107 ≈ 0.187, C = 2109/6107 ≈ 0.345, D = 1429/6107 ≈ 0.234](../_assets/mkv-c2-web-juguete.svg)
:::

En el orden A, B, C, D, la cadena del navegante da esta matriz:

$$
P=\begin{pmatrix}
0&1/2&1/2&0\\
0&0&1&0\\
1/2&0&0&1/2\\
0&0&0&0
\end{pmatrix}.
$$

- **Filas A, B, C.** Suman 1: A reparte entre dos enlaces, B tiene uno, C reparte entre dos.
- **Fila D.** Suma 0. $P$ no es una matriz de transición, y ningún teorema de la estacionaria aplica todavía.

::: exercise {#mkv-c2-pr-ej-fila title="Escribe la fila que cambia"}
Agrega un enlace B→A a la web de juguete. ¿Cómo queda la fila B de $P$? ¿Cambia alguna otra fila?
:::

::: hint {#mkv-c2-pr-pista-fila of="mkv-c2-pr-ej-fila" title="¿Cuántas salidas tiene B ahora?"}
¿Cuántas páginas enlaza B después del cambio?
:::

::: answer {#mkv-c2-pr-resp-fila of="mkv-c2-pr-ej-fila"}
Ahora B enlaza a dos páginas, A y C, así que la fila B es ${(1/2,\ 0,\ 1/2,\ 0)}$. Las demás filas no cambian: cada fila depende solo de los enlaces que **salen** de su página.
:::

La fila en ceros es el primer problema; hay un segundo, menos visible.

---

## 2 · Reparar los dos agujeros

**Piensa: ¿qué hace el navegante cuando llega a D, y qué pasa si cae en un ciclo?**

Hay dos agujeros, y cada uno tiene su arreglo.

- **Página sin salidas.** En D el navegante no tiene a dónde ir. La fila no suma 1.
- **Ciclo que atrapa.** Si dos páginas solo se enlazan entre sí, forman una clase cerrada: quien entra no sale. Si es la única clase cerrada, toda estacionaria vale 0 fuera de ella.
- **Con dos ciclos así.** Hay dos clases cerradas y la estacionaria deja de ser única (@mkv-c2-teo-unica).
- **Con periodo.** Un par que se alterna es la cadena A↔B de periodo 2: desde una de sus páginas, $\mu_t$ alterna entre dos vectores distintos y no converge (@mkv-c2-teo-converge).

El primer arreglo tapa la fila vacía. Para escribirlo usamos un **vector de salto** $v$: una fila $1\times k$ con ${v(s)>0}$ y ${\sum_sv(s)=1}$. Aquí, uniforme: ${v(s)=1/k}$.

::: definition {#mkv-c2-pr-def-barra title="La matriz con las filas vacías tapadas, P̄"}
- **Qué es:** $\overline P$ («pe barra») es $P$ con cada fila sin salidas sustituida por $v$.
- **Cómo se calcula:** si $s$ enlaza a alguna página, su fila no cambia; si no enlaza a ninguna, su fila es $v$.
- **Qué significa:** desde una página sin salidas, el navegante va a una página elegida con $v$.
- **Qué no es:** no es la tilde de la clase 1, que marca una estimación suavizada. La barra marca una fila reparada.
:::

**En el juguete.** Con ${k=4}$, la fila D pasa a ser ${v=(1/4,\ 1/4,\ 1/4,\ 1/4)}$. Las otras tres filas son las de $P$.

El segundo arreglo rompe los ciclos. En cada paso, con probabilidad $\alpha$ el navegante sigue $\overline P$; con probabilidad ${1-\alpha}$ se aburre y salta a una página elegida con $v$.

::: definition {#mkv-c2-pr-def-google title="La matriz de Google, G"}
- **Qué es:** la matriz de transición del navegante que a veces salta:

$$
G=\alpha\overline P+(1-\alpha)\mathbf 1v.
$$

- **Cómo se calcula:** $\mathbf 1v$ es la matriz $k\times k$ cuyas filas son todas $v$. Entonces ${G_{ss'}=\alpha\overline P_{ss'}+(1-\alpha)v(s')}$.
- **Qué significa:** $\alpha$ es la probabilidad de seguir un enlace; ${1-\alpha}$, la de saltar. El valor usual es ${\alpha=0.85}$.
- **Qué no es:** este $\alpha$ no es el de la poda alfa-beta. En esta unidad no hay otro $\alpha$.
:::

- **El PageRank.** Es la estacionaria $\mu$ de $G$: ${\mu G=\mu}$, ${\mu\ge0}$, ${\sum_s\mu(s)=1}$.
- **Un atajo útil.** Como $\mu$ suma 1, ${\mu\mathbf 1=1}$ y ${\mu(\mathbf 1v)=v}$. Por eso:

$$
\mu G=\alpha\,\mu\overline P+(1-\alpha)\,v.
$$

**En el juguete.** Con ${\alpha=17/20}$, cada entrada recibe ${(1-\alpha)/4=3/80}$ del salto. La fila B, que manda todo a C, queda así:

$$
\begin{aligned}
G_{BC}&=\tfrac{17}{20}\cdot1+\tfrac{3}{80}=\tfrac{71}{80},\\
G_{BA}&=G_{BB}=G_{BD}=\tfrac{3}{80}.
\end{aligned}
$$

::: theorem {#mkv-c2-teo-pagerank title="El salto da una sola estacionaria y la iteración converge"}
Sea una web finita de $k$ páginas, $\overline P$ como en @mkv-c2-pr-def-barra y ${G=\alpha\overline P+(1-\alpha)\mathbf 1v}$.

**Condición.** ${0\le\alpha<1}$, ${v(s)>0}$ para toda página y ${\sum_sv(s)=1}$.

Entonces:

1. $G$ es una matriz de transición con todas sus entradas positivas: ${G_{ss'}\ge(1-\alpha)v(s')>0}$.
2. $G$ tiene una sola estacionaria $\mu$, y ${\mu_0G^t\to\mu}$ desde todo $\mu_0$.
3. Cada paso multiplica la distancia por $\alpha$ o menos:

$$
\begin{aligned}
\lVert\mu_{t+1}-\mu\rVert_1&\le\alpha\,\lVert\mu_t-\mu\rVert_1,\\
\lVert\mu_t-\mu\rVert_1&\le2\alpha^t.
\end{aligned}
$$
:::

- **Lectura.** El salto conecta toda página con toda página en un paso. No quedan ciclos que atrapen ni periodos que hagan oscilar.
- **Casos nulos.** Con ${\alpha=0}$, ${G=\mathbf 1v}$ y ${\mu=v}$: los enlaces no importan. Con ${\alpha=1}$, ${G=\overline P}$ y vuelven las trampas; por eso se excluye.
- **Suficiente, no necesaria.** En el juguete, $\overline P$ sola ya tiene una sola clase cerrada, aperiódica por el lazo de D. El salto sirve para **toda** web, no solo para esta.

::: proof {#mkv-c2-pr-dem-pagerank of="mkv-c2-teo-pagerank"}
**1. Entradas.** Cada fila de $\overline P$ y de $\mathbf 1v$ suma 1, así que la de $G$ suma ${\alpha+(1-\alpha)=1}$. Como ${\overline P_{ss'}\ge0}$, se tiene ${G_{ss'}\ge(1-\alpha)v(s')>0}$.

**2. Una clase, aperiódica.** Con todas las entradas positivas, cada página alcanza a cada otra en un paso: hay una sola clase y es cerrada. Además ${G_{ss}>0}$, un lazo, así que es aperiódica. @mkv-c2-teo-unica y @mkv-c2-teo-converge dan el resto.

**3. Contracción.** Sea ${z=\mu_t-\mu}$; sus entradas suman 0, así que ${z\mathbf 1v=0}$. Como ${\mu G=\mu}$:

$$
\begin{aligned}
\mu_{t+1}-\mu&=zG=\alpha\,z\overline P,\\
\lVert z\overline P\rVert_1
&\le\sum_s\lvert z_s\rvert\sum_{s'}\overline P_{ss'}=\lVert z\rVert_1.
\end{aligned}
$$

Al empezar, ${\lVert\mu_0-\mu\rVert_1\le\lVert\mu_0\rVert_1+\lVert\mu\rVert_1=2}$; cada paso multiplica por $\alpha$ o menos.
:::

> [!WARNING]
> **Confundir importancia con enlaces recibidos.** En el juguete, B y D reciben un enlace cada una.
> **Pesa quién enlaza y entre cuántas salidas reparte:** B recibe la mitad de A, y D la mitad de C, que es más visitada.

**De dónde viene.** Brin y Page describieron PageRank en 1998, en «The Anatomy of a Large-Scale Hypertextual Web Search Engine». Su $d$ es nuestra $\alpha$: «We usually set d to 0.85». Escribieron la fórmula con $(1-d)$ en lugar de $(1-d)/k$. Con ella los valores suman el número de páginas, aunque el artículo dice que forman una distribución de probabilidad y suman 1.

En el reporte técnico de 1999 de Page, Brin, Motwani y Winograd, el navegante «se aburre» (*gets bored*) y salta a una página al azar. Las páginas sin salidas las quitaban, calculaban y luego las reinsertaban. Sustituir su fila por $v$, como hace $\overline P$, es la convención moderna.

::: exercise {#mkv-c2-pr-ej-fila-g title="Arma otra fila de G"}
Con ${\alpha=17/20}$ y $v$ uniforme, escribe la fila A de $G$ en el juguete. Comprueba que suma 1.
:::

::: hint {#mkv-c2-pr-pista-fila-g of="mkv-c2-pr-ej-fila-g" title="¿Qué recibe cada entrada?"}
¿Cuánto vale ${\alpha\overline P_{As'}}$ para cada $s'$, y cuánto le suma el salto a todas?
:::

::: answer {#mkv-c2-pr-resp-fila-g of="mkv-c2-pr-ej-fila-g"}
La fila A de $\overline P$ es ${(0,\ 1/2,\ 1/2,\ 0)}$. Con ${\tfrac{17}{20}\cdot\tfrac12=\tfrac{34}{80}}$ y el salto ${\tfrac{3}{80}}$:

$$
G_{A\cdot}=\left(\tfrac{3}{80},\ \tfrac{37}{80},\ \tfrac{37}{80},\ \tfrac{3}{80}\right),
$$

que suma ${80/80=1}$.
:::

$G$ ya cumple el teorema; falta calcular su estacionaria.

---

## 3 · Resolver la web de juguete a mano

**Piensa: ¿hay que escribir $G$ completa para resolver ${\mu G=\mu}$?**

No. El atajo ${\mu G=\alpha\mu\overline P+(1-\alpha)v}$ da una ecuación por página sin armar $G$.

> **Dado:** los enlaces de una web finita, ${0\le\alpha<1}$ y un vector de salto $v$ positivo que suma 1.
>
> **Encontrar:** el PageRank $\mu$, la única estacionaria de $G$ (@mkv-c2-teo-pagerank).

- **En general.** Para cada página $s'$, lo que llega por enlaces más lo que llega por salto:

$$
\mu(s')=\alpha\sum_{s}\mu(s)\,\overline P_{ss'}+(1-\alpha)\,v(s').
$$

- **En el juguete.** Escribimos ${\mu=(a,\ b,\ c,\ d)}$. Con ${\alpha=17/20}$ y ${(1-\alpha)/4=3/80}$:

$$
\begin{aligned}
a&=\tfrac{17}{20}\left(\tfrac{c}{2}+\tfrac{d}{4}\right)+\tfrac{3}{80},\\
b&=\tfrac{17}{20}\left(\tfrac{a}{2}+\tfrac{d}{4}\right)+\tfrac{3}{80},\\
c&=\tfrac{17}{20}\left(\tfrac{a}{2}+b+\tfrac{d}{4}\right)+\tfrac{3}{80},\\
d&=\tfrac{17}{20}\left(\tfrac{c}{2}+\tfrac{d}{4}\right)+\tfrac{3}{80}.
\end{aligned}
$$

- **Un empate.** Las ecuaciones de $a$ y $d$ tienen el mismo lado derecho: ${a=d}$. A y D reciben lo mismo, la mitad de C y la cuarta parte de D.
- **Despejar.** Con ${d=a}$, la primera da ${63a=34c+3}$ y la segunda ${80b=51a+3}$.
- **Normalizar.** Con ${2a+b+c=1}$, multiplicamos por 1360 y queda ${6107a=1429}$.

$$
\begin{aligned}
\mu&=\tfrac{1}{6107}\,(1429,\ 1140,\ 2109,\ 1429)\\
&\approx(0.234,\ 0.187,\ 0.345,\ 0.234).
\end{aligned}
$$

- **El orden.** C primero, A y D empatadas, B al final. Por los enlaces originales, C recibe de A y de B, y B solo de A. Además, las cuatro reciben partes iguales de la fila reparada de D (un cuarto cada una) y del salto.
- **D sin salidas.** D empata con A aunque no enlaza a nadie: no tener salidas no la deja en cero. Sus salidas también cuentan: con un enlace D→A, D bajaría a 0.175. El PageRank depende de toda la red y del salto.

::: exercise {#mkv-c2-pr-ej-comprobar title="Comprueba la tercera ecuación"}
Sustituye ${a=d=1429/6107}$ y ${b=1140/6107}$ en la ecuación de $c$. ¿Obtienes ${2109/6107}$?
:::

::: hint {#mkv-c2-pr-pista-comprobar of="mkv-c2-pr-ej-comprobar" title="¿Con qué denominador trabajas?"}
¿Puedes multiplicar todo por 6107 y trabajar con enteros?
:::

::: answer {#mkv-c2-pr-resp-comprobar of="mkv-c2-pr-ej-comprobar"}
Por 6107: ${\tfrac{1429}{2}+1140+\tfrac{1429}{4}=\tfrac{8847}{4}}$. Luego:

$$
\begin{aligned}
&\tfrac{17}{20}\cdot\tfrac{8847}{4}+\tfrac{3}{80}\cdot6107\\
&\quad=\tfrac{150399+18321}{80}\\
&\quad=\tfrac{168720}{80}=2109.
\end{aligned}
$$

Sí: ${c=2109/6107}$.
:::

Con cuatro páginas bastan fracciones; con millones de páginas, el sistema no se resuelve así.

---

## 4 · Iterar sin armar la matriz de Google

**Piensa: ¿qué cambia en la iteración de potencias cuando la matriz tiene millones de filas?**

Solo el producto. ${G}$ es densa: tiene $k^2$ entradas positivas. Pero $\overline P$ casi no tiene enlaces por fila, y el atajo ${\mu G=\alpha\mu\overline P+(1-\alpha)v}$ evita armar $G$.

### El mapa de PAGERANK

- **Qué calcula:** el PageRank $\mu$, la estacionaria de $G$.
- **Qué guarda:** la lista de enlaces que salen de cada página, $v$, el vector actual y el siguiente.
- **Cómo avanza:** reparte $\mu(s)$ entre los enlaces de $s$; junta el peso de las páginas sin salidas y lo reparte con $v$. Multiplica por $\alpha$ y suma ${(1-\alpha)v}$.
- **A qué converge y bajo qué condición:** a $\mu$, desde todo inicio, si ${0\le\alpha<1}$ y ${v>0}$ (@mkv-c2-teo-pagerank).

El flujo es el de la iteración de potencias de [[mkv-olvida-su-inicio|¿Olvida su inicio?]]: multiplicar, medir la distancia, parar con $\mathrm{tol}$ o con el tope. Las líneas 4 a 11 sustituyen su línea 4, `nuevo ← μ·P`; el paro y el tope no cambian.

```text
INPUT   páginas 0…k−1; salidas(s),
        lista de destinos de s, sin
        repetir; 0 ≤ α < 1; v > 0
        que suma 1; tol > 0; tope.
OUTPUT  μ, cerca de la estacionaria
        de G, y los pasos dados (o
        «no paró» si llegó al tope).

 1 function PAGERANK(salidas,α,v,tol,tope)
 2   μ ← v
 3   for t ← 1 to tope
 4     nuevo ← k ceros
 5     colgado ← 0          ▷ cambia
 6     for each s in 0…k−1
 7       if salidas(s) está vacía
 8         colgado ← colgado + μ(s)
 9       for each s′ in salidas(s)
10         nuevo(s′) += μ(s)/|salidas(s)|
11     nuevo ← α·(nuevo + colgado·v)
              + (1 − α)·v   ▷ cambia
12     if ‖nuevo − μ‖₁ ≤ tol
13       return nuevo, t
14     μ ← nuevo
15   return μ, «no paró»
```

**Gemelo Python.** Cada comentario numerado remite al pseudocódigo. Las páginas son ${0,\dots,k-1}$, en el orden de `v`.

```python
def pagerank(salidas, alfa, v, tol, tope=10_000):  # (1)
    k = len(v)
    mu = list(v)                                   # (2)
    for t in range(1, tope + 1):                   # (3)
        nuevo = [0.0] * k                          # (4)
        colgado = 0.0                              # (5)
        for s in range(k):                         # (6)
            if not salidas[s]:                     # (7)
                colgado += mu[s]                   # (8)
            for s2 in salidas[s]:                  # (9)
                nuevo[s2] += mu[s] / len(salidas[s])  # (10)
        nuevo = [alfa * (x + colgado * v[j])       # (11)
                 + (1 - alfa) * v[j]
                 for j, x in enumerate(nuevo)]
        dist = sum(abs(x - y) for x, y in zip(nuevo, mu))
        if dist <= tol:                            # (12)
            return nuevo, t                        # (13)
        mu = nuevo                                 # (14)
    return mu, None                                # (15)

salidas = [[1, 2], [2], [0, 3], []]   # A, B, C, D
mu, pasos = pagerank(salidas, 0.85, [0.25] * 4, 1e-8)
print([round(x, 3) for x in mu], pasos)
# [0.234, 0.187, 0.345, 0.234] 28
```

**Cada pieza, en su línea:**

- **Líneas 7 y 8.** El peso de D no se pierde: se guarda en `colgado`. Es la fila $v$ de $\overline P$, sin escribirla.
- **Líneas 9 y 10.** Cada página reparte su peso entre sus enlaces: es ${\mu\overline P}$ en las filas con salidas.
- **Línea 11.** Aplica el atajo: ${\alpha\,\mu\overline P+(1-\alpha)v}$.
- **Línea 12.** Es el paro de la iteración de potencias: la distancia entre dos vectores seguidos.

**Cómo leer la traza.** Empezamos en ${\mu_0=v}$. Cada renglón muestra $\mu$ tras la vuelta $t$, con tres decimales. A y D comparten columna porque son iguales en todo paso.

**Tramo único · La web de juguete**

| t | μ(A) = μ(D) | μ(B) | μ(C) |
|---:|---|---|---|
| 0 | 0.250 | 0.250 | 0.250 |
| 1 | 0.197 | 0.197 | 0.409 |
| 2 | 0.253 | 0.163 | 0.330 |
| 3 | 0.232 | 0.199 | 0.338 |
| 28 | 0.234 | 0.187 | 0.345 |

- **Paso 1.** C recibe de A, de B y del colgado de D: salta a 0.409.
- **Paso 28.** La distancia entre dos vectores seguidos baja de ${10^{-8}}$ y el algoritmo para. Coincide con la cuenta a mano.

::: exercise {#mkv-c2-pr-ej-alfa-cero title="Quita los enlaces"}
Corre una vuelta de PAGERANK a mano con ${\alpha=0}$ en el juguete. ¿Qué devuelve y en cuántos pasos?
:::

::: hint {#mkv-c2-pr-pista-alfa-cero of="mkv-c2-pr-ej-alfa-cero" title="¿Qué sobrevive en la línea 11?"}
Con ${\alpha=0}$, ¿qué términos de la línea 11 se anulan?
:::

::: answer {#mkv-c2-pr-resp-alfa-cero of="mkv-c2-pr-ej-alfa-cero"}
La línea 11 da ${\text{nuevo}=v}$. Como ${\mu_0=v}$, la distancia es 0 y para en el paso 1 con ${\mu=v}$. Es el caso nulo del teorema: sin seguir enlaces, todas las páginas valen ${1/4}$.
:::

### Lo que garantiza y cuánto cuesta

- **Propiedades:** cada vuelta conserva una distribución: suma 1 y no tiene entradas negativas.
- **Número que da:** en el juguete, ${(0.234,\ 0.187,\ 0.345,\ 0.234)}$ en 28 pasos con ${\mathrm{tol}=10^{-8}}$.
- **Garantía:** por @mkv-c2-teo-pagerank, ${\lVert\mu_t-\mu\rVert_1\le2\alpha^t}$; con ${\alpha=0.85}$, 118 pasos bastan para ${10^{-8}}$ en **cualquier** web. Si para por la línea 12, el vector devuelto está a lo más a ${\alpha\,\mathrm{tol}/(1-\alpha)}$ de $\mu$. Si para por el tope, esa cota no está garantizada: con tope 1, el juguete queda a 0.148 de $\mu$.
- **Costo:** cada vuelta cuesta del orden de $k$ más el número de enlaces. Armar $G$ costaría $k^2$ por vuelta.
- **Supuestos:** ${0\le\alpha<1}$, ${v>0}$, enlaces sin repetir y una web fija mientras se itera.

**De dónde sale la cota al parar.** Sea $x$ el vector anterior y ${y=xG}$ el que se devuelve, con ${\lVert y-x\rVert_1\le\mathrm{tol}}$. Por la contracción y la desigualdad del triángulo, ${\lVert y-\mu\rVert_1\le\alpha\lVert x-\mu\rVert_1\le\alpha(\mathrm{tol}+\lVert y-\mu\rVert_1)}$. Despejando, ${\lVert y-\mu\rVert_1\le\alpha\,\mathrm{tol}/(1-\alpha)}$.

La cuenta da $\mu$; un navegante simulado debería pasar ese tiempo en cada página.

---

## 5 · Simular al navegante

**Piensa: ¿qué tendría que observar un navegante que camina mucho tiempo?**

La fracción del tiempo que pasa en cada página. $G$ tiene una sola clase cerrada, así que @mkv-c2-teo-ergodico asegura, con probabilidad 1:

$$
\frac{N_T(s)}{T}\xrightarrow[T\to\infty]{}\mu(s).
$$

- **El experimento.** Una sola trayectoria de ${T=100\,000}$ pasos desde A, con semilla 2040. Cada paso muestrea la fila de $G$ con MUESTREAR-FILA.
- **Qué compara.** La fracción del tiempo en cada página contra el PageRank exacto.

| Página | Navegante | PageRank exacto |
|---|---|---|
| A | 0.234 | 0.234 |
| B | 0.185 | 0.187 |
| C | 0.346 | 0.345 |
| D | 0.235 | 0.234 |

- **Lectura.** C sigue primero y B al final. La simulación pone a D una milésima por encima de A, aunque sus PageRank exactos empatan: una trayectoria finita no tiene por qué conservar el empate. La mayor diferencia está en B: 0.18514 frente a 0.18667, es decir, 0.0015; la tabla, redondeada a tres cifras, la muestra como 0.002.
- **Lo que no dice.** Es una sola trayectoria. No da un intervalo de error con la fórmula de la clase 1.

> [!WARNING]
> **Usar el error estándar de réplicas independientes.** La fórmula ${\sqrt{p(1-p)/n}}$ supone $n$ réplicas independientes.
> **Las visitas de una misma trayectoria dependen unas de otras: el teorema ergódico asegura el límite, no ese error.**

::: exercise {#mkv-c2-pr-ej-inicio title="Cambia el inicio"}
Si el navegante empezara en D en lugar de A, ¿cambiaría el límite de las fracciones? ¿Cambiarían las fracciones observadas con ${T=100\,000}$?
:::

::: hint {#mkv-c2-pr-pista-inicio of="mkv-c2-pr-ej-inicio" title="¿Qué pide el teorema ergódico?"}
¿El teorema depende del estado inicial?
:::

::: answer {#mkv-c2-pr-resp-inicio of="mkv-c2-pr-ej-inicio"}
El límite no cambia: con una sola clase cerrada, la fracción tiende a $\mu(s)$ desde cualquier inicio. Las fracciones observadas pueden cambiar, porque la trayectoria es otra; el teorema habla del límite y no fija cuánto difieren dos corridas con ${T=100\,000}$.
:::

El juguete se resuelve a mano; la prueba de verdad es una web que nadie diseñó para el ejemplo.

---

## 6 · La web de este curso

**Piensa: si un navegante recorriera este curso siguiendo sus enlaces, ¿dónde pasaría más tiempo?**

Para responder tomamos una foto fija de los enlaces del curso, el 21 de octubre de 2026, antes de escribir esta clase.

- **Nodos.** Cada página de `course/` con id, fuera de los directorios de soporte: 134.
- **Enlaces.** Cada wikilink o enlace `raya:` a otra página, sin repetir ni a sí misma: 506.
- **Sin salidas.** 5 páginas no enlazan a ninguna, como D en el juguete. La notación de esta unidad es una.
- **Iteración.** Con ${\alpha=0.85}$, $v$ uniforme y ${\mathrm{tol}=10^{-8}}$, PAGERANK para en 88 pasos.

Las cinco de mayor PageRank:

1. [[ia-y-sociedad|IA y sociedad]], 0.061.
2. [[imaginar-la-maquina|Imaginar la máquina]], 0.057.
3. [[todo-es-un-numero|Todo es un número]], 0.030.
4. [[problema-de-la-parada|El problema de la parada]], 0.028.
5. [[la-bitacora-del-taller|La bitácora del taller]], 0.025.

- **Comparación.** Con $v$ uniforme, cada página arrancaría con ${1/134\approx0.007}$. Las dos primeras valen unas ocho veces eso.
- **Un casi-ciclo.** «IA y sociedad» enlaza solo a «Imaginar la máquina», y esta solo a «IA y sociedad». Quien entra a ese par solo sale saltando.
- **Más enlaces no es más rango.** La página que más enlaces recibe, [[escribir-el-juego|Escribir el juego]], con 12, no está entre las cinco.

> [!WARNING]
> **Leer el PageRank como calidad.** Mide dónde se acumula un navegante que sigue enlaces.
> **«IA y sociedad» sube por cómo está enlazada, no porque sea la página más importante del curso.**

::: exercise {#mkv-c2-pr-ej-par title="Sin el salto"}
Con ${\alpha=1}$, ¿qué haría el navegante del curso al entrar al par «IA y sociedad» – «Imaginar la máquina»? ¿Qué condición de @mkv-c2-teo-pagerank falla?
:::

::: hint {#mkv-c2-pr-pista-par of="mkv-c2-pr-ej-par" title="¿Sale alguna flecha del par?"}
Sin salto, ¿hay algún enlace que lleve fuera de esas dos páginas?
:::

::: answer {#mkv-c2-pr-resp-par of="mkv-c2-pr-ej-par"}
No saldría nunca: alternaría entre las dos, una clase cerrada de periodo 2. Falla ${\alpha<1}$.

Y el par no es la única clase cerrada: las cuatro páginas del taller («El modelo, escrito», «Enumerar», «La bitácora del taller» y «Ramificar y acotar») forman otra, aperiódica. Sin el salto, la estacionaria deja de ser única: la importancia se reparte entre las dos clases según dónde empiece el navegante, y desde el par ${\mu_t}$ alterna sin converger.
:::

---

## Ejercicios

::: exercise {#mkv-c2-pr-ej-trampa title="Calcula el PageRank de una web con trampa"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Una web tiene tres páginas, A, B y C, con enlaces A→B, B→C y C→B. Ninguna página está sin salidas. **Cambia una idea:** el problema ya no es una fila vacía, sino un ciclo que atrapa. Usa ${\alpha=1/2}$ y $v$ uniforme, ${v(s)=1/3}$.

1. **Diagnostica.** Escribe $P$ en el orden A, B, C. ¿Qué clase cerrada hay y qué periodo tiene?
2. **Sin salto.** Con ${\alpha=1}$, ¿cuánto vale la estacionaria en A? ¿Qué hace ${\mu_t}$ desde B?
3. **Con salto.** Escribe las tres ecuaciones de ${\mu=\alpha\mu\overline P+(1-\alpha)v}$ y resuélvelas.
4. **Garantía.** ¿Qué distancia a $\mu$ asegura el teorema tras $t$ pasos?

:::

::: hint {#mkv-c2-pr-pista-trampa-1 of="mkv-c2-pr-ej-trampa" title="Pista 1 · ¿Quién enlaza a cada página?"}
¿Qué páginas aportan a la ecuación de A? ¿Y a las de B y C?
:::

::: hint {#mkv-c2-pr-pista-trampa-2 of="mkv-c2-pr-ej-trampa" title="Pista 2 · ¿Tu respuesta pasa dos controles?"}
¿Suman 1 tus tres valores? ¿Cumple cada uno su ecuación al sustituirlo?
:::

::: answer {#mkv-c2-pr-resp-trampa of="mkv-c2-pr-ej-trampa" title="Respuesta · El PageRank de la web con trampa"}
**1. Diagnóstico.**

$$
P=\begin{pmatrix}0&1&0\\0&0&1\\0&1&0\end{pmatrix}.
$$

$\{B,C\}$ es una clase cerrada de periodo 2; A es transitoria. Como no hay filas vacías, ${\overline P=P}$.

**2. Sin salto.** La estacionaria vale 0 en A, porque A queda fuera de la clase cerrada; es ${(0,\ 1/2,\ 1/2)}$. Desde B, ${\mu_t}$ alterna entre B y C y no converge.

**3. Con salto.** Con ${(1-\alpha)/3=1/6}$:

$$
\begin{aligned}
a&=\tfrac16,\\
b&=\tfrac12(a+c)+\tfrac16,\\
c&=\tfrac12\,b+\tfrac16.
\end{aligned}
$$

Nadie enlaza a A: ${a=1/6}$. Sustituyendo, ${b=4/9}$ y ${c=7/18}$; suman ${3/18+8/18+7/18=1}$.

**4. Garantía.** ${\lVert\mu_t-\mu\rVert_1\le2\cdot(1/2)^t}$: la distancia se reduce al menos a la mitad en cada paso.
:::

**Punto de control:** deberías poder convertir una lista de enlaces en $P$, repararla con $\overline P$ y el salto, y escribir $G$. También, explicar qué condición de @mkv-c2-teo-pagerank resuelve cada arreglo, y calcular el PageRank a mano, con PAGERANK y simulando.

---

## Lo que hay que llevarse

- **El modelo.** El navegante sigue un enlace con probabilidad $\alpha$ y salta con ${1-\alpha}$: ${G=\alpha\overline P+(1-\alpha)\mathbf 1v}$, con ${\alpha=0.85}$.
- **Los arreglos.** $\overline P$ tapa las filas sin salidas con $v$; el salto rompe ciclos y periodos. Brin y Page quitaban esas páginas; $\overline P$ es la convención moderna.
- **El teorema.** Con ${0\le\alpha<1}$ y ${v>0}$, todas las entradas de $G$ son positivas: una estacionaria y convergencia, con distancia ${\le2\alpha^t}$.
- **El juguete.** La estacionaria es

  $$
  \begin{aligned}
  \mu&=(1429,\ 1140,\ 2109,\ 1429)/6107\\
  &\approx(0.234,\ 0.187,\ 0.345,\ 0.234);
  \end{aligned}
  $$

  PAGERANK para en 28 pasos, y el navegante simulado queda a menos de 0.002 en cada página.
- **El costo.** Cada vuelta cuesta del orden de $k$ más los enlaces, porque ${\mu G=\alpha\mu\overline P+(1-\alpha)v}$ no arma $G$.
- **El curso.** 134 páginas, 506 enlaces, 88 pasos; arriba, «IA y sociedad» con 0.061.
- **La clase, junta.** Clasificar los estados dice qué clases cerradas hay; eso decide si la estacionaria es única y si $\mu_t$ olvida su inicio. La absorción mide cuánto falta para llegar, y PageRank arregla una cadena para que tenga una sola estacionaria.

Continúa con [[mkv-resumen-a-la-larga|el resumen de la clase]].
