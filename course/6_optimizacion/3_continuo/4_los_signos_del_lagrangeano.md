---
id: los-signos-del-lagrangeano
title: Los signos del lagrangeano
nav_title: Signos y KKT
summary: "Cómo se escribe el lagrangeano con igualdades y con desigualdades, por qué a veces el multiplicador entra restando y a veces sumando, y qué signo le toca en cada caso."
status: ready
estimated_time: 30m
tags: [optimizacion, kkt, lagrange, signos]
---

# Los signos del lagrangeano

**¿Con qué signo entra cada restricción, y qué significa el número que sale?**

Falta la cota que la bitácora dejó pendiente: el soporte vital no aguanta más de
cinco. Es una **desigualdad**, y con ella llega la pregunta que más confusión
causa de toda la unidad.

## 1 · Un solo lagrangeano para los tres sentidos

Abre cualquier libro y verás $\mathcal{L} = f + \lambda g$ en uno y
$\mathcal{L} = f - \lambda g$ en el siguiente, sin que ninguno de los dos esté
mal. Conviene entender por qué antes de fijar el de estas notas.

::: definition {#opt-lagrangeano-general title="El lagrangeano, con igualdades y desigualdades"}
En estas notas las restricciones se escriben siempre con la constante a la
derecha —$h_j(x) = c_j$, $g_i(x) \le b_i$ o $g_i(x) \ge b_i$— y el lagrangeano
lleva **todos los términos restando**:

$$\begin{aligned}
\mathcal{L}(x,\lambda,\mu) = f(x)
&\;-\; \sum_j \lambda_j\bigl(h_j(x) - c_j\bigr) \\
&\;-\; \sum_i \mu_i\bigl(g_i(x) - b_i\bigr).
\end{aligned}$$

Pedir $\nabla_x\mathcal{L} = 0$ es pedir

$$\nabla f(x) = \sum_j \lambda_j \nabla h_j(x) + \sum_i \mu_i \nabla g_i(x).$$

Una variable nueva por restricción: $\lambda$ para las igualdades, $\mu$ para las
desigualdades.
:::

::: table {#opt-letras-kkt title="Qué es cada letra, para no tener que adivinarlo"}
| Letra | Qué es |
|---|---|
| $f$ | El objetivo, lo que se maximiza |
| $h_j$, $c_j$ | La función y el lado derecho de la **igualdad** $j$ |
| $g_i$, $b_i$ | La función y el lado derecho de la **desigualdad** $i$ |
| $\lambda_j$ | El multiplicador de la igualdad $j$ |
| $\mu_i$ | El multiplicador de la desigualdad $i$ |
:::

En el reactor con su cota hay una de cada una: $h(p) = p_1+p_2+p_3$ con $c = 15$,
y $g(p) = p_3$ con $b = 5$.

### Qué va dentro del paréntesis, y qué signo lleva delante

Son las dos decisiones que hay que tomar para **escribir** $\mathcal{L}$, y
ninguna se deduce: se eligen. Lo que no se elige es la consecuencia.

**Dentro del paréntesis va el lado izquierdo menos el derecho.** Siempre
$(g(x) - b)$, y no $(b - g(x))$, por una razón práctica: así el paréntesis vale
**cero exactamente cuando la restricción está apretada**. En el reactor,
$(p_3 - 5)$ se anula cuando el soporte vital está pegado a su tope, y por eso la
holgura complementaria de la sección 3 se lee de un golpe.

**Delante va restando.** Tampoco es capricho: es lo que hace que $\mu$ **sea** el
precio sombra en vez de su negativo, que es el teorema de la sección siguiente.

**Y las dos decisiones se compensan entre sí**, que es la razón de que veas el
mismo problema escrito de cuatro maneras sin que ninguna esté mal:

::: table {#opt-cuatro-escrituras title="Las cuatro maneras de escribir el mismo término"}
| Cómo lo escribes | Qué es | Qué mide su multiplicador |
|---|---|---|
| $f - \mu\,(g - b)$ | **la de estas notas** | $\partial f^\ast/\partial b$ |
| $f + \mu\,(b - g)$ | idéntica a la de arriba | $\partial f^\ast/\partial b$ |
| $f + \mu\,(g - b)$ | la primera con el signo volteado | $-\partial f^\ast/\partial b$ |
| $f - \mu\,(b - g)$ | idéntica a la de arriba | $-\partial f^\ast/\partial b$ |
:::

Los renglones van en pares porque **voltear el paréntesis y voltear el signo de
delante son la misma operación**: cada una por separado cambia $\mu$ por
$-\mu$, y hacer las dos deja todo igual.

**¿Y qué tiene que ver con maximizar o minimizar? Nada — y por eso confunde.**
El signo de delante se puede elegir igual en los dos casos. Lo que sí depende de
si maximizas o minimizas es **qué signo acaba teniendo el multiplicador**, que es
la tabla de la sección siguiente. El enredo viene de que la costumbre de los
libros es elegir el signo de delante **para que el multiplicador salga no
negativo**, y como eso depende del sentido de la optimización y del de la
desigualdad, cada libro escribe una cosa distinta. Estas notas hacen lo
contrario: fijan el signo de delante, y dejan que el multiplicador salga con el
signo que le toque — porque así el número significa algo.

**El reactor con su cota, escrito de las tres formas.** El óptimo es $(4,6,5)$ en
las tres, y lo único que se mueve son los signos de los multiplicadores:

| Lagrangeano | $\lambda$ | $\mu_3$ |
|---|---:|---:|
| $f - \lambda\,(p_1+p_2+p_3-15) - \mu_3\,(p_3-5)$ | $2$ | $3$ |
| $f + \lambda\,(15-p_1-p_2-p_3) + \mu_3\,(5-p_3)$ | $2$ | $3$ |
| $f + \lambda\,(p_1+p_2+p_3-15) + \mu_3\,(p_3-5)$ | $-2$ | $-3$ |

**No hay un signo correcto: hay una convención, y lo que cambia con ella es qué
significa el número que sale.** Elige una, escríbela una vez, y no la cambies a
media hoja.

## 2 · De dónde sale el signo

Escrito como arriba, el multiplicador no es un residuo del método: es una
cantidad con significado, y de ahí sale su signo sin memorizar nada.

::: theorem {#opt-mu-derivada title="Cada multiplicador es la derivada del valor óptimo respecto de su lado derecho"}
Con el lagrangeano de arriba, y llamando $f^\ast(b_i)$ al valor óptimo cuando se
mueve el lado derecho de la restricción $i$,

$$\mu_i = \frac{\partial f^\ast}{\partial b_i}.$$

Vale igual si el problema maximiza o minimiza, y es
[[el-multiplicador|el mismo enunciado de la página anterior]] extendido a las
desigualdades.
:::

Entonces el signo sale de dos preguntas, las dos sobre el mundo y ninguna sobre
la notación: **¿subir $b$ afloja o aprieta?** y **¿el problema maximiza o
minimiza?**

::: table {#opt-tabla-signos title="El signo del multiplicador, caso por caso"}
| Problema | Restricción | Subir $b$… | Signo |
|---|---|---|---|
| máximo | $g(x) \le b$ | afloja | $\mu \ge 0$ |
| máximo | $g(x) \ge b$ | aprieta | $\mu \le 0$ |
| mínimo | $g(x) \le b$ | afloja | $\mu \le 0$ |
| mínimo | $g(x) \ge b$ | aprieta | $\mu \ge 0$ |
:::

Lee el primer renglón despacio, que es el de esta unidad: en un máximo, aflojar
un recurso **no puede empeorar** el óptimo, así que su derivada no es negativa.
El tercero es el mismo argumento con el objetivo cambiado de signo: aflojar
tampoco puede empeorar, y en un mínimo «no empeorar» es **bajar**.

> [!NOTE]
> **La igualdad no tiene signo, y ninguna convención puede dárselo.** $h(x) = c$
> no se afloja ni se aprieta: moverla puede subir o bajar el valor óptimo, según
> hacia dónde. Y hay un argumento de una línea que lo cierra: $h - c = 0$ y
> $c - h = 0$ son **la misma restricción**, y sus multiplicadores son opuestos.
> Un signo fijo tendría que ser positivo y negativo a la vez.
>
> Por eso $\lambda$ es **libre**, y el reactor no lo delata: ahí sale positivo
> las dos veces.

## 3 · La cota del soporte vital

Con la cota, el problema del reactor queda

$$\begin{aligned}
\max \;&\sum_i \left(b_i p_i - \tfrac12 p_i^2\right) \\
\text{s.a.}\;\; &p_1+p_2+p_3 = 15,\quad p_3 \le 5,\quad p \ge 0,
\end{aligned}$$

y su lagrangeano, con la convención de arriba, es
$\mathcal{L} = \sum_i u_i(p_i) - \lambda(p_1+p_2+p_3-15) - \mu_3(p_3 - 5)$.

::: definition {#opt-kkt title="Las condiciones KKT"}
Un punto y sus multiplicadores cumplen las condiciones de
**Karush–Kuhn–Tucker** si cumplen las cuatro:

1. **Estacionariedad** — $\nabla_x \mathcal{L} = 0$.
2. **Factibilidad** — el punto cumple todas las restricciones.
3. **Signo** — cada $\mu_i$ tiene el signo que le toca en
   @opt-tabla-signos; $\lambda_j$ es libre.
4. **Holgura complementaria** — $\mu_i\,(g_i(x) - b_i) = 0$ para cada
   desigualdad: o la restricción está activa, o su multiplicador es cero. Dicho
   en corto: **una restricción que no se toca no empuja**.
:::

Resolviendo: la estacionariedad da $b_i - p_i = \lambda$ para escudos y motores,
y $b_3 - p_3 = \lambda + \mu_3$ para el soporte vital. Con la cota activa
—$p_3 = 5$— sale

$$p = (4,\,6,\,5), \qquad \lambda = 2, \qquad \mu_3 = 3.$$

::: table {#opt-kkt-reactor title="El reparto con cota, y qué dice cada multiplicador"}
| | Sin cota | Con $p_3 \le 5$ |
|---|---:|---:|
| Reparto | $(3,5,7)$ | $(4,6,5)$ |
| Rendimiento | 86.5 | 83.5 |
| $\lambda$ — vale una unidad más de potencia | 3 | **2** |
| $\mu_3$ — vale una unidad más de cota | — | **3** |
:::

Los dos números se leen solos. **$\mu_3 = 3 > 0$**: la cota está activa y
empuja, y subirla una unidad rendiría 3 más. **$\lambda$ baja de 3 a 2**: con el
mejor sistema tapado, la potencia extra vale menos, porque ya no puede irse a
donde más rendía. Y la cota cuesta exactamente $86.5 - 83.5 = 3$.

## 4 · Qué garantizan, y cómo se traduce

::: theorem {#opt-teo-kkt title="Qué garantiza KKT, y dónde deja de garantizarlo"}
Si el objetivo es diferenciable y **todas las restricciones son afines** —rectas
y planos, como en toda esta unidad—, las condiciones KKT son **necesarias** en
todo óptimo local, sin pedir nada más.

Si además el objetivo es **cóncavo y se maximiza** sobre restricciones afines,
entonces cualquier punto que las cumpla es un **máximo global**: aquí son
necesarias y suficientes.

Fuera de ese caso, KKT solo produce **candidatos**.
:::

> [!WARNING]
> **Dos cosas que la versión de receta no dice.** Que las condiciones sean
> «necesarias» no es gratis: sin restricciones afines hace falta una hipótesis
> extra, y minimizar $x$ sujeto a $x^2 = 0$ tiene óptimo y **no** tiene
> multiplicador. Y la diferenciabilidad tampoco: $\min(x,\,2-x)$ es cóncava y no
> es derivable en $x=1$, que es justo donde está su máximo. En esta unidad las
> dos hipótesis se cumplen siempre; fuera de ella, hay que mirarlas.

**Y el dibujo de por qué el signo no puede ser otro.** A $\nabla g_i$ se le llama
la **normal exterior** de esa restricción: sale de su frontera en ángulo recto
—igual que $\nabla h$ en [[el-multiplicador|la página anterior]]— y apunta hacia
el lado prohibido, porque es la dirección en la que $g_i$ crece y la restricción
pide que no crezca.

En un máximo con restricciones $\le$, la estacionariedad dice entonces que
$\nabla f$ es una combinación **con coeficientes no negativos** de las normales
exteriores de las restricciones activas. Con un coeficiente negativo, la flecha
del objetivo apuntaría hacia adentro de la región — y hacia adentro siempre se
puede caminar, así que el punto no sería óptimo.

::: figure {#opt-normales title="El gradiente del objetivo, escrito con las normales activas"}
![El polígono de la clase 1 con su esquina óptima; desde ella salen las dos normales de las restricciones activas y la flecha del objetivo, que es la diagonal del paralelogramo que forman](../_assets/opt-normales.svg)
:::

Ese dibujo es el óptimo de la impresora, y los coeficientes **2 y 1** no son
nuevos: son los precios sombra que [[cuanto-vale-una-hora-mas|la clase 2]]
calculó para las horas y el polímero. La energía, que sobraba, tiene
multiplicador cero — holgura complementaria, otra vez. **Los precios sombra de la
programación lineal son los multiplicadores KKT del problema lineal**, y eso
demuestra lo que la clase 2 prometió: que siempre existen no es casualidad, es el
teorema de arriba aplicado al caso afín.

::: table {#opt-convenciones-kkt title="La misma cuenta en tres convenciones"}
| Dónde | Cómo se escribe | Qué sale |
|---|---|---|
| Estas notas | máximo, $g \le b$, $\mathcal{L} = f - \mu(g-b)$ | $\mu$ **es** el precio sombra, con su signo |
| Forma estándar de los libros | mínimo, $g(x) \le 0$, $\mathcal{L} = f + \mu g$ | $\mu \ge 0$ siempre: el signo ya se absorbió al pasar a la forma estándar. Es **menos** el de aquí |
| `scipy` | minimiza, y devuelve los duales de ese mínimo | los precios sombra del máximo son $-\texttt{marginals}$ |
:::

Ese último renglón es el que explica un tropiezo de la clase 2: `linprog`
devuelve $-2$ donde la página enseña 2. No es un error del solver ni de la
página: **son el mismo número en dos convenciones**, y ahora se sabe cuál es
cuál.

## Lo que hay que llevarse

- El lagrangeano no tiene un signo correcto: tiene una convención. Voltear el
  término y voltear la desigualdad es la misma operación, y hacer las dos no
  cambia nada.
- Con los términos restando, cada multiplicador **es** la derivada del valor
  óptimo respecto de su lado derecho, y de ahí sale su signo: aflojar o apretar,
  maximizar o minimizar.
- Una restricción que no se toca no empuja, y su multiplicador es cero.

Falta el caso en que estas condiciones no se pueden resolver a mano:
[[bajar-la-pendiente|la página siguiente]].
