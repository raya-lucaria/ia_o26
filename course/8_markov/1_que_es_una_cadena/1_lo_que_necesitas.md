---
id: mkv-lo-que-necesitas
title: "Lo que necesitas de probabilidad"
nav_title: "Lo que necesitas"
summary: "Experimento, evento, probabilidad condicional, variable aleatoria, regla del producto, independencia, independencia condicional, probabilidad total y el promedio de muchas repeticiones, contados en una frase del Quijote."
status: ready
estimated_time: 33m
tags: [markov]
---

# Lo que necesitas de probabilidad

**¿Qué tanto cambia la probabilidad de una vocal si ya sabes cuál fue la letra anterior?**

Al terminar tendrás:

- **Probabilidades contadas en una frase:** la de un evento, la conjunta y la condicional, cada una con su experimento declarado.
- **La variable aleatoria $S_t$,** su distribución y la regla del producto encadenada.
- **Independencia e independencia condicional,** con un contraejemplo en la frase y un supuesto medido en el *Quijote*.
- **La probabilidad total** con una partición, y por qué el promedio de muchas repeticiones independientes se acerca a una probabilidad.

## Lo que traes

- **Una probabilidad dentro de un modelo.** En [[cuando-decide-un-dado|Cuando decide un dado]], ${\Pr(a\mid s)}$ daba la probabilidad de cada resultado del dado en el estado $s$, y esas probabilidades sumaban 1. Aquí construimos esa notación desde cero.
- **Un promedio de muchas repeticiones.** En [[simular-en-vez-de-evaluar|Simular partidas]], Monte Carlo plano promediaba el pago de muchas partidas al azar. Aquí verás por qué un promedio así se acerca a una probabilidad.

> **Esta página va sin simulación: es de conceptos.** Cada idea se cuenta a mano en una frase del *Quijote*, «Con la iglesia hemos dado, Sancho», y después se dice en general.

---

## 1 · Montar un experimento con la frase

**Piensa: ¿qué significa «la probabilidad de que la siguiente letra sea vocal»?**

Nada, hasta que digas cómo se elige la letra. Toda probabilidad es de un **experimento**: un procedimiento con azar y con resultados posibles bien definidos.

Primero prepara la frase. Pasa todo a minúsculas, quita espacios y signos, y cambia cada letra por su clase: V si es vocal (a, e, i, o, u) y C si es consonante. La «y» contaría como consonante; aquí no aparece.

```text
conlaiglesiahemosdadosancho
CVCCVVCCVCVVCVCVCCVCVCVCCCV
```

Son 27 letras. Numera sus posiciones desde 0. La última, la «o» de «Sancho», no tiene letra siguiente.

**El experimento.** Elige al azar una de las 26 posiciones que tienen siguiente, todas con la misma probabilidad. Mira la letra elegida, la **actual**, y la que le sigue.

- **Evento $A$:** la siguiente es vocal.
- **Evento $B$:** la actual es vocal.

**Contar $A$.** La siguiente es vocal cuando la posición de al lado tiene V. La frase tiene 12 vocales, y ninguna está en la posición 0, así que 12 de las 26 posiciones cumplen $A$:

$$
\Pr(A)=\frac{12}{26}\approx0.462.
$$

::: definition {#mkv-c1-experimento title="Experimento, evento y probabilidad"}
**Qué es.** Un experimento es un procedimiento con azar. Un evento es un conjunto de sus resultados. $\Pr(A)$, «probabilidad de $A$», es un número entre 0 y 1 que dice qué tan probable es que ocurra $A$.

**Cómo se calcula.** Si todos los resultados son igual de probables, $\Pr(A)$ es el número de resultados en $A$ entre el total.

**Qué significa.** Como la posición se sortea con probabilidades iguales, $\Pr(A)$ es la frecuencia de $A$ en la frase. Es una probabilidad exacta de este sorteo, no una aproximación.

**Qué no es.** No es una afirmación sobre el español. Cuando un texto sirva como datos para un modelo, sus frecuencias serán **estimaciones** y llevarán gorro: $\widehat{\Pr}(A)$.
:::

::: exercise {#mkv-c1-ej-actual-vocal title="Cuenta el evento B"}
¿Cuánto vale $\Pr(B)$, la probabilidad de que la letra actual sea vocal?
:::

::: hint {#mkv-c1-pista-actual-vocal of="mkv-c1-ej-actual-vocal" title="Dónde puede caer el sorteo"}
¿Cuántas posiciones entran al sorteo, y en cuántas de ellas la letra actual es vocal?
:::

::: answer {#mkv-c1-resp-actual-vocal of="mkv-c1-ej-actual-vocal"}
**${\Pr(B)=11/26}$.** Hay 12 vocales, pero la «o» final no tiene siguiente y no entra al sorteo. Quedan 11 de las 26 posiciones.
:::

Ya sabes cuántas posiciones tienen vocal actual. ¿Cambia la probabilidad de $A$ si solo miras esas?

---

## 2 · Calcular una probabilidad condicional

**Piensa: si te dicen que la letra actual es vocal, ¿sigue valiendo $12/26$ para $A$?**

No: saber $B$ reduce los casos posibles. Ahora solo cuentan las 11 posiciones con vocal actual. Para verlo, cruza las dos letras de cada posición:

::: table {#mkv-c1-tabla-experimento title="Las 26 posiciones, por letra actual y siguiente"}
| Actual (total) | Siguiente V | Siguiente C |
|---|---:|---:|
| V (11) | 2 | 9 |
| C (15) | 10 | 5 |
:::

Entre paréntesis, el total de cada renglón: 11 posiciones con vocal actual y 15 con consonante.

Solo 2 posiciones tienen vocal actual y vocal siguiente: la de «ai» y la de «ia». El evento «ocurren $A$ y $B$» se escribe ${A\cap B}$, y su **probabilidad conjunta** es ${\Pr(A\cap B)=2/26}$. Dentro de las 11 posiciones de $B$, esas 2 dan la proporción $2/11$.

::: definition {#mkv-c1-prob-condicional title="Probabilidad condicional"}
**Qué es.** ${\Pr(A\mid B)}$, «probabilidad de $A$ dado $B$», es la probabilidad de $A$ cuando ya sabes que ocurrió $B$.

**Cómo se calcula.**

$$
\Pr(A\mid B)=\frac{\Pr(A\cap B)}{\Pr(B)},
\qquad \Pr(B)>0.
$$

**Qué significa.** Te quedas solo con los resultados de $B$ y mides qué fracción de ellos está en $A$. En la frase, ${\Pr(A\mid B)=\dfrac{2/26}{11/26}=\dfrac{2}{11}}$.

**Qué no es.** No es ${\Pr(B\mid A)}$. Ahí te quedas con las 12 posiciones de $A$, no con las 11 de $B$, y el cociente cambia.
:::

**La condición ${\Pr(B)>0}$ no es un detalle.** Si $B$ fuera «la actual es una k», no habría ninguna posición que mirar: la frase no tiene «k», y la condicional no se define.

::: exercise {#mkv-c1-ej-tras-consonante title="Condiciona a la consonante"}
Usa la definición, no solo la tabla: ¿cuánto vale la probabilidad de que la siguiente sea vocal si la actual es consonante?
:::

::: hint {#mkv-c1-pista-tras-consonante of="mkv-c1-ej-tras-consonante" title="Dos probabilidades, un cociente"}
¿Cuánto valen la probabilidad conjunta y la de «actual consonante», cada una sobre 26?
:::

::: answer {#mkv-c1-resp-tras-consonante of="mkv-c1-ej-tras-consonante"}
**Vale ${10/15=2/3}$.** La conjunta es $10/26$ y la del condicionante, $15/26$; su cociente es $10/15$. Tras consonante, la vocal es mucho más probable que tras vocal.
:::

«Actual», «siguiente», «la de antes»: nombrar cada letra con palabras empieza a estorbar. ¿Cómo se nombran?

---

## 3 · Nombrar las letras con variables aleatorias

**Piensa: ¿cómo escribes «la actual es vocal y la siguiente también» sin inventar un evento para cada caso?**

Con un nombre para cada letra que todavía depende del sorteo. $S_0$ es la clase de la letra sorteada y $S_1$, la de la que le sigue. En general, $S_t$ es la clase de la letra que está $t$ pasos después de la sorteada, con ${t=0,1,2,\dots}$

- **Los eventos se vuelven igualdades.** $B$ es ${\{S_0=V\}}$ y $A$ es ${\{S_1=V\}}$.
- **La coma se lee «y».** ${\Pr(S_0=V,\ S_1=V)}$ es ${\Pr(A\cap B)=2/26}$.
- **La condicional se escribe igual.** ${\Pr(S_1=V\mid S_0=V)=2/11}$.

::: definition {#mkv-c1-variable-aleatoria title="Variable aleatoria y distribución"}
**Qué es.** Una variable aleatoria asigna un valor a cada resultado del experimento: aquí, a cada posición sorteada le asigna V o C. Va con mayúscula, $S_t$. Los valores que puede tomar, como V o C, no son aleatorios.

**Cómo se calcula.** Su **distribución** da la probabilidad de cada valor posible: un vector de números entre 0 y 1 que suma 1. Para $S_0$, en el orden V, C:

$$
\bigl(\Pr(S_0=V),\ \Pr(S_0=C)\bigr)=\Bigl(\frac{11}{26},\ \frac{15}{26}\Bigr).
$$

**Qué significa.** Antes del sorteo no sabes qué valor tomará $S_0$, y la distribución dice cómo se reparte. Después del sorteo conoces el valor que tomó, como C: $S_0$ sigue siendo la variable, y C es el valor observado.

**Qué no es.** $S_t$ no es la letra fija de la posición $t$ de la frase. Es la letra $t$ pasos **después de la sorteada**; por eso es aleatoria.
:::

**La posición debe existir.** Para hablar de $S_t$, el experimento debe sortear posiciones con al menos $t$ letras siguientes. El sorteo entre 26 posiciones garantiza $S_0$ y $S_1$.

**Lo mismo con cualquier alfabeto.** Nada de lo anterior usa que haya solo dos clases. Si cada letra toma valores de un conjunto de cualquier tamaño, con $a$ y $b$ dos de ellos, la condicional se cuenta igual, siempre que haya alguna posición con $a$:

$$
\begin{aligned}
&\Pr(S_1=b\mid S_0=a)\\
&\quad=\frac{\text{posiciones con }a\text{ y luego }b}{\text{posiciones con }a\text{ y siguiente}}.
\end{aligned}
$$

En Python, la misma cuenta sirve para cualquier texto ya convertido en clases o en letras:

```python
from fractions import Fraction

def condicional(clases, a, b):
    """Pr(S_1 = b | S_0 = a)."""
    # con a y con siguiente
    con_a = 0
    # de ellas, seguidas de b
    a_luego_b = 0
    # solo las que tienen siguiente
    for j in range(len(clases)-1):
        if clases[j] == a:
            con_a += 1
            if clases[j + 1] == b:
                a_luego_b += 1
    if con_a == 0:
        # Pr(S_0=a)=0: indefinida
        return None
    return Fraction(a_luego_b, con_a)

frase = "CVCCVVCCVCVVCVCVCCVCVCVCCCV"
print(condicional(frase, "V", "V"))   # 2/11
```

::: exercise {#mkv-c1-ej-distribucion-tras-v title="Escribe una distribución condicional"}
Escribe la distribución de $S_1$ dado ${S_0=V}$, en el orden V, C. ¿Suma 1?
:::

::: hint {#mkv-c1-pista-distribucion-tras-v of="mkv-c1-ej-distribucion-tras-v" title="El otro valor"}
De las 11 posiciones con vocal actual, ¿cuántas van seguidas de consonante?
:::

::: answer {#mkv-c1-resp-distribucion-tras-v of="mkv-c1-ej-distribucion-tras-v"}
**Es $(2/11,\ 9/11)$.** Suma ${11/11=1}$: dado ${S_0=V}$, la siguiente tiene que ser V o C.
:::

Con un nombre para cada letra ya puedes preguntar por tres seguidas. ¿Cómo se calcula la probabilidad de un tramo como C, V, C?

---

## 4 · Encadenar la regla del producto

**Piensa: si conoces una condicional, ¿cómo recuperas la probabilidad de que dos cosas pasen juntas?**

Despejas la definición: ${\Pr(A\cap B)=\Pr(B)\,\Pr(A\mid B)}$. En la frase, ${\frac{11}{26}\cdot\frac{2}{11}=\frac{2}{26}}$: lo mismo que contar las posiciones con V seguida de V.

**Con tres letras, se encadena.** Cambia el experimento: sortea una de las 25 posiciones que tienen **dos** letras siguientes. Así $S_0$, $S_1$ y $S_2$ existen siempre. El tramo C, V, C se calcula letra por letra:

$$
\begin{aligned}
\Pr(S_0=C,\ S_1=V,\ S_2=C)
&=\tfrac{14}{25}\cdot\tfrac{9}{14}\cdot\tfrac{7}{9}\\
&=\tfrac{7}{25}.
\end{aligned}
$$

- **Primer factor.** 14 de las 25 posiciones tienen C: ${\Pr(S_0=C)=14/25}$.
- **Segundo factor.** De esas 14, 9 van seguidas de V: ${\Pr(S_1=V\mid S_0=C)=9/14}$.
- **Tercer factor.** De esas 9, 7 siguen con C: ${\Pr(S_2=C\mid S_0=C,\ S_1=V)=7/9}$.

Contar directamente da lo mismo: 7 de las 25 posiciones empiezan un tramo C, V, C.

En general se escribe con el símbolo $\prod$, que indica multiplicar los factores mientras el índice $j$ recorre los pasos.

::: theorem {#mkv-c1-teo-producto title="Regla del producto, encadenada"}
Para valores $a_0,\dots,a_t$ de $S_0,\dots,S_t$:

$$
\begin{aligned}
&\Pr(S_0=a_0,\dots,S_t=a_t)=\Pr(S_0=a_0)\,\times\\
&\prod_{j=0}^{t-1}\Pr(S_{j+1}=a_{j+1}\mid S_0=a_0,\dots,S_j=a_j).
\end{aligned}
$$

Vale si ${\Pr(S_0=a_0,\dots,S_{t-1}=a_{t-1})>0}$, para que cada condicional esté definida. Si esa probabilidad es 0, la conjunta también vale 0.
:::

Cada factor pregunta por la siguiente letra **dado todo lo anterior**, así que la condición crece: el último condiciona en $t$ letras.

::: exercise {#mkv-c1-ej-catorce title="Explica el primer factor"}
En la sección 3, ${\Pr(S_0=C)=15/26}$. ¿Por qué aquí el primer factor es $14/25$?
:::

::: hint {#mkv-c1-pista-catorce of="mkv-c1-ej-catorce" title="Compara los dos sorteos"}
¿Qué posición con C dejó de entrar al sorteo?
:::

::: answer {#mkv-c1-resp-catorce of="mkv-c1-ej-catorce"}
**Porque cambió el experimento.** La posición 25, la «h» de «Sancho», tiene una sola letra siguiente y sale del sorteo. Quedan 14 consonantes entre 25 posiciones. Una probabilidad siempre es de un experimento.
:::

Condicionar en todo lo anterior es mucho que recordar. ¿Hay casos en que lo anterior no cambia nada?

---

## 5 · Probar la independencia

**Piensa: ¿hay eventos para los que saber uno no cambia nada del otro?**

Sí, y se llaman independientes: dos tiradas de un dado justo, por ejemplo. Si $A$ no dependiera de $B$, la regla del producto perdería la condición y daría ${\Pr(A\cap B)=\Pr(A)\Pr(B)}$. En la frase, compara los dos lados:

$$
\begin{aligned}
\Pr(A)\Pr(B)&=\tfrac{12}{26}\cdot\tfrac{11}{26}\approx0.195,\\
\Pr(A\cap B)&=\tfrac{2}{26}\approx0.077.
\end{aligned}
$$

**No coinciden.** Juntas ocurren menos de la mitad de lo que darían sin dependencia. Con la condicional se ve igual: ${\Pr(A\mid B)=2/11}$, muy por debajo de ${\Pr(A)=12/26}$. En esta frase, otra vocal tras vocal es rara: 2 de 11 veces.

::: definition {#mkv-c1-independencia-simple title="Independencia"}
**Qué es.** $A$ y $B$ son independientes si ${\Pr(A\cap B)=\Pr(A)\,\Pr(B)}$.

**Cómo se calcula.** Calcula los dos lados y compáralos. Si ${\Pr(B)>0}$, equivale a ${\Pr(A\mid B)=\Pr(A)}$: saber $B$ no mueve la probabilidad de $A$. En la frase, $A$ y $B$ no son independientes.

**Qué significa.** $S_0$ y $S_1$ son independientes si esto vale para todo par de valores:

$$
\begin{aligned}
&\Pr(S_0=a,\ S_1=b)\\
&\quad=\Pr(S_0=a)\,\Pr(S_1=b).
\end{aligned}
$$

**Qué no es.** No es «no pueden ocurrir juntos». Si ${A\cap B}$ es imposible y los dos eventos tienen probabilidad positiva, la conjunta vale 0 y el producto no: no son independientes.
:::

> [!WARNING]
> **Leer «dependen» como «una causa la otra».** Que $S_1$ dependa de $S_0$ **solo dice que saber una cambia la probabilidad de la otra**. No dice que una vocal provoque una consonante.

::: exercise {#mkv-c1-ej-independiente-c title="Prueba con la consonante"}
¿Son independientes $A$ y el evento ${\{S_0=C\}}$? Usa la forma con la condicional.
:::

::: hint {#mkv-c1-pista-independiente-c of="mkv-c1-ej-independiente-c" title="Ya la calculaste"}
¿Qué condicional obtuviste en el ejercicio de la sección 2?
:::

::: answer {#mkv-c1-resp-independiente-c of="mkv-c1-ej-independiente-c"}
**No lo son.** Como ${\Pr(S_0=C)=15/26>0}$, se puede comparar: ${\Pr(A\mid S_0=C)=10/15}$, más de la mitad, y ${\Pr(A)=12/26}$, menos de la mitad. Saber que la actual es consonante sube la probabilidad de vocal.
:::

Las letras seguidas no son independientes. ¿Y la letra de hace dos? Quizá no agregue nada **si ya sabes la anterior**.

---

## 6 · Suponer independencia condicional

**Piensa: si ya sabes la letra anterior, ¿saber también la de hace dos cambia la probabilidad de la siguiente?**

Depende del texto, y una frase de 27 letras es muy poco para decidirlo. Por eso medimos en el libro completo.

**Medido en el *Quijote*.** Tomamos el texto entero con la misma normalización V/C y contamos tras cada consonante. Aquí el texto se usa como datos, así que sus frecuencias llevan gorro: $\widehat{\Pr}$.

**El experimento.** Sortea una posición del libro que tenga al menos dos letras después, y mira tres letras seguidas. Para no atarnos a un lugar, la sorteada (la de hace dos) es $S_{t-1}$, la anterior es $S_t$ y la siguiente, $S_{t+1}$.

::: table {#mkv-c1-tabla-dos-atras title="Tras una consonante en el Quijote: ¿importa la letra de hace dos?"}
| La de hace dos | La anterior | Siguiente vocal |
|---|---|---:|
| cualquiera | C | 0.710 |
| V | C | 0.624 |
| C | C | 0.922 |
:::

La primera fila es ${\widehat{\Pr}(S_{t+1}=V\mid S_t=C)}$. Las otras dos agregan la letra de hace dos, $S_{t-1}$; los tres contextos tienen observaciones en el libro. Si la de hace dos no agregara nada, las tres filas dirían lo mismo.

**No dicen lo mismo.** Tras dos consonantes seguidas, la vocal sale 0.922: en el *Quijote*, tres consonantes seguidas son raras. En este texto, **la letra de hace dos sí agrega información**.

La propiedad que aquí falla tiene nombre:

::: definition {#mkv-c1-independencia-condicional title="Independencia condicional"}
**Qué es.** $A$ y $D$ son independientes dado $B$ si, una vez que sabes $B$, saber también $D$ no cambia nada de $A$.

**Cómo se calcula.** Si ${\Pr(D\cap B)>0}$, la condición es

$$
\Pr(A\mid D,\ B)=\Pr(A\mid B).
$$

La coma, otra vez, es «y»: ${\Pr(A\mid D,\ B)}$ condiciona a que ocurran $D$ y $B$.

**Qué significa.** Con letras: $A$ es «la siguiente es vocal», $B$ dice cuál es la anterior y $D$, cuál es la de hace dos. La de hace dos no agrega nada **si ya sabes la anterior**.

**Qué no es.** No es independencia. Dos eventos pueden depender uno del otro y ser independientes dado un tercero, y también al revés.
:::

**En un modelo, es un supuesto.** En el *Quijote* no se cumple exactamente. Un modelo que solo mira la letra anterior supone que la de hace dos no agrega nada. Es una simplificación del modelo, no un hecho del español: sirve si lo que pierde es poco.

::: exercise {#mkv-c1-ej-supuesto-exacto title="Imagina el supuesto cumplido"}
Si el *Quijote* cumpliera exactamente el supuesto, ¿cuánto valdrían las filas de V y de C?
:::

::: hint {#mkv-c1-pista-supuesto-exacto of="mkv-c1-ej-supuesto-exacto" title="Lee la fórmula"}
En ${\Pr(A\mid D,\ B)=\Pr(A\mid B)}$, ¿qué fila de la tabla es el lado derecho?
:::

::: answer {#mkv-c1-resp-supuesto-exacto of="mkv-c1-ej-supuesto-exacto"}
**Las dos valdrían 0.710,** igual que la primera fila. Que valgan 0.624 y 0.922 dice que, en este texto, la de hace dos sí agrega información.
:::

La primera fila mezcla las otras dos. ¿Cómo se combinan varios casos en una sola probabilidad?

---

## 7 · Sumar por casos con la probabilidad total

**Piensa: si conoces la probabilidad de vocal tras V y tras C, ¿puedes recuperar la de vocal sin condición?**

Sí, si también sabes qué tan frecuente es cada caso. Las 26 posiciones de la frase se parten en dos grupos: actual V y actual C. Cada posición está en exactamente uno. Pesa cada condicional por la probabilidad de su caso y suma:

$$
\begin{aligned}
\Pr(A)
&=\tfrac{2}{11}\cdot\tfrac{11}{26}+\tfrac{10}{15}\cdot\tfrac{15}{26}\\
&=\tfrac{2+10}{26}=\tfrac{12}{26}.
\end{aligned}
$$

Es lo que dice la tabla de la sección 2: 2 vocales siguientes tras V y 10 tras C.

::: definition {#mkv-c1-particion title="Partición"}
**Qué es.** Una partición es una lista de casos $B_1,B_2,\dots$ que no se enciman y que, entre todos, cubren todos los resultados.

**Cómo se calcula.** Revisa que cada resultado caiga en exactamente un caso. Los valores de una variable siempre forman una partición: aquí, ${\{S_0=V\}}$ y ${\{S_0=C\}}$.

**Qué significa.** Puedes resolver el problema caso por caso y después juntar.
:::

::: theorem {#mkv-c1-teo-total title="Probabilidad total"}
Si $B_1,B_2,\dots$ forman una partición,

$$
\Pr(A)=\sum_j\Pr(A\mid B_j)\,\Pr(B_j).
$$

Se suman solo los casos con ${\Pr(B_j)>0}$. Los de probabilidad 0 se omiten: su condicional no está definida y no aportan nada.
:::

El símbolo $\sum$ indica sumar un término por caso. **Con cualquier alfabeto,** la partición tiene un caso por valor de $S_0$:

$$
\begin{aligned}
&\Pr(S_1=b)\\
&\quad=\sum_a\Pr(S_1=b\mid S_0=a)\,\Pr(S_0=a).
\end{aligned}
$$

También aquí se omiten los valores $a$ con ${\Pr(S_0=a)=0}$.

**Lo que no generaliza del juguete.** Con dos clases, «no V» es un solo caso, C, y una distribución se fija con un número. Con más valores, «no V» se parte en varios casos, cada uno con su condicional, y hacen falta tantos números como valores menos uno.

La misma regla explica la tabla de la sección 6. El 0.710 mezcla los casos «la de hace dos fue V» (0.624) y «fue C» (0.922), cada uno con su peso: tras una C, la de hace dos fue V en unas 7 de cada 10 posiciones. Por eso queda entre los dos, más cerca de 0.624.

::: exercise {#mkv-c1-ej-no-particion title="Revisa una partición"}
¿Forman los eventos $A$ y $B$ una partición de las 26 posiciones?
:::

::: hint {#mkv-c1-pista-no-particion of="mkv-c1-ej-no-particion" title="Dos revisiones"}
¿Hay posiciones que estén en los dos? ¿Hay posiciones que no estén en ninguno?
:::

::: answer {#mkv-c1-resp-no-particion of="mkv-c1-ej-no-particion"}
**No.** Las 2 posiciones con V seguida de V están en los dos, y las 5 con C seguida de C no están en ninguno.
:::

Todo esto salió de contar en una sola frase. ¿Por qué contar en muchos datos debería acercarte a una probabilidad?

---

## 8 · Repetir muchas veces y promediar

**Piensa: si repites el sorteo muchas veces, ¿qué fracción de las veces será vocal la siguiente?**

Cerca de ${\Pr(A)=12/26\approx0.462}$, si las repeticiones son muchas e independientes. Cada repetición sortea de nuevo entre las 26 posiciones, sin mirar las anteriores. Llama $n$ al número de repeticiones.

::: theorem {#mkv-c1-teo-promedio title="El promedio de muchas repeticiones"}
Repite $n$ veces el mismo experimento, con repeticiones independientes. Con probabilidad 1, la fracción de veces en que ocurre $A$ se acerca a $\Pr(A)$ cuando $n$ crece.
:::

Es la ley de los grandes números (*law of large numbers*), en la forma que necesitamos. El azar está en los sorteos repetidos, y el valor al que se acerca es $12/26$.

- **Se acerca, no coincide.** Con ${n=26}$ repeticiones, $A$ no tiene por qué salir exactamente 12 veces.
- **La condición importa.** Si sorteas una sola vez y copias el resultado $n$ veces, las repeticiones no son independientes: la fracción vale 0 o 1 para siempre.
- **Es lo que hacía Monte Carlo plano.** Con partidas independientes y la misma regla al azar, su promedio se acercaba al pago esperado bajo esa regla.

::: exercise {#mkv-c1-ej-repetir title="Elige la repetición válida"}
¿Cuál de estas formas de repetir cumple la condición del teorema?

1. **Sortear de nuevo.** Sortear $n$ veces entre las 26 posiciones.
2. **Leer de corrido.** Sortear una posición y tomar las que le siguen en la frase.
:::

::: hint {#mkv-c1-pista-repetir of="mkv-c1-ej-repetir" title="Mira la segunda repetición"}
En la forma 2, ¿saber la primera posición te dice algo de la segunda?
:::

::: answer {#mkv-c1-resp-repetir of="mkv-c1-ej-repetir"}
**Solo la primera.** En la segunda, la primera posición fija todas las demás: no son independientes. Además, las letras seguidas dependen entre sí, como viste en la sección 5.
:::

En un texto, las letras seguidas no son repeticiones independientes. ¿Puede contar en un texto largo acercarse a algo, si sus letras dependen unas de otras?

---

## Ejercicios

::: exercise {#mkv-c1-ej-mancha title="Tres valores en «En un lugar de la Mancha»"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Toma la primera frase del *Quijote*, «En un lugar de la Mancha». **Cambia una idea:** el espacio ya no se quita, y cada letra puede tomar tres valores: V, C o espacio. En la secuencia, el espacio se escribe `_`. Normaliza igual que antes, con un solo espacio entre palabras. El experimento es el mismo: sortear con probabilidades iguales una posición que tenga siguiente.

1. **Traduce.** Escribe la frase como V, C y `_`, y di cuántas posiciones entran al sorteo.
2. **Condiciona.** Escribe la distribución de $S_1$ dado cada valor de $S_0$, en el orden V, C, espacio.
3. **Suma por casos.** Calcula ${\Pr(S_1=V)}$ con la probabilidad total y compruébalo contando.
4. **Decide.** ¿Son independientes $S_0$ y $S_1$? Justifica con un par de valores.
5. **Explica un cero.** ¿Qué cero se mantendría con cualquier otra frase, normalizada igual, y por qué?
:::

::: hint {#mkv-c1-pista-mancha-1 of="mkv-c1-ej-mancha" title="Pista 1 · ¿Qué cuentas en cada renglón?"}
¿Cuántas veces aparece cada valor con una letra siguiente? De esas apariciones, ¿cuántas van seguidas de cada valor?
:::

::: hint {#mkv-c1-pista-mancha-2 of="mkv-c1-ej-mancha" title="Pista 2 · ¿Cuadran tus cuentas?"}
¿Cada distribución condicional suma 1? ¿Los tres casos de $S_0$ suman todas las posiciones del sorteo? ¿La probabilidad total coincide con el conteo directo?
:::

::: answer {#mkv-c1-resp-mancha of="mkv-c1-ej-mancha" title="Respuesta · Tres casos en vez de dos"}
**1. Traducción.** «en un lugar de la mancha» queda así:

```text
VC_VC_CVCVC_CV_CV_CVCCCV
```

Son 24 símbolos. La última «a» no tiene siguiente: entran 23 posiciones al sorteo.

**2. Condicionales.** $S_0$ vale V en 7 posiciones, C en 11 y espacio en 5; suman 23. Cada fila es la distribución de $S_1$ dado ese valor de $S_0$:

| Actual | V | C | espacio |
|---|---:|---:|---:|
| V | 0 | 5/7 | 2/7 |
| C | 6/11 | 2/11 | 3/11 |
| espacio | 1/5 | 4/5 | 0 |

**3. Probabilidad total.** Los tres valores de $S_0$ son la partición:

$$
\begin{aligned}
\Pr(S_1=V)
&=0\cdot\tfrac{7}{23}+\tfrac{6}{11}\cdot\tfrac{11}{23}+\tfrac{1}{5}\cdot\tfrac{5}{23}\\
&=\tfrac{0+6+1}{23}=\tfrac{7}{23}.
\end{aligned}
$$

Contando directamente: 7 de las 23 posiciones van seguidas de vocal.

**4. Independencia.** No son independientes. Como ${\Pr(S_0=V)>0}$, se puede comparar: ${\Pr(S_1=V\mid S_0=V)=0}$, pero ${\Pr(S_1=V)=7/23}$. Saber que la actual es vocal cambia la probabilidad de que la siguiente lo sea.

**5. El cero que no cambia.** Espacio seguido de espacio vale 0 por cómo normalizamos: los espacios seguidos se juntan en uno. El cero de V seguida de V solo dice que esta frase no tiene dos vocales juntas; «iglesia» sí las tiene.
:::

**Punto de control:** deberías poder declarar un experimento y contar en él una probabilidad, una conjunta y una condicional. También, escribirlas con $S_t$, encadenar la regla del producto, distinguir independencia de independencia condicional y sumar por casos con una partición.

---

## Lo que hay que llevarse

- **Toda probabilidad es de un experimento.** Sorteando una de las 26 posiciones con siguiente, ${\Pr(A)=12/26}$ y ${\Pr(B)=11/26}$.
- **Condicionar reduce los casos.** ${\Pr(A\mid B)=2/11}$, contra $10/15$ tras consonante; solo se define si el evento dado tiene probabilidad positiva.
- **La regla del producto encadena condicionales.** El tramo C, V, C vale ${\frac{14}{25}\cdot\frac{9}{14}\cdot\frac{7}{9}=\frac{7}{25}}$; cada factor condiciona en todo lo anterior.
- **Las letras seguidas no son independientes.** ${\Pr(A)\Pr(B)\approx0.195}$, pero ${\Pr(A\cap B)\approx0.077}$.
- **La independencia condicional es un supuesto.** En el *Quijote*, tras C la vocal sale 0.710; si la de hace dos fue V, 0.624, y si fue C, 0.922. Un modelo que solo mira la anterior usaría 0.710 en los tres casos.
- **La probabilidad total suma por casos,** con un caso por valor. El promedio de $n$ repeticiones **independientes** se acerca a la probabilidad, con probabilidad 1.

Continúa con [[mkv-el-problema-de-markov|El problema de Markov]].
