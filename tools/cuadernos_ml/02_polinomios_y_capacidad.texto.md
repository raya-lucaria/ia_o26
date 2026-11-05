<!--
Tipo: guion_notebook_clase
Etiqueta: codex-red-c1-nb02
Contrato: v5.1 · API ml_lab: 1.3 · Protocolo: p5.2
Plan: clase_1 (sha256 478d429f)
Rama de origen: aprendizaje-maquina-clase-1-b@52a875a
Archivo permitido: tools/cuadernos_ml/02_polinomios_y_capacidad.texto.md

Decisiones del registro que aplican
D-008: sin fechas ni plazos; recorrido autónomo en casa y repaso en clase.
D-009.1: notación del curso; D-009.3: parámetro e hiperparámetro en clase 1;
D-009.5: cifras tomadas del brief y vinculadas con sus bloques de código.
D-013b: API ratificada para las funciones de este notebook.
D-015: notación aditiva admitida según la regla por omisión.
Se aplica la anatomía del notebook, sin frontmatter, badge ni directivas Raya.
Las claves y su orden corresponden al .py; la parte B del bloque 6 es código.

-->

### celda: portada

# Notebook 2 · Polinomios, capacidad y supuestos

Acompaña la página [Polinomios y capacidad](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/polinomios-y-capacidad/). Duración: ~30 min.

Puedes recorrerlo solo en casa, de arriba abajo. Ejecuta primero la celda de
arranque. En cada bloque, anota tu predicción antes de ejecutar «Juega»;
después mueve los controles, mira el resultado y abre «Explicación».

### celda: idea

Agregar potencias permite seguir mejor los datos, pero también sus accidentes.
El grado máximo $N$ limita los polinomios disponibles; el ajuste elige sus
coeficientes $\widehat\beta$. El gorro indica que se estimaron con una muestra.

$L_{\text{ent}}$ es el error cuadrático promedio en entrenamiento y $R$ es el
riesgo: la pérdida cuadrática esperada en la población.
La página [La capacidad como restricción y Brecha de generalización](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/polinomios-y-capacidad/)
conecta la elección del grado con la diferencia entre esos errores:

$$
\min_\beta L_{\text{ent}}(\beta)\quad\text{s.a.}\quad\operatorname{grado}(f_\beta)\le N,
\qquad \mathrm{brecha}=R-L_{\text{ent}}.
$$

### celda: bloque-1-predice

**Predice.** Con grado 3, ¿quién acierta mejor en el borde derecho del intervalo:
Taylor centrado en $x_0=1$ o el ajuste a datos? ¿Y si subes Taylor a grado 9?

Anota si esperas que gane Taylor o mínimos cuadrados, y si el error de Taylor
mejorará al subir el grado. Deja «función» en «recíproca», «centro x₀» en 1
y «datos con ruido» activado. Aquí $x_0$ es el centro de Taylor, no una
observación inicial.

Ejecuta con «grado N» en 3 y después muévelo a 9: el control cambia ambos
polinomios. Compara los errores impresos en el borde $x=3$.
Luego puedes elegir «seno»; allí el centro se recorta al dominio $[0,2]$,
aunque el control permita ir más lejos.

### celda: bloque-1-mira

**Mira.** Los puntos son los datos; la curva verde gruesa es $f$, y la leyenda distingue Taylor de mínimos cuadrados.
La franja gris marca la zona fuera del rango de los datos. En la figura de la
página ocurre al revés: la franja sombreada marca dónde están los datos.
La línea vertical punteada marca $x=2$ para la recíproca con $x_0=1$.
Compara Taylor cerca del centro y en el borde derecho; si sale del panel, lee su error debajo de la gráfica.

### celda: bloque-1-explica

<details><summary>Explicación</summary>

Gana mínimos cuadrados con los valores indicados: en $x=3$, el error de
Taylor es 26.667 y el del ajuste es 0.948. Al subir el grado a 9, el error
de Taylor llega aproximadamente a 1707. Más grado empeoró esa aproximación.

Taylor usa el valor y las derivadas de la función en su centro. Mínimos
cuadrados reparte el error entre los datos al minimizar $L_{\text{ent}}$.
Cuando solo tenemos observaciones, no contamos con las derivadas exactas de $f$.

La observación [El polinomio de Taylor](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/polinomios-y-capacidad/)
explica el límite: para $1/x$ centrada en $x_0=1$, la serie converge solo
en $(0,2)$. A la derecha de $x=2$, subir el grado no resuelve el problema.
Taylor es una aproximación local; su comportamiento aquí no dice que todo
polinomio de grado alto deba fallar.

</details>

### celda: bloque-2-predice

**Predice.** Si subes $N$ de 4 a 12 con $n=20$, ¿$L_{\text{ent}}$ baja o sube? ¿Y $R$? ¿Y si pones $n=200$?

Anota por separado si cada error bajará, subirá o quedará casi igual.
Mantén «ruido σ_ε» en 0.5. Con «datos n» en 20, mueve «grado N» de 4 a 12;
después repite con «datos n» en 200. Compara los valores impresos y las
curvas del panel derecho. Aquí $n$ es el número de datos de entrenamiento.

### celda: bloque-2-mira

**Mira.** Izquierda: los puntos son datos, la curva verde gruesa es $f$ y la otra,
el ajuste. Derecha: círculos para $L_{\text{ent}}$ y discontinua para $R$,
aproximado con observaciones nuevas.
El eje vertical es logarítmico; la brecha está sombreada. La punteada marca el piso; la raya-punto, la media como punto de comparación (*benchmark*).
La estrella señala el menor $R$ medido; el círculo destacado, el grado actual.
Arriba, los rótulos marcan la zona de subajuste, a la izquierda, y la de
sobreajuste, a la derecha. La leyenda va a la derecha del panel.

### celda: bloque-2-explica

<details><summary>Explicación</summary>

$L_{\text{ent}}$ no sube al pasar de grado 4 a 12. Con 20 datos, $R$ aumenta;
con 200, $R$ ya no sube por encima de su valor en grado 5. Con los controles
iniciales, el grado 4 da $L_{\text{ent}}=0.184$, $R=0.444$ y brecha 0.260.
El menor $R$ medido aparece en grado 6; en grado 15 llega aproximadamente a 1537.

La monotonía del mínimo de entrenamiento sí es una ley para familias
anidadas: el polinomio anterior sigue disponible al permitir un grado mayor.
La U de $R$ es de este experimento, no una ley. Aquí los grados altos
incurren en sobreajuste (*overfitting*): mejoran en entrenamiento y empeoran
al recibir observaciones nuevas. Con más datos o poco ruido, la subida puede
ser mucho menos marcada.

La definición [Brecha de generalización y el teorema El entrenamiento miente a tu favor, en promedio](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/polinomios-y-capacidad/)
explican $\mathrm{brecha}=R-L_{\text{ent}}$. Bajo los supuestos del teorema,
su promedio sobre muestras no es negativo; una muestra particular puede
tener brecha negativa. Tampoco hay una ley que obligue a la brecha a crecer
con cada aumento de grado.

El control mueve la desviación estándar del ruido, $\sigma_\varepsilon$.
Su cuadrado, $\sigma_\varepsilon^2$, mide la dispersión cuadrática del ruido
alrededor de su media cero; aquí determina el piso, 0.250 con los valores
iniciales. La estrella de la gráfica marca el grado con menor $R$ medido
en esta muestra.

</details>

### celda: bloque-3-predice

**Predice.** En 200 muestras, ¿cuántas veces elegirá $L_{\text{ent}}$ el grado máximo?

Elige entre ninguna, algunas o todas. Ejecuta con «N_max» en 15 y lee el
conteo bajo los histogramas. Después mueve «N_max» hacia 5 y comprueba si
las elecciones siguen al máximo permitido. Cada muestra tiene 20 datos.

### celda: bloque-3-mira

**Mira.** En el histograma «N_ent», cada barra cuenta las muestras que eligieron ese grado por su error de entrenamiento.
En «N_R», cada barra cuenta las que tuvieron su menor riesgo medido en ese grado; compara la concentración de ambos histogramas.
Tú eliges $N$; el ajuste elige $\widehat\beta$.

### celda: bloque-3-explica

<details><summary>Explicación</summary>

Con «N_max» en 15, entrenamiento elige grado 15 en 200 de 200 muestras.
El histograma de menor $R$ se reparte entre varios grados. Volver a medir
en los mismos datos premia la libertad de ajuste, aunque no beneficie las
predicciones para observaciones nuevas.

Por familias anidadas, el grado máximo siempre alcanza un mínimo de
$L_{\text{ent}}$ entre los candidatos, salvo diferencias de aritmética.
Si hay empates, un grado menor también puede minimizarlo; la monotonía no
obliga a escoger el máximo entre candidatos empatados.

La definición [Parámetro contra hiperparámetro](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/polinomios-y-capacidad/)
distingue los coeficientes $\beta$, que se ajustan dentro de una familia,
del hiperparámetro $N$, que decide qué familia permites. Minimizar
$L_{\text{ent}}$ dentro de cada familia no resuelve cómo elegir entre ellas.

</details>

### celda: bloque-4-predice

**Predice.** ¿Qué baja más $R$: el polinomio de grado 40 o la $\phi$ de dos columnas $(1,1/x)$?

Elige polinomio, recíproca o empate. Conserva «escalar x» activado, deja
«φ» en «polinomio» y lleva «grado N» a 40. Anota $R$ y cambia «φ» a
«(1, 1/x)» para compararlo. Después, con el grado 40, desactiva «escalar x»
y compara $L_{\text{ent}}$ y el aviso con los de antes.

$\phi$ transforma cada observación en las columnas que usa el modelo;
$\Phi$ es la matriz que las reúne para todos los datos. Incluye la columna
constante 1. Si escribimos $\phi_N$, su subíndice numérico indica solo el grado.

### celda: bloque-4-mira

**Mira.** Los puntos son observaciones de la recíproca cerca de cero; la curva muestra el ajuste elegido.
Debajo aparecen cuatro filas de $\Phi$: compara sus dos columnas para $(1,1/x)$ con las 41 del grado 40.
Lee $R$, el piso y el benchmark; sin escalar, vigila también el aviso y cuánto
cambia $L_{\text{ent}}$.
Dos datos, con $y$ mayor que 40, quedan arriba del cuadro.

### celda: bloque-4-explica

<details><summary>Explicación</summary>

Gana $(1,1/x)$ en esta comparación. Con dos columnas alcanza $R=0.250$,
cerca del piso, y estima $\widehat\beta=(2.03,\ 5.00)$.
El polinomio inicial de grado 10 usa 11 columnas y da $R=1.279$.
Con el grado 40 que pediste, $L_{\text{ent}}=0.074$, pero $R=199\,262$:
muy lejos del piso.
La representación recíproca puede expresar la forma del proceso con menos
coeficientes: reduce tanto la capacidad como el error de aproximación.

Como explica [Elegir modelo es elegir supuestos](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/polinomios-y-capacidad/),
la ventaja depende de acertar con la forma del proceso. Elegir columnas
informativas puede ayudar más que agregar potencias. El ajuste sigue siendo
lineal en sus coeficientes, aunque aparezca $1/x$ como columna.

Sin escalar, las potencias producen mal condicionamiento: la aritmética pierde
precisión.
Con el grado 40, $L_{\text{ent}}$ pasa de 0.074 con escala a 293.1 sin escalar;
con el grado 25, de 0.111 a 8.59.
La familia es la misma, así que esa subida no refuta la monotonía del mínimo
exacto entre familias anidadas: el cálculo ya no lo alcanza.
El mayor coeficiente no sirve de alarma: con escala, en grado 40 llega a
$3.0\times10^{11}$, porque el ajuste sobreajusta.
Sin escalar, el cálculo descarta direcciones casi repetidas y deja los
coeficientes pequeños.
El caso 4 de la galería muestra esta misma subida sin escalar, con 100 datos y
grados 10 y 25.

Escalar ayuda, pero tampoco garantiza la monotonía: con «escalar x» activado,
$L_{\text{ent}}$ pasa de 0.0763 en grado 35 a 0.0764 en grado 36.
Esos dos grados se prueban en este bloque.

</details>

### celda: bloque-5-predice

**Predice.** Con el seno y grado 7, ¿el error fuera de la zona de datos será mayor o menor que adentro?

Anota mayor, menor o parecido. Cambia «proceso» de «entregas» a «seno»,
deja «grado N» en 7 y «zona de uso (× el rango)» en 1.5. Compara
«dentro» y «fuera» en `R_zona`. Mueve después la zona de uso para ver
hasta dónde estás pidiendo predicciones.

Para explorar «recursivo», baja «grado N» a 1 y compara con «agregar la
columna del tiempo anterior» apagado y encendido. Ese interruptor solo
cuenta en el proceso recursivo; allí la comparación es con los pasos futuros.

### celda: bloque-5-mira

**Mira.** Con el seno, los puntos son datos; compara el polinomio con la curva verde de $f$ y lee `R_zona` para la franja gris exterior.
Con «recursivo», el eje horizontal ordena los pasos: 60 de entrenamiento como
puntos llenos y 19 siguientes como círculos huecos; la línea predice a un paso.
Lo impreso da primero $L_{\text{ent}}$ sobre la serie dibujada y después el
error esperado, aproximado con series nuevas del mismo proceso: dentro
(pasos 0 a 59) y a un paso en el futuro (pasos 60 a 79).

### celda: bloque-5-explica

<details><summary>Explicación</summary>

El error del seno es mayor fuera: con los controles indicados, pasa de
0.097 dentro a 609 fuera. El intervalo de uso se extiende de 2 a 3;
el ajuste no recibió datos en esa extensión.
Cada `R_zona` aproxima el riesgo si las entradas se distribuyeran uniformemente
en esa zona, incluido el ruido; no es su contribución al riesgo del despliegue
actual. En «entregas», con grado 7,
pasa de 1.824 dentro a más de un millón fuera al extender de 6 a 9 km.

La observación [Interpolar, extrapolar y el riesgo](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/polinomios-y-capacidad/)
explica por qué un buen ajuste dentro del intervalo no garantiza buenas
predicciones fuera. Allí los datos no restringen directamente al polinomio.
La tabla separa errores por zona; ampliar la ventana no cambia por sí solo
la población de despliegue que define $R$.

El recursivo muestra además una variable ausente: el tiempo de entrega
anterior observado. Con grado 1 y sin esa columna, los errores esperados,
promediados sobre series nuevas del mismo proceso, son aproximadamente 5.5
dentro y 36.4 en el futuro. Sobre la serie dibujada, $L_{\text{ent}}$ es 6.55.
Al agregarla quedan cerca de 1.05 en ambos, frente al piso 1
(0.90 sobre la serie dibujada).

Estas predicciones son **a un paso**: reciben el valor anterior observado,
no una predicción anterior encadenada. A varios pasos el error puede
acumularse. Con grado 7, aun agregando esa columna, la parte polinómica en
$x$ vuelve a extrapolar mal. La separación de series se estudia en la clase 5.

</details>

### celda: bloque-6-predice

**Predice.** Promediando sobre las 256 funciones, ¿qué regla acierta más fuera
de la muestra: el vecino más cercano o «siempre 1»?

Elige vecino, siempre 1 o empate. Ejecuta «Juega» y cambia «regla» entre
«vecino más cercano» y «siempre 1»; compara el promedio exacto impreso.
Después selecciona «mayoría (empate → 1)». Ejecuta también la siguiente
celda, «Mira: cada modelo gana en su proceso», para obtener la parte B.

### celda: bloque-6-mira

**Mira.** El vecino copia la etiqueta de la entrada de entrenamiento que
difiere en menos bits; con empate, la de menor número.
En A, cada punto de la curva resume los aciertos fuera de la muestra para un
grupo de funciones de igual rugosidad.
La referencia horizontal marca $1/2$; compara la curva por grupos con el promedio exacto impreso para todas las funciones.
En B, cada fila de la tabla es un proceso y cada columna, un modelo: busca el menor $R$ dentro de cada fila.

### celda: bloque-6-explica

<details><summary>Explicación</summary>

Empatan exactamente: cada regla promedia $1/2$ de aciertos fuera de la
muestra sobre las 256 funciones. «Siempre 1» queda en 0.5 en cada grupo.
El vecino pasa de 1.0 en rugosidad 0 a 0.0 en rugosidad 12;
la mayoría también favorece lo suave y falla en lo rugoso.

El promedio global pondera cada grupo por su número de funciones.
No basta promediar las alturas de la curva dando el mismo peso a todos
los grupos. Al considerar todas las funciones por igual, la ventaja en
unas se compensa con la desventaja en otras. Es el alcance del teorema
[No free lunch (Wolpert, 1996)](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/polinomios-y-capacidad/).

En B, el polinomio de grado 3 gana en el proceso suave: $R=1.046$ frente
a 1.486 de vecinos. En el periódico ganan los vecinos: 0.314 frente a
2.027 del polinomio. Esta parte ilustra especialización y **no demuestra
el teorema**. Tampoco son aciertos: B compara riesgos con pérdida cuadrática.
Elegir un modelo supone apostar por ciertas formas del proceso.

</details>

### celda: taller-intro

**Taller.** Ejecuta el ejemplo activo: usa 20 datos de la recíproca y
`ml.taller(datos, clase=1, phi=ml.polinomio(4), N_max=15)`.
Mira la nube con $f$, la curva de capacidad y la matriz $\Phi$ de la
representación elegida, junto con sus errores y su piso.
El taller aproxima $R$ con otra muestra grande, así que puede diferir en el
segundo decimal del que da el bloque 2.

Para comparar con $(1,1/x)$, comenta la llamada activa y descomenta la
línea con `phi=ml.columnas("1/x")`. Para el seno, descomenta todas las
líneas de su definición de `datos` y la llamada con `ml.periodicas`.
La constante 1 se incluye también en esa representación.

El último ejemplo permite cambiar la expresión de una $f$ propia.
Descomenta su definición completa y coloca después la llamada a `ml.taller`
que quieras usar. Se usa la última asignación a `datos` anterior a la
llamada. Cambia una representación a la vez y compara entrenamiento,
riesgo, piso y benchmark.

### celda: galeria-intro

**Galería.** Pulsa los botones de los casos 3, 4, 5 y 23. En cada uno,
lee la pregunta y anota una predicción antes de abrir «¿Qué se ve?».
Usa la gráfica y los valores que aparezcan para justificar tu respuesta;
después compárala con la explicación del botón.

### celda: ejercicio-fuerza-bruta

**Ejercicio.** Si más potencias bajan $L_{\text{ent}}$, ¿por qué no poner mil?

Responde usando la curva de capacidad del bloque 2, el interruptor
«escalar x» del bloque 4 y el caso 23 de la galería. Distingue el
problema de predecir observaciones nuevas del problema de calcular el ajuste.

**Pista:** ¿qué garantiza un error pequeño en los datos usados para ajustar,
y qué puedes concluir si el cálculo pierde precisión?

### celda: ejercicio-fuerza-bruta-respuesta

<details><summary>Explicación</summary>

Bajar $L_{\text{ent}}$ no garantiza bajar $R$. En el bloque 2, el grado 15
tiene un riesgo cercano a 1537: la brecha crece aunque mejore entrenamiento.
Ese crecimiento pertenece al experimento; no es una ley para toda muestra.

Además, con potencias sin escalar, el mal condicionamiento deteriora la
precisión del cálculo. Por eso un aumento observado de $L_{\text{ent}}$
puede ser un problema de aritmética. En el caso 23, con más coeficientes
que datos, el ajuste interpola: reproduce los datos de entrenamiento.
Eso tampoco asegura acertar en observaciones nuevas. Agregar potencias
no resuelve por sí solo ninguno de estos problemas.

</details>

### celda: ejercicio-grado-con-entrenamiento

**Ejercicio.** Deja que $L_{\text{ent}}$ elija $N$ en el bloque 3.
Mueve «N_max» de 15 a 5, anota qué grado elige y explica por qué
su elección sigue al máximo permitido. Distingue lo que eliges tú de
lo que decide el ajuste.

**Pista:** ¿deja de estar disponible el mejor polinomio anterior cuando
permites un grado mayor?

### celda: ejercicio-grado-con-entrenamiento-respuesta

<details><summary>Explicación</summary>

Entrenamiento elige el máximo permitido en este experimento. Las familias
son anidadas: permitir otro grado conserva los polinomios anteriores y
agrega posibilidades. Por eso el mínimo de $L_{\text{ent}}$ no sube;
si hubiera empates, el máximo no tendría que ser el único minimizador.

Tú fijas el hiperparámetro $N$ y el ajuste estima $\widehat\beta$.
Para elegir el grado con datos reales usaremos datos que no tocaron el
ajuste; la clase 2 presenta cómo hacerlo. Aquí podemos comparar con $R$
porque conocemos el proceso que produjo los datos.

</details>

### celda: cierre

Te llevas: aproximar no es aprender; la capacidad se elige; los supuestos deciden.

En este laboratorio podíamos mirar detrás del escenario. Con datos reales no podemos. ¿Cómo medimos el error que importa?
