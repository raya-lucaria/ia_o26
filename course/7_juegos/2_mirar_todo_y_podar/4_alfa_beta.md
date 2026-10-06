---
id: alfa-beta
title: Alfa-beta a mano
nav_title: Alfa-beta a mano
summary: "Dos recorridos de alfa-beta sobre el subgrafo de n1: dónde se corta, qué estados nunca se generan y por qué la raíz da el mismo valor que minimax."
status: ready
estimated_time: 25m
tags: [juegos, alfa-beta, poda]
---

# Alfa-beta a mano

**¿Cómo dejar ramas sin generar sin cambiar la respuesta?**

Al terminar tendrás **dos recorridos de alfa-beta hechos a mano** sobre n1,
uno que genera 5 de los 13 estados y otro que genera 8, y sabrás explicar
por qué los dos dan el mismo valor que minimax.

> **Las reglas, en cuatro líneas.** Tablero de 3×3; Blancas (B) abajo en la
> fila 1 y Negras (N) arriba en la fila 3. Empiezan Blancas. Un peón avanza
> una casilla si está vacía o captura en diagonal hacia delante. Gana quien
> llega a la fila del rival, captura todos los peones rivales o deja al rival
> sin jugada; ganar vale $+1$ y perder, $-1$.

> **Supuestos de esta página.** Los mismos de
> [[escribir-el-juego|Escribir el juego]]: dos jugadores por turnos, sin
> azar, todo a la vista, toda partida termina y suma cero.

> **Las piezas que usa esta página.** Vienen de
> [[escribir-el-juego|Escribir el juego]]: $S_F$, los finales
> (@jue-c1-finales); $\mathrm{Pl}(s)$, quién mueve, leído del turno guardado
> (@jue-c1-pl); $A(s)$, las jugadas permitidas (@jue-c1-acciones); $T(s,a)$,
> a dónde lleva cada una (@jue-c1-transicion); y $U(s)$, $+1$ si gana
> Blancas y $-1$ si gana Negras (@jue-c1-utilidad).

> **El problema de esta página.**
>
> **Dado:** el estado n1 y las reglas del juego, $S_F$, $\mathrm{Pl}$, $A$,
> $T$ y $U$: lo mismo que recibe minimax.
>
> **Encontrar:** $V(\text{n1})$ y la jugada que lo alcanza, **sin generar**
> los estados que no pueden cambiar la respuesta.

Minimax generó los 13 estados de n1 y obtuvo $V(\text{n1})=+1$ con
$\text{c1}\textbf{-}\text{c2}$. **Nosotros ya conocemos ese $+1$; el
algoritmo empezará sin él.** Lo usaremos al final para comprobar.

## 1 · Ver un corte con números

**Piensa: si Blancas ya tiene una jugada que gana, ¿necesita saber
exactamente cuánto vale otra?**

Sigamos el recorrido en profundidad, en el orden fijo de las jugadas:

1. Blancas genera **n2**, tras $\text{c1}\textbf{-}\text{c2}$: es final y
   vale $+1$. Blancas ya tiene **asegurado $+1$**, juegue lo que juegue
   después.
2. Blancas genera **n3**, tras $\text{c1}\textbf{x}\text{b2}$. Ahí mueve
   Negras. Su primera respuesta, $\text{a3}\textbf{x}\text{b2}$, lleva a n4
   y luego a n5, que vale $+1$.
3. Con solo eso, Negras **ya puede dejar a Blancas en $+1$ o menos** en
   esta rama: le basta con jugar $\text{a3}\textbf{x}\text{b2}$. Sus otras
   respuestas solo podrían bajar ese número, nunca subirlo.

Para Blancas, «$+1$ o menos» no es mejor que el $+1$ que ya tiene. **n3 no
puede mejorar a Blancas**, valgan lo que valgan sus otros hijos. Así que n6
y n13 **no se generan**, y tampoco nada de lo que cuelga de n6.

Se generan **5 estados de 13**: n1, n2, n3, n4 y n5. La respuesta es la
misma: $V(\text{n1})=+1$, con $\text{c1}\textbf{-}\text{c2}$.

**Ojo:** no supimos cuánto vale n3. Solo supimos que vale **a lo más
$+1$**. Su valor exacto, $-1$, nunca se calculó, y no hacía falta.

## 2 · Nombrar lo que cada jugador ya tiene asegurado

**Piensa: ¿qué dos números usaste para decidir que n3 no valía la pena?**

El $+1$ que Blancas ya tenía, y el $+1$ al que Negras podía limitar la
rama. Alfa-beta lleva esos dos números en cada nodo.

::: definition {#jue-c2-alfa-beta title="Alfa y beta"}
En un nodo del recorrido,

- $\alpha$ («alfa») es el **mayor valor que MAX ya tiene asegurado** con
  alguna alternativa en el camino desde la raíz hasta ese nodo;
- $\beta$ («beta») es el **menor valor que MIN ya tiene asegurado** con
  alguna alternativa en ese mismo camino.

Al empezar no hay nada asegurado: $\alpha=-\infty$ y $\beta=+\infty$. Cada
hijo **hereda** el $\alpha$ y el $\beta$ que tiene su padre en el momento de
generarlo.

**Qué significa:** el valor que puede cambiar la decisión de arriba está
entre $\alpha$ y $\beta$. Lo que cae fuera, alguno de los dos ya lo evitó.
:::

Con esos dos números y $v$, el mejor valor visto entre los hijos del nodo
actual, hay dos cortes:

::: definition {#jue-c2-cortes title="Corte alfa y corte beta"}
- **Corte alfa**, en un nodo de MIN: si $v\le\alpha$, MIN ya puede dejar a
  MAX en $v$ o menos, y MAX tiene asegurado $\alpha$ en otra parte. MAX
  nunca elegirá entrar aquí: los hijos que faltan no se generan.
- **Corte beta**, en un nodo de MAX: si $v\ge\beta$, MAX ya puede conseguir
  $v$ o más, y MIN tiene asegurado $\beta$ en otra parte. MIN nunca dejará
  que la partida llegue aquí: los hijos que faltan no se generan.

**Qué no es:** un corte no dice cuánto vale el nodo. Dice que su valor exacto
ya no puede cambiar la decisión de arriba.
:::

El corte de la sección 1 fue un **corte alfa**: en n3, un nodo de MIN,
$v=+1\le\alpha=+1$. Fíjate en el **igual**: un empate con lo que MAX ya
tiene tampoco le sirve, así que también se corta.

## 3 · La traza con el orden fijo

**Piensa: ¿con qué $\alpha$ y $\beta$ llega cada nodo?**

Repetimos la sección 1 anotando $\alpha$, $\beta$ y lo que devuelve cada
nodo. La figura lo muestra sobre el mismo dibujo de n1; el número en la
esquina es el orden de visita.

::: figure {#jue-c2-ab-fijo title="Alfa-beta con el orden fijo"}
![El subgrafo de n1 recorrido por alfa-beta con el orden fijo. Primero n1 (α −∞, β +∞, MAX, devuelve +1); segundo n2, final +1; tercero n3 (α +1, β +∞, MIN, devuelve +1); cuarto n4 (α +1, β +∞, MAX, devuelve +1); quinto n5, final +1. Una barra de acento debajo de n3 marca el corte alfa sobre las jugadas c3-c2 y c3xb2. n6, n7, n8, n9, n10, n11, n12 y n13 son cajas punteadas con signo de interrogación: no se generan](../_assets/jue-alfa-beta-fijo.svg)
:::

La traza, un estado por renglón, en el orden en que se generan. Entre
corchetes, $[\alpha,\beta]$ al llegar:

1. **n1**, MAX, $[-\infty,+\infty]$: revisa sus hijos. Devuelve $+1$.
2. **n2**, final, $[-\infty,+\infty]$: vale $+1$. La raíz pasa a
   $\alpha=+1$.
3. **n3**, MIN, $[+1,+\infty]$: **corte alfa** tras n4. Devuelve $+1$.
4. **n4**, MAX, $[+1,+\infty]$: un solo hijo. Devuelve $+1$.
5. **n5**, final, $[+1,+\infty]$: vale $+1$.

n6 y n13 no se generan.

::: exercise {#jue-c2-ej-primer-corte title="Decide si se corta en n3"}
1. ¿Por qué n3 llega con $\alpha=+1$ y no con $-\infty$?
2. Tras valorar n4, n3 tiene $v=+1$. ¿Se cumple la condición de algún
   corte? ¿Cuál?
3. ¿Qué devuelve n3 a la raíz y qué sabe el algoritmo de su valor exacto?
:::

::: hint {#jue-c2-pista-primer-corte of="jue-c2-ej-primer-corte" title="Hereda y compara"}
Un hijo hereda el $\alpha$ de su padre **en el momento de generarlo**. ¿Qué
había pasado en n1 antes de generar n3? Para el corte, n3 es de MIN: mira
la condición del corte alfa.
:::

::: answer {#jue-c2-resp-primer-corte of="jue-c2-ej-primer-corte"}
1. Porque antes de generar n3, la raíz ya había valorado n2 y había subido
   su $\alpha$ a $+1$. n3 lo hereda.
2. Sí: $v=+1\le\alpha=+1$, un **corte alfa**. Los dos hijos que faltan,
   n6 y n13, no se generan.
3. Devuelve $+1$. Del valor exacto solo sabe que es **a lo más $+1$**.
   Minimax calculó que es $-1$, pero alfa-beta no lo sabe ni lo necesita.
:::

## 4 · Cambiar el orden de las jugadas

**Piensa: si Blancas hubiera mirado primero la captura, ¿se habría
ahorrado lo mismo?**

Repetimos todo con el orden **invertido en todos los nodos**: la última
jugada de cada lista se revisa primero. El árbol y sus finales no cambian, y
los nodos conservan sus números. En la figura, el dibujo está reflejado para
que de izquierda a derecha se lea el nuevo orden.

**Paso 1 · La raíz empieza por n3.** n3 es de MIN y su primer hijo ahora es
n13, tras $\text{c3}\textbf{x}\text{b2}$: final, vale $-1$. En n3, $v=-1$.
¿$-1\le\alpha=-\infty$? No. Actualizamos $\beta=-1$: **Negras ya tiene
asegurado $-1$**.

**Paso 2 · Blancas en n6.** n6 hereda $\alpha=-\infty$ y $\beta=-1$. Su
primer hijo, en el orden invertido, es n12, tras
$\text{b2}\textbf{x}\text{a3}$: final, vale $+1$. En n6, $v=+1$.

::: exercise {#jue-c2-ej-corte-beta title="Decide si se corta en n6"}
1. En n6, $\beta=-1$ y $v=+1$. Es un nodo de MAX. ¿Se cumple la condición
   de algún corte?
2. ¿Qué hijos de n6 no se generan?
3. Dilo en palabras: ¿por qué Negras no necesita saber cuánto vale n6
   exactamente?
:::

::: hint {#jue-c2-pista-corte-beta of="jue-c2-ej-corte-beta" title="Desde el lado de Negras"}
$\beta=-1$ es lo que Negras ya tiene asegurado en n3 con otra jugada. Si
entra en n6, Blancas consigue al menos $+1$. ¿Le conviene a Negras?
:::

::: answer {#jue-c2-resp-corte-beta of="jue-c2-ej-corte-beta"}
1. Sí: $v=+1\ge\beta=-1$, un **corte beta**.
2. n11, tras $\text{b2}\textbf{-}\text{b3}$, y n7, tras
   $\text{b1}\textbf{x}\text{c2}$, con todo lo que cuelga de n7: n8, n9 y
   n10.
3. Negras ya tiene $\text{c3}\textbf{x}\text{b2}$, que gana. Si jugara
   $\text{c3}\textbf{-}\text{c2}$, Blancas conseguiría **al menos** $+1$.
   Negras nunca elegirá esa jugada, y no importa cuánto más valga.
:::

**Paso 3 · Negras termina, y la raíz también.** De vuelta en n3, $v$ sigue
en $-1$. Falta n4, que hereda $\beta=-1$. Su único hijo, n5, vale $+1$;
como $+1\ge\beta$, se cumpliría un corte beta, pero n4 ya no tiene más hijos
que ahorrar. n3 devuelve $-1$. En la raíz, $\alpha$ sube a $-1$, y el
último hijo, n2, vale $+1$: la raíz devuelve **$+1$**. Mismo valor, misma
jugada.

::: figure {#jue-c2-ab-invertido title="Alfa-beta con el orden invertido"}
![El subgrafo de n1, reflejado, recorrido por alfa-beta con el orden invertido. Primero n1; segundo n3 (α −∞, β +∞, MIN, devuelve −1); tercero n13, final −1; cuarto n6 (α −∞, β −1, MAX, devuelve +1); quinto n12, final +1; sexto n4 (α −∞, β −1, MAX, devuelve +1); séptimo n5, final +1; octavo n2, final +1. Una barra de acento debajo de n6 marca el corte beta sobre las jugadas b2-b3 y b1xc2. n11, n7, n8, n9 y n10 no se generan](../_assets/jue-alfa-beta-invertido.svg)
:::

La traza, con $[\alpha,\beta]$ al llegar a cada estado:

1. **n1**, MAX, $[-\infty,+\infty]$: revisa sus hijos. Devuelve $+1$.
2. **n3**, MIN, $[-\infty,+\infty]$: revisa sus tres hijos. Devuelve
   $-1$.
3. **n13**, final, $[-\infty,+\infty]$: vale $-1$. n3 pasa a $\beta=-1$.
4. **n6**, MAX, $[-\infty,-1]$: **corte beta** tras n12. Devuelve $+1$.
5. **n12**, final, $[-\infty,-1]$: vale $+1$.
6. **n4**, MAX, $[-\infty,-1]$: un solo hijo, nada que ahorrar. Devuelve
   $+1$.
7. **n5**, final, $[-\infty,-1]$: vale $+1$.
8. **n2**, final, $[-1,+\infty]$: vale $+1$. La raíz termina en $+1$.

n11 y n7 no se generan, ni lo que cuelga de n7.

## 5 · Una cota no es un valor

**Piensa: n3 devolvió $+1$ en el primer recorrido. ¿Vale $+1$?**

No. En los dos recorridos, la **raíz** devuelve el valor exacto, $+1$. Los
nodos donde hubo corte, no:

| Nodo y recorrido | Devolvió | Valor exacto | Lo que el algoritmo sabe |
|---|---:|---:|---|
| n3, orden fijo | +1 | −1 | A lo más $+1$ |
| n6, orden invertido | +1 | +1 | Al menos $+1$ |

En el segundo caso el número coincide, pero por suerte: el algoritmo **no
lo sabe**. Un nodo donde se cortó devuelve una **cota**, no un valor. Si
necesitaras el valor exacto de n6, tendrías que generar n11 y n7.

**Punto de control:** deberías poder recorrer un árbol de cuatro niveles
con alfa-beta, anotar $\alpha$ y $\beta$ al llegar a cada nodo, marcar cada
corte como alfa o beta y decir qué estados no se generan. Si te pierdes,
vuelve a la traza de la sección 3 y sigue un renglón a la vez.

## Lo que hay que llevarse

- $\alpha$ es lo que MAX ya tiene asegurado y $\beta$ lo que MIN ya tiene
  asegurado. Se corta en un nodo de MIN cuando $v\le\alpha$ y en uno de MAX
  cuando $v\ge\beta$, con igualdad incluida.
- Lo cortado **no se genera**: alfa-beta recibe las mismas reglas que
  minimax y ahorra justo lo que deja de generar.
- La raíz da el mismo valor que minimax; un nodo donde se cortó solo da una
  cota.
- El orden cambia el ahorro: en n1, 5 estados con el orden fijo y 8 con el
  invertido.

Continúa con [[alfa-beta-como-algoritmo|alfa-beta como algoritmo]].
