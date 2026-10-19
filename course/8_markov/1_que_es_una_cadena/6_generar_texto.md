---
id: mkv-generar-texto
title: "Generar texto"
nav_title: "Generar texto"
summary: "Generar con cualquier alfabeto y memoria: filas, contextos y probabilidad del texto. El algoritmo a mano y en Python, las salidas del Quijote, Shannon y los riesgos de aumentar la memoria."
status: ready
estimated_time: 31m
tags: [markov]
---

# Generar texto

**¿Cómo genera texto una cadena con memoria, y qué cambia al recordar más símbolos?**

Al terminar tendrás:

- **La regla general:** filas por contexto, actualización y probabilidad de un texto dado su inicio.
- **GENERAR:** pseudocódigo, Python y una traza con tres uniformes.
- **Una regla para filas ausentes:** uniforme por símbolo, sin reiniciar.
- **Las salidas del Quijote:** memorias 0 a 3 y memoria 1 de palabras.
- **Una comparación:** órdenes de Shannon (1948), escasez de datos y copia.

> [!TIP]
> **Míralo correr: el generador de texto**
>
> **▶ [El generador](../_assets/generador_texto.html#h=2&semilla=2034&largo=200&paso=148)** muestra contexto, fila y uniforme. Cambia memoria y semilla; avanza un símbolo por paso.

## Lo que traes

- **La cadena y sus dos movimientos.** En [[mkv-cadena-en-general|La cadena de Markov, en general]]: la definición (@mkv-c1-cadena), la distribución $\mu_t$ que se multiplica (@mkv-c1-teo-predecir) y la trayectoria que se sortea. Aquí se sortea.
- **Muestrear una fila.** En [[mkv-el-problema-de-markov|El problema de Markov]], MUESTREAR-FILA con ${u\in[0,1)}$ y la fila acumulada, y la matriz de V, C y espacio (`_`).
- **Contar, suavizar, memoria.** En [[mkv-ajustar-contando|Ajustar contando]]: $\widehat P$, los ceros, Laplace y la memoria $h$ (@mkv-c1-memoria).

> **Modelo y datos.** Generar con $\widehat P$ muestra lo que la cadena ajustada considera probable, no qué es el español.

---

## 1 · Generar a mano tres símbolos

**Piensa: ¿cómo convierte una fila de probabilidades en texto cualquier modelo con memoria?**

Sortea un símbolo con la fila del contexto y conserva los últimos $h$ símbolos (@mkv-c1-memoria).

$Z_j$ es el símbolo aleatorio; $z_j$, su valor. $\operatorname{suf}_h(w)$ toma los últimos $h$ símbolos de $w$; con $h=0$, devuelve $()$.

$$
\begin{aligned}
c_0&\in\Sigma^h,\\
c_{j+1}&=\operatorname{suf}_h(c_jz_{j+1}),\\
p(\cdot\mid c)&\in\mathbb R^{1\times|\Sigma|},\\
p(z\mid c)&\ge0,\qquad
\sum_{z\in\Sigma}p(z\mid c)=1.
\end{aligned}
$$

### La tabla y la matriz

La tabla por símbolos guarda $|\Sigma|^h\times|\Sigma|$ probabilidades. La matriz $P$ entre contextos sigue siendo cuadrada:

$$
\begin{aligned}
P(c'\mid c)
&=\sum_{\substack{z\in\Sigma:\\
\operatorname{suf}_h(cz)=c'}}p(z\mid c),\\
P&\in\mathbb R^{|\Sigma|^h\times|\Sigma|^h}.
\end{aligned}
$$

Con memoria 1, $p(z\mid c)=P(z\mid c)$; con memoria 0, $P=(1)$ y los símbolos se sortean de una sola fila.

### La probabilidad del texto

$S_j$ es el contexto aleatorio; $c_j$, su valor. Fijamos el inicio $S_0=c_0$. Con filas fijas y un uniforme independiente por paso:

$$
\begin{aligned}
&\Pr(Z_1=z_1,\ldots,Z_T=z_T\mid S_0=c_0)\\
&\qquad=\prod_{j=0}^{T-1}p(z_{j+1}\mid c_j).
\end{aligned}
$$

La regla del producto (@mkv-c1-teo-producto) multiplica las probabilidades por símbolo. Los contextos forman los estados de @mkv-c1-cadena.

### La matriz de V, C y espacio

- **Ejemplo:** la matriz de [[mkv-el-problema-de-markov|El problema de Markov]], memoria 1, en el orden V, C, `_`.
- **Inicio:** C. Los uniformes dados son 0.90, 0.55 y 0.30.

$$
\widehat P=\begin{pmatrix}
1/11 & 7/11 & 3/11\\
2/3 & 1/5 & 2/15\\
1/5 & 4/5 & 0
\end{pmatrix}.
$$

**Cómo leer la traza.** Cada renglón es un paso $j$; las sumas acumuladas siguen el orden V, C, `_`.

::: table {#mkv-c1-traza-generar-a-mano title="Generar desde C con tres uniformes dados"}
| j | Desde · acumuladas | u | Sale |
|---:|---|---:|---|
| 0 | C · (2/3, 13/15, 1) | 0.90 | `_` |
| 1 | `_` · (1/5, 1, 1) | 0.55 | C |
| 2 | C · (2/3, 13/15, 1) | 0.30 | V |
:::

- **Paso 0:** 0.90 supera 2/3 y 13/15; sale `_`, con probabilidad 2/15.
- **Paso 1:** 0.55 supera 1/5; sale C.
- **Paso 2:** 0.30 es menor que 2/3; sale V.
- **Resultado:** `C_CV`, con el inicio incluido. Antes de fijar los uniformes, la probabilidad de esa continuación es:

$$
\Pr(\mathtt{\_CV}\mid C)
=\frac{2}{15}\cdot\frac{4}{5}\cdot\frac{2}{3}.
$$

::: exercise {#mkv-c1-ej-espacio-doble title="Busca otro espacio"}
En el paso 1 estás en `_`. ¿Qué $u$ haría que saliera otro espacio?
:::

::: hint {#mkv-c1-pista-espacio-doble of="mkv-c1-ej-espacio-doble" title="Mira la última suma"}
¿Cuánto crece la suma acumulada al llegar a la entrada de `_`?
:::

::: answer {#mkv-c1-resp-espacio-doble of="mkv-c1-ej-espacio-doble"}
Ninguno. La fila acumulada es (1/5, 1, 1): la entrada de `_` vale 0 y la suma no crece.
Todo ${u<1}$ ya eligió V o C. Es el cero estructural de la normalización: tras un espacio nunca hay otro.
:::

El deslizamiento ya fija el contexto siguiente; para programar la generación falta completar las filas sin datos.

---

## 2 · Escribir el algoritmo GENERAR

**Piensa: ¿cómo cambia el contexto y qué fila usas si nunca se observó?**

Deslizas el contexto con la regla anterior; si no tuvo salidas, usas una fila uniforme.

### Un contexto nunca visto

Con $N(c)=\sum_{z\in\Sigma}N(c,z)$, elegimos:

$$
p(z\mid c)=
\begin{cases}
\widehat p(z\mid c)=\dfrac{N(c,z)}{N(c)},
   &N(c)>0,\\[4pt]
\dfrac1{|\Sigma|},&N(c)=0.
\end{cases}
$$

Para $N(c)=0$, Laplace también da $\widetilde p(z\mid c)=1/|\Sigma|$ (@mkv-c1-laplace).

- **Filas vistas:** se usan sin suavizar; un siguiente no observado conserva probabilidad 0.
- **Filas ausentes:** la «k» no aparece en el *Quijote*; con memoria 1, recibe la uniforme.
- **Sin reinicio:** se conserva el texto y se sigue deslizando el contexto.

::: definition {#mkv-c1-generar title="Generar con una cadena"}
- **Qué es:** producir una trayectoria desde $c_0$, sorteando un símbolo por paso.
- **Cómo se calcula:** muestrear $p(\cdot\mid c_j)$, escribir $z_{j+1}$ y actualizar $c_j$ con la regla anterior.
- **Qué significa:** cada salida es una réplica del modelo; en la traza fue `C_CV`.
- **Qué no es:** no calcula $\mu_t$ ni elige el máximo de cada fila; sortea según sus probabilidades.
:::

> **Dado:** alfabeto $\Sigma$, filas de probabilidades para contextos vistos, contexto inicial de $h$ símbolos y largo ${T\ge0}$.
>
> **Encontrar:** el contexto inicial seguido de $T$ símbolos generados según @mkv-c1-generar.

### El mapa de GENERAR

- **Qué calcula:** una réplica del modelo con memoria $h$.
- **Qué guarda:** el texto escrito; sus últimos $h$ símbolos forman el contexto.
- **Cómo avanza:** busca la fila, sortea $u$, escribe $z$ y desliza el contexto.
- **Qué devuelve al terminar:** el inicio seguido de los símbolos generados.

::: figure {#mkv-c1-flujo-generar title="Generar, en palabras"}
![Diagrama de flujo de generar texto: empieza con un contexto de h símbolos; pregunta si faltan símbolos, y si no, devuelve el texto; si sí, pregunta si se vio el contexto, y si no, usa la fila suavizada; muestrea su fila con un u nuevo; escribe el símbolo, desliza el contexto y vuelve a preguntar si faltan símbolos. Con largo = 0 devuelve el contexto sin escribir nada. Al pie: un contexto nunca visto no se reinicia, su fila suavizada da 1/|Σ| a cada símbolo](../_assets/mkv-c1-flujo-generar.svg)
:::

- **Convención del código:** `s` representa $c_j$ y `largo` representa $T$.

```text
INPUT   el alfabeto Σ; una tabla
        con una fila sobre Σ
        por cada contexto visto;
        un contexto inicial de h
        símbolos; un largo ≥ 0.
OUTPUT  el contexto inicial
        seguido de largo
        símbolos generados.

 1 function GENERAR(Σ, tabla,
              contexto, largo)
 2   texto ← contexto
     h ← |contexto|
 3   for j ← 0 to largo − 1
 4     s ← últimos h de texto
 5     if s está en la tabla
 6       fila ← tabla[s]  # P̂
 7     else       # nunca visto
 8       fila ← 1/|Σ| en cada z
 9     u ← uniforme en [0, 1)
10     z ← Σ[MUESTREAR-FILA(
              fila, u)]
11     texto ← texto seguido de z
12   return texto
```

**Gemelo Python.** Pega antes `muestrear_fila` de [[mkv-el-problema-de-markov|El problema de Markov]]. Los comentarios `# (n)` corresponden al pseudocódigo.

```python
from fractions import Fraction

# (1)
def generar(tabla, alfabeto,
            contexto, largo,
            rng):
    texto = contexto       # (2)
    h = len(contexto)      # (2)
    for j in range(largo): # (3)
        # (4)
        s = texto[len(texto)-h:]
        if s in tabla:     # (5)
            # (6)
            fila = tabla[s]
        else:              # (7)
            # (8)
            k = len(alfabeto)
            fila = [1 / k] * k
        u = rng.random()   # (9)
        # (10)
        i = muestrear_fila(
            fila, u)
        z = alfabeto[i]
        texto = texto + z  # (11)
    return texto           # (12)

class UsDados:
    # da los u de la traza a mano
    def __init__(self, us):
        self.us = list(us)

    def random(self):
        return self.us.pop(0)

F = Fraction
tabla = {
    "V": [F(1, 11), F(7, 11),
          F(3, 11)],
    "C": [F(2, 3), F(1, 5),
          F(2, 15)],
    "_": [F(1, 5), F(4, 5),
          F(0)],
}
us = UsDados([0.90, 0.55, 0.30])
print(generar(tabla, "VC_", "C",
              3, us))
# C_CV
```

**Cada pieza, en su línea:**

- **Línea 4:** `texto[len(texto)-h:]` da el contexto vacío con ${h=0}$; `texto[-0:]` daría todo el texto.
- **Líneas 5 a 8:** usan las frecuencias $\widehat p$ para contextos vistos y la uniforme para los ausentes; con memoria 1, esas frecuencias forman $\widehat P$.
- **Líneas 9 y 11:** un uniforme por símbolo; al agregar $z$, la línea 4 siguiente lee el contexto desplazado.

### Lo que garantiza y cuánto cuesta

- **Propiedades:** termina tras `largo` pasos; con largo 0 devuelve el inicio.
- **Reproducibilidad:** misma tabla, orden del alfabeto, inicio y semilla producen el mismo texto.
- **Número que da:** `C_CV` en la traza; devuelve texto, no su probabilidad.
- **Garantía:** con uniformes independientes en ${[0,1)}$, cada símbolo tiene la probabilidad de su fila, en aritmética exacta.
- **Costo del muestreo:** hasta ${\lvert\Sigma\rvert}$ entradas por paso; en total, ${O(T\lvert\Sigma\rvert)}$, sin contar operaciones sobre cadenas.
- **Almacenamiento:** hasta ${\lvert\Sigma\rvert^h}$ filas de ${\lvert\Sigma\rvert}$ entradas, además del texto.
- **Supuestos:** alfabeto finito no vacío, filas no negativas que suman 1 e inicio en ${\Sigma^h}$.
- **Implementación:** este Python usa caracteres; con palabras, usaríamos una lista y contextos como tuplas.

::: exercise {#mkv-c1-ej-memoria-cero title="Corre GENERAR sin memoria"}
Con ${h=0}$, ¿qué contexto lee la línea 4 y qué fila usa en cada paso?
:::

::: hint {#mkv-c1-pista-memoria-cero of="mkv-c1-ej-memoria-cero" title="Cuenta lo que queda"}
¿Cuántos símbolos quedan si tomas los últimos 0?
:::

::: answer {#mkv-c1-resp-memoria-cero of="mkv-c1-ej-memoria-cero"}
Lee el contexto vacío, siempre el mismo. Usa la fila de frecuencias de los símbolos.
Con uniformes independientes, cada símbolo sale independiente de los anteriores.
:::

GENERAR corre con cualquier tabla. ¿Qué escribe con las tablas del *Quijote*?

---

## 3 · Leer ejemplos con semilla

**Piensa: ¿qué conserva del corpus cada fragmento generado?**

Desde una fila vista sin suavizar, cada continuación conserva un bloque observado de $h+1$ símbolos:

$$
\widehat p(z\mid c)>0
\quad\Longrightarrow\quad N(c,z)>0.
$$

La palabra o la frase completa puede ser nueva.

### Las condiciones del experimento

- **Corpus:** contamos los 28 símbolos normalizados del *Quijote*: 27 letras sin acentos, con ñ, más espacio.
- **Normalización:** todo signo que no sea letra separa palabras; los espacios consecutivos se juntan.
- **Orden:** `abcdefghijklmnñopqrstuvwxyz`, con espacio al final. Cambiarlo puede cambiar la salida con la misma semilla.
- **Filas:** conteos divididos entre salidas; aplicamos la regla declarada para contextos ausentes.
- **Inicio:** primeros $h$ símbolos de «en un lugar»; vacío con memoria 0.
- **Largo:** 200 símbolos totales, incluido el inicio:

$$
\begin{aligned}
\text{largo total}&=h+T,\\
T&=200-h.
\end{aligned}
$$

- **Semillas:** 2032, 2033, 2034 y 2035 para memorias 0, 1, 2 y 3.
- **Presentación:** los renglones se cortan en espacios; cada salida es una sola línea.

**Memoria 0 · semilla 2032** (el primer símbolo sorteado fue un espacio; con memoria 0 el contexto es vacío)

```text
 pusnve dprate duuutesrsacee insi
qlsao iamsopaa ceecae do
vnoov  oausu q i etg anls
oalilanosll y  grcgiiypeo ldes
eees eebdessatoes uoed nn enlea
aa oehtbo mehs n naoeesiaya
ysitrn laa  muercltsoi n
```

**Memoria 1 · semilla 2033**

```text
er gonos sesel usiava lera
cuecive de lo ta ques pera a
lodasijeralgosper ene l y y
mabera y tidelerla tia
quenoncalerela tre dandaue cr s
quede en ve sin suieo e a
cuestadui des que pa fe y
mbesctrta
```

**Memoria 2 · semilla 2034**

```text
enchombolaso aquisia
veasagionallegar que parespel er
arovicino pro es quecienes do la
dos mues y fue el minto acaba
queño as dejote noco a y
dechacescuanajabese lle nos hano
de encera quesar y pue ma
```

**Memoria 3 · semilla 2035**

```text
en su amosura en el dijote espero
otrastilla paremostan de señor
como acomo el cuerte lo en
cuandoliconvies sustra y un gran
vizcaidad del fio hacenca que
pros de burrespondios en loco de
tendicen otr
```

- **Memoria 0:** frecuencias sin dependencia entre símbolos; «duuutesrsacee». Los espacios también siguen su frecuencia; sin memoria, salen espacios dobles que el corpus normalizado no tiene.
- **Memoria 1:** aparecen palabras cortas reales: «de», «lo», «que», «sin».
- **Memoria 2:** aparecen sílabas y fragmentos como «la», «y fue el» y «acaba».
- **Memoria 3:** se reconocen frases como «en su amosura» y «un gran vizcaidad». Cada tramo de cuatro caracteres fue observado.

### El generador interactivo

- **Cada paso:** muestra contexto, fila, $u$ y el intervalo acumulado elegido.
- **Repetir las salidas:** usa la semilla correspondiente y largo 200; el interactivo cuenta el total, incluido el contexto.

::: figure {#mkv-c1-generador title="El generador escribiendo con memoria 2"}
[![Captura del generador de texto con memoria 2 y semilla 2034, en el símbolo 150 de 200. El panel del paso muestra el contexto «ce», con 6 942 salidas; las más probables son r 0.260, d 0.196, s 0.162, espacio 0.153 y n 0.099, y el resto suma 0.129. El u sorteado, 0.7149, cae en el pedazo de «s», de 0.6788 a 0.8410, y se escribe «s».](../_assets/mkv-c1-generador.png)](../_assets/generador_texto.html#h=2&semilla=2034&largo=200&paso=148)
:::

> **▶ [Abre el generador](../_assets/generador_texto.html#h=2&semilla=2034&largo=200&paso=148)**: pulsa la imagen o este enlace. Cambia memoria y semilla; avanza un símbolo a la vez.

### Palabras en vez de letras

$$
\begin{aligned}
\Sigma&=\text{vocabulario del corpus},\\
h&=1.
\end{aligned}
$$

- **Contexto:** la palabra anterior. Generamos 30 palabras totales, con semilla 2036 e inicio «en».

> en tanto artificio que sus aguelos ahora la ventana que venian del pie llano a don quijote de sirgo pon el famoso caballero en las desdichas del a pasar habiendole

- **Lectura:** cada par consecutivo aparece en el *Quijote*; la frase completa, no. La normalización quita acentos: «venian».

::: exercise {#mkv-c1-ej-palabra-inventada title="Desarma una palabra inventada"}
La salida de memoria 2 dice «veasagionallegar», que no está en el *Quijote*. ¿De qué pedazos está hecha?
:::

::: hint {#mkv-c1-pista-palabra-inventada of="mkv-c1-ej-palabra-inventada" title="El tamaño de cada pieza"}
¿Qué bloques del corpus garantiza una fila vista sin suavizar?
:::

::: answer {#mkv-c1-resp-palabra-inventada of="mkv-c1-ej-palabra-inventada"}
De tríos: «vea», «eas», «asa», … Cada trío tuvo conteo positivo; la palabra completa no apareció.
El modelo recuerda dos letras y combina tríos que se traslapan.
:::

Estas salidas tienen un antecedente famoso, hecho sin computadora.

---

## 4 · Traducir las aproximaciones de Shannon

**Piensa: ¿cómo se relacionan el tamaño del bloque y la memoria del contexto?**

El bloque contiene el contexto y el símbolo siguiente: mide $h+1$. Desde el primer orden, Shannon numera por el tamaño del bloque:

$$
\begin{aligned}
\text{tamaño del bloque}&=h+1,\\
\text{orden de Shannon}&=h+1.
\end{aligned}
$$

- **Orden cero:** es la excepción; usa símbolos independientes y equiprobables.
- **Shannon (1948):** presentó aproximaciones al inglés en «Una teoría matemática de la comunicación» (*A Mathematical Theory of Communication*).
- **Fuente:** *Bell System Technical Journal*, parte I, sección 3.
- **Alfabeto:** 27 símbolos: 26 letras y espacio.

::: table {#mkv-c1-shannon title="Los órdenes de Shannon, en memoria"}
| Shannon | Aquí | Qué usa |
|---|---|---|
| Orden 0 | Uniforme | Nada |
| Orden 1 | Memoria 0 | Letras |
| Orden 2 | Memoria 1 | Pares |
| Orden 3 | Memoria 2 | Tríos |
:::

- **Primer orden:** usó frecuencias de letras y un libro de números aleatorios; las letras sueltas conservan sus frecuencias.
- **Segundo orden:** abría un libro al azar y elegía una letra; después, buscaba esa letra en otra página y anotaba la siguiente.
- **Idea:** el libro proporciona continuaciones observadas, como una tabla de la que se muestrea.
- **Nuestros ejemplos:** las salidas del *Quijote* usan computadora y semillas fijas; no son las muestras de Shannon.

::: exercise {#mkv-c1-ej-orden-shannon title="Traduce la memoria 3"}
¿Con qué orden llamaría Shannon a nuestra salida de memoria 3?
:::

::: hint {#mkv-c1-pista-orden-shannon of="mkv-c1-ej-orden-shannon" title="Las dos numeraciones"}
Con memoria 3, ¿cuántas letras tiene cada bloque (contexto, siguiente)?
:::

::: answer {#mkv-c1-resp-orden-shannon of="mkv-c1-ej-orden-shannon"}
Cuarto orden: cada bloque tiene ${h+1=4}$ letras.
Es una traducción de numeración; Shannon publicó hasta el tercer orden en letras.
:::

Memoria 3 se lee mejor que memoria 2. ¿Por qué no subirla sin límite?

---

## 5 · Medir qué gana y qué arriesga la memoria

**Piensa: si memoria 3 se lee mejor, ¿por qué no usar memoria 10?**

Porque reparte los mismos datos entre más contextos: mejorar el ajuste no garantiza mejores textos nuevos.

$$
\begin{aligned}
\text{contextos con memoria }h
   &: |\Sigma|^h,\\
\text{contextos con memoria }h+1
   &: |\Sigma|^{h+1},\\
\max\mathcal L_{h+1}&\ge\max\mathcal L_h.
\end{aligned}
$$

- **Condición:** $\mathcal L_h$ es la verosimilitud con memoria $h$, sobre las mismas transiciones, el mismo inicio y filas libres sin suavizar.
- **Razón:** la memoria $h+1$ puede ignorar el símbolo adicional e imitar a la memoria $h$.

### Medir la escasez

La @mkv-c1-ceros cuenta pares de la segunda mitad del corpus no vistos en la primera.
GENERAR usa la uniforme solo si ${N(c)=0}$; si ${N(c)>0}$ y ${N(c,z)=0}$, conserva ${\widehat p(z\mid c)=0}$. Las barras no miden cuántas veces se usa la uniforme.

::: figure {#mkv-c1-ceros-generar title="Lo que nunca se vio, por memoria"}
![Barras horizontales por memoria, con la fracción de transiciones de la segunda mitad del corpus nunca vistas en la primera. Memoria 0: 0 %, 0 de 998 564, contextos vistos 1 de 1. Memoria 1: 0.003 %, 29 de 998 563, contextos vistos 27 de 28. Memoria 2: 0.072 %, 718 de 998 562, contextos vistos 379 de 784. Memoria 3: 0.570 %, 5 694 de 998 561, contextos vistos 3 328 de 21 952. Las barras están a escala de la mayor (memoria 3). Al pie: solo diagnostica escasez, no elige la memoria](../_assets/mkv-c1-ceros.svg)
:::

- **Distinción:** puede faltar el siguiente en una fila vista o faltar el contexto entero. Solo el segundo caso activa la uniforme.

### Medir la copia

- **Tramo más largo:** subcadena consecutiva de la salida que aparece literal en el corpus.
- **Porcentaje copiado:** fracción de sus 8-gramas observados en el corpus; cada 8-grama contiene 8 caracteres consecutivos.

::: table {#mkv-c1-tabla-copiar title="Cuánto copia cada salida del corpus"}
| Memoria | Tramo más largo | % copiado |
|---:|---:|---:|
| 0 | 6 | 0 % |
| 1 | 10 | 9 % |
| 2 | 11 | 20 % |
| 3 | 13 | 42 % |
:::

- **Una réplica:** cada fila mide una sola salida de la sección 3; otra semilla puede cambiar las cifras.
- **Copia sin obligación:** cada contexto del tramo de 13 admitía varios siguientes observados; los sorteos reprodujeron una secuencia del corpus.
- **Continuación forzada:** si una fila observada concentra probabilidad 1 en un símbolo, siempre genera ese símbolo.
- **Tramos forzados:** si cada contexto sucesivo tiene una sola continuación, la salida es determinista hasta encontrar otra opción o una fila ausente; no tiene que ser un tramo del corpus.
- **Ciclos:** con memoria 1 y corpus «abab», sale «ababab…», más largo que el corpus.
- **Variedad:** más continuaciones, con probabilidades parejas, facilitan combinar fragmentos.

> [!WARNING]
> **Confundir legibilidad con novedad.** La salida de memoria 3 parece más legible, pero copia 42 % de sus 8-gramas. **Leer bien no asegura ser nuevo.**

::: exercise {#mkv-c1-ej-subcadena-minima title="Acota la copia por abajo"}
La salida de memoria 3 empieza en un contexto visto. ¿Por qué su subcadena literal más larga no puede medir menos de 4?
:::

::: hint {#mkv-c1-pista-subcadena-minima of="mkv-c1-ej-subcadena-minima" title="Qué apareció seguro"}
¿Qué bloque tuvo que aparecer en el corpus para que la fila de un contexto visto diera un símbolo?
:::

::: answer {#mkv-c1-resp-subcadena-minima of="mkv-c1-ej-subcadena-minima"}
El primer símbolo sale de una fila vista sin suavizar, con conteo positivo.
Ese bloque de ${h+1=4}$ letras apareció en el corpus: la subcadena más larga mide al menos 4. Aquí mide 13.
:::

Los ejercicios reúnen ambas decisiones: cómo generar cada símbolo y cómo elegir la memoria según el uso.

---

## Ejercicios

::: exercise {#mkv-c1-ej-generar-letras title="Genera cuatro símbolos con letras y espacio"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Una cadena de memoria 1 usa este alfabeto, en el orden escrito:

$$
\Sigma=\{\mathrm a,\mathrm n,\text{espacio}\}.
$$

**Cambia una idea:** el cero de una fila está al inicio, así que la primera suma parcial no crece.

- **Desde a:** (0, 1/2, 1/2).
- **Desde n:** (3/4, 0, 1/4).
- **Desde espacio:** (1/2, 1/2, 0).

Empiezas en espacio y usas $u$ = 0.62, 0.15, 0.40 y 0.90.

1. **Acumula.** Escribe la fila acumulada de cada estado.
2. **Traza.** Para cada paso $j$, da el contexto, $u$ y el símbolo que sale.
3. **Devuelve.** Escribe lo que devuelve GENERAR, contexto inicial incluido.
4. **Interpreta el cero.** ¿Puede salir «aa»? ¿Puedes saber, con la tabla, si es un cero estructural?
5. **Quita una fila.** Si n nunca hubiera tenido salidas observadas, faltaría su fila. ¿Qué haría GENERAR al llegar a n?
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

En el paso 0, 0.62 no es menor que 1/2, pero sí que 1.
En el paso 2, 0.40 no es menor que 0: la a no puede salir.

**3. Texto.** GENERAR devuelve espacio, n, a, n, espacio: « nan ».

**4. El cero.** «aa» no puede salir: la entrada a→a vale 0 y su suma no crece.
La tabla sola no dice si es estructural o solo no observado.

**5. Fila uniforme.** Al llegar a n, la línea 5 no encuentra su fila.
GENERAR usa ${1/\lvert\Sigma\rvert}$ en cada símbolo y no se reinicia.
:::

::: exercise {#mkv-c1-ej-elegir-memoria title="Elige la memoria para letreros de un juego"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Un videojuego necesita letreros de relleno «con sabor a *Quijote*».
**Cambia una idea:** ahora hay una restricción de uso: evitar copiar tramos largos.
Usa @mkv-c1-ceros-generar, @mkv-c1-tabla-copiar y las salidas de la sección 3. La respuesta desarrolla una opción.

1. **Lee la escasez.** Con memoria 3, ¿cuántas transiciones de prueba no se vieron y cuántos contextos se vieron? ¿Basta para descartarla?
2. **Compara dos salidas.** Contrasta memoria 1 y memoria 3 en legibilidad y copia.
3. **Elige.** Escoge una memoria y justifícala con dos cifras.
4. **Planea la comprobación.** ¿Qué medirías antes de confiar en tu elección?
:::

::: hint {#mkv-c1-pista-elegir-memoria-1 of="mkv-c1-ej-elegir-memoria" title="Pista 1 · ¿Qué mide cada número?"}
¿Qué cifras describen los datos de ajuste y cuáles las salidas generadas? ¿Cómo se relacionan con la restricción del juego?
:::

::: hint {#mkv-c1-pista-elegir-memoria-2 of="mkv-c1-ej-elegir-memoria" title="Pista 2 · ¿Cuántas réplicas viste?"}
¿Tu justificación descansa en una sola salida por memoria? ¿Qué cambiaría con otra semilla?
:::

::: answer {#mkv-c1-resp-elegir-memoria of="mkv-c1-ej-elegir-memoria" title="Respuesta · Legible sin copiar"}
**1. Escasez.** No se vieron 5 694 de 998 561 transiciones de prueba, el 0.570 %.
Se vieron 3 328 de 21 952 contextos posibles.
Eso no basta para descartarla: la restricción exige medir copia.

**2. Dos salidas.** Memoria 1 da palabras cortas entre ruido, con 9 % de 8-gramas copiados.
Memoria 3 casi se lee, pero copia 42 %; su tramo literal máximo mide 13.

**3. Elección.** Probaría memoria 2: forma sílabas y palabras cortas, copia 20 % y tiene un tramo máximo de 11.
Estas cifras justifican probarla; no garantizan poca copia en otras salidas.

**4. Comprobación.** Generaría réplicas con distintas semillas y mediría la distribución del porcentaje copiado y del tramo máximo.
Descartaría los letreros con tramos literales largos.
:::

**Punto de control:** traza GENERAR, calcula la probabilidad de su texto dado el inicio y explica cómo trata filas ausentes.
Traduce los órdenes de Shannon y justifica una memoria con evidencia de escasez y copia.

---

## Lo que hay que llevarse

$$
\begin{aligned}
Z_{j+1}&\sim p(\cdot\mid c_j),\\
c_{j+1}&=\operatorname{suf}_h(c_jz_{j+1}),\\
p(\cdot\mid c)&\in\mathbb R^{1\times\lvert\Sigma\rvert}.
\end{aligned}
$$

- **El algoritmo.** GENERAR muestrea, escribe y desliza, un $u$ por símbolo. Un contexto nunca visto usa ${1/\lvert\Sigma\rvert}$; no se reinicia.
- **A mano.** Desde C, con $u$ = 0.90, 0.55 y 0.30, sale `C_CV`. El cero de `_`→`_` nunca sale.
- **Las salidas.** Con semillas 2032 a 2035, memoria 0 da letras sueltas y memoria 3 frases casi legibles.
- **Shannon (1948).** Su primer orden es nuestra memoria 0; su segundo, memoria 1. Usó números aleatorios para el primero y continuaciones de un libro para el segundo.
- **Ganar y arriesgar.** Más memoria no baja la verosimilitud máxima, pero las transiciones no vistas suben a 0.570 % en memoria 3. La copia de 8-gramas pasa de 0 % a 42 %, y el tramo literal más largo de 6 a 13.

Continúa con [[tarea-que-es-una-cadena|la tarea de la clase 1]]. Para consultar símbolos, usa [[notacion-markov|la hoja de notación]].
