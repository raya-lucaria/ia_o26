---
id: mkv-generar-texto
title: "Generar texto"
nav_title: "Generar texto"
summary: "Escribir texto al estilo del Quijote muestreando una fila tras otra: GENERAR trazado a mano y en Python, salidas con semilla de memoria 0 a 3, la traducción de las aproximaciones de Shannon y lo que gana y arriesga más memoria."
status: ready
estimated_time: 28m
tags: [markov]
---

# Generar texto

**¿Cómo se escribe un texto «al estilo» del *Quijote*, y qué cambia al darle más memoria?**

Al terminar tendrás:

- **El algoritmo GENERAR,** en pseudocódigo y en Python, trazado a mano con tres uniformes.
- **Una regla declarada** para el contexto que nunca se vio: la fila suavizada, sin reiniciar.
- **Cuatro salidas con semilla,** de memoria 0 a 3, y una de palabras.
- **La traducción** entre los órdenes de Shannon (1948) y nuestra memoria.
- **Lo que gana y lo que arriesga** subir la memoria, medido en el *Quijote*.

## Lo que traes

- **Muestrear una fila.** En [[mkv-el-problema-de-markov|El problema de Markov]], MUESTREAR-FILA recorre la fila sumando y devuelve el primer estado cuya suma pasa a un uniforme $u\in[0,1)$.
- **La cadena de tres estados.** En la misma página, «con la iglesia hemos dado sancho», con sus espacios, dio una matriz con estados V, C y espacio (`_`).
- **Contar y suavizar.** En [[mkv-ajustar-contando|Ajustar contando]], $\widehat P(s'\mid s)=N(s,s')/N(s)$, solo si $N(s)>0$. Con Laplace, un contexto sin observaciones recibe la fila uniforme.
- **La memoria.** Con memoria $h$, el estado es el contexto: los últimos $h$ símbolos. El símbolo que sigue es $z\in\Sigma$, y el contexto se desliza al agregarlo.
- **Predecir.** En [[mkv-predecir|Predecir]] calculaste qué tan probable es cada estado $t$ pasos después. Aquí no se calcula una probabilidad: se produce una trayectoria.

> **Modelo y datos.** Generar con $\widehat P$ muestra lo que la cadena ajustada considera probable. No muestra qué es el español: una salida rara habla del modelo, no del idioma.

---

## 1 · Generar a mano tres símbolos

**Piensa: si cada fila es solo una lista de probabilidades, ¿cómo sale un texto de una matriz?**

Sale muestreando una fila tras otra: el símbolo que sale se vuelve el estado actual. Usa la matriz de tres estados de la página 2, en el orden V, C, `_`:

$$
\widehat P=\begin{pmatrix}
1/11 & 7/11 & 3/11\\
2/3 & 1/5 & 2/15\\
1/5 & 4/5 & 0
\end{pmatrix}.
$$

Empieza en C y usa tres uniformes dados: 0.90, 0.55 y 0.30. Cada paso suma su fila hasta pasar a $u$.

**Cómo leer la traza.** Cada renglón es un paso $j$. La fila acumulada va en el orden V, C, `_`.

::: table {#mkv-c1-traza-generar-a-mano title="Generar desde C con tres uniformes dados"}
| j | Estado · fila acumulada | u | Sale |
|---:|---|---:|---|
| 0 | C · (2/3, 13/15, 1) | 0.90 | `_` |
| 1 | `_` · (1/5, 1, 1) | 0.55 | C |
| 2 | C · (2/3, 13/15, 1) | 0.30 | V |
:::

- **Paso 0.** 0.90 no es menor que 2/3 ni que 13/15; es menor que 1. Sale el espacio, con probabilidad 2/15.
- **Paso 1.** Desde el espacio, 0.55 no es menor que 1/5, pero sí que 1: sale C.
- **Paso 2.** 0.30 es menor que 2/3: sale V.

El texto, con el inicio incluido, es `C_CV`: una consonante, un espacio, otra consonante y una vocal. Es una réplica corta de la cadena.

::: exercise {#mkv-c1-ej-espacio-doble title="Busca otro espacio"}
En el paso 1 estás en `_`. ¿Qué $u$ haría que saliera otro espacio?
:::

::: hint {#mkv-c1-pista-espacio-doble of="mkv-c1-ej-espacio-doble" title="Mira la última suma"}
¿Cuánto crece la suma acumulada al llegar a la entrada de `_`?
:::

::: answer {#mkv-c1-resp-espacio-doble of="mkv-c1-ej-espacio-doble"}
Ninguno. La fila acumulada es (1/5, 1, 1): la entrada de `_` vale 0 y la suma no crece. Todo $u<1$ ya eligió V o C. Es el cero estructural de la página 2: tras un espacio nunca hay otro.
:::

La cuenta solo usó una fila por paso. ¿Qué hace falta para escribirla con cualquier alfabeto y cualquier memoria?

---

## 2 · Escribir el algoritmo GENERAR

**Piensa: ¿qué tiene que recordar el programa entre un símbolo y el siguiente?**

Solo el contexto: los últimos $h$ símbolos escritos. Con memoria 1 el contexto es la letra anterior, como en la traza. Con memoria $h$, la tabla tiene una fila por contexto visto y una columna por símbolo de $\Sigma$.

**Un contexto nunca visto no tiene fila.** Pasa si el contexto inicial no aparece en los datos, como la «k» del *Quijote*, o si la tabla sale de un texto corto. Hay dos salidas: reiniciar desde otro contexto, o suavizar. **Aquí se declara la segunda.** Con conteos 0, Laplace da $\widetilde p(z\mid s)=\frac{0+1}{0+|\Sigma|}$: la fila uniforme. Las filas vistas se usan sin suavizar.

::: definition {#mkv-c1-generar title="Generar con una cadena"}
**Qué es.** Generar es producir una trayectoria: desde un contexto inicial, muestrear el siguiente símbolo de la fila del contexto actual, escribirlo y deslizar el contexto.

**Cómo se calcula.** En cada paso, $z$ sale de la fila de $s$ con MUESTREAR-FILA y un $u$ nuevo. El nuevo contexto quita el primer símbolo de $s$ y agrega $z$.

**Qué significa.** Cada salida es una réplica de la cadena de memoria $h$ ajustada. En la traza, la réplica fue C, `_`, C, V.

**Qué no es.** No es predecir: $\mu_t$ da probabilidades, y generar da una muestra. Tampoco es escribir lo más probable: no elige el máximo de cada fila, sino que sortea.
:::

> **Dado:** un alfabeto $\Sigma$, una tabla con una fila de probabilidades sobre $\Sigma$ por cada contexto visto, un contexto inicial de $h$ símbolos y un largo.
>
> **Encontrar:** un texto que empiece con el contexto inicial y siga con tantos símbolos como diga el largo, cada uno muestreado de la fila de su contexto (@mkv-c1-generar).

### El mapa de GENERAR

- **Qué calcula:** produce una réplica de la cadena, símbolo por símbolo.
- **Qué guarda:** conserva el texto escrito; el contexto son sus últimos $h$ símbolos.
- **Cómo avanza:** busca la fila del contexto, sortea un $u$ nuevo, escribe el símbolo y desliza el contexto.
- **Qué devuelve al terminar:** entrega el contexto inicial seguido de los símbolos generados.

::: figure {#mkv-c1-flujo-generar title="Generar, en palabras"}
![Diagrama de flujo de generar texto: empieza con un contexto de h símbolos; pregunta si se vio el contexto, y si no, usa la fila suavizada; muestrea su fila con un u nuevo; escribe el símbolo y desliza el contexto; pregunta si llegaste al largo, y si no, vuelve a la pregunta del contexto con otro símbolo; si sí, devuelve el texto. Al pie: un contexto nunca visto no se reinicia, su fila suavizada da 1/|Σ| a cada símbolo](../_assets/mkv-c1-flujo-generar.svg)
:::

```text
INPUT   el alfabeto Σ; una tabla con una fila
        sobre Σ por cada contexto visto; un
        contexto inicial de h símbolos; un
        largo ≥ 0.
OUTPUT  el contexto inicial seguido de largo
        símbolos generados.

 1 function GENERAR(Σ, tabla, contexto, largo)
 2   texto ← contexto ; h ← |contexto|
 3   for j ← 0 to largo − 1   # un símbolo por paso
 4     s ← últimos h símbolos de texto
 5     if s está en la tabla  # contexto visto
 6       fila ← tabla[s]      # su fila de P̂
 7     else                   # nunca visto
 8       fila ← 1/|Σ| en cada z  # Laplace, N = 0
 9     u ← uniforme en [0, 1)    # un u nuevo
10     z ← Σ[MUESTREAR-FILA(fila, u)]
11     texto ← texto seguido de z  # desliza
12   return texto
```

**Gemelo Python.** Los comentarios indican la línea del pseudocódigo. `muestrear_fila` es la de la página 2, y `rng` da los uniformes con `rng.random()`.

```python
def generar(tabla, alfabeto, contexto, largo, rng):  # (1)
    texto, h = contexto, len(contexto)                # (2)
    for j in range(largo):                            # (3)
        s = texto[len(texto) - h:]                    # (4)
        if s in tabla:                                # (5)
            fila = tabla[s]                           # (6)
        else:                                         # (7)
            fila = [1 / len(alfabeto)] * len(alfabeto)  # (8)
        u = rng.random()                              # (9)
        z = alfabeto[muestrear_fila(fila, u)]         # (10)
        texto = texto + z                             # (11)
    return texto                                      # (12)

class UsDados:            # da los u de la traza a mano
    def __init__(self, us):
        self.us = list(us)

    def random(self):
        return self.us.pop(0)

tabla = {"V": [Fraction(1, 11), Fraction(7, 11),
               Fraction(3, 11)],
         "C": [Fraction(2, 3), Fraction(1, 5),
               Fraction(2, 15)],
         "_": [Fraction(1, 5), Fraction(4, 5),
               Fraction(0)]}
print(generar(tabla, "VC_", "C", 3,
              UsDados([0.90, 0.55, 0.30])))
# C_CV
```

**Cada pieza, en su línea:**

- **Línea 4.** Toma los últimos $h$ símbolos. En Python, `texto[len(texto) - h:]` da la cadena vacía con $h=0$; `texto[-0:]` daría todo el texto.
- **Líneas 5 a 8.** Usan la fila de $\widehat P$ si el contexto se vio, y la uniforme si no.
- **Línea 9.** Gasta exactamente un $u$ por símbolo. Con una semilla fija, `random.Random(semilla)` da siempre los mismos $u$, y por eso el mismo texto.
- **Línea 11.** Agregar $z$ desliza el contexto: la línea 4 del paso siguiente ya no ve el primer símbolo.

::: exercise {#mkv-c1-ej-memoria-cero title="Corre GENERAR sin memoria"}
Con $h=0$, ¿qué contexto lee la línea 4 y qué fila usa en cada paso?
:::

::: hint {#mkv-c1-pista-memoria-cero of="mkv-c1-ej-memoria-cero" title="Cuenta lo que queda"}
¿Cuántos símbolos quedan si tomas los últimos 0?
:::

::: answer {#mkv-c1-resp-memoria-cero of="mkv-c1-ej-memoria-cero"}
Lee el contexto vacío, siempre el mismo. Usa en cada paso la fila de frecuencias de los símbolos, así que cada símbolo sale independiente de los anteriores.
:::

### Lo que garantiza y cuánto cuesta

- **Propiedades:** termina tras largo pasos y gasta un $u$ por símbolo. La misma tabla, el mismo orden de $\Sigma$, el mismo contexto inicial y la misma semilla dan el mismo texto.
- **Número que da:** devuelve un texto, no una probabilidad. En la traza, `C_CV`: el contexto C y tres símbolos.
- **Garantía:** si los $u$ son uniformes en $[0,1)$ e independientes, cada símbolo sale con la probabilidad que su fila le asigna. La salida es una réplica de la cadena de la tabla, no del *Quijote*.
- **Costo:** cada paso busca una fila y suma hasta $|\Sigma|$ entradas: tiempo proporcional a largo por $|\Sigma|$. La tabla guarda hasta $|\Sigma|^h$ filas de $|\Sigma|$ entradas.
- **Supuestos:** cada fila suma 1; el contexto inicial tiene $h$ símbolos de $\Sigma$; las filas no vistas reciben la uniforme.

**Lo que no generaliza del juguete.** En la traza, cada estado era un símbolo y la matriz era cuadrada, $3\times3$. Con memoria $h$, la tabla útil tiene $|\Sigma|^h$ filas y $|\Sigma|$ columnas. Con el *Quijote*, $|\Sigma|=28$.

GENERAR ya corre con cualquier tabla. ¿Qué escribe con las del *Quijote*?

---

## 3 · Leer ejemplos con semilla

**Piensa: ¿qué cambia en el texto cuando la memoria pasa de 0 a 3?**

En estas cuatro réplicas, primero aparecen sílabas, luego palabras cortas, y con memoria 3 frases casi legibles. Cada salida es una simulación: una réplica de la cadena de memoria $h$ ajustada en el corpus completo.

- **La tabla.** Contamos con los 28 símbolos normalizados del *Quijote* y dividimos cada fila entre sus salidas.
- **El inicio.** El contexto inicial son los primeros $h$ símbolos de «en un lugar»; con memoria 0 es vacío.
- **El largo.** Cada salida tiene 200 símbolos en total, contexto incluido.
- **Las semillas.** Usamos 2032 para memoria 0, 2033 para 1, 2034 para 2 y 2035 para 3.

Cada salida se corta en renglones para que quepa; el texto es una sola línea.

**Memoria 0 · semilla 2032** (empieza con un espacio: no hay contexto)

```text
 pusnve dprate duuutesrsacee insi qlsao
iamsopaa ceecae do vnoov  oausu q i etg
anls oalilanosll y  grcgiiypeo ldes eees
eebdessatoes uoed nn enlea aa oehtbo
mehs n naoeesiaya ysitrn laa  muercltsoi
n
```

**Memoria 1 · semilla 2033**

```text
er gonos sesel usiava lera cuecive de lo
ta ques pera a lodasijeralgosper ene l y
y mabera y tidelerla tia quenoncalerela
tre dandaue cr s quede en ve sin suieo e
a cuestadui des que pa fe y mbesctrta
```

**Memoria 2 · semilla 2034**

```text
enchombolaso aquisia veasagionallegar
que parespel er arovicino pro es
quecienes do la dos mues y fue el minto
acaba queño as dejote noco a y
dechacescuanajabese lle nos hano de
encera quesar y pue ma
```

**Memoria 3 · semilla 2035**

```text
en su amosura en el dijote espero
otrastilla paremostan de señor como
acomo el cuerte lo en cuandoliconvies
sustra y un gran vizcaidad del fio
hacenca que pros de burrespondios en
loco de tendicen otr
```

- **Memoria 0.** Las letras salen con su frecuencia y sin orden: «duuutesrsacee». El espacio también sale con su frecuencia, y por eso hay «palabras» de largo creíble.
- **Memoria 1.** Vocales y consonantes alternan, y aparecen palabras reales cortas: «de», «lo», «que», «sin».
- **Memoria 2.** Hay sílabas del español y palabras de tres o cuatro letras: «la», «y fue el», «acaba».
- **Memoria 3.** Casi todo se lee: «en su amosura», «de señor como», «un gran vizcaidad». «dijote» no existe, pero cada tramo de cuatro letras sí.

**Míralo escribir, símbolo por símbolo.** El generador de texto corre lo mismo con memoria 0, 1, 2 o 3. Para cada símbolo muestra el contexto, su fila, el $u$ sorteado y dónde cae en la suma acumulada. Con la semilla de cada ejemplo y largo 200 escribe el mismo texto, porque sortea igual que el Python de esta página.

::: figure {#mkv-c1-generador title="El generador escribiendo con memoria 2"}
[![Captura del generador de texto con memoria 2 y semilla 2034, a 148 de 198 símbolos. El panel del paso muestra el contexto «ce», con 6 942 salidas; las más probables son r 0.260, d 0.196, s 0.162, espacio 0.153 y n 0.099, y el resto suma 0.129. El u sorteado, 0.7149, cae en el tramo de «s», de 0.6788 a 0.8410, y se escribe «s».](../_assets/mkv-c1-generador.png)](../_assets/generador_texto.html#h=2&semilla=2034&largo=200&paso=148)
:::

> **▶ [Abre el generador](../_assets/generador_texto.html#h=2&semilla=2034&largo=200&paso=148)**: pulsa la imagen o este enlace. Cambia la memoria y la semilla, y avanza un símbolo a la vez.

**Con palabras en vez de letras.** El estado es la palabra anterior y el alfabeto es el vocabulario del corpus, con memoria 1. Con 30 palabras, semilla 2036 y contexto inicial «en»:

> en tanto artificio que sus aguelos ahora la ventana que venian del pie llano a don quijote de sirgo pon el famoso caballero en las desdichas del a pasar habiendole

Cada par de palabras seguidas aparece en el *Quijote*; la frase completa, no. La normalización quita los acentos: «venian».

::: exercise {#mkv-c1-ej-palabra-inventada title="Desarma una palabra inventada"}
La salida de memoria 2 dice «veasagionallegar», que no está en el *Quijote*. ¿De qué pedazos está hecha?
:::

::: hint {#mkv-c1-pista-palabra-inventada of="mkv-c1-ej-palabra-inventada" title="El tamaño de cada pieza"}
Con memoria 2, ¿cuántas letras tiene cada bloque (contexto, siguiente)?
:::

::: answer {#mkv-c1-resp-palabra-inventada of="mkv-c1-ej-palabra-inventada"}
De tríos de letras seguidas: «vea», «eas», «asa», … Cada trío salió de una fila con conteo positivo, así que apareció en el corpus. La palabra completa no: el modelo solo recuerda dos letras, y pega tríos que se traslapan.
:::

Estas salidas tienen un antecedente famoso, hecho sin computadora.

---

## 4 · Traducir las aproximaciones de Shannon

**Piensa: ¿se puede generar texto así sin computadora?**

Sí: Claude Shannon lo hizo a mano en 1948, en «Una teoría matemática de la comunicación» (*A Mathematical Theory of Communication*), publicado en el *Bell System Technical Journal*. En la parte I, sección 3, presenta una serie de aproximaciones al inglés con un alfabeto de 27 símbolos: 26 letras y el espacio.

**Shannon numera uno arriba.** Su «orden» cuenta las letras del bloque que se cuenta, $h+1$; nuestra memoria cuenta las del contexto, $h$.

::: table {#mkv-c1-shannon title="Los órdenes de Shannon, en memoria"}
| Shannon (1948) | Qué usa | Aquí |
|---|---|---|
| Orden cero | Símbolos equiprobables | Fila uniforme |
| Primer orden | Frecuencias de letras | Memoria 0 |
| Segundo orden | Pares de letras | Memoria 1 |
| Tercer orden | Tríos de letras | Memoria 2 |
:::

**Cómo lo hizo, a mano.** Para el primer orden usó una tabla de frecuencias de letras y un libro de números aleatorios. Desde el segundo, abría un libro al azar y elegía una letra de la página. Luego abría otra página, leía hasta encontrar esa letra y anotaba la que la seguía.

Ese truco es, en esencia, MUESTREAR-FILA sin contar. La letra que sigue a la que encuentras sale con las frecuencias del libro: el libro hace de tabla.

Las salidas de la sección 3 son nuestras: el *Quijote*, una computadora y semillas fijas. Shannon usó textos en inglés y tablas impresas.

::: exercise {#mkv-c1-ej-orden-shannon title="Traduce la memoria 3"}
¿Con qué orden llamaría Shannon a nuestra salida de memoria 3?
:::

::: hint {#mkv-c1-pista-orden-shannon of="mkv-c1-ej-orden-shannon" title="Cuenta el bloque"}
Con memoria 3, ¿cuántas letras tiene cada bloque (contexto, siguiente)?
:::

::: answer {#mkv-c1-resp-orden-shannon of="mkv-c1-ej-orden-shannon"}
Cuarto orden: cada bloque tiene $h+1=4$ letras. Es una traducción de numeración; Shannon publicó hasta el tercer orden en letras.
:::

Memoria 3 se lee mejor que memoria 2. ¿Por qué no subirla sin límite?

---

## 5 · Medir qué gana y qué arriesga la memoria

**Piensa: si memoria 3 se lee mejor, ¿por qué no usar memoria 10?**

Porque los datos son finitos. Más memoria representa más, pero cada contexto se ve menos veces.

**Lo que gana.** Representa más dependencias locales: la «u» tras la «q», las sílabas, las palabras cortas. Sobre las mismas transiciones del texto con que se cuenta, y sin suavizar, la verosimilitud máxima no baja. Un modelo de memoria $h+1$ puede ignorar el símbolo extra e imitar al de memoria $h$.

**Lo que arriesga, primero: contextos sin observaciones.** @mkv-c1-ceros-generar repite el diagnóstico de la página 3: contar con la primera mitad del corpus y probar en la segunda.

::: figure {#mkv-c1-ceros-generar title="Lo que nunca se vio, por memoria"}
![Barras horizontales por memoria, con la fracción de transiciones de la segunda mitad del corpus nunca vistas en la primera. Memoria 0: 0 %, 0 de 998 564, contextos vistos 1 de 1. Memoria 1: 0.003 %, 29 de 998 563, contextos vistos 27 de 28. Memoria 2: 0.072 %, 718 de 998 562, contextos vistos 379 de 784. Memoria 3: 0.570 %, 5 694 de 998 561, contextos vistos 3 328 de 21 952. Las barras están a escala de la mayor (memoria 3). Al pie: solo diagnostica escasez, no elige la memoria](../_assets/mkv-c1-ceros.svg)
:::

- **Las fracciones suben.** Son 0.003 %, 0.072 % y 0.570 % para memorias 1, 2 y 3.
- **Los contextos posibles crecen más rápido.** Con memoria 3 se vieron 3 328 de 21 952.

**Lo que arriesga, después: repetir fragmentos del corpus.** Para cada salida de la sección 3 medimos dos cosas:

- **La subcadena literal más larga.** Es el tramo seguido más largo de la salida que está tal cual en el corpus.
- **Los 8-gramas copiados.** Un 8-grama es un tramo de 8 caracteres seguidos. Contamos qué fracción de los de la salida está en el corpus.

::: table {#mkv-c1-tabla-copiar title="Cuánto copia cada salida del corpus"}
| Memoria | Subcadena más larga | 8-gramas en el corpus |
|---:|---:|---:|
| 0 | 6 | 0 % |
| 1 | 10 | 9 % |
| 2 | 11 | 20 % |
| 3 | 13 | 42 % |
:::

Cada fila es **una sola réplica**: con otra semilla, las cifras pueden cambiar.

**No es inevitable.** Lo que copia es una fila con una sola continuación observada. En el extremo, si cada contexto apareciera una vez, cada fila tendría un 1 y GENERAR copiaría el corpus letra por letra. Si cada contexto se vio seguido de muchos símbolos distintos, la salida puede combinar trozos sin repetir tramos largos.

> [!WARNING]
> **Confundir que se lea bien con que sea nuevo.** De estas cuatro, la salida de memoria 3 es la más legible, y 42 % de sus 8-gramas están literales en el *Quijote*. **Parte de lo que se lee bien es copia.**

::: exercise {#mkv-c1-ej-subcadena-minima title="Acota la copia por abajo"}
La salida de memoria 3 empieza en un contexto visto. ¿Por qué su subcadena literal más larga no puede medir menos de 4?
:::

::: hint {#mkv-c1-pista-subcadena-minima of="mkv-c1-ej-subcadena-minima" title="Qué apareció seguro"}
¿Qué bloque tuvo que aparecer en el corpus para que la fila de un contexto visto diera un símbolo?
:::

::: answer {#mkv-c1-resp-subcadena-minima of="mkv-c1-ej-subcadena-minima"}
El contexto inicial se vio, y su fila se usa sin suavizar: el primer símbolo generado sale con conteo positivo. Así, ese bloque (contexto, siguiente) de $h+1=4$ letras apareció en el corpus, y la subcadena más larga mide al menos 4. Aquí mide 13.
:::

Ya puedes generar a mano, con el algoritmo y con el corpus, y leer qué arriesga cada memoria.

---

## Ejercicios

::: exercise {#mkv-c1-ej-generar-letras title="Genera cuatro símbolos con letras y espacio"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Una cadena de memoria 1 tiene $\Sigma$ = {a, n, espacio}, en ese orden. **Cambia una idea:** los estados son letras y espacio, no clases, y una fila tiene un cero al inicio. Las filas son:

- **Desde a:** (0, 1/2, 1/2).
- **Desde n:** (3/4, 0, 1/4).
- **Desde espacio:** (1/2, 1/2, 0).

Empiezas en espacio y usas $u$ = 0.62, 0.15, 0.40 y 0.90.

1. **Acumula.** Escribe la fila acumulada de cada estado.
2. **Traza.** Para cada paso $j$, da el contexto, $u$ y el símbolo que sale.
3. **Devuelve.** Escribe lo que devuelve GENERAR, contexto inicial incluido.
4. **Interpreta el cero.** ¿Puede salir «aa»? ¿Puedes saber, con la tabla, si es un cero estructural?
5. **Quita una fila.** Si n nunca hubiera tenido salidas en los datos, la tabla no traería su fila. ¿Qué haría GENERAR al llegar a n?
:::

::: hint {#mkv-c1-pista-generar-letras-1 of="mkv-c1-ej-generar-letras" title="Pista 1 · ¿Qué suma corresponde a cada símbolo?"}
¿Qué sumas parciales tiene cada fila en el orden a, n, espacio? ¿Qué fila lees en cada paso?
:::

::: hint {#mkv-c1-pista-generar-letras-2 of="mkv-c1-ej-generar-letras" title="Pista 2 · ¿Comparaste como MUESTREAR-FILA?"}
¿Usaste «$u$ menor que la suma», y no «menor o igual»? ¿Qué pasa con una suma parcial que no crece?
:::

::: answer {#mkv-c1-resp-generar-letras of="mkv-c1-ej-generar-letras" title="Respuesta · Cuatro sorteos, una palabra"}
**1. Filas acumuladas.** Desde a: (0, 1/2, 1). Desde n: (3/4, 3/4, 1). Desde espacio: (1/2, 1, 1).

**2. Traza.**

| j | Contexto | u | Sale |
|---:|---|---:|---|
| 0 | espacio | 0.62 | n |
| 1 | n | 0.15 | a |
| 2 | a | 0.40 | n |
| 3 | n | 0.90 | espacio |

En el paso 0, 0.62 no es menor que 1/2, pero sí que 1. En el paso 2, 0.40 no es menor que 0: la a no puede salir.

**3. Texto.** GENERAR devuelve espacio, n, a, n, espacio: « nan ».

**4. El cero.** «aa» no puede salir: la entrada a→a vale 0 y su suma no crece. La tabla sola no dice si es estructural o solo no observado.

**5. Fila uniforme.** Al llegar a n, la línea 5 no encuentra su fila. GENERAR usa $1/|\Sigma|$ en cada uno de los tres símbolos y no se reinicia.
:::

::: exercise {#mkv-c1-ej-elegir-memoria title="Elige la memoria para letreros de un juego"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Un videojuego necesita letreros de relleno «con sabor a *Quijote*». **Cambia una idea:** ahora hay una restricción de uso, no copiar tramos largos del libro. Usa @mkv-c1-ceros-generar, la tabla de copia y las salidas de la sección 3. La respuesta desarrolla una opción.

1. **Lee la escasez.** ¿Qué memoria tiene más transiciones no vistas, y cuántas?
2. **Compara dos salidas.** Contrasta memoria 1 y memoria 3 en lo que se lee y en lo que copian.
3. **Elige.** Escoge una memoria y justifícala con dos cifras.
4. **Planea la comprobación.** ¿Qué medirías antes de confiar en tu elección?
:::

::: hint {#mkv-c1-pista-elegir-memoria-1 of="mkv-c1-ej-elegir-memoria" title="Pista 1 · ¿Qué mide cada número?"}
¿Qué cifras dicen cuánto se parece la salida al español, y cuáles cuánto copia?
:::

::: hint {#mkv-c1-pista-elegir-memoria-2 of="mkv-c1-ej-elegir-memoria" title="Pista 2 · ¿Cuántas réplicas viste?"}
¿Tu justificación descansa en una sola salida por memoria? ¿Qué cambiaría con otra semilla?
:::

::: answer {#mkv-c1-resp-elegir-memoria of="mkv-c1-ej-elegir-memoria" title="Respuesta · Legible sin copiar"}
**1. Escasez.** Memoria 3: 0.570 % de transiciones no vistas, y 3 328 de 21 952 contextos vistos. Aun así, es poca: el corpus es largo.

**2. Dos salidas.** Memoria 1 da palabras cortas reales entre ruido, y 9 % de 8-gramas copiados. En esta réplica, memoria 3 casi se lee, pero copia 42 % y su tramo literal más largo mide 13.

**3. Elección.** Memoria 2: ya forma sílabas y palabras cortas, y copia 20 %, con un tramo máximo de 11. Estas cifras justifican probarla; no garantizan que otras salidas copien poco.

**4. Comprobación.** Generar muchas réplicas con semillas distintas y mirar el reparto de la fracción copiada, no una sola salida. Descartar los letreros con un tramo literal largo.
:::

**Punto de control:** deberías poder trazar GENERAR a mano con uniformes dados, decir qué fila usa un contexto nunca visto y traducir los órdenes de Shannon. También, leer qué gana y qué arriesga subir la memoria con datos limitados.

---

## Lo que hay que llevarse

- **A mano.** Desde C, con $u$ = 0.90, 0.55 y 0.30, la matriz de tres estados da `_`, C y V. El cero de `_`→`_` nunca sale.
- **El algoritmo.** GENERAR gasta un $u$ por símbolo y desliza el contexto. Un contexto nunca visto usa la fila uniforme, $1/|\Sigma|$; no se reinicia.
- **Las salidas.** Con semillas 2032 a 2035, memoria 0 da letras sueltas y memoria 3 frases casi legibles.
- **Shannon (1948).** Su primer orden es nuestra memoria 0; su segundo, memoria 1. Lo hizo a mano, con tablas y abriendo un libro al azar.
- **Ganar y arriesgar.** Más memoria representa más y no empeora el ajuste en los datos. Con datos limitados, las transiciones no vistas suben a 0.570 % en memoria 3. La copia de 8-gramas pasa de 0 % a 42 %, y el tramo literal más largo de 6 a 13.

Continúa con [[markov|Cadenas de Markov]], el índice de la unidad, o repasa los símbolos en [[notacion-markov|la hoja de notación]].
