<!--
Tipo: guion_notebook_tarea
Etiqueta: prog-c1 (tramo de la tarea)
Contrato: v5.1 · API ml_lab: 1.6 · Protocolo: p5.2
Plan: clase_1 §10.6 y brief B-T1
Rama de origen: aprendizaje-maquina-clase-1-c
Archivo permitido: tools/cuadernos_ml/tarea_1_proponer_phi.texto.md

Decisiones del registro que aplican
D-008: sin fechas ni plazos.
D-009.1: notación del curso; D-009.5: ninguna cifra de resultado en el guion.
Anatomía de tarea: portada, idea, seis bloques con Predice, Mira y Entrega,
y cierre. Sin -explica ni respuestas. Las claves vienen del .py.
Los bloques 2 y 3 siguen propón → registra → revela.
-->

### celda: portada

# Tarea 1 · Propón la representación

**¿Puedes proponer una $\phi$ mirando solo los datos, y decir con honestidad cuánto te equivocaste?**

Duración de trabajo: unos 90 min, en casa.
Acompaña la página [Tarea de la clase 1](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/tarea/).

Al terminar tendrás:

- **Predicciones revisadas:** qué mueve $L_{\text{ent}}$, $R$ y el piso.
- **Una $\phi$ periódica:** un periodo propuesto con la nube y $L_{\text{ent}}$.
- **Una $\phi$ para una nube nueva:** que no sea polar.
- **Su matriz $\Phi$:** qué es parámetro y qué es hiperparámetro.
- **Un veredicto:** qué error queda y qué te falta para fiarte de tus propuestas.

Se entrega el `.ipynb` por Canvas, con las celdas corridas.
Llena las seis celdas `entrega-<k>`. La fecha la da el profesor.

> **Colab:** guarda una copia propia y ejecuta primero la celda de arranque.
> Después avanza bloque por bloque, de arriba abajo.

**No abras el código de la celda «Prepara los procesos» hasta el bloque 6.**
Ahí está el proceso que vas a adivinar. Si lo lees antes, la tarea pierde su sentido.

**Propón, registra, revela.** En los bloques 2 y 3 eliges algo. Primero
lo propones con lo que tienes: la nube y $L_{\text{ent}}$. Después lo
registras: pones `REGISTRAR = True` en la celda «Juega» y la corres.
El notebook congela esa propuesta y su ajuste. Solo entonces corres la
celda «Revela», que está justo debajo y revisa lo congelado, no otra cosa.
La celda «Juega» guardada con `REGISTRAR = True` es tu registro: no la
cambies después de revelar.

Si reinicias el entorno o vuelves a correr «Prepara los procesos», el
registro en memoria se borra. Vuelve a correr las celdas sin cambiar tus
propuestas.

### celda: idea

Esta tarea usa la muestra enorme del proceso: cien mil observaciones que
dan $R$ casi exacto (veinte mil en el bloque 1, para que corra rápido). **En la vida real no existe.** Aquí sirve para
revisar una propuesta ya registrada, nunca para elegir. La clase 2 la
reemplaza por datos que sí existen: validación.

El periodo del bloque 2 y la $\phi$ del bloque 3 son hiperparámetros. La
definición [Parámetro contra hiperparámetro](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/polinomios-y-capacidad/#ml-c1-def-param-hiper)
pide elegirlos con datos que no tocaron el ajuste. En la clase 1 no hay
otros datos. Por eso tus elecciones son **propuestas exploratorias,
todavía sin validar**. Si agregas columnas a una $\phi$, el mínimo de
$L_{\text{ent}}$ no sube, y una propuesta elegida así puede salir optimista.

Si quieres repasar, vuelve a [¿Qué es f?](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/que-es-f/)
y a [Polinomios y capacidad](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/polinomios-y-capacidad/).

### celda: bloque-1-predice

## 1 · Predice antes de tocar

**Predice.** El proceso es $y=4+2\,\sin(3x)+\varepsilon$, con
$x\sim U(0,2)$ y $\varepsilon\sim\mathcal N(0,\sigma_\varepsilon^2)$.
La base: $\sigma_\varepsilon=0.5$, $n=20$ datos y un polinomio de grado $N=3$.
Cambias una cosa a la vez:

1. subes $\sigma_\varepsilon$ a 1;
2. subes $n$ a 200;
3. subes $N$ a 8.

En cada caso, ¿sube, baja o se queda $L_{\text{ent}}$? ¿Y $R$? ¿Y el piso?

Escribe tus nueve respuestas en `entrega-1` **antes** de correr la celda.
La celda repite cada caso con 30 muestras y da la mediana, para que una
muestra rara no decida.

### celda: bloque-1-mira

**Mira.** La tabla tiene un renglón por caso. Las columnas son la mediana de
$L_{\text{ent}}$, la mediana de $R$ y el piso $R_{\text{Bayes}}=\sigma_\varepsilon^2$.
Compara cada renglón con el de la base, no entre sí.

La segunda celda solo prepara los procesos de los bloques 2 a 5.
Córrela, pero no abras su código.

### celda: entrega-1

**Entrega 1.** Copia tus nueve predicciones tal como las escribiste.
Después marca cuáles acertaste. Para cada error, explica en una línea qué
pieza de $y=f(x)+\varepsilon$ no tomaste en cuenta.
No corrijas las predicciones: se califica la revisión honesta.

### celda: bloque-2-predice

## 2 · Un proceso periódico

**Predice.** Los datos vienen de $y=3+2\,\sin(2\pi x/\text{periodo})+\varepsilon$.
No sabes el periodo. ¿Cuál propones, mirando la nube?
¿Quién crees que tendrá menor $R$: tu periódica o un polinomio de grado 5?

Corre primero la celda con `PERIODO = None`: verás la nube y el polinomio.
El grado $N=5$ lo fija el notebook; no lo cambies.
Luego escribe tu `PERIODO` y tu `POR_QUE` y vuelve a correrla.
Puedes listar otros periodos en `PERIODOS_A_PROBAR` para comparar su
$L_{\text{ent}}$. Eso sigue siendo explorar con datos que tocaron el ajuste.

Con `PERIODO` puesto, la base es $\phi=(1,\sin(2\pi x/\text{periodo}),\cos(2\pi x/\text{periodo}))$.

Cuando tu propuesta sea final, pon `REGISTRAR = True` y vuelve a correr.
La salida dice «registrada en el bloque 2». Si después cambias `PERIODO`,
la celda te avisa, y «Revela» sigue revisando lo registrado.
Solo entonces corre la celda «Revela».

### celda: bloque-2-mira

**Mira.** En la gráfica, los puntos son los datos de entrenamiento. La
línea continua es el polinomio y la punteada, tu periódica. Los renglones
de abajo dan $L_{\text{ent}}$ de cada ajuste, y el último dice si tu
propuesta ya está registrada.

Al revelar aparece $R$ junto a $L_{\text{ent}}$, para los dos ajustes.
Compara dos cosas: quién gana en $R$, y cuánto se parecen $L_{\text{ent}}$ y
$R$ en cada uno.

### celda: entrega-2

**Entrega 2.** Lo que registraste, copiado de la salida de «Juega»:

- tu $\phi$ y tu periodo, **propuesta exploratoria, todavía sin validar**;
- con qué lo propusiste: lo que viste en la nube y, si los usaste, los $L_{\text{ent}}$;
- ¿el periodo es parámetro o hiperparámetro? Responde con la definición:
  ¿por qué elegirlo con $L_{\text{ent}}$ no basta?

Después de revelar, sin tocar la celda «Juega»:

- $R$ de tu periódica y del polinomio, copiados de la salida;
- qué tan lejos quedó tu propuesta y si $L_{\text{ent}}$ la hacía ver mejor de lo que fue.

Se premia el razonamiento, no haber atinado al periodo.

### celda: bloque-3-predice

## 3 · Una nube nueva

**Predice.** Hay dos clases y dos variables, $x_1$ y $x_2$. ¿Cuántos aciertos
esperas de la logística en cartesianas, $(1,x_1,x_2)$, comparada con la moda?

Corre la celda con `MI_PHI = None`: verás la nube con la frontera de las
cartesianas, y los aciertos en entrenamiento.
Mira la forma de la región donde vive la clase 1.

Luego propón tu $\phi$ con `ml.columnas(...)`, por ejemplo
`ml.columnas("x1", "x2 ** 2")`. Ese ejemplo no es la respuesta.
Tu $\phi$ no puede ser polar ni el producto $x_1x_2$ del ejercicio de la página.
Escribe `POR_QUE_3` y vuelve a correr. Tu $\phi$ solo puede usar $x_1$ y $x_2$.

Puedes probar varias $\phi$ con los aciertos en entrenamiento. Es
exploración. Más columnas no bajan el mínimo de la pérdida logarítmica de
entrenamiento, pero los aciertos pueden subir o bajar.
Si el ajuste da un aviso, por ejemplo que los datos se separan, aparece
impreso: anótalo, porque la entrega 6 pregunta por la optimización.

Cuando tu $\phi$ sea final, pon `REGISTRAR = True`, vuelve a correr y
solo entonces corre «Revela».

### celda: bloque-3-mira

**Mira.** En cada figura, los círculos son la clase 0 y los triángulos la
clase 1. La línea es la frontera, donde la probabilidad estimada vale 1/2.
Si no aparece línea, el modelo predice la misma clase en todo el cuadro.

Al revelar aparecen los aciertos en el despliegue, la diferencia entre
entrenamiento y despliegue, la moda y el techo de Bayes.
El techo estima el máximo de aciertos posible: lo que logra quien conoce
$\Pr(y=1\mid x)$, medido en la muestra enorme. Los aciertos son una métrica, no un riesgo $R$.

### celda: entrega-3

**Entrega 3.** Lo que registraste, copiado de la salida de «Juega»:

- tu $\phi$, **propuesta exploratoria, todavía sin validar**, y por qué la
  propusiste: qué forma viste en la nube;
- los aciertos en entrenamiento de tu $\phi$, de las cartesianas y de la moda;
- la frontera de tu $\phi$ dibujada, que queda en la salida.

Después de revelar, sin tocar la celda «Juega»:

- los aciertos de tu $\phi$ en el despliegue, contra la moda y contra el techo de Bayes;
- cuánto los exageraban los aciertos de entrenamiento.

### celda: bloque-4-predice

## 4 · Muestra la matriz

**Predice.** ¿Cuántas columnas tendrá la $\Phi$ de tu $\phi$, contando la del 1?

La celda imprime cuatro filas de $\Phi$ de tu $\phi$ registrada, con los
datos de entrenamiento, y los coeficientes $\widehat\beta$ del ajuste.

### celda: bloque-4-mira

**Mira.** Cada fila de $\Phi$ es una observación, ya transformada por tu $\phi$.
Cada columna es una entrada del modelo lineal; la primera es el 1.
Debajo vienen los $\widehat\beta$, uno por columna, con el mismo nombre.

### celda: entrega-4

**Entrega 4.** Copia las cuatro filas de $\Phi$. Di qué es parámetro y qué es
hiperparámetro en tu modelo: los $\widehat\beta$, las columnas que elegiste
y cualquier número que hayas escrito dentro de ellas.
Justifica cada uno con quién lo eligió: el ajuste o tú.

### celda: bloque-5-predice

## 5 · Dónde se usará

**Predice.** Los datos del bloque 2 tienen $x$ entre 0 y 6. Si el modelo se
usa con $x$ entre 6 y 9, ¿cuál de tus dos ajustes empeora más?

La celda usa los dos ajustes que registraste en el bloque 2. Dibuja de 0 a 9 y mide el
error en cada zona con `error_por_zona`. Esa función supone que el uso cae
uniforme en la zona y conoce $f$; tampoco existe en la vida real.

### celda: bloque-5-mira

**Mira.** La línea punteada vertical marca el borde de los datos, $x=6$.
Cada tabla tiene un renglón por zona. `dif2` es el error de la curva contra
$f$, `var_y_dado_x` es el ruido y `R_zona` es su suma.

### celda: entrega-5

**Entrega 5.** Copia `R_zona` dentro y fuera para los dos ajustes.
Explica por qué difieren: qué supone cada $\phi$ sobre lo que pasa donde
no hubo datos. ¿Alguno de tus dos ajustes extrapola bien, o solo interpolan?
Puede que ninguno funcione fuera: dilo con tus cifras.
Qué evaluación correspondería a cada uso es tema de la clase 2: aquí no se pide.

### celda: bloque-6-predice

## 6 · Veredicto

**Predice.** Antes de abrir el proceso, escribe en una línea qué periodo y qué
forma de la nube crees que había.

Ahora sí: corre la celda y, si quieres, abre el código de «Prepara los procesos».
La salida da las fórmulas, el piso del bloque 2 y el techo de Bayes del bloque 3.

### celda: bloque-6-mira

**Mira.** El primer renglón es el proceso de los bloques 2 y 5, con tu
propuesta y el piso $R_{\text{Bayes}}=\sigma_\varepsilon^2$.
Después viene el proceso de la nube. La frontera de Bayes es donde
$\Pr(y=1\mid x)=1/2$: dos curvas, y entre ellas la clase 1 es la más probable.
La celda solo corre si registraste tus propuestas de los bloques 2 y 3.

### celda: entrega-6

**Entrega 6.** En 150 palabras o menos:

- qué aprendiste al proponer $\phi$;
- qué error queda en tus dos modelos. Nómbralo con las cuatro fuentes:
  azar, variables que no medimos, familia equivocada o pocos datos.
  Aparte, ¿la optimización falló?
- **la limitación de tus propuestas:** las elegiste con datos que tocaron
  el ajuste. Sin la muestra enorme, todavía no sabrías si son fiables;
- qué evidencia te falta: datos que no tocaron el ajuste, lo que trae la clase 2.

Si exploraste mirando $R$ o los aciertos del despliegue, decláralo aquí como experimento.

### celda: cierre

Antes de entregar, corre el notebook de arriba abajo y revisa que no haya
celdas con error. Las seis celdas de entrega deben estar llenas.

La rúbrica suma 10 puntos:

| Evidencia | Puntos |
|---|---:|
| Predicciones registradas antes y revisadas con honestidad | 2 |
| Periódica razonada, reconocida como exploratoria y auditada con $R$ | 1.5 |
| $\phi$ de la nube que funciona, contra la moda y con la distancia entre entrenamiento y despliegue | 2 |
| $\Phi$ y parámetro contra hiperparámetro | 1.5 |
| Interpolar contra extrapolar | 1 |
| Veredicto con las cuatro fuentes y la limitación de elegir con entrenamiento | 1 |
| No usaste $R$ para elegir: la propuesta quedó registrada antes de revelar | 1 |

No se premia coincidir con el periodo verdadero. Se premia el razonamiento
y la honestidad sobre lo que todavía no está validado.

Te llevas una pregunta para la clase 2: ¿con qué datos revisarías una
propuesta si no existiera la muestra enorme?
