---
id: los-signos-del-lagrangeano
title: Los signos del lagrangeano
nav_title: Signos y KKT
summary: "Con qué signo entra cada restricción en el lagrangeano y qué signo tiene su multiplicador, con una regla de dos miradas que decide las dos cosas sin memorizar casos."
status: ready
estimated_time: 28m
tags: [optimizacion, kkt, lagrange, signos]
---

# Los signos del lagrangeano

**¿Con qué signo entra cada restricción, y qué signo tiene su multiplicador?**

Falta la cota que la bitácora dejó pendiente: el soporte vital no aguanta más de
cinco. Es una **desigualdad**, y con ella llega la pregunta que más confusión
causa de toda la unidad.

Abre dos libros y verás $\mathcal{L} = f + \mu g$ en uno y
$\mathcal{L} = f - \mu g$ en el otro, sin que ninguno esté mal. Esta página
da la regla que decide, y de paso explica por qué los dos libros tienen razón.

## 1 · Escribir el lagrangeano

### El problema canónico

Antes de elegir ningún signo, el problema entero se escribe en una sola forma. Es
[[escribir-el-modelo|la forma canónica de la clase 1]] —objetivo arriba, una
restricción por renglón, el dominio al final— con **un paso más: cada restricción
también contra cero**.

$$\begin{aligned}
\max_{x} \;\text{ o }\; \min_{x} \quad & f(x) && \text{el objetivo} \\
\text{sujeto a} \quad & h_j(x) - c_j = 0 && j = 1,\dots,r \\
& g_i(x) - d_i \le 0 \;\text{ o }\; g_i(x) - d_i \ge 0 && i = 1,\dots,m \\
& x \in X && \text{el dominio}
\end{aligned}$$

**Por qué esta forma y no otra.** Porque la regla de los signos lee exactamente
dos cosas, y las dos solo son visibles cuando el problema está así escrito:

- **El sentido de la optimización**, que vive en el primer renglón y vale para
  **todo** el problema. Es una sola decisión: o maximizas o minimizas.
- **El sentido de cada restricción contra cero**, que vive en su propio renglón y
  puede ser **distinto en cada una**. Un mismo problema puede tener unas $\le 0$
  y otras $\ge 0$, y cada una se decide por separado.

Esa asimetría es la razón de que la regla sea un cuadro de dos por dos y no una
sola respuesta: el máximo o mínimo lo fijas una vez y te acompaña hasta el final;
el sentido de la restricción lo vuelves a mirar en cada renglón.

El dominio $x \in X$ (la no negatividad, casi siempre) se queda donde está y **no
entra al lagrangeano** en esta unidad: es una restricción como las demás y podría
llevar su propio multiplicador, pero aquí se trata aparte, igual que en
[[cuando-se-acaba-el-dibujo|la clase 2]].

### La restricción contra cero

De ese paso extra sale todo lo demás, así que vale la pena aislarlo.

::: definition {#opt-contra-cero title="Dejar una restricción contra cero"}
**Pasa toda la restricción a un lado y compárala con cero.** Es el mismo
movimiento que ya hiciste en [[tres-bitacoras|las bitácoras de práctica]], donde
«la telemetría al menos el doble que los datos» se escribió $2d - t \le 0$.

Contra cero solo quedan tres formas, y solo tres:

$$h(x) - c = 0, \qquad g(x) - d \le 0, \qquad g(x) - d \ge 0.$$
:::

> [!WARNING]
> **Mira hacia dónde quedó la restricción, no el signo de la constante.** El error típico
> es decidir el signo del lagrangeano por cómo venía escrita la frase, o por si
> la constante es positiva o negativa. Ninguna de las dos cosas importa: lo
> único que cuenta es si, ya contra cero, la restricción quedó $\le 0$ o
> $\ge 0$.

**Y no importa hacia qué lado la pases.** Una misma restricción se puede dejar
contra cero de dos maneras ($p_3 - 5 \le 0$ o $5 - p_3 \ge 0$), y la regla de
abajo les asigna signos de delante distintos. Da igual: el término que resulta es
**el mismo**, porque también se volteó el paréntesis, y el multiplicador sale
idéntico por los dos caminos.

### La regla, en dos miradas

::: definition {#opt-lagrangeano-general title="El lagrangeano, con el multiplicador siempre no negativo"}
En estas notas, para cada **desigualdad**, **se fija $\mu \ge 0$** y se deja que el
signo de delante se acomode. Para cada restricción:

1. déjala contra cero;
2. mira si el problema es de **mínimo o de máximo**;
3. mira si quedó **$\le 0$ o $\ge 0$**.

Con esas dos miradas, el signo de delante está decidido, y el multiplicador de esa
desigualdad sale no negativo siempre. (El de una **igualdad** es otra cosa: se
llama $\lambda$ y no tiene signo obligado.)
:::

::: table {#opt-regla-signos title="El signo de delante, caso por caso"}
| Problema | Restricción original | Contra cero | Lagrangeano |
|---|---|---|---|
| **Mín** $f$ | $g(x) \le d$ | $g(x) - d \le 0$ | $\mathcal{L} = f + \mu\,(g-d)$ |
| **Mín** $f$ | $g(x) \ge d$ | $g(x) - d \ge 0$ | $\mathcal{L} = f - \mu\,(g-d)$ |
| **Máx** $f$ | $g(x) \le d$ | $g(x) - d \le 0$ | $\mathcal{L} = f - \mu\,(g-d)$ |
| **Máx** $f$ | $g(x) \ge d$ | $g(x) - d \ge 0$ | $\mathcal{L} = f + \mu\,(g-d)$ |
:::

Los cuatro renglones caben en un cuadro de dos por dos. El signo de la casilla es
el que va **antes de $\mu$**:

::: table {#opt-atajo-signos title="El atajo mental"}
| | Restricción $\le 0$ | Restricción $\ge 0$ |
|---|---:|---:|
| **Minimizar** | $+\mu$ | $-\mu$ |
| **Maximizar** | $-\mu$ | $+\mu$ |
:::

**Fíjate en que no son dos reglas sino una:** el signo es el **producto** de las
dos miradas. Cambiar una sola lo voltea; cambiar las dos lo deja igual — que es
exactamente lo que pasa al pasar la misma restricción contra cero por el otro
lado.

**Y no hace falta memorizar el cuadro, porque las cuatro casillas salen de una
sola idea:** el término se escribe de modo que **violar la restricción empeore el
objetivo**. Para ver cuál toca, mira dos cosas: qué signo toma $(g-d)$ cuando la
restricción se viola, y qué significa empeorar en tu problema.

- **Máx con $g-d \le 0$.** Violarla es que $g$ se pase de $d$, así que $(g-d)$ se
  vuelve **positivo**. En un máximo, empeorar es **bajar**. Ese positivo hay que
  **restarlo**.
- **Máx con $g-d \ge 0$.** Violarla es que $g$ se quede corto, así que $(g-d)$ se
  vuelve **negativo**. Y sumar un negativo **baja**. Hay que **sumarlo**.
- **Mín con $g-d \le 0$.** Violarla hace $(g-d)$ **positivo**, y en un mínimo
  empeorar es **subir**. Sumar un positivo sube: hay que **sumarlo**.
- **Mín con $g-d \ge 0$.** Violarla hace $(g-d)$ **negativo**, y restar un
  negativo **sube**, que es empeorar. Hay que **restarlo**.

En los cuatro el castigo apunta al mismo lado; lo único que cambia es hacia dónde
queda «peor» y con qué signo llega el paréntesis.

> [!NOTE]
> **Por qué dos libros serios parecen contradecirse.** Boyd y Vandenberghe
> minimizan con las restricciones escritas $f_i(x) \le 0$ y escriben
> $\mathcal{L} = f_0 + \sum \lambda_i f_i$, sumando. Nocedal y Wright también
> minimizan, pero escriben sus restricciones $c_i(x) \ge 0$, y su lagrangeano es
> $\mathcal{L} = f - \sum \lambda_i c_i$, restando. Uno suma y el otro resta, los
> dos exigen que ese multiplicador (su $\lambda$ es nuestra $\mu$) sea $\ge 0$, y
> **los dos usan exactamente la misma convención**:
> son los dos renglones de «Mín» del cuadro de arriba.
>
> Y el renglón que más raro se ve (máximo con $\ge$, que suma) es el del
> **artículo original de Kuhn y Tucker**, de 1951: maximizan $g(x)$ sujeto a
> $Fx \ge 0$ y forman $\varphi(x,u) = g(x) + u'Fx$ con $u$ no negativo. Los
> cuatro renglones del cuadro están en la literatura; lo que no suele estar es
> los cuatro juntos.

Con el multiplicador anclado en no negativo, el número deja de depender de la
escritura y pasa a medir siempre lo mismo:

::: theorem {#opt-mu-mejora title="Qué mide el multiplicador"}
Con la regla de arriba, para cada desigualdad, $\mu$ es la **derivada del
valor óptimo** respecto del lado derecho de esa restricción, con el signo puesto
de modo que **aflojar cuente como mejorar**.

Y por eso $\mu \ge 0$: aflojar nunca puede empeorar. Aflojar es **subir** el
lado derecho si la restricción quedó $\le 0$, y **bajarlo** si quedó $\ge 0$.

En un máximo «mejorar» es subir y en un mínimo es bajar, y el enunciado no
cambia: en los cuatro casos $\mu$ es la tasa a la que mejora el óptimo.
:::

> [!WARNING]
> **Es una tasa, no lo que rinde una unidad entera.** Es la misma distinción que
> [[el-multiplicador|la página anterior]] puso en el centro, y aquí vuelve a
> morder con los mismos números: en el reactor con cota sale $\mu_3 = 3$, y sin
> embargo subir la cota de 5 a 6 rinde **2.25**. El 3 es la pendiente en ese
> punto; la unidad entera paga menos porque la curva se dobla mientras la
> recorres.

## 2 · Holgura complementaria: apretar o no apretar

::: definition {#opt-kkt title="Las condiciones KKT"}
Un punto y sus multiplicadores cumplen las condiciones de
**Karush–Kuhn–Tucker** si cumplen las cuatro:

1. **Estacionariedad**: $\nabla_x \mathcal{L} = 0$.
2. **Factibilidad**: el punto cumple todas las restricciones.
3. **Signo**: $\mu \ge 0$ para cada desigualdad; el $\lambda$ de una **igualdad**
   es libre.
4. **Holgura complementaria**: $\mu\,\bigl(g(x) - d\bigr) = 0$ para cada
   desigualdad.
:::

Las tres primeras son las de siempre, escritas con el signo de la sección
anterior. **La cuarta es la que solo aparece con desigualdades**, y es la que
convierte todo esto en algo que se puede resolver. Vale la pena leerla despacio,
porque es un producto igualado a cero: **uno de los dos factores tiene que
anularse**.

- Si la restricción **no se cumple con igualdad** (sobra, hay holgura: $g(x) < d$
  si quedó $\le 0$, y $g(x) > d$ si quedó $\ge 0$), entonces el paréntesis no es
  cero, así que el que tiene que anularse es el
  otro: $\mu = 0$, **obligatoriamente**. Lo que sobra no se paga.
- Si la restricción **sí se cumple con igualdad** (aprieta: $g(x) = d$), entonces
  el paréntesis ya es cero y el producto se anula solo. El multiplicador queda
  **libre dentro de su signo**: puede ser positivo, y también puede ser cero.
- Leído al revés, que es como más sirve: **si $\mu > 0$, la restricción está
  activa**, sin necesidad de volver a mirar el punto. Un multiplicador positivo
  es un certificado de que esa restricción aprieta.

Los cuatro casos caben en un cuadro, y **una de las casillas es imposible**: ésa
es exactamente la holgura complementaria.

::: table {#opt-implicaciones title="Qué puede pasar, y qué no"}
| | $\mu = 0$ | $\mu > 0$ |
|---|---|---|
| **$g(x) < d$** — no se cumple con igualdad | El caso normal: sobra, y conseguir más no vale nada | **Imposible** |
| **$g(x) = d$** — se cumple con igualdad | Posible, y es el caso **degenerado**: se toca pero no empuja | El caso normal: aprieta, y aflojar pagaría $\mu$ |
:::

> [!NOTE]
> **La casilla de abajo a la izquierda es la que sorprende, y existe.** Que una
> restricción esté activa no obliga a que su multiplicador sea positivo.
> Maximiza $-(x-1)^2$ sujeto a $x \le 1$: el óptimo es $x = 1$, la cota se cumple
> con igualdad, y aun así $\mu = 0$, porque aflojarla no mejora nada — el
> máximo libre ya estaba justo ahí.
>
> Tiene consecuencia práctica: **un recurso puede agotarse exacto y no valer nada
> conseguir más.** Si lees el multiplicador y no el punto, no te confundes.

**Y la igualdad se queda fuera de este cuadro**, porque no tiene dónde caer:
$h(x) = c$ está activa siempre, por definición, así que su holgura complementaria
se cumple sola y su multiplicador nunca queda obligado a cero ni a un signo.

## 3 · El reactor con su cota

Con la cota, el problema queda

$$\begin{aligned}
\max \;&\sum_i \left(b_i p_i - \tfrac12 p_i^2\right) \\
\text{s.a.}\;\; &p_1+p_2+p_3 = 15,\quad p_3 \le 5,\quad p \ge 0.
\end{aligned}$$

Las dos miradas: es un **máximo**, y la cota contra cero queda $p_3 - 5 \le 0$.
Casilla inferior izquierda del atajo: **restando**. La igualdad lleva su propio
multiplicador, libre de signo, y se escribe restando también para que valga lo
que ya valía en [[el-multiplicador|la página anterior]]:

$$\mathcal{L} = \sum_i u_i(p_i) - \lambda\,(p_1+p_2+p_3-15) - \mu_3\,(p_3 - 5).$$

La estacionariedad da $b_i - p_i = \lambda$ para escudos y motores, y
$b_3 - p_3 = \lambda + \mu_3$ para el soporte vital. **Suponiendo que la cota
aprieta** ($p_3 = 5$), que es lo que [[resolver-paso-a-paso|la página siguiente]]
comprueba en vez de suponer, sale

$$p = (4,\,6,\,5), \qquad \lambda = 2, \qquad \mu_3 = 3.$$

::: table {#opt-kkt-reactor title="El reparto con cota, y qué dice cada multiplicador"}
| | Sin cota | Con $p_3 \le 5$ |
|---|---:|---:|
| Reparto | $(3,5,7)$ | $(4,6,5)$ |
| Rendimiento | 86.5 | 83.5 |
| $\lambda$: derivada respecto de la potencia total | 3 | **2** |
| $\mu_3$: derivada respecto de la cota | no aplica | **3** |
| Lo que rinde de verdad **una unidad entera** más de potencia | $17/6 = 2.83…$ | $7/4 = 1.75$ |
:::

Los dos números se leen solos, **con el cuidado de la advertencia de arriba**.
$\mu_3 = 3$ dice que la cota está activa y empuja, y que **al margen** paga 3;
subirla de 5 a 6 completa paga 2.25. Y $\lambda$ **baja de 3 a 2**: con el mejor
sistema tapado, la potencia extra vale menos, porque ya no puede irse a donde más
rendía. La cota, en total, cuesta $86.5 - 83.5 = 3$.

## 4 · Por qué el signo es el que es

::: definition {#opt-normal-exterior title="Normal exterior"}
La **normal exterior** de una restricción es el gradiente de su función,
$\nabla g_i$ cuando la restricción quedó $\le 0$, y $-\nabla g_i$ cuando quedó
$\ge 0$. Sale de la frontera en ángulo recto (igual que $\nabla h$ en
[[el-multiplicador|la página anterior]]) y apunta hacia **el lado prohibido**: en
el primer caso, la dirección en la que $g_i$ crece, que es lo que la restricción
no permite.
:::

En un máximo con restricciones $\le$, la estacionariedad dice que $\nabla f$ es
una combinación **con coeficientes no negativos** de las normales exteriores de
las restricciones activas. Con una sola restricción activa se ve de inmediato:
un coeficiente negativo pondría la flecha del objetivo apuntando hacia adentro, y
hacia adentro siempre se puede caminar, así que el punto no sería óptimo. Con
varias activas la conclusión es la misma pero el dibujo ya no basta para
probarla; hace falta un resultado sobre conos que esta unidad no cubre.

::: figure {#opt-normales title="El gradiente del objetivo, escrito con las normales activas"}
![El polígono de la clase 1 con su esquina óptima; desde ella salen las dos normales de las restricciones activas y la flecha del objetivo, que es la diagonal del paralelogramo que forman](../_assets/opt-normales.svg)
:::

Ese dibujo es el óptimo de la impresora, y los coeficientes **2 y 1** no son
nuevos: son los precios sombra que [[cuanto-vale-una-hora-mas|la clase 2]]
calculó para las horas y el polímero. La energía, que sobraba, tiene
multiplicador cero — holgura complementaria, otra vez. **Los precios sombra de la
programación lineal son los multiplicadores KKT del problema lineal**, y eso
demuestra lo que la clase 2 prometió: que siempre existan no es casualidad, sino
el teorema que [[resolver-paso-a-paso|la página siguiente]] enuncia, aplicado al
caso de restricciones que son rectas y planos.

::: table {#opt-convenciones-kkt title="La misma cuenta, en el papel y en el código"}
| Dónde | Cómo se escribe | Qué sale |
|---|---|---|
| Estas notas y los libros | el signo de delante según @opt-atajo-signos | $\mu \ge 0$ siempre |
| `scipy` | minimiza, y los multiplicadores que devuelve son los de **ese** mínimo | los precios sombra de un máximo son $-\texttt{marginals}$ |
:::

Ese último renglón explica un tropiezo de la clase 2: `linprog` devuelve $-2$
donde la página enseña 2. No es un error del solver ni de la página: **es el
mismo número visto desde el problema minimizado**.

## Lo que hay que llevarse

- Primero la restricción **contra cero**; sin ese paso, ninguna regla de signos
  significa nada.
- Dos miradas deciden el signo de delante: **mín o máx**, y **$\le 0$ o
  $\ge 0$**. Con eso, $\mu \ge 0$ siempre.
- El multiplicador mide **la tasa a la que mejora el óptimo al aflojar**, que no
  es lo que paga una unidad entera. Vale cero cuando la restricción no se toca, y
  también puede valer cero tocándola.

Ya sabes qué escribir. Falta resolverlo:
[[resolver-paso-a-paso|la página siguiente]].
