---
id: mkv-lo-que-necesitas
title: "Lo que necesitas de probabilidad"
nav_title: "Lo que necesitas"
summary: "Experimento, evento, probabilidad condicional, variable aleatoria, regla del producto, independencia, independencia condicional, probabilidad total y promedio de muchas repeticiones: primero las fórmulas generales, después los ejemplos del Quijote."
status: ready
estimated_time: 33m
tags: [markov]
---

# Lo que necesitas de probabilidad

**¿Qué tanto cambia la probabilidad de una vocal si ya sabes cuál fue la letra anterior?**

Al terminar tendrás:

- **Probabilidades de eventos:** conjunta y condicional, con su experimento declarado.
- **Una variable aleatoria:** su distribución y la regla del producto encadenada.
- **Independencia e independencia condicional:** una comparación en la frase y un supuesto contrastado con el *Quijote*.
- **Probabilidad total y promedios:** cómo sumar por casos y qué garantiza repetir independientemente.

## Lo que traes

- **Probabilidades de un modelo.** En [[cuando-decide-un-dado|Cuando decide un dado]], $\Pr(a\mid s)$ repartía los resultados posibles; sus probabilidades sumaban 1.
- **Promedios de repeticiones.** En [[simular-en-vez-de-evaluar|Simular partidas]], Monte Carlo plano promediaba pagos de partidas al azar.

> **Página de conceptos, sin simulación.** Primero, cada fórmula general; después, su cuenta a mano en «Con la iglesia hemos dado, Sancho».

---

## 1 · Montar un experimento con la frase

**Piensa: ¿qué significa «la probabilidad de que la siguiente letra sea vocal»?**

Significa algo preciso cuando declaras cómo eliges la letra.

::: definition {#mkv-c1-experimento title="Experimento, evento y probabilidad"}
$$
\begin{aligned}
&A\subseteq\{\text{resultados posibles}\},\\
&0\le\Pr(A)\le1,\\
&\Pr(A)=\frac{\#A}{\#\{\text{resultados posibles}\}}\\
&\quad\text{si son finitos y equiprobables.}
\end{aligned}
$$

- **Qué es.** Un experimento produce un resultado al azar; un evento $A$ reúne los resultados que cumplen una condición.
- **Cómo se calcula.** El símbolo $\#$ cuenta elementos; con resultados equiprobables, divides los favorables entre el total.
- **Qué significa.** $\Pr(A)$ mide qué tan probable es que el resultado pertenezca a $A$.
- **Qué no es.** No es una afirmación sobre el español. Cuando un texto sirva como datos de un modelo, sus frecuencias serán **estimaciones**, con gorro: $\widehat{\Pr}(A)$.
:::

- **Prepara la frase.** Pasa a minúsculas y quita espacios y signos.
- **Clasifica.** V representa a, e, i, o, u; C representa consonantes. La «y» contaría como consonante.

```text
conlaiglesiahemosdadosancho
CVCCVVCCVCVVCVCVCCVCVCVCCCV
```

- **Posiciones.** Son 27 letras, numeradas desde 0; la «o» final no tiene siguiente.
- **Sorteo.** Elige una de las 26 posiciones con siguiente, todas con igual probabilidad.
- **Evento $A$.** La siguiente letra es vocal.
- **Evento $B$.** La letra actual es vocal.

$$
\Pr(A)=\frac{12}{26}\approx0.462.
$$

- **Conteo.** Hay 12 vocales y ninguna ocupa la posición 0: las 12 pueden ser la siguiente.
- **Alcance.** $12/26$ es exacta para este sorteo; no describe por sí sola el español.

::: exercise {#mkv-c1-ej-actual-vocal title="Cuenta el evento B"}
¿Cuánto vale $\Pr(B)$, la probabilidad de que la letra actual sea vocal?
:::

::: hint {#mkv-c1-pista-actual-vocal of="mkv-c1-ej-actual-vocal" title="Dónde puede caer el sorteo"}
¿Cuántas posiciones entran al sorteo, y en cuántas de ellas la letra actual es vocal?
:::

::: answer {#mkv-c1-resp-actual-vocal of="mkv-c1-ej-actual-vocal"}
$$
\Pr(B)=\frac{11}{26}.
$$

**Se excluye la vocal final.** Hay 12 vocales, pero la «o» final no tiene siguiente. Quedan 11 entre las 26 posiciones.
:::

¿Cambia la probabilidad de $A$ si solo miras las posiciones de $B$?

---

## 2 · Calcular una probabilidad condicional

**Piensa: si te dicen que la letra actual es vocal, ¿sigue valiendo $12/26$ para $A$?**

No: saber $B$ reduce los casos posibles.

::: definition {#mkv-c1-prob-condicional title="Probabilidad condicional"}
$$
\begin{aligned}
\Pr(A\mid B)&=\frac{\Pr(A\cap B)}{\Pr(B)},\\
&\Pr(B)>0.
\end{aligned}
$$

- **Qué es.** $\Pr(A\mid B)$ es la probabilidad de $A$ dado que ocurrió $B$.
- **Cómo se calcula.** Divide la probabilidad conjunta, ${\Pr(A\cap B)}$, entre la del condicionante, $\Pr(B)$. La intersección significa «ocurren ambos».
- **Qué significa.** Dentro de $B$, mides qué fracción también cumple $A$.
- **Qué no es.** No es $\Pr(B\mid A)$: invertir la barra cambia los casos que cuentas.
:::

::: table {#mkv-c1-tabla-experimento title="Las 26 posiciones, por letra actual y siguiente"}
| Actual (total) | Siguiente V | Siguiente C |
|---|---:|---:|
| V (11) | 2 | 9 |
| C (15) | 10 | 5 |
:::

- **Lee la tabla.** Cada renglón reúne las posiciones con una misma clase actual; su total aparece entre paréntesis.
- **Intersección.** Las 2 posiciones con vocal actual y siguiente corresponden a «ai» y «ia».

$$
\begin{aligned}
\Pr(A\cap B)&=\frac{2}{26},\\
\Pr(A\mid B)&=\frac{2/26}{11/26}
=\frac{2}{11}.
\end{aligned}
$$

- **La barra cambia el universo.** ${\Pr(B\mid A)}$ usa las 12 posiciones de $A$; ${\Pr(A\mid B)}$, las 11 de $B$.
- **La condición $\Pr(B)>0$ no es un detalle.** Si $B$ fuera «la actual es k», no habría posiciones que mirar: la condicional no se define.

::: exercise {#mkv-c1-ej-tras-consonante title="Condiciona a la consonante"}
Usa la definición: ¿cuánto vale la probabilidad de que la siguiente sea vocal si la actual es consonante?
:::

::: hint {#mkv-c1-pista-tras-consonante of="mkv-c1-ej-tras-consonante" title="Dos probabilidades, un cociente"}
¿Cuánto valen la probabilidad conjunta y la de «actual consonante», cada una sobre 26?
:::

::: answer {#mkv-c1-resp-tras-consonante of="mkv-c1-ej-tras-consonante"}
$$
\begin{aligned}
&\Pr(\text{siguiente V}\mid\text{actual C})\\
&\quad=\frac{10/26}{15/26}
=\frac{10}{15}=\frac{2}{3}.
\end{aligned}
$$

**Tras consonante aumenta.** La conjunta vale $10/26$ y el condicionante, $15/26$; su cociente supera $2/11$.
:::

¿Cómo nombras «actual» y «siguiente» para escribir estas cuentas sin repetir palabras?

---

## 3 · Nombrar las letras con variables aleatorias

**Piensa: ¿cómo escribes «la actual es vocal y la siguiente también» sin inventar un evento para cada caso?**

Asignas una variable aleatoria a cada letra que depende del sorteo.

::: definition {#mkv-c1-variable-aleatoria title="Variable aleatoria y distribución"}
$$
\begin{aligned}
&S_t(\text{resultado})\in\{a_1,\ldots,a_k\},\\
&\bigl(\Pr(S_t=a_1),\ldots,\Pr(S_t=a_k)\bigr),\\
&\Pr(S_t=a_j)\ge0,\qquad
\sum_{j=1}^{k}\Pr(S_t=a_j)=1.
\end{aligned}
$$

- **Qué es.** $S_t$ asigna un valor a cada resultado; su distribución es el vector de probabilidades de esos valores.
- **Cómo se calcula.** Enumera sus $k$ valores posibles, distintos y finitos, en un orden fijo; calcula una probabilidad por valor.
- **Qué significa.** Cada entrada dice qué tan probable es observar ese valor; juntas suman 1.
- **Qué no es.** La variable $S_t$ y el valor observado son objetos distintos.
:::

**Para cualquier alfabeto.** Al sortear uniformemente una posición con siguiente:

$$
\begin{aligned}
&\Pr(S_1=b\mid S_0=a)\\
&\quad=\frac{\#\{\text{posiciones con }a\text{ y luego }b\}}
{\#\{\text{posiciones con }a\text{ y siguiente}\}},\\
&\Pr(S_0=a)>0.
\end{aligned}
$$

- **En la frase.** $S_t$ es la clase de la letra $t$ pasos después de la sorteada, con ${t=0,1,2,\ldots}$
- **Origen aleatorio.** $S_0$ es la actual y $S_1$, la siguiente; $t$ no es una posición fija de la frase.
- **Existencia.** El sorteo debe dejar al menos $t$ letras siguientes. Las 26 posiciones garantizan $S_0$ y $S_1$.

$$
\begin{aligned}
B&=\{S_0=V\},\\
A&=\{S_1=V\},\\
\Pr(S_0=V,\ S_1=V)&=\frac{2}{26},\\
\Pr(S_1=V\mid S_0=V)&=\frac{2}{11}.
\end{aligned}
$$

**La coma se lee «y».** Pide que ambas igualdades se cumplan.

$$
\begin{aligned}
&\bigl(\Pr(S_0=V),\Pr(S_0=C)\bigr)\\
&\quad=\left(\frac{11}{26},\frac{15}{26}\right).
\end{aligned}
$$

**La misma cuenta en Python.** Sirve para cualquier texto convertido en clases o letras.

```python
from fractions import Fraction

def condicional(clases, a, b):
    """Pr(S_1 = b | S_0 = a)."""
    # con a y con siguiente
    con_a = 0
    # de ellas, seguidas de b
    a_luego_b = 0
    # con siguiente
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
# imprime 2/11
print(condicional(frase, "V", "V"))
```

::: exercise {#mkv-c1-ej-distribucion-tras-v title="Escribe una distribución condicional"}
Escribe la distribución de $S_1$ dado ${S_0=V}$, en el orden V, C. ¿Suma 1?
:::

::: hint {#mkv-c1-pista-distribucion-tras-v of="mkv-c1-ej-distribucion-tras-v" title="El otro valor"}
De las 11 posiciones con vocal actual, ¿cuántas van seguidas de consonante?
:::

::: answer {#mkv-c1-resp-distribucion-tras-v of="mkv-c1-ej-distribucion-tras-v"}
$$
\left(\frac{2}{11},\frac{9}{11}\right),
\qquad
\frac{2}{11}+\frac{9}{11}=\frac{11}{11}=1.
$$

**Cubre ambos valores.** Dado ${S_0=V}$, la siguiente letra tiene que ser V o C.
:::

¿Cómo calculas la probabilidad de tres letras seguidas, como C, V, C?

---

## 4 · Encadenar la regla del producto

**Piensa: si conoces una condicional, ¿cómo recuperas la probabilidad de que dos cosas pasen juntas?**

Multiplicas la condicional por la probabilidad del evento dado.

::: theorem {#mkv-c1-teo-producto title="Regla del producto, encadenada"}
$$
\begin{aligned}
&\Pr(A\cap B)=\Pr(B)\Pr(A\mid B),\\
&\Pr(B)>0.
\end{aligned}
$$

Con $t\ge1$ y valores $a_0,\dots,a_t$ de $S_0,\dots,S_t$:

$$
\begin{aligned}
&\Pr(S_0=a_0,\dots,S_t=a_t)\\
&\quad=\Pr(S_0=a_0)\\
&\qquad{}\times\prod_{j=0}^{t-1}
\Pr(S_{j+1}=a_{j+1}\mid S_0=a_0,\\
&\qquad\qquad\dots,S_j=a_j),\\
&\Pr(S_0=a_0,\dots,S_{t-1}=a_{t-1})>0.
\end{aligned}
$$

**Lectura.** Multiplica la probabilidad inicial por cada condicional, conservando toda la historia.

- **Símbolos.** La coma significa «y»; $\prod$ multiplica un factor por cada índice $j$.
- **Condición.** Cada historia usada para condicionar debe tener probabilidad positiva.
- **Caso cero.** Si la historia hasta ${t-1}$ tiene probabilidad 0, la conjunta completa también vale 0.
:::

**Dos letras en la frase.**

$$
\Pr(A\cap B)=\frac{11}{26}\cdot\frac{2}{11}
=\frac{2}{26}.
$$

**Tres letras.** Sortea entre las 25 posiciones con dos letras siguientes: ahora siempre existen $S_0$, $S_1$ y $S_2$.

$$
\begin{aligned}
&\Pr(S_0=C,\ S_1=V,\ S_2=C)\\
&\quad=\frac{14}{25}\cdot\frac{9}{14}\cdot\frac{7}{9}
=\frac{7}{25}.
\end{aligned}
$$

- **Primer factor.** 14 de las 25 posiciones empiezan con C: ${\Pr(S_0=C)=14/25}$.
- **Segundo factor.** De esas 14, 9 siguen con V: $\Pr(S_1=V\mid S_0=C)=9/14$.
- **Tercer factor.** De esas 9, 7 siguen con C:

$$
\Pr(S_2=C\mid S_0=C,\ S_1=V)=\frac{7}{9}.
$$

**Comprobación.** Contar directamente también da 7 tramos C, V, C entre 25 posiciones.

::: exercise {#mkv-c1-ej-catorce title="Explica el primer factor"}
En la sección 3, $\Pr(S_0=C)=15/26$. ¿Por qué aquí el primer factor es $14/25$?
:::

::: hint {#mkv-c1-pista-catorce of="mkv-c1-ej-catorce" title="Compara los dos sorteos"}
¿Qué posición con C dejó de entrar al sorteo?
:::

::: answer {#mkv-c1-resp-catorce of="mkv-c1-ej-catorce"}
**Cambió el experimento.** La posición 25, la «h» de «Sancho», solo tiene una letra siguiente y sale del sorteo. Quedan 14 consonantes entre 25 posiciones.
:::

¿En qué casos saber lo anterior no cambia la probabilidad siguiente?

---

## 5 · Probar la independencia

**Piensa: ¿hay eventos para los que saber uno no cambia nada del otro?**

Sí: esos eventos son independientes.

::: definition {#mkv-c1-independencia-simple title="Independencia"}
$$
\Pr(A\cap B)=\Pr(A)\Pr(B).
$$

Si $\Pr(B)>0$, equivale a:

$$
\Pr(A\mid B)=\Pr(A).
$$

- **Qué es.** Independencia significa que la probabilidad conjunta es el producto de las probabilidades individuales.
- **Cómo se calcula.** Compara ambos lados; con condicionante positivo, también puedes comparar la condicional con la probabilidad sin condición.
- **Qué significa.** Saber que ocurrió $B$ no cambia la probabilidad de $A$.
- **Qué no es.** Eventos que no pueden ocurrir juntos, ambos con probabilidad positiva, no son independientes: su conjunta vale 0.

Para variables aleatorias, la igualdad debe cumplirse para todos sus valores $a,b$:

$$
\begin{aligned}
&\Pr(S_0=a,\ S_1=b)\\
&\quad=\Pr(S_0=a)\Pr(S_1=b).
\end{aligned}
$$
:::

**En la frase, compara.**

$$
\begin{aligned}
\Pr(A)\Pr(B)&=\frac{12}{26}\cdot\frac{11}{26}
\approx0.195,\\
\Pr(A\cap B)&=\frac{2}{26}\approx0.077.
\end{aligned}
$$

**La condicional confirma la diferencia.**

$$
\Pr(A\mid B)=\frac{2}{11}
\ne\frac{12}{26}=\Pr(A).
$$

**Conclusión.** Los eventos no son independientes: tras vocal, otra vocal aparece en 2 de 11 posiciones.

> [!WARNING]
> **Confundir dependencia con causa.** Saber una letra cambia la probabilidad de la otra; **eso no demuestra causalidad**.

::: exercise {#mkv-c1-ej-independiente-c title="Prueba con la consonante"}
¿Son independientes $A$ y el evento $\{S_0=C\}$? Usa la forma con la condicional.
:::

::: hint {#mkv-c1-pista-independiente-c of="mkv-c1-ej-independiente-c" title="Ya la calculaste"}
¿Qué condicional obtuviste en el ejercicio de la sección 2?
:::

::: answer {#mkv-c1-resp-independiente-c of="mkv-c1-ej-independiente-c"}
$$
\begin{aligned}
\Pr(S_0=C)&=\frac{15}{26}>0,\\
\Pr(A\mid S_0=C)&=\frac{10}{15}
\ne\frac{12}{26}=\Pr(A).
\end{aligned}
$$

**No son independientes.** Saber que la actual es consonante aumenta la probabilidad de vocal.
:::

Si ya sabes la letra anterior, ¿la de hace dos todavía agrega información?

---

## 6 · Suponer independencia condicional

**Piensa: si ya sabes la letra anterior, ¿saber también la de hace dos cambia la probabilidad de la siguiente?**

Puede cambiarla; la independencia condicional afirma que esa información adicional no la cambia.

::: definition {#mkv-c1-independencia-condicional title="Independencia condicional"}
$$
\begin{aligned}
&\Pr(A\cap D\mid B)\\
&\quad=\Pr(A\mid B)\Pr(D\mid B),\\
&\Pr(B)>0.
\end{aligned}
$$

Si $\Pr(D\cap B)>0$, equivale a:

$$
\Pr(A\mid D,\ B)=\Pr(A\mid B).
$$

- **Qué es.** $A$ y $D$ son independientes dado $B$ cuando conocer también $D$ no cambia la probabilidad de $A$.
- **Cómo se calcula.** Compara las probabilidades dentro de $B$; para agregar $D$ como condición, exige ${\Pr(D\cap B)>0}$.
- **Qué significa.** La coma es «y»: $\Pr(A\mid D,B)$ condiciona en la intersección $D\cap B$.
- **Qué no es.** La independencia sin condición y la independencia dado $B$ no se implican entre sí.
:::

- **Datos.** La frase tiene 27 letras; contrastamos el supuesto con el *Quijote* completo: minúsculas, vocales sin acento, sin espacios ni signos. La ñ y la «y» cuentan como consonantes.
- **Experimento.** Sortea una posición del libro con al menos dos letras siguientes; observa las tres.
- **Nombres.** Como en la sección 3, la sorteada es $S_0$; la siguiente, $S_1$; la última, $S_2$.
- **Estimaciones.** Usamos el libro como datos de un modelo; sus frecuencias llevan gorro: $\widehat{\Pr}$.

::: table {#mkv-c1-tabla-dos-atras title="Tras una consonante en el Quijote: ¿importa la letra de hace dos?"}
| La de hace dos | La anterior | Siguiente vocal |
|---|---|---:|
| cualquiera | C | 0.710 |
| V | C | 0.624 |
| C | C | 0.922 |
:::

**Instancia de la definición.** Aquí ${A=\{S_2=V\}}$, ${B=\{S_1=C\}}$ y $D$ fija la clase de $S_0$.

$$
\begin{aligned}
\widehat{\Pr}(A\mid B)&=0.710,\\
\widehat{\Pr}(A\mid S_0=V,B)&=0.624,\\
\widehat{\Pr}(A\mid S_0=C,B)&=0.922.
\end{aligned}
$$

- **Comparación.** Los tres contextos tienen observaciones, y sus frecuencias difieren: en este texto, la de hace dos sí agrega información.
- **El caso C, C.** Tras dos consonantes, la vocal sale 0.922: tres consonantes seguidas son raras en el *Quijote*.
- **Supuesto.** Un modelo que solo usa la anterior omite esa información; no afirma una propiedad exacta del español.

::: exercise {#mkv-c1-ej-supuesto-exacto title="Imagina el supuesto cumplido"}
Si el *Quijote* cumpliera exactamente el supuesto, ¿cuánto valdrían las filas de V y de C?
:::

::: hint {#mkv-c1-pista-supuesto-exacto of="mkv-c1-ej-supuesto-exacto" title="Lee la fórmula"}
En $\Pr(A\mid D,\ B)=\Pr(A\mid B)$, ¿qué fila de la tabla es el lado derecho?
:::

::: answer {#mkv-c1-resp-supuesto-exacto of="mkv-c1-ej-supuesto-exacto"}
**Ambas valdrían 0.710.** Las frecuencias 0.624 y 0.922 muestran que esa igualdad no se cumple exactamente en el texto.
:::

La primera fila mezcla las otras dos: ¿cómo combinas varios casos en una sola probabilidad?

---

## 7 · Sumar por casos con la probabilidad total

**Piensa: con la probabilidad de vocal tras V y tras C, ¿puedes recuperar la probabilidad sin condición?**

Sí, si también conoces la probabilidad de cada caso.

::: definition {#mkv-c1-particion title="Partición"}
$$
\begin{aligned}
&B_j\ne\varnothing,\\
&B_i\cap B_j=\varnothing\qquad(i\ne j),\\
&\bigcup_j B_j=\{\text{resultados posibles}\}.
\end{aligned}
$$

- **Qué es.** Una partición divide los resultados en casos que no se enciman y cubren todo.
- **Cómo se calcula.** Revisa que cada resultado pertenezca a exactamente un caso.
- **Qué significa.** Puedes resolver por casos y reunir las contribuciones sin contar dos veces.
:::

::: theorem {#mkv-c1-teo-total title="Probabilidad total"}
$$
\Pr(A)=\sum_{j:\Pr(B_j)>0}
\Pr(A\mid B_j)\Pr(B_j).
$$

**Condición.** Los eventos $B_1,B_2,\ldots$ forman una partición finita o numerable.

**Lectura.** Multiplica cada condicional por la probabilidad de su caso y suma.

**Casos nulos.** Se omiten los de probabilidad 0: sus condicionales no están definidas y no aportan probabilidad.
:::

**Para cualquier alfabeto.** Los eventos $\{S_0=a\}$ forman una partición:

$$
\begin{aligned}
&\Pr(S_1=b)\\
&\quad=\sum_a
\Pr(S_1=b\mid S_0=a)\Pr(S_0=a).
\end{aligned}
$$

Se omiten los valores $a$ con ${\Pr(S_0=a)=0}$.

**En la frase.** Las 26 posiciones se reparten entre actual V y actual C.

$$
\begin{aligned}
\Pr(A)
&=\frac{2}{11}\cdot\frac{11}{26}\\
&\quad+\frac{10}{15}\cdot\frac{15}{26}\\
&=\frac{2+10}{26}=\frac{12}{26}.
\end{aligned}
$$

- **Comprobación.** La tabla de la sección 2 cuenta 2 vocales siguientes tras V y 10 tras C.
- **Más valores.** Con dos clases, «no V» significa C; con más clases, puede reunir varios casos con distintas condicionales.
- **Distribución.** Con dos valores basta un número; con más, necesitas tantos como valores menos uno.
- **En el libro.** En la sección 6, el 0.710 combina 0.624 y 0.922 con sus pesos respectivos.
- **Peso mayor.** Tras C, la de hace dos fue V en unas 7 de cada 10 posiciones. La mezcla queda más cerca de 0.624.

::: exercise {#mkv-c1-ej-no-particion title="Revisa una partición"}
¿Forman los eventos $A$ y $B$ una partición de las 26 posiciones?
:::

::: hint {#mkv-c1-pista-no-particion of="mkv-c1-ej-no-particion" title="Dos revisiones"}
¿Hay posiciones que estén en los dos? ¿Hay posiciones que no estén en ninguno?
:::

::: answer {#mkv-c1-resp-no-particion of="mkv-c1-ej-no-particion"}
**No.** Las 2 posiciones con V seguida de V están en ambos. Las 5 con C seguida de C no están en ninguno.
:::

Si repites el sorteo, ¿por qué la frecuencia observada debería acercarse a la probabilidad?

---

## 8 · Repetir muchas veces y promediar

**Piensa: si repites el sorteo muchas veces, ¿qué fracción de las veces será vocal la siguiente?**

La fracción se acerca a la probabilidad del evento cuando repites independientemente el mismo experimento.

::: theorem {#mkv-c1-teo-promedio title="El promedio de muchas repeticiones"}
$$
\begin{aligned}
&\widehat{\Pr}_n(A)
=\frac{\text{veces que ocurre }A}{n},\\
&\Pr\!\left(
\lim_{n\to\infty}\widehat{\Pr}_n(A)=\Pr(A)
\right)=1.
\end{aligned}
$$

**Condición.** Repite el mismo experimento de manera independiente; $n$ cuenta las repeticiones y todas tienen la misma probabilidad $\Pr(A)$.

**Lectura.** Con probabilidad 1, la frecuencia observada converge a la probabilidad del evento.

Es la **ley de los grandes números** (*law of large numbers*).
:::

**En la frase.** Cada repetición vuelve a sortear entre las 26 posiciones, sin depender de los sorteos anteriores.

$$
\begin{aligned}
\widehat{\Pr}_n(A)&\longrightarrow\Pr(A),\\
\Pr(A)&=\frac{12}{26}\approx0.462,\\
&\text{con probabilidad }1.
\end{aligned}
$$

- **Con pocas repeticiones.** Con ${n=26}$, el evento no tiene por qué ocurrir exactamente 12 veces.
- **Sin independencia.** Si sorteas una vez y copias el resultado $n$ veces, la fracción queda en 0 o 1.
- **En Monte Carlo plano.** Con partidas independientes y una regla fija, el promedio se acerca al pago esperado bajo esa regla.

::: exercise {#mkv-c1-ej-repetir title="Elige la repetición válida"}
¿Cuál de estas formas de repetir cumple la condición del teorema?

1. **Sortear de nuevo.** Sortear $n$ veces entre las 26 posiciones.
2. **Leer de corrido.** Sortear una posición y tomar las que le siguen en la frase.
:::

::: hint {#mkv-c1-pista-repetir of="mkv-c1-ej-repetir" title="Mira la segunda repetición"}
En la forma 2, ¿saber la primera posición te dice algo de la segunda?
:::

::: answer {#mkv-c1-resp-repetir of="mkv-c1-ej-repetir"}
**Solo la primera.** En la segunda, la posición inicial fija las demás. Las letras seguidas también dependen entre sí, como viste en la sección 5.
:::

¿Puedes aplicar estas cuentas a otra frase cuando el espacio también cuenta como un valor?

---

## Ejercicios

::: exercise {#mkv-c1-ej-mancha title="Tres valores en «En un lugar de la Mancha»"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Toma la primera frase del *Quijote*, «En un lugar de la Mancha».

- **Cambia una idea.** Conserva el espacio: cada símbolo toma uno de tres valores, V, C o espacio.
- **Representación.** Escribe el espacio como `_`. Normaliza igual que antes, con un solo espacio entre palabras.
- **Experimento.** Sortea con probabilidades iguales una posición que tenga siguiente.

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

Son 24 símbolos; la última «a» no tiene siguiente. Entran 23 posiciones al sorteo.

**2. Condicionales.** $S_0$ vale V en 7 posiciones, C en 11 y espacio en 5; suman 23. Cada fila da la distribución de $S_1$ condicionada en su valor actual:

| Actual | V | C | espacio |
|---|---:|---:|---:|
| V | 0 | 5/7 | 2/7 |
| C | 6/11 | 2/11 | 3/11 |
| espacio | 1/5 | 4/5 | 0 |

**3. Probabilidad total.** Los tres valores de $S_0$ forman la partición:

$$
\begin{aligned}
\Pr(S_1=V)
&=0\cdot\frac{7}{23}\\
&\quad+\frac{6}{11}\cdot\frac{11}{23}\\
&\quad+\frac{1}{5}\cdot\frac{5}{23}\\
&=\frac{0+6+1}{23}=\frac{7}{23}.
\end{aligned}
$$

Contando directamente, 7 de las 23 posiciones van seguidas de vocal.

**4. Independencia.** Basta encontrar un par que no cumpla la igualdad:

$$
\begin{aligned}
\Pr(S_0=V)&>0,\\
\Pr(S_1=V\mid S_0=V)&=0,\\
\Pr(S_1=V)&=\frac{7}{23}.
\end{aligned}
$$

La condicional difiere de la probabilidad sin condición: $S_0$ y $S_1$ no son independientes.

**5. El cero que no cambia.** Espacio seguido de espacio vale 0 porque la normalización junta los espacios consecutivos. El cero de V seguida de V depende de esta frase; «iglesia» sí tiene vocales consecutivas.
:::

**Punto de control:** deberías poder declarar el experimento y calcular una probabilidad, una conjunta y una condicional. También, escribir distribuciones, encadenar productos, distinguir ambas independencias, sumar por casos y reconocer cuándo vale promediar repeticiones.

---

## Lo que hay que llevarse

- **Experimento.** Entre 26 posiciones con siguiente, ${\Pr(A)=12/26}$ y ${\Pr(B)=11/26}$.
- **Condicional.** $\Pr(A\mid B)=2/11$, frente a $10/15$ tras consonante; el condicionante debe tener probabilidad positiva.
- **Producto.** Cada factor conserva toda la historia:

$$
\frac{14}{25}\cdot\frac{9}{14}\cdot\frac{7}{9}
=\frac{7}{25}.
$$

- **Independencia.** Compara ${\Pr(A\cap B)}$ con ${\Pr(A)\Pr(B)}$; aquí, $0.077\ne0.195$.
- **Independencia condicional.** Compara ${\Pr(A\mid D,B)}$ con ${\Pr(A\mid B)}$, si ${\Pr(D\cap B)>0}$.
- **En el libro.** Tras C, 0.710; agregando la de hace dos, 0.624 o 0.922. El supuesto usaría 0.710 en ambos casos.
- **Probabilidad total.** Suma condicional por peso sobre una partición; omite los casos de probabilidad 0.
- **Promedio.** La frecuencia de $n$ repeticiones independientes del mismo experimento converge a $\Pr(A)$ con probabilidad 1.

Continúa con [[mkv-cadena-en-general|La cadena de Markov, en general]].

