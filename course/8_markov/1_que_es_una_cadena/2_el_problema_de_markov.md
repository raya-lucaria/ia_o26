---
id: mkv-el-problema-de-markov
title: "El problema de Markov"
nav_title: "El problema de Markov"
summary: "¿Las letras de un texto son tiradas independientes de un dado? El conteo de Markov en 1913 y el mismo en el Quijote; la definición de cadena, la probabilidad de una trayectoria, cómo leer su matriz y su grafo, cómo se muestrea una fila y qué dicen las rachas de consonantes."
status: ready
estimated_time: 35m
tags: [markov]
---

# El problema de Markov

**¿Las letras de un texto son como tiradas independientes de un dado?**

Al terminar tendrás:

- **La pregunta de Markov, contada** en la frase, en el *Eugenio Oneguin* y en el *Quijote*.
- **La definición de cadena** finita y homogénea, $(\mathcal S,\mu_0,P)$: «sin memoria» no es «independiente».
- **La probabilidad de una trayectoria,** como producto de entradas de $P$.
- **La anatomía de una matriz de transición,** con 2, 3 y $k$ estados.
- **MUESTREAR-FILA,** trazado a mano y en Python, y las rachas de consonantes como prueba de la hipótesis.

## Lo que traes

- **Probabilidad condicional.** En [[mkv-lo-que-necesitas|Lo que necesitas de probabilidad]] calculaste $\Pr(A\mid B)=\Pr(A\cap B)/\Pr(B)$, definida si $\Pr(B)>0$, y la estimaste con frecuencias, $\widehat{\Pr}$.
- **Variables y distribuciones.** $S_t$ es el estado en la posición $t$, todavía aleatorio. Una distribución es un vector de probabilidades que suma 1.
- **Regla del producto.** Una probabilidad conjunta se encadena: $\Pr(A\cap B)=\Pr(A)\Pr(B\mid A)$, y así con más eventos.
- **Independencia e independencia condicional.** $A$ es independiente de $B$ si $\Pr(A\mid B)=\Pr(A)$; lo es **dado** $C$ si $\Pr(A\mid B,C)=\Pr(A\mid C)$.
- **Una probabilidad dentro de un modelo.** En [[cuando-decide-un-dado|Cuando decide un dado]], $\Pr(a\mid s)$ daba la probabilidad de cada resultado del dado en el estado $s$.

---

## 1 · Contar vocales y consonantes en la frase

**Piensa: si la letra actual es vocal, ¿cambia la probabilidad de que la siguiente también lo sea?**

Sí, y se ve contando. Toma la frase del hilo, «Con la iglesia hemos dado, Sancho», sin mayúsculas, espacios ni puntuación, como Markov. Quedan 27 letras; debajo de cada una va V si es vocal y C si es consonante:

```text
conlaiglesiahemosdadosancho
CVCCVVCCVCVVCVCVCCVCVCVCCCV
```

Una vocal acentuada cuenta como su vocal; la ñ y la «y», como consonantes. La «y» va siempre así porque la regla debe depender solo de la letra, no de sus vecinas.

Hay 12 vocales y 15 consonantes, y 26 pares. La «o» final no tiene siguiente: solo 11 vocales cuentan.

::: table {#mkv-c1-tabla-pares-frase title="Qué sigue a cada clase de letra, en la frase"}
| Letra actual | Le sigue V | Le sigue C | Con siguiente |
|---|---:|---:|---:|
| V | 2 | 9 | 11 |
| C | 10 | 5 | 15 |
:::

Divide cada renglón entre su total:

$$
\widehat{\Pr}(V\mid V)=\frac{2}{11},
\qquad
\widehat{\Pr}(V\mid C)=\frac{10}{15}=\frac{2}{3}.
$$

- **Tras una vocal,** otra vocal salió 2 de 11 veces.
- **Tras una consonante,** una vocal salió 2 de cada 3 veces.

Con letras independientes, las dos estimarían lo mismo: la probabilidad de vocal. Aquí una es más del triple de la otra. **Las letras tienden a alternarse.**

::: exercise {#mkv-c1-ej-complementos title="Completa los complementos"}
Con la tabla de los pares de la frase, calcula $\widehat{\Pr}(C\mid V)$ y $\widehat{\Pr}(C\mid C)$. ¿Cuánto suma cada una con su $\widehat{\Pr}(V\mid\cdot)$?
:::

::: hint {#mkv-c1-pista-complementos of="mkv-c1-ej-complementos" title="El mismo renglón"}
¿Entre qué total divides si la letra actual sigue siendo la misma?
:::

::: answer {#mkv-c1-resp-complementos of="mkv-c1-ej-complementos"}
$\widehat{\Pr}(C\mid V)=9/11$ y $\widehat{\Pr}(C\mid C)=5/15=1/3$. Cada una suma 1 con su complemento: $2/11+9/11=1$ y $2/3+1/3=1$. Tras cualquier letra viene una vocal o una consonante.
:::

Con 26 pares, la diferencia podría ser casualidad. Markov hizo la misma cuenta con miles de letras.

---

## 2 · Plantear el problema original

**Piensa: ¿por qué un matemático contaría a mano las vocales de un poema?**

Por una disputa sobre la ley de los grandes números: con repeticiones independientes, la frecuencia de un evento se acerca a su probabilidad. ¿Hace falta la independencia?

- **1902 · Nekrásov.** Pável Nekrásov sostuvo que la independencia era condición **necesaria** para la ley de los grandes números. Así interpretó Markov su tesis.
- **1906 · Markov.** Respondió con variables dependientes, encadenadas, que también cumplen la ley. Así definió lo que hoy llamamos cadenas; él hablaba de «ensayos ligados en cadena».
- **1913 · *Eugenio Oneguin*.** Siete años después aplicó la idea a un texto. No era la respuesta a Nekrásov, sino una aplicación a datos.

En 1913 contó a mano las primeras 20 000 letras del poema, sin espacios ni puntuación. Son letras, no palabras.

- **Vocales y consonantes.** Halló 8 638 vocales y 11 362 consonantes.
- **Tras vocal.** Hubo 1 104 pares vocal-vocal: $\widehat{\Pr}(V\mid V)=1\,104/8\,638\approx0.128$.
- **Tras consonante.** Hubo 7 534 pares consonante-vocal: $\widehat{\Pr}(V\mid C)=7\,534/11\,362\approx0.663$.

**Lo mismo en el *Quijote*.** Con las mismas reglas, sus 1 620 532 letras tienen 752 551 vocales: $\widehat{\Pr}(V)\approx0.464$. Tras una vocal, la siguiente es vocal con frecuencia $0.181$; tras una consonante, con $0.710$.

::: table {#mkv-c1-tabla-oneguin-quijote title="La pregunta de Markov en ruso y en español"}
| Cifra | *Oneguin* (1913) | *Quijote* |
|---|---:|---:|
| Letras contadas | 20 000 | 1 620 532 |
| Vocal tras vocal | 0.128 | 0.181 |
| Vocal tras consonante | 0.663 | 0.710 |
:::

Poema y novela repiten la forma de la frase: tras vocal, otra vocal es rara. Con más de un millón de letras, eso ya no se explica por haber contado poco. **Las letras no se comportan como tiradas independientes.**

::: exercise {#mkv-c1-ej-denominador title="Elige el denominador"}
¿Por qué Markov dividió los 1 104 pares vocal-vocal entre 8 638 y no entre 20 000?
:::

::: hint {#mkv-c1-pista-denominador of="mkv-c1-ej-denominador" title="Qué se sabe ya"}
En $\Pr(V\mid V)$, ¿qué evento ya ocurrió?
:::

::: answer {#mkv-c1-resp-denominador of="mkv-c1-ej-denominador"}
Porque condiciona a que la letra actual sea vocal: el denominador cuenta solo los casos donde $B$ ocurrió, como en $\Pr(A\cap B)/\Pr(B)$. Dividir entre 20 000 estimaría la probabilidad de que un par sea vocal-vocal, que es otra pregunta.
:::

Contar muestra que la letra actual importa. Para trabajar con eso hace falta un modelo.

---

## 3 · Definir una cadena de Markov

**Piensa: ¿qué es lo mínimo que hay que saber para producir letras como las de esas tablas?**

Basta saber dónde empezar y, desde cada estado, con qué probabilidad sigue cada otro. Un **estado** es lo que el modelo mira en cada paso; aquí, la clase de la letra. Los estados forman $\mathcal S$, con $k=|\mathcal S|$; en la frase, $\mathcal S=\{V,C\}$ y $k=2$. Un estado concreto es $s$; el siguiente, $s'$.

::: definition {#mkv-c1-cadena title="Cadena de Markov finita y homogénea"}
**Qué es.** Una sucesión $S_0,S_1,S_2,\dots$ con valores en un conjunto finito $\mathcal S$, descrita por tres piezas, $(\mathcal S,\mu_0,P)$:

- **$\mathcal S$,** los estados.
- **$\mu_0$,** la distribución inicial: un vector fila con $\mu_0(s)=\Pr(S_0=s)$ que suma 1. Empezar en C es $\mu_0=(0,1)$.
- **$P$,** la matriz de transición, de $k\times k$: $P(s'\mid s)$ es la probabilidad de pasar de $s$ a $s'$ en un paso.

**Cómo se calcula.** Para todo $t$ y toda historia $s_0,\dots,s_{t-1},s$ con probabilidad positiva:

$$
\begin{aligned}
&\Pr(S_{t+1}=s'\mid S_t=s,\,S_{t-1}=s_{t-1},\dots,S_0=s_0)\\
&\quad=\Pr(S_{t+1}=s'\mid S_t=s)=P(s'\mid s).
\end{aligned}
$$

La primera igualdad es la **propiedad de Markov**. La segunda dice que la cadena es **homogénea**: la misma $P$ sirve en cada paso $t$.

**Qué significa.** Dado el presente, el pasado no agrega nada para predecir el siguiente paso: $S_{t+1}$ es independiente de $S_0,\dots,S_{t-1}$ **dado** $S_t$. La entrada $P(s'\mid s)$ también se escribe $P_{ss'}$ y se lee «estando en $s$, ir a $s'$».

**Qué no es.** No es independencia. «Sin memoria» no quiere decir que el siguiente ignore el presente: en la frase, la vocal pasó de $2/11$ a $2/3$ según la letra actual. Lo que sobra es lo anterior al presente.
:::

Como avisa [[notacion-markov|la hoja de notación]], esta $P$ no es la clase P de complejidad ni esta $\mu$ el multiplicador de KKT.

**El grafo dibuja la misma cadena.** Lleva un nodo por estado y una flecha $s\to s'$ por cada $P(s'\mid s)>0$, con su número.

**En la frase.** Las frecuencias contadas dan una cadena con $\mu_0=(0,1)$ y, en el orden V, C:

$$
\widehat P=\begin{pmatrix}2/11 & 9/11\\ 2/3 & 1/3\end{pmatrix}.
$$

El gorro marca que la matriz sale de datos. $P$ sin gorro es la matriz de un modelo, genérica o verdadera.

::: figure {#mkv-c1-grafo-vc title="El grafo de la frase"}
![Grafo de dos estados, V (vocal, círculo) y C (consonante, cuadro), con la matriz estimada de la frase. Desde V: un lazo a V con 2/11 y una flecha a C con 9/11. Desde C: una flecha a V con 2/3 y un lazo a C con 1/3. Las flechas que salen de un mismo estado suman 1](../_assets/mkv-c1-grafo-vc.svg)
:::

::: exercise {#mkv-c1-ej-dado-markov title="¿Un dado es una cadena?"}
Imagina letras independientes: cada una es vocal con la misma probabilidad, sin importar las anteriores. ¿Es una cadena de Markov? ¿Cómo son las filas de su $P$?
:::

::: hint {#mkv-c1-pista-dado-markov of="mkv-c1-ej-dado-markov" title="Prueba la definición"}
Si nada del pasado importa, ¿importa el presente?
:::

::: answer {#mkv-c1-resp-dado-markov of="mkv-c1-ej-dado-markov"}
Sí. Con independencia, condicionar a cualquier historia no cambia nada, así que la propiedad de Markov se cumple. Las dos filas de $P$ son iguales: la probabilidad de V y la de C. Toda sucesión independiente con la misma distribución en cada paso es una cadena homogénea, pero no al revés: en $\widehat P$ las filas difieren.
:::

La cadena ya tiene sus tres piezas. ¿Qué probabilidad le da a un tramo entero de texto?

---

## 4 · Calcular la probabilidad de una trayectoria

**Piensa: ¿qué probabilidad le da la cadena a una secuencia completa de estados?**

La probabilidad inicial por una entrada de $P$ en cada paso. Una **trayectoria** es la secuencia de estados $s_0,s_1,\dots,s_t$; un texto pasado a V y C es una trayectoria observada. Escribimos $\Pr(s_0,\dots,s_t)$ por $\Pr(S_0=s_0,\dots,S_t=s_t)$.

**A mano, el tramo `conla`.** Es C V C C V, con $\mu_0=(0,1)$ y la cadena $\widehat P$:

::: table {#mkv-c1-tabla-tramo-conla title="Los factores de C V C C V"}
| Paso | Par | Factor |
|---|---|---:|
| inicio | empieza en C | 1 |
| $j=0$ | C→V | 2/3 |
| $j=1$ | V→C | 9/11 |
| $j=2$ | C→C | 1/3 |
| $j=3$ | C→V | 2/3 |
:::

$$
\Pr(C,V,C,C,V)=1\cdot\tfrac{2}{3}\cdot\tfrac{9}{11}\cdot\tfrac{1}{3}\cdot\tfrac{2}{3}=\tfrac{4}{33}.
$$

Si la cadena produjera muchas veces cinco estados desde C, unas 4 veces de cada 33 saldría C V C C V.

**Con cualquier número de estados.** La regla del producto encadena un factor por paso. La propiedad de Markov recorta cada condición al estado anterior, y la homogeneidad vuelve cada factor una entrada de $P$:

$$
\begin{aligned}
\Pr(s_0,\dots,s_t)
&=\Pr(s_0)\prod_{j=0}^{t-1}\Pr(s_{j+1}\mid s_0,\dots,s_j)\\
&=\mu_0(s_0)\prod_{j=0}^{t-1}P(s_{j+1}\mid s_j).
\end{aligned}
$$

El índice $j$ recorre los pasos, de 0 a $t-1$. **La fórmula vale con propiedad de Markov y homogeneidad.** Si un tramo inicial tiene probabilidad 0, los dos lados valen 0.

::: exercise {#mkv-c1-ej-tramo-corto title="Multiplica un tramo corto"}
Con $\mu_0=(0,1)$ y $\widehat P$ de la frase:

1. **Calcula.** ¿Cuánto vale $\Pr(C,C,V)$?
2. **Cambia el inicio.** ¿Cuánto vale $\Pr(V,C)$?
:::

::: hint {#mkv-c1-pista-tramo-corto of="mkv-c1-ej-tramo-corto" title="El primer factor"}
¿Cuánto vale $\mu_0$ en el primer estado de cada tramo?
:::

::: answer {#mkv-c1-resp-tramo-corto of="mkv-c1-ej-tramo-corto"}
1. **$\Pr(C,C,V)=1\cdot\frac{1}{3}\cdot\frac{2}{3}=\frac{2}{9}$.**
2. **$\Pr(V,C)=0$.** El factor inicial es $\mu_0(V)=0$: la cadena empieza en C.
:::

Cada factor salió de un renglón de $\widehat P$. ¿Cómo se lee una matriz así cuando hay más estados?

---

## 5 · Leer la matriz de transición

**Piensa: ¿qué dice cada renglón, cada columna y cada cero de $P$?**

Cada fila es una distribución: la del siguiente estado, estando en el estado de esa fila.

- **Filas = desde dónde; columnas = hacia dónde.** $P_{ss'}$ está en la fila $s$ y la columna $s'$. La fila C de $\widehat P$, $(2/3,\ 1/3)$, va desde C.
- **Es cuadrada, $k\times k$.** Los mismos estados están de los dos lados: de donde sales y a donde llegas.
- **Cada fila suma 1; las columnas no.** Desde $s$ hay que ir a algún lado: es estocástica por filas. La columna V, $2/11+2/3$, no suma 1.
- **Un 0 dice «imposible en el modelo».** No prueba que sea imposible en la realidad.
- **La diagonal es quedarse.** $\widehat P(V\mid V)=2/11$ es seguir en vocal.
- **Matriz y grafo son lo mismo.** Cada entrada positiva es una flecha de la figura @mkv-c1-grafo-vc.
- **Conteos frente a probabilidades.** La tabla @mkv-c1-tabla-pares-frase también es cuadrada, pero sus filas suman 11 y 15. Dividir cada fila entre su total la vuelve estocástica.
- **Vector fila, a la izquierda.** Una distribución como $\mu_0$ es fila y multiplica a $P$ por la izquierda. Algunos libros usan columnas y $P^{\mathsf T}$.

**Con 3 estados.** Si conservas los espacios, el espacio «_» es un tercer estado:

```text
con la iglesia hemos dado sancho
CVC_CV_VCCVCVV_CVCVC_CVCV_CVCCCV
```

Son 32 símbolos y 31 transiciones. En el orden V, C, _:

::: table {#mkv-c1-tabla-pares-tres title="Qué sigue a cada estado, con espacios"}
| Desde | A V | A C | A _ |
|---|---:|---:|---:|
| V | 1 | 7 | 3 |
| C | 10 | 3 | 2 |
| _ | 1 | 4 | 0 |
:::

$$
\widehat P=\begin{pmatrix}
1/11 & 7/11 & 3/11\\
2/3 & 1/5 & 2/15\\
1/5 & 4/5 & 0
\end{pmatrix}.
$$

- **Las filas suman 1.** Sus totales eran 11, 15 y 5 transiciones.
- **Las columnas no.** La columna _ suma $3/11+2/15+0$, menos de 1.
- **El 0 es por construcción.** Los blancos seguidos se juntan en uno, así que tras un espacio nunca viene otro.
- **El paso cambió.** Con espacios, V→V baja de 2 a 1: «la iglesia» ya no junta la «a» con la «i».

**Con $k$ estados.** Si $\mathcal S=\{s_1,\dots,s_k\}$, la matriz tiene $k^2$ entradas y cada fila es una distribución sobre los $k$ estados:

$$
P=\begin{pmatrix}
P_{s_1s_1} & \cdots & P_{s_1s_k}\\
\vdots & \ddots & \vdots\\
P_{s_ks_1} & \cdots & P_{s_ks_k}
\end{pmatrix},
\qquad
\sum_{s'\in\mathcal S}P(s'\mid s)=1.
$$

**Lo que el juguete no muestra.** Con 2 estados, una fila se fija con un solo número; con $k$, hacen falta $k-1$.

::: exercise {#mkv-c1-ej-fila-c-tres title="Lee la fila C con espacios"}
En la matriz de 3 estados, ¿qué dice la entrada $2/15$? ¿Suma 1 su fila?
:::

::: hint {#mkv-c1-pista-fila-c-tres of="mkv-c1-ej-fila-c-tres" title="Fila y columna"}
¿En qué fila y en qué columna está?
:::

::: answer {#mkv-c1-resp-fila-c-tres of="mkv-c1-ej-fila-c-tres"}
Está en la fila C y la columna _: tras una consonante, un espacio salió 2 de 15 veces. La fila suma $\frac{10+3+2}{15}=1$.
:::

Hasta aquí, la matriz describe lo contado. ¿Prueba que el texto sea una cadena?

---

## 6 · Separar la hipótesis del hecho

**Piensa: ¿el texto «es» una cadena de Markov?**

No lo sabemos. **El texto es una trayectoria observada; la cadena es un modelo.** Contar da frecuencias $\widehat{\Pr}$ y una matriz $\widehat P$. Que una cadena haya producido el texto es una hipótesis útil, no un hecho.

**Un contraejemplo diminuto.** Un proceso repite el bloque C C V para siempre: C C V C C V C C V… Empieza en cualquiera de las tres letras del bloque, al azar. Entonces:

- **Después de C C,** la siguiente es V con probabilidad 1.
- **Después de V C,** la siguiente es V con probabilidad 0.

Saber solo «estoy en C» no basta: hace falta la letra anterior. Ninguna $P(V\mid C)$ sirve para las dos historias, así que la propiedad de Markov falla. Y sin ella, la fórmula de la trayectoria deja de valer.

Agrupar letras tampoco la garantiza: aunque las letras siguieran una cadena, juntarlas en V y C puede romper la propiedad.

> [!WARNING]
> **Leer $\widehat P$ como una ley del idioma.** La matriz resume lo contado en un texto. **Es un modelo ajustado a esos datos; su validez se pone a prueba, no se supone.**

::: exercise {#mkv-c1-ej-estado-ccv title="Arregla el estado"}
En el proceso que repite C C V, ¿qué tendría que guardar el estado para que el siguiente dependa solo de él?
:::

::: hint {#mkv-c1-pista-estado-ccv of="mkv-c1-ej-estado-ccv" title="Lo que faltaba"}
¿Qué información distinguía las dos historias que terminan en C?
:::

::: answer {#mkv-c1-resp-estado-ccv of="mkv-c1-ej-estado-ccv"}
Las dos últimas letras. Con pares como estados, cada uno fija el siguiente: CC pasa a CV, CV pasa a VC y VC pasa a CC. El estado cambió; la idea de cadena, no.
:::

Para poner a prueba la hipótesis, produce texto con la cadena y compáralo con el real. Primero hay que sacar al azar un estado de una fila.

---

## 7 · Muestrear una fila

**Piensa: ¿cómo eliges al azar el siguiente estado si la fila dice $2/3$ para V y $1/3$ para C?**

Partes $[0,1)$ en pedazos tan largos como cada probabilidad y sorteas en cuál cae un número $u$. Es uniforme en $[0,1)$: cae en un pedazo de largo $p$ con probabilidad $p$. Elegir así, según una distribución, es **muestrear** (*sampling*).

**A mano, la fila C.** Las sumas acumuladas son $2/3$ y $1$. Si $u<2/3$, el siguiente es V; si no, C. Con $u=0.40$ sale V.

> **Dado:** una fila $(p_1,\dots,p_k)$ de $P$, en el orden $s_1,\dots,s_k$ de $\mathcal S$, y un uniforme $u\in[0,1)$.
>
> **Encontrar:** el índice $i$ del siguiente estado, $s_i$, de modo que cada $i$ salga con probabilidad $p_i$.

### El mapa de MUESTREAR-FILA

- **Qué calcula:** elige el siguiente estado de una fila con un solo uniforme.
- **Qué guarda:** una suma acumulada, que crece estado por estado.
- **Cómo avanza:** recorre la fila en el orden de $\mathcal S$ y suma la probabilidad de cada estado.
- **Qué devuelve al terminar:** el primer índice cuya suma acumulada pasa a $u$.

::: figure {#mkv-c1-flujo-muestrear title="Muestrear una fila, en palabras"}
![Diagrama de flujo de muestrear una fila, en palabras. Sortea u uniforme entre 0 y 1; empieza en el primer estado, con suma 0; suma la probabilidad de ese estado; pregunta si u es menor que la suma. Si sí, el siguiente estado es ese estado. Si no, pasa al que sigue y vuelve a sumar. Al pie: un solo u por paso; es lo que usa toda simulación de la clase](../_assets/mkv-c1-flujo-muestrear.svg)
:::

```text
INPUT   una fila p_1, …, p_k de P, en el orden
        s_1, …, s_k de 𝒮, que suma 1, y un
        uniforme u en [0, 1).
OUTPUT  el índice i del siguiente estado, s_i.

 1 function MUESTREAR-FILA(p_1, …, p_k, u)
 2   suma ← 0
 3   for i ← 1 to k            # en el orden de 𝒮
 4     suma ← suma + p_i       # fin del pedazo i
 5     if u < suma             # u cayó en el i
 6       return i
 7   return el último i con p_i > 0  # redondeo
```

**Gemelo Python.** Los comentarios indican la línea del pseudocódigo. Python cuenta desde 0: en el orden V, C, el índice 0 es V.

```python
from fractions import Fraction

def muestrear_fila(fila, u):                    # (1)
    suma = 0                                    # (2)
    for i, p in enumerate(fila):                # (3)
        suma += p                               # (4)
        if u < suma:                            # (5)
            return i                            # (6)
    return max(i for i, p in enumerate(fila) if p > 0)  # (7)

estados = ("V", "C")                  # el orden de 𝒮
P_gorro = [[Fraction(2, 11), Fraction(9, 11)],
           [Fraction(2, 3), Fraction(1, 3)]]
s = estados.index("C")                # s_0 = C
visitados = "C"
for u in (0.40, 0.75, 0.90, 0.25, 0.10):
    s = muestrear_fila(P_gorro[s], u)
    visitados += estados[s]
print(visitados)
# CVCCVV
```

**Cada pieza, en su línea:**

- **Línea 4.** La suma es el final del pedazo $i$: $[0,p_1)$, $[p_1,p_1+p_2)$ y así.
- **Línea 5.** El «menor que» estricto manda cada frontera al pedazo siguiente: cada pedazo mide exactamente $p_i$.
- **Línea 7.** Solo actúa si el redondeo deja la suma bajo $u$; nunca devuelve un estado con probabilidad 0.

**Cómo leer la traza.** Cada renglón es un paso $j$: el estado actual con las sumas de su fila, el uniforme y lo que devuelve.

**Tramo único · De C a CVCCVV**

| j | Desde · acumuladas | u | Siguiente |
|---:|---|---:|---|
| 0 | C · 2/3, 1 | 0.40 | V |
| 1 | V · 2/11, 1 | 0.75 | C |
| 2 | C · 2/3, 1 | 0.90 | C |
| 3 | C · 2/3, 1 | 0.25 | V |
| 4 | V · 2/11, 1 | 0.10 | V |

- **Paso 0.** $0.40<2/3$: cae en el pedazo de V.
- **Paso 1.** $0.75$ no es menor que $2/11$, pero sí que 1: sale C.
- **Paso 4.** $0.10<2/11$: sale V, aunque V→V sea la transición menos probable.

Los cinco uniformes producen la trayectoria `CVCCVV`. Una trayectoria simulada así, con sus propios uniformes e independiente de las demás, es una **réplica**.

### Lo que garantiza y cuánto cuesta

- **Propiedades:** termina en a lo más $k$ vueltas y usa un solo $u$. El orden de $\mathcal S$ cambia qué $u$ da cada estado, no su probabilidad.
- **Número que da:** un índice; desde C con $u=0.40$, el de V.
- **Garantía:** si $u$ es uniforme en $[0,1)$ y la fila suma 1, devuelve $i$ con probabilidad $p_i$, en aritmética exacta.
- **Costo:** hasta $k$ sumas y $k$ comparaciones; guarda un número.
- **Supuestos:** cada paso de una réplica usa un uniforme nuevo e independiente. En el código del curso salen de `random.Random(semilla)`: cada réplica se puede repetir.

::: exercise {#mkv-c1-ej-orden-estados title="Cambia el orden de los estados"}
En la fila V de $\widehat P$:

1. **Separa los pedazos.** ¿Qué valores de $u$ dan V y cuáles dan C?
2. **Invierte el orden.** Si $\mathcal S$ se recorre como C, V, ¿qué cambia?
:::

::: hint {#mkv-c1-pista-orden-estados of="mkv-c1-ej-orden-estados" title="Las sumas acumuladas"}
¿Cuál es la primera suma acumulada en cada orden?
:::

::: answer {#mkv-c1-resp-orden-estados of="mkv-c1-ej-orden-estados"}
1. **En el orden V, C,** $u<2/11$ da V y $u\ge2/11$ da C.
2. **En el orden C, V,** la primera suma es $9/11$: $u<9/11$ da C y el resto da V. Cambian los $u$ de cada estado; las probabilidades siguen siendo $2/11$ y $9/11$.
:::

Con MUESTREAR-FILA, la cadena produce réplicas tan largas como el *Quijote*. ¿Se parecen a él?

---

## 8 · Comparar las rachas de consonantes

**Piensa: si la cadena V/C fuera un buen modelo del texto, ¿qué debería reproducir?**

Entre otras cosas, cuántas consonantes seguidas aparecen. Una **racha** es un bloque de consonantes seguidas; su largo $L$ se cuenta desde la primera, y un valor concreto es $\ell$. Se descartan las rachas cortadas por el principio o el final del texto.

Bajo la cadena, tras cada consonante la siguiente es consonante con probabilidad $q=P(C\mid C)$, sin importar cuántas van. Una racha mide $\ell$ si siguen $\ell-1$ consonantes y luego una vocal:

$$
\Pr(L=\ell)=(1-q)\,q^{\ell-1},
\qquad \ell=1,2,\dots
$$

Vale con propiedad de Markov, homogeneidad y $q<1$; con $q=1$ la racha no termina. Con letras independientes sale la misma fórmula, con $q=\Pr(C)$.

**En el *Quijote*.** La cadena usa $q=\widehat P(C\mid C)\approx0.290$; las letras independientes, $q=\widehat{\Pr}(C)\approx0.536$. El corpus tiene 616 634 rachas completas:

::: table {#mkv-c1-tabla-rachas title="Fracción de rachas de cada largo"}
| ℓ | Reales | Cadena | Independientes |
|---:|---:|---:|---:|
| 1 | 0.624 | 0.710 | 0.464 |
| 2 | 0.344 | 0.206 | 0.249 |
| 3 | 0.031 | 0.060 | 0.133 |
:::

Las reales son 384 971 de largo 1, 212 310 de largo 2, 19 027 de largo 3 y 323 de largo 4.

**La figura contesta:** ¿cuántas rachas de cada largo da un texto simulado del largo del corpus? Hay 10 réplicas por modelo, hechas con MUESTREAR-FILA. **Cada barra es el número real de rachas de ese largo;** cada marca, la mediana de las 10 réplicas. El eje vertical es logarítmico.

::: figure {#mkv-c1-rachas title="Ni la cadena ni la independencia reproducen las rachas"}
![Número de rachas de consonantes de cada largo ℓ, de 1 a 5, en escala logarítmica. Barras: las reales del corpus. Círculos: mediana de 10 réplicas del largo del corpus de una cadena con q = 0.290. Cuadros: lo mismo con letras independientes, q = 0.536. Largo 1: reales 384 971, cadena 438 112, independientes 187 124. Largo 2: reales 212 310, cadena 126 722, independientes 100 176. Largo 3: reales 19 027, cadena 36 729, independientes 53 611. Largo 4: reales 323, cadena 10 684, independientes 28 819. Largo 5: reales 3, cadena 3 072, independientes 15 360. La franja del 5 % al 95 % de las réplicas es más angosta que la marca](../_assets/mkv-c1-rachas.svg)
:::

- **Largo 1 y 2.** La cadena da de más rachas de 1 y de menos de 2. Las independientes fallan más en el largo 1.
- **Largo 4.** Hay 323 reales, contra unas 10 700 de la cadena y 28 800 de las independientes.
- **Ruido de la simulación.** La franja del 5 % al 95 % mide menos del 7 % de la mediana: la diferencia no es azar de las réplicas.

**Ni la cadena ni la independencia reproducen las rachas reales.** La cadena se acerca más en el largo 1, pero predice demasiadas rachas largas: una letra de pasado no ve cuántas consonantes caben juntas. **Hipótesis, no hecho:** la cadena V/C es un modelo útil con límites que se miden.

::: exercise {#mkv-c1-ej-rachas-q title="Lee la fórmula de las rachas"}
1. **Largo 1.** Con $q=0.290$, ¿qué fracción de rachas de largo 1 predice la cadena, y por qué es $1-q$?
2. **Sin salida.** ¿Qué da la fórmula con $q=1$?
:::

::: hint {#mkv-c1-pista-rachas-q of="mkv-c1-ej-rachas-q" title="Tras la primera"}
¿Qué tiene que pasar justo después de la primera consonante?
:::

::: answer {#mkv-c1-resp-rachas-q of="mkv-c1-ej-rachas-q"}
1. **Es 0.710.** Una racha de largo 1 termina en la letra siguiente, que debe ser vocal: $\Pr(L=1)=1-q$.
2. **Da 0 para todo $\ell$.** Tras una C siempre viene C: ninguna racha termina, y $q=1$ queda fuera de la condición $q<1$.
:::

Ya tienes las piezas de una cadena: definirla, leer su matriz, multiplicar una trayectoria, muestrearla y ponerla a prueba.

---

## Ejercicios

::: exercise {#mkv-c1-ej-grafo-tres title="Pasa un grafo de tres estados a su matriz"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Una cadena tiene $\mathcal S=\{1,2,3\}$ y empieza en 1: $\mu_0=(1,0,0)$. Su grafo tiene estas flechas:

- **Desde 1:** a 2 con $3/4$ y a 3 con $1/4$.
- **Desde 2:** a 1 con $1/2$ y a 3 con $1/2$.
- **Desde 3:** a 1, a 2 y a sí mismo, con $1/3$ cada una.

**Cambia una idea:** los estados no son letras, son tres, y la cadena llega como grafo y no como texto.

1. **Escribe la matriz.** Arma $P$ en el orden 1, 2, 3.
2. **Comprueba las sumas.** ¿Cada fila suma 1? ¿Y cada columna?
3. **Lee ceros y diagonal.** ¿Dónde hay ceros, qué dicen, y desde qué estado se puede uno quedar?
4. **Calcula una trayectoria.** ¿Cuánto vale $\Pr(1,2,3,3)$?
:::

::: hint {#mkv-c1-pista-grafo-tres-1 of="mkv-c1-ej-grafo-tres" title="Pista 1 · ¿Dónde va cada flecha?"}
¿En qué fila va una flecha que sale de 2, y en qué columna una que llega a 3? ¿Qué entradas se quedan sin flecha?
:::

::: hint {#mkv-c1-pista-grafo-tres-2 of="mkv-c1-ej-grafo-tres" title="Pista 2 · ¿Cuántos factores lleva tu producto?"}
¿Tu producto tiene un factor de $\mu_0$ y uno por cada paso? ¿Cada factor está en la fila del estado de donde sales?
:::

::: answer {#mkv-c1-resp-grafo-tres of="mkv-c1-ej-grafo-tres" title="Respuesta · Una flecha, una entrada"}
**1. Matriz.** Cada flecha $s\to s'$ va en la fila $s$ y la columna $s'$:

$$
P=\begin{pmatrix}
0 & 3/4 & 1/4\\
1/2 & 0 & 1/2\\
1/3 & 1/3 & 1/3
\end{pmatrix}.
$$

**2. Sumas.** Las filas suman $3/4+1/4$, $1/2+1/2$ y tres veces $1/3$: todas 1. La columna 1 suma $0+1/2+1/3$, que no es 1.

**3. Ceros y diagonal.** Los ceros son $P(1\mid1)$ y $P(2\mid2)$: en el modelo, desde 1 y desde 2 siempre se sale. Solo desde 3 se puede quedar, con $1/3$.

**4. Trayectoria.** $\Pr(1,2,3,3)=1\cdot\frac{3}{4}\cdot\frac{1}{2}\cdot\frac{1}{3}=\frac{1}{8}$.
:::

::: exercise {#mkv-c1-ej-e-no-e title="Cuenta la «e» en otra frase"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Sancho recibe este consejo: «Llaneza, muchacho; no te encumbres» (*Quijote*, II, 26). **Cambia una idea:** otra frase y otro par de clases de letras, E = «e» y N = cualquier otra letra.

1. **Normaliza y clasifica.** Escribe la frase sin espacios ni signos y marca E o N bajo cada letra. ¿Cuántas letras y cuántas «e» hay?
2. **Cuenta los pares.** Arma la tabla de qué sigue a E y a N.
3. **Estima.** Escribe $\widehat P$ en el orden E, N.
4. **Decide.** ¿Parecen independientes? Compara con el corpus: $\widehat{\Pr}(e)\approx0.140$, $\widehat{\Pr}(e\mid e)\approx0.034$ y $\widehat{\Pr}(e\mid\text{no }e)\approx0.157$.
:::

::: hint {#mkv-c1-pista-e-no-e-1 of="mkv-c1-ej-e-no-e" title="Pista 1 · ¿Qué letra no tiene siguiente?"}
¿Cuántos pares forma una frase de $m$ letras? ¿Qué letra se queda sin siguiente?
:::

::: hint {#mkv-c1-pista-e-no-e-2 of="mkv-c1-ej-e-no-e" title="Pista 2 · ¿Cuadran tus totales?"}
¿Las dos filas de tu tabla suman, juntas, el número de pares? ¿Con qué cifra del corpus comparas cada fila de $\widehat P$?
:::

::: answer {#mkv-c1-resp-e-no-e of="mkv-c1-ej-e-no-e" title="Respuesta · La frase y el corpus no dicen lo mismo"}
**1. Clases.** Quedan 28 letras con 4 «e»: $\widehat{\Pr}(e)=4/28=1/7$.

```text
llanezamuchachonoteencumbres
NNNNENNNNNNNNNNNNNEENNNNNNEN
```

**2. Pares.** Son 27. De E salen 4: una a E («ee» de «te encumbres») y 3 a N. De N salen 23: 3 a E y 20 a N.

**3. Matriz.** En el orden E, N:

$$
\widehat P=\begin{pmatrix}1/4 & 3/4\\ 3/23 & 20/23\end{pmatrix}.
$$

**4. Decisión.** En la frase, $\widehat P(E\mid E)=1/4$ supera a $\widehat P(E\mid N)=3/23$, pero la fila E se apoya en 4 pares: una sola «ee» la mueve mucho. El corpus dice lo contrario y con millones de pares: tras una «e», otra «e» sale con 0.034; tras otra letra, con 0.157. No parecen independientes, y la frase sola no alcanzaba para decidirlo.
:::

**Punto de control:** deberías poder definir una cadena como $(\mathcal S,\mu_0,P)$ y explicar por qué «sin memoria» es independencia condicional. También, leer filas, columnas, ceros y diagonal de una matriz de cualquier tamaño, multiplicar una trayectoria y muestrear una fila a mano.

---

## Lo que hay que llevarse

- **La pregunta.** En la frase, tras vocal sigue vocal $2/11$ de las veces y tras consonante, $2/3$. Markov contó lo mismo en 20 000 letras del *Oneguin* (0.128 y 0.663); el *Quijote* da 0.181 y 0.710.
- **La cadena.** $(\mathcal S,\mu_0,P)$, finita y homogénea: el siguiente depende solo del presente, con la misma $P$ en cada paso. Es independencia condicional, no independencia.
- **La trayectoria.** Con Markov y homogeneidad, su probabilidad es $\mu_0(s_0)\prod_{j=0}^{t-1}P(s_{j+1}\mid s_j)$; `conla` da $4/33$.
- **La matriz.** Filas desde, columnas hacia, $k\times k$; cada fila suma 1 y las columnas no; un 0 es imposible en el modelo, la diagonal es quedarse. Con 2 estados una fila se fija con un número; con $k$, con $k-1$.
- **Muestrear.** MUESTREAR-FILA con $u$ = 0.40, 0.75, 0.90, 0.25 y 0.10 da `CVCCVV` desde C.
- **Hipótesis, no hecho.** De las rachas reales, una fracción de 0.624 tiene largo 1; la cadena predice 0.710 y la independencia, 0.464. De largo 4 hay 323 reales contra miles simuladas.

Continúa con [[mkv-ajustar-contando|Ajustar contando]].
