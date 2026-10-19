---
id: mkv-el-problema-de-markov
title: "El problema de Markov"
nav_title: "El problema de Markov"
summary: "¿Las letras de un texto son tiradas independientes de un dado? El conteo de Markov en 1913 y el mismo en el Quijote; la cadena V/C como caso de la definición general, la probabilidad de una trayectoria, la lectura de matrices de 2 y 3 estados, MUESTREAR-FILA y las rachas de consonantes."
status: ready
estimated_time: 37m
tags: [markov]
---

# El problema de Markov

**¿Las letras de un texto son como tiradas independientes de un dado?**

Al terminar tendrás:

- **La pregunta de Markov, contada** en la frase, el *Eugenio Oneguin* y el *Quijote*.
- **Una aplicación de @mkv-c1-cadena:** la cadena V/C con inicio fijo en C.
- **La probabilidad de una trayectoria,** aplicada a la secuencia de clases de `conla`.
- **La lectura de matrices concretas** con 2 y 3 estados.
- **MUESTREAR-FILA y las rachas,** con fórmulas, traza y comparación contra datos.

## Lo que traes

- **La cadena y sus formas.** [[mkv-cadena-en-general|La cadena, en general]] presenta $(\mathcal S,\mu_0,P)$ en @mkv-c1-cadena: $\mu_0$ es $1\times k$ y $P$, $k\times k$.
- **La matriz y la trayectoria.** @mkv-c1-matriz-transicion: filas desde, columnas hacia; cada fila suma 1. La probabilidad de una trayectoria está en la sección «Distinguir distribución y trayectoria» de esa página.
- **Las herramientas de probabilidad.** [[mkv-lo-que-necesitas|Lo que necesitas de probabilidad]] aporta la condicional (@mkv-c1-prob-condicional), el producto (@mkv-c1-teo-producto) y la independencia condicional (@mkv-c1-independencia-condicional).

---

## 1 · Contar vocales y consonantes en la frase

**Piensa: si la letra actual es vocal, ¿cambia la probabilidad de que la siguiente también lo sea?**

Sí: la frecuencia condicional (@mkv-c1-prob-condicional) cambia según la letra actual. Para cualquier par de estados:

$$
\begin{aligned}
\widehat{\Pr}(s'\mid s)
&=\frac{\#\{s\to s'\}}{\#\{s\to\cdot\}},\\
&\qquad \#\{s\to\cdot\}>0.
\end{aligned}
$$

El denominador cuenta apariciones de $s$ con siguiente; el numerador, las que van a $s'$.

**En la frase**, quitamos espacios y puntuación:

```text
conlaiglesiahemosdadosancho
CVCCVVCCVCVVCVCVCCVCVCVCCCV
```

Hay 26 pares. La «o» final no tiene siguiente: de las 12 vocales, solo 11 cuentan.

::: table {#mkv-c1-tabla-pares-frase title="Qué sigue a cada clase de letra, en la frase"}
| Actual (total) | Sigue V | Sigue C |
|---|---:|---:|
| V (11) | 2 | 9 |
| C (15) | 10 | 5 |
:::

Dividimos cada fila entre su total:

$$
\begin{aligned}
\widehat{\Pr}(V\mid V)&=\frac{2}{11},\\
\widehat{\Pr}(V\mid C)&=\frac{10}{15}=\frac{2}{3}.
\end{aligned}
$$

- **Tras vocal:** otra vocal salió 2 de 11 veces.
- **Tras consonante:** una vocal salió 2 de cada 3 veces.
- **Comparación:** con letras independientes, ambas estimarían la misma probabilidad y solo diferirían por azar. Aquí una supera el triple de la otra.

**El gorro cambia la lectura.** Antes, $2/11$ era exacto para el sorteo entre 26 posiciones. Aquí usamos la frase como datos para estimar un modelo.

::: exercise {#mkv-c1-ej-una-vocal-mas title="Agrega una letra"}
Si a la frase le siguiera una vocal más, ¿cuánto valdrían ${\widehat{\Pr}(V\mid V)}$ y ${\widehat{\Pr}(V\mid C)}$?
:::

::: hint {#mkv-c1-pista-una-vocal-mas of="mkv-c1-ej-una-vocal-mas" title="El par nuevo"}
¿Qué letra gana un siguiente, y en qué fila de la tabla cae ese par?
:::

::: answer {#mkv-c1-resp-una-vocal-mas of="mkv-c1-ej-una-vocal-mas"}
La «o» final gana un siguiente vocal. La fila V pasa a 3 de 12; la fila C no cambia. Quedan ${\widehat{\Pr}(V\mid V)=3/12=1/4}$ y $\widehat{\Pr}(V\mid C)=2/3$. Un dato más movió la estimación.
:::

Con 26 pares, la diferencia podría ser casualidad. Markov contó miles de letras.

---

## 2 · Plantear el problema original

**Piensa: ¿por qué un matemático contaría a mano las vocales de un poema?**

Por una disputa sobre la ley de los grandes números: con repeticiones independientes, la frecuencia de un evento se acerca a su probabilidad. ¿Hace falta la independencia?

- **1902 · Nekrásov.** Pável Nekrásov sostuvo que la independencia era condición **necesaria** para la ley de los grandes números. Así interpretó Markov su tesis.
- **1906 · Markov.** Respondió con variables dependientes, encadenadas, que también cumplen la ley. Así definió lo que hoy llamamos cadenas; él hablaba de «ensayos ligados en cadena».
- **1913 · *Eugenio Oneguin*.** Siete años después aplicó la idea a un texto. No era la respuesta a Nekrásov, sino una aplicación a datos.

En 1913 contó a mano las primeras 20 000 letras del poema, sin espacios ni puntuación. Son letras, no palabras.

- **Vocales y consonantes.** Halló 8 638 vocales y 11 362 consonantes.
- **Tras vocal.** Hubo 1 104 pares vocal-vocal: $\widehat{\Pr}(V\mid V)={1\,104}/{8\,638}\approx0.128$.
- **Tras consonante.** Markov puso en el numerador las vocales que no siguen a otra vocal, 8 638 − 1 104 = 7 534: $\widehat{\Pr}(V\mid C)={7\,534}/{11\,362}\approx0.663$.

**Lo mismo en el *Quijote*.** Con la estimación de la sección 1, sus 1 620 532 letras tienen 752 551 vocales: $\widehat{\Pr}(V)\approx0.464$. Tras vocal, la siguiente es vocal con frecuencia $0.181$; tras consonante, con $0.710$.

::: table {#mkv-c1-tabla-oneguin-quijote title="La pregunta de Markov en ruso y en español"}
| Cifra | *Oneguin* | *Quijote* |
|---|---:|---:|
| Letras contadas | 20 000 | 1 620 532 |
| Vocal tras vocal | 0.128 | 0.181 |
| Vocal tras consonante | 0.663 | 0.710 |
:::

**Las letras no se comportan como tiradas independientes.** Poema y novela repiten la diferencia observada en la frase.

::: exercise {#mkv-c1-ej-denominador title="Elige el denominador"}
¿Por qué Markov dividió los 1 104 pares vocal-vocal entre 8 638 y no entre 20 000?
:::

::: hint {#mkv-c1-pista-denominador of="mkv-c1-ej-denominador" title="Qué se sabe ya"}
En $\Pr(V\mid V)$, ¿qué evento ya ocurrió?
:::

::: answer {#mkv-c1-resp-denominador of="mkv-c1-ej-denominador"}
Porque condiciona a que la letra actual sea vocal: el denominador cuenta solo los casos donde $B$ ocurrió, como en $\Pr(A\cap B)/\Pr(B)$. Dividir entre 20 000 estimaría la probabilidad de que un par sea vocal-vocal, que es otra pregunta.
:::

Contar muestra que la letra actual importa. Usemos esa información en una cadena.

---

## 3 · Armar la cadena de la frase

**Piensa: ¿qué piezas necesitas para convertir los conteos en una cadena?**

Los estados, el inicio y las transiciones: $(\mathcal S,\mu_0,P)$, con las condiciones de @mkv-c1-cadena.

En la frase, $k=2$, $\mathcal S=\{V,C\}$ en ese orden, $\mu_0=\mathbf e_2=(0,1)$ y:

$$
\widehat P=
\begin{pmatrix}
2/11 & 9/11\\
2/3 & 1/3
\end{pmatrix}.
$$

- **Inicio fijo:** $\mu_0$ es una fila $1\times2$; la cadena empieza en C.
- **Estimación:** el gorro señala datos; $P$ sin gorro nombra una matriz genérica o verdadera.
- **Qué no es:** «sin memoria» ≠ independencia; la probabilidad de vocal depende del presente: $2/11$ contra $2/3$.

::: figure {#mkv-c1-grafo-vc title="El grafo de la frase"}
![Grafo de dos estados, V (vocal, círculo) y C (consonante, cuadro), con la matriz estimada de la frase. Desde V: un lazo a V con 2/11 y una flecha a C con 9/11. Desde C: una flecha a V con 2/3 y un lazo a C con 1/3. Las flechas que salen de un mismo estado suman 1](../_assets/mkv-c1-grafo-vc.svg)
:::

::: exercise {#mkv-c1-ej-dado-markov title="¿Un dado es una cadena?"}
Imagina letras independientes: cada una es vocal con la misma probabilidad, sin importar las anteriores. ¿Es una cadena de Markov? ¿Cómo son las filas de su $P$?
:::

::: hint {#mkv-c1-pista-dado-markov of="mkv-c1-ej-dado-markov" title="Prueba la definición"}
¿Qué condición de @mkv-c1-cadena tienes que revisar?
:::

::: answer {#mkv-c1-resp-dado-markov of="mkv-c1-ej-dado-markov"}
Sí. Con independencia, condicionar a cualquier historia no cambia nada, así que la propiedad de Markov se cumple. Las dos filas de $P$ son iguales: la probabilidad de V y la de C. Toda sucesión independiente con la misma distribución en cada paso es una cadena homogénea. Lo inverso falla en $\widehat P$: sus filas difieren.
:::

Las tres piezas permiten calcular la probabilidad de un trozo completo.

---

## 4 · Calcular la probabilidad de una trayectoria

**Piensa: ¿qué probabilidad le da la cadena a una secuencia completa de estados?**

La probabilidad inicial por una entrada de $P$ en cada paso, como en [[mkv-cadena-en-general|La cadena, en general]]:

$$
\begin{aligned}
&\Pr(S_0=s_{i_0},\dots,S_t=s_{i_t})\\
&\quad=\mu_0(s_{i_0})
\prod_{j=0}^{t-1}P_{i_ji_{j+1}}.
\end{aligned}
$$

- **De dónde sale:** @mkv-c1-teo-producto encadena un factor por paso; Markov y homogeneidad (@mkv-c1-cadena) vuelven cada factor una entrada de $P$.
- **Notación corta:** con estados concretos escribimos $\Pr(C,V,\dots)$ por $\Pr(S_0=C,S_1=V,\dots)$.
- **Camino imposible:** si el inicio o una transición vale 0, el producto da 0.

**A mano, `conla`.** Es C V C C V, con $\mu_0=(0,1)$ y $\widehat P$ de la frase:

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
\begin{aligned}
\Pr(C,V,C,C,V)
&=1\cdot\tfrac{2}{3}\cdot\tfrac{9}{11}
       \cdot\tfrac{1}{3}\cdot\tfrac{2}{3}\\
&=\tfrac{4}{33}.
\end{aligned}
$$

Al repetir muchas veces cinco estados desde C, unas 4 de cada 33 trayectorias serían C V C C V.

::: exercise {#mkv-c1-ej-tramo-corto title="Multiplica un trozo corto"}
Con ${\mu_0=(0,1)}$ y $\widehat P$ de la frase:

1. **Calcula.** ¿Cuánto vale $\Pr(C,C,V)$?
2. **Cambia el primer estado.** Con el mismo $\mu_0$, ¿cuánto vale $\Pr(V,C)$?
:::

::: hint {#mkv-c1-pista-tramo-corto of="mkv-c1-ej-tramo-corto" title="El primer factor"}
¿Cuánto vale $\mu_0$ en el primer estado de cada trozo?
:::

::: answer {#mkv-c1-resp-tramo-corto of="mkv-c1-ej-tramo-corto"}
1. **$\Pr(C,C,V)=1\cdot\frac{1}{3}\cdot\frac{2}{3}=\frac{2}{9}$.**
2. **$\Pr(V,C)=0$.** El factor inicial es $\mu_0(V)=0$: la cadena empieza en C.
:::

Cada factor salió de una fila de $\widehat P$. ¿Qué dice el resto de sus entradas, y las de una matriz de 3 estados?

---

## 5 · Leer la matriz de transición

**Piensa: ¿qué dice cada fila, cada columna y cada cero de estas matrices?**

Cada fila distribuye las salidas; cada columna reúne las llegadas; un cero descarta una transición en el modelo (@mkv-c1-matriz-transicion).

**Con V y C**, en la $\widehat P$ de la sección 3:

- **Forma:** $2\times2$, con V y C en ambos ejes.
- **Fila C:** $(2/3,1/3)$ reparte las salidas de C hacia V y C.
- **Sumas:** cada fila suma 1; la columna V suma $2/11+2/3\ne1$.
- **Diagonal:** $2/11$ permite seguir en V; $1/3$, seguir en C.
- **Grafo:** todas las entradas son positivas; todas aparecen como flechas en @mkv-c1-grafo-vc.
- **Conteos:** las filas de @mkv-c1-tabla-pares-frase suman 11 y 15. Dividirlas entre esos totales produce $\widehat P$.
- **Vector fila:** $\mu_0=(0,1)$ multiplica por la izquierda: $\mu_0\widehat P=(2/3,1/3)$, de tamaño $1\times2$.

**Con 3 estados**, conservamos los espacios como «_»:

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
\widehat P=
\begin{pmatrix}
1/11 & 7/11 & 3/11\\
2/3 & 1/5 & 2/15\\
1/5 & 4/5 & 0
\end{pmatrix}.
$$

- **Forma:** $3\times3$; dividimos las filas entre 11, 15 y 5. Cada fila resultante suma 1.
- **Columna del espacio:** suma $3/11+2/15+0<1$.
- **Cero estructural:** juntamos blancos consecutivos; por eso no hay espacio seguido de espacio ni lazo en ese estado.
- **Diagonal:** quedarse tiene probabilidades $1/11$, $1/5$ y $0$, respectivamente.
- **El paso cambió:** V→V baja de 2 a 1; «la iglesia» ya no junta la «a» con la «i».
- **Fuera del juguete:** con 2 estados basta un número por fila; con $k$, hacen falta $k-1$.

::: exercise {#mkv-c1-ej-fila-c-tres title="Lee la fila C con espacios"}
En la matriz de 3 estados, ¿qué dice la entrada $2/15$? ¿Suma 1 su fila?
:::

::: hint {#mkv-c1-pista-fila-c-tres of="mkv-c1-ej-fila-c-tres" title="Fila y columna"}
¿En qué fila y en qué columna está?
:::

::: answer {#mkv-c1-resp-fila-c-tres of="mkv-c1-ej-fila-c-tres"}
Está en la fila C y la columna _: tras una consonante, un espacio salió 2 de 15 veces. La fila suma $\frac{10+3+2}{15}=1$.
:::

La matriz resume los pares. Falta decidir si describe las dependencias del texto.

---

## 6 · Separar la hipótesis del hecho

**Piensa: ¿el texto «es» una cadena de Markov?**

No se deduce de los conteos: la propiedad de @mkv-c1-cadena es un supuesto que hay que contrastar. Para toda historia de probabilidad positiva, con dos letras de pasado:

$$
\begin{aligned}
&\Pr(S_{t+1}=s_j\mid S_t=s_i,\\
&\qquad S_{t-1}=s_l)\\
&\qquad\stackrel{?}{=}P_{ij}.
\end{aligned}
$$

Una desigualdad basta para refutarla.

**Contraejemplo.** Un proceso repite C C V C C V C C V… Empieza al azar en cualquiera de las tres letras del bloque.

- **Después de C C:** la siguiente es V con probabilidad 1.
- **Después de V C:** la siguiente es V con probabilidad 0.

Saber «estoy en C» no basta. Ninguna $P(V\mid C)$ sirve para ambas historias; falla Markov y no podemos usar su producto de transiciones.

**Agrupar tampoco garantiza Markov.** Aunque las letras siguieran una cadena, juntarlas en V/C podría romper la propiedad.

> [!WARNING]
> **Leer $\widehat P$ como una ley del idioma.** El texto es una trayectoria observada; la cadena, un modelo.
> **La matriz resume los pares; su validez se contrasta.**

::: exercise {#mkv-c1-ej-estado-ccv title="Arregla el estado"}
En el proceso que repite C C V, toma como estado las dos últimas letras. ¿Qué pares aparecen, a cuál pasa cada uno y con qué probabilidad? ¿Ahora sí es una cadena?
:::

::: hint {#mkv-c1-pista-estado-ccv of="mkv-c1-ej-estado-ccv" title="Desliza el par"}
Si el par es CC, ¿qué letra llega, y qué letra se cae del par?
:::

::: answer {#mkv-c1-resp-estado-ccv of="mkv-c1-ej-estado-ccv"}
Aparecen tres pares: CC, CV y VC. CC pasa a CV, CV pasa a VC y VC pasa a CC, cada uno con probabilidad 1. Sí es una cadena: el siguiente par depende solo del par actual. El estado cambió; la idea de cadena, no.
:::

Para contrastarla, generamos réplicas y las comparamos con el texto. Cada paso requiere elegir al azar una salida.

---

## 7 · Muestrear una fila

**Piensa: ¿cómo eliges un estado con las probabilidades de cualquier fila?**

Partes $[0,1)$ en intervalos de largos $p_i$ y eliges el que contiene al uniforme $u$.

$$
\begin{aligned}
(p_1,\dots,p_k)&\in\mathbb R^{1\times k},\\
p_i&\ge0,\qquad \sum_{i=1}^kp_i=1,\\
u&\sim\operatorname{Unif}[0,1),\\
\Delta_i&=\left[\sum_{j=1}^{i-1}p_j,\
                 \sum_{j=1}^{i}p_j\right),\\
|\Delta_i|&=p_i,\qquad \Pr(u\in \Delta_i)=p_i.
\end{aligned}
$$

- **Uniforme:** $u\sim\operatorname{Unif}[0,1)$ se lee «$u$ es un número al azar en $[0,1)$, cualquiera igual de probable». La probabilidad de caer en un intervalo es su largo.
- **Intervalos:** $\Delta_i$ es el pedazo del estado $s_i$; la suma vacía del primer extremo vale 0.

Eso es **muestrear** (*sampling*).

> **Dado:** una fila $(p_1,\dots,p_k)$ de $P$, ordenada como $s_1,\dots,s_k$, y un uniforme $u\in[0,1)$.
>
> **Encontrar:** el índice $i$ del siguiente estado $s_i$, con probabilidad $p_i$ de devolver cada índice.

**A mano, la fila C.** Sus acumuladas son $2/3$ y $1$:

$$
\Delta_V=[0,2/3),\qquad \Delta_C=[2/3,1).
$$

Si $u<2/3$, sale V; en caso contrario, C. Con $u=0.40$, sale V.

### El mapa de MUESTREAR-FILA

- **Qué calcula:** elige el siguiente estado de una fila con un solo uniforme.
- **Qué guarda:** una suma acumulada, que crece estado por estado.
- **Cómo avanza:** recorre la fila en el orden de $\mathcal S$ y suma la probabilidad de cada estado.
- **Qué devuelve al terminar:** el primer índice cuya suma acumulada pasa a $u$.

::: figure {#mkv-c1-flujo-muestrear title="Muestrear una fila, en palabras"}
![Diagrama de flujo de muestrear una fila, en palabras. Sortea u uniforme entre 0 y 1; empieza en el primer estado, con suma 0; suma la probabilidad de ese estado; pregunta si u es menor que la suma. Si sí, el siguiente estado es ese estado. Si no, pasa al que sigue y vuelve a sumar. Al pie: un solo u por paso; es lo que usa toda simulación de la clase](../_assets/mkv-c1-flujo-muestrear.svg)
:::

```text
INPUT   una fila p = (p_1,…,p_k)
        de P, en el orden
        s_1, …, s_k de 𝒮, que
        suma 1, y un uniforme
        u en [0, 1).
OUTPUT  el índice i del
        siguiente estado, s_i.

 1 function MUESTREAR-FILA(p, u)
 2   suma ← 0
     # en el orden de 𝒮
 3   for i ← 1 to k
       # fin del pedazo i
 4     suma ← suma + p_i
 5     if u < suma
         # u cayó en el pedazo i
 6       return i
     # solo si el redondeo falla
 7   return el último i con
       p_i > 0
```

**Gemelo Python.** Los comentarios indican la línea del pseudocódigo. Python cuenta desde 0: en el orden V, C, el índice 0 es V.

```python
from fractions import Fraction

# (1)
def muestrear_fila(fila, u):
    suma = 0  # (2)
    # (3)
    for i, p in enumerate(fila):
        suma += p  # (4)
        if u < suma:  # (5)
            return i  # (6)
    # (7)
    return max(i for i, p
               in enumerate(fila)
               if p > 0)

# el orden de 𝒮
estados = ("V", "C")
P_gorro = [
    [Fraction(2, 11),
     Fraction(9, 11)],
    [Fraction(2, 3),
     Fraction(1, 3)],
]
s = estados.index("C")  # s_0
visitados = "C"
U = (0.40, 0.75, 0.90,
     0.25, 0.10)
for u in U:
    fila = P_gorro[s]
    s = muestrear_fila(fila, u)
    visitados += estados[s]
print(visitados)
# CVCCVV
```

**Cada pieza, en su línea:**

- **Línea 4:** suma el extremo derecho de $\Delta_i$.
- **Línea 5:** el «menor que» asigna cada frontera al intervalo siguiente; los intervalos de largo 0 nunca se eligen.
- **Línea 7:** cubre el redondeo cuando ninguna suma supera a $u$; nunca devuelve un estado con probabilidad 0.

**Traza:** cada renglón muestra el paso $j$, el estado actual, las acumuladas, el uniforme y el estado devuelto.

**Tramo único · De C a CVCCVV**

| j | Desde · acumuladas | u | Siguiente |
|---:|---|---:|---|
| 0 | C · 2/3, 1 | 0.40 | V |
| 1 | V · 2/11, 1 | 0.75 | C |
| 2 | C · 2/3, 1 | 0.90 | C |
| 3 | C · 2/3, 1 | 0.25 | V |
| 4 | V · 2/11, 1 | 0.10 | V |

- **Paso 0:** $0.40<2/3$; sale V.
- **Paso 1:** $0.75$ supera $2/11$, pero es menor que 1; sale C.
- **Paso 4:** $0.10<2/11$; sale V, aunque V→V sea la transición menos probable.

Los cinco uniformes producen `CVCCVV`. Una trayectoria simulada con uniformes propios, independiente de las demás, es una **réplica**.

### Lo que garantiza y cuánto cuesta

- **Propiedades:** termina en a lo más $k$ vueltas con un solo $u$. Reordenar los estados cambia los intervalos, no sus probabilidades.
- **Número que da:** un índice; desde C con $u=0.40$, el de V.
- **Garantía:** con $p_i\ge0$, $\sum_i p_i=1$ y $u$ uniforme, devuelve $i$ con probabilidad $p_i$, en aritmética exacta.
- **Costo:** hasta $k$ sumas y $k$ comparaciones; guarda un número.
- **Supuestos:** cada paso usa un uniforme nuevo e independiente. El curso usa `random.Random(semilla)` para reproducir las réplicas.

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

Podemos generar réplicas del largo del *Quijote* y comparar sus rachas.

---

## 8 · Comparar las rachas de consonantes

**Piensa: si la cadena V/C fuera un buen modelo del texto, ¿qué debería reproducir?**

Entre otras cosas, la distribución del largo de las rachas de consonantes.

Una **racha** es un tramo máximo de consonantes seguidas, entre vocales; $L$ es su largo, todavía aleatorio, y $\ell$ un largo concreto. $q$ es la probabilidad de que a una C le siga otra, igual en cada paso. Una racha de largo $\ell$ son $\ell-1$ continuaciones y después una vocal:

$$
\begin{aligned}
\Pr(L=\ell)
&=\underbrace{q\cdots q}_{\ell-1\text{ continuaciones}}(1-q)\\
&=(1-q)q^{\ell-1},\\
\ell&\ge1,\qquad 0\le q<1.
\end{aligned}
$$

- **Cadena homogénea:** $q=P_{CC}=P(C\mid C)$; Markov y homogeneidad (@mkv-c1-cadena) repiten el mismo factor.
- **Letras independientes:** con la misma distribución en cada paso, $q=\Pr(C)$.
- **Condición:** $q<1$; con $q=1$, la racha no termina.
- **Datos:** descartamos las rachas truncadas por el principio o el final del texto.

**En el *Quijote***, la cadena usa $q=\widehat P(C\mid C)\approx0.290$; la independencia, $q=\widehat{\Pr}(C)\approx0.536$. Hay 616 634 rachas completas; «Indep.» representa letras independientes:

::: table {#mkv-c1-tabla-rachas title="Fracción de rachas de cada largo"}
| ℓ | Reales | Cadena | Indep. |
|---:|---:|---:|---:|
| 1 | 0.624 | 0.710 | 0.464 |
| 2 | 0.344 | 0.206 | 0.249 |
| 3 | 0.031 | 0.060 | 0.133 |
:::

Hay 384 971 rachas de largo 1, 212 310 de largo 2 y 19 027 de largo 3. También, 323 de largo 4 y 3 de largo 5.

**La figura compara conteos de rachas** con 10 réplicas por modelo, del largo del corpus, hechas con MUESTREAR-FILA. Cada barra es el conteo real; cada marca, la mediana de las 10 réplicas. El eje vertical es logarítmico.

::: figure {#mkv-c1-rachas title="Ni la cadena ni la independencia reproducen las rachas"}
![Número de rachas de consonantes de cada largo ℓ, de 1 a 5, en escala logarítmica. Barras: las reales del corpus. Rombos: mediana de 10 réplicas del largo del corpus de una cadena con q = 0.290. Triángulos: lo mismo con letras independientes, q = 0.536. Largo 1: reales 384 971, cadena 438 112, independientes 187 124. Largo 2: reales 212 310, cadena 126 722, independientes 100 176. Largo 3: reales 19 027, cadena 36 729, independientes 53 611. Largo 4: reales 323, cadena 10 684, independientes 28 819. Largo 5: reales 3, cadena 3 072, independientes 15 360. La franja del 5 % al 95 % de las réplicas es más angosta que la marca](../_assets/mkv-c1-rachas.svg)
:::

- **Largos 1 y 2:** la cadena produce demasiadas rachas de 1 y pocas de 2. La independencia falla más en largo 1.
- **Largo 4:** hay 323 reales, contra unas 10 700 de la cadena y 28 800 de la independencia.
- **Ruido:** la franja del 5 % al 95 % mide menos del 7 % de la mediana; no explica las diferencias.

**Ambos modelos fallan al reproducir las rachas.** La cadena predice demasiadas rachas largas: el estado V/C no recuerda cuántas consonantes van seguidas.

::: exercise {#mkv-c1-ej-rachas-q title="Lee la fórmula de las rachas"}
1. **Largo 1.** Con $q=0.290$, ¿qué fracción de rachas de largo 1 predice la cadena, y por qué es ${1-q}$?
2. **Sin salida.** ¿Qué da la fórmula con $q=1$?
:::

::: hint {#mkv-c1-pista-rachas-q of="mkv-c1-ej-rachas-q" title="Tras la primera"}
¿Qué tiene que pasar justo después de la primera consonante?
:::

::: answer {#mkv-c1-resp-rachas-q of="mkv-c1-ej-rachas-q"}
1. **Es 0.710.** Una racha de largo 1 termina en la letra siguiente, que debe ser vocal: ${\Pr(L=1)=1-q}$.
2. **Da 0 para todo $\ell$.** Tras una C siempre viene C: ninguna racha termina, y ${q=1}$ queda fuera de la condición ${q<1}$.
:::

Las mismas fórmulas permiten cambiar los estados y resolver otros ejemplos.

---

## Ejercicios

::: exercise {#mkv-c1-ej-grafo-tres title="Pasa un grafo de tres estados a su matriz"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

Una cadena tiene $\mathcal S=\{1,2,3\}$ y empieza en 1: $\mu_0=(1,0,0)$. Su grafo tiene estas flechas:

- **Desde 1:** a 2 con $3/4$ y a 3 con $1/4$.
- **Desde 2:** a 1 con $1/2$ y a 3 con $1/2$.
- **Desde 3:** a 1, a 2 y a sí mismo, con $1/3$ cada una.

**Cambia una idea:** la cadena llega como grafo, no como texto.

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

**4. Trayectoria.** ${\Pr(1,2,3,3)=1\cdot\frac{3}{4}\cdot\frac{1}{2}\cdot\frac{1}{3}=\frac{1}{8}}$.
:::

::: exercise {#mkv-c1-ej-e-no-e title="Cuenta la «e» en otra frase"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

Sancho recibe este consejo: «Llaneza, muchacho; no te encumbres» (*Quijote*, II, 26). **Cambia una idea:** otro par de clases de letras, E = «e» y O = cualquier otra letra.

1. **Normaliza y clasifica.** Escribe la frase sin espacios ni signos y marca E u O bajo cada letra. ¿Cuántas letras y cuántas «e» hay?
2. **Cuenta los pares.** Arma la tabla de qué sigue a E y a O.
3. **Estima.** Escribe $\widehat P$ en el orden E, O.
4. **Decide.** ¿Parecen independientes? Compara con el corpus: $\widehat{\Pr}(e)\approx0.140$, $\widehat{\Pr}(e\mid e)\approx0.034$ y $\widehat{\Pr}(e\mid\text{no }e)\approx0.157$.
:::

::: hint {#mkv-c1-pista-e-no-e-1 of="mkv-c1-ej-e-no-e" title="Pista 1 · ¿Cuántos pares salen?"}
¿Cuántos pares forma una frase de $m$ letras? ¿Qué letra se queda sin siguiente?
:::

::: hint {#mkv-c1-pista-e-no-e-2 of="mkv-c1-ej-e-no-e" title="Pista 2 · ¿Cuadran tus totales?"}
¿Las dos filas de tu tabla suman, juntas, el número de pares? ¿Con qué cifra del corpus comparas cada fila de $\widehat P$?
:::

::: answer {#mkv-c1-resp-e-no-e of="mkv-c1-ej-e-no-e" title="Respuesta · La frase y el corpus no dicen lo mismo"}
**1. Clases.** Quedan 28 letras con 4 «e»: $\widehat{\Pr}(e)=4/28=1/7$.

```text
llanezamuchachonoteencumbres
OOOOEOOOOOOOOOOOOOEEOOOOOOEO
```

**2. Pares.** Son 27. De E salen 4: una a E («ee» de «te encumbres») y 3 a O. De O salen 23: 3 a E y 20 a O.

**3. Matriz.** En el orden E, O:

$$
\widehat P=\begin{pmatrix}1/4 & 3/4\\ 3/23 & 20/23\end{pmatrix}.
$$

**4. Decisión.** En la frase, ${\widehat P(E\mid E)=1/4}$ supera a ${\widehat P(E\mid O)=3/23}$. La fila E solo tiene 4 pares; una «ee» la mueve mucho. El corpus, con millones de pares, dice lo contrario: tras una «e», otra sale con 0.034. Tras otra letra, sale con 0.157. No parecen independientes; la frase sola no bastaba para decidir.
:::

**Punto de control:** aplica @mkv-c1-cadena, distingue independencia de independencia condicional y lee una matriz. Calcula una trayectoria, muestrea una fila y contrasta una predicción con datos.

---

## Lo que hay que llevarse

- **La pregunta:** tras V y C, la frase da $2/11$ y $2/3$; las 20 000 letras del *Oneguin*, 0.128 y 0.663. El *Quijote* da 0.181 y 0.710.
- **La cadena:** aplica @mkv-c1-cadena, $(\mathcal S,\mu_0,P)$, con independencia condicional y transiciones homogéneas.
- **La trayectoria:** $\mu_0(s_{i_0})\prod_{j=0}^{t-1}P_{i_ji_{j+1}}$ (@mkv-c1-teo-producto, @mkv-c1-cadena); `conla` da $4/33$.
- **La matriz:** $k\times k$, filas desde y columnas hacia. Con 2 estados basta un número por fila; con $k$, hacen falta $k-1$.
- **Muestrear:** desde C, los uniformes 0.40, 0.75, 0.90, 0.25 y 0.10 producen `CVCCVV`.
- **Contrastar:** las rachas de largo 1 dan 0.624 real, 0.710 Markov y 0.464 independiente. De largo 4 hay 323 reales, contra miles simuladas.

Continúa con [[mkv-ajustar-contando|Ajustar contando]].
