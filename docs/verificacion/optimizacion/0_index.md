# Verificación — Modelado y optimización

Registro de fuentes de `course/6_optimizacion/`. Como en complejidad, **un solo
archivo cubre la unidad**: es matemática, no historia, y lo que hay que respaldar
no son fechas sino **convenciones** —qué signo lleva el lagrangeano, qué signo
lleva el multiplicador— y **números**, que se verifican calculándolos.

**Cobertura, dicha por delante:** este registro cubre hoy la **clase 3**. Las
clases 1 y 2 no tienen entrada todavía; sus números están verificados en
`docs/superpowers/verificacion-optimizacion/` (local, no versionado) pero no
trasladados aquí.

Las fuentes bibliográficas se consultaron el **14 de septiembre de 2026**,
descargando y leyendo el PDF o la página original, no resúmenes de buscador.
Donde no se pudo leer el original, se dice.

## La convención de signos del lagrangeano

La regla de la clase —fijar $\lambda \ge 0$ y dejar que el signo de delante lo
decidan dos miradas, mín/máx y $\le 0$/$\ge 0$— tiene sus cuatro casos
respaldados por separado. **Ninguna fuente los presenta juntos en una sola
tabla**; la combinación es de la clase, los casos son de la literatura.

| # | Caso | Fuente | Verificado |
|---|---|---|---|
| 1 | **Máx** con $g \le b$ → el término **resta** | Osborne, *Mathematical methods for economic theory* §7.1: «$L(x) = f(x) - \sum_j \lambda_j(g_j(x) - c_j)$» con «$\lambda_j \ge 0$». Igual en Varian, *Microeconomic Analysis* 3ª ed. §27.5 p. 503 | Sí |
| 2 | **Máx** con $g \ge b$ → el término **suma** | Kuhn y Tucker, *Nonlinear Programming* (1951), §3 pp. 483–484, el artículo original: «To find an $x^0$ that maximizes $g(x)$ constrained by $Fx \ge 0$ […] form the function $\varphi(x,u) \equiv g(x) + u'Fx$», con $u$ no negativo | Sí |
| 3 | **Mín** con $g \le b$ → el término **suma** | Boyd y Vandenberghe, *Convex Optimization* §5.1.1 p. 215: «minimize $f_0(x)$ subject to $f_i(x) \le 0$ […] $L(x,\lambda,\nu) = f_0(x) + \sum \lambda_i f_i(x) + \sum \nu_i h_i(x)$», con $\lambda \succeq 0$ como factibilidad dual (§5.1.3 p. 216) | Sí |
| 4 | **Mín** con $g \ge b$ → el término **resta** | Ireland, *The Kuhn-Tucker and Envelope Theorems* (Boston College) §3.2 p. 19, literal: «where the term involving the multiplier $\lambda$ is **subtracted rather than added in the case of a minimization problem**, the Kuhn-Tucker conditions (1)-(4) continue to apply» | Sí |
| 5 | Cambiar de mín a máx obliga a voltear **también** el sentido de las desigualdades | Chiang y Wainwright, *Fundamental Methods of Mathematical Economics* 4ª ed. §13.1 p. 410: «To minimize $C$ is equivalent to maximizing $-C$ […] **But we must, of course, also reverse the constraint inequalities by multiplying every constraint through by $-1$**» | Sí |
| 6 | El signo de delante es **convención**, no obligación | Wikipedia, «Lagrange multiplier»: «*(In some conventions $\lambda$ is preceded by a minus sign)*» y «the $\lambda$ term **may be either added or subtracted**». Ruye Wang (Harvey Mudd), *Optimization with Inequality Constraints*: «in some literatures, a plus sign is used […] **This is equivalent to our discussion here so long as the sign of $\mu$ […] is negated**» | Sí |
| 7 | Para una **igualdad** el multiplicador no tiene signo obligado | Varian §27.5 p. 503: «the signs of the Kuhn-Tucker multipliers are nonnegative while **the signs of the Lagrange multipliers can be anything**» | Sí |

**Matiz que la página usa y conviene tener escrito.** Boyd escribe
$f_0 + \sum\lambda_i f_i$ con $f_i \le 0$ y Nocedal y Wright escriben
$f - \sum\lambda_i c_i$ con $c_i \ge 0$ (*Numerical Optimization* 2ª ed. §12.1
p. 304 y §12.3 p. 320, con $\lambda_i \ge 0$ en el Teorema 12.1 p. 321). Uno suma
y el otro resta, y **son la misma convención**: los dos minimizan y sus
restricciones están contra cero en sentidos opuestos. La página lo usa como
ejemplo de que los dos volteos se cancelan, y es literal, no una analogía.

**Lo que no se pudo verificar en el original.** Mas-Colell, Whinston y Green, y
Simon y Blume, solo circulan tras registro. La forma $u(x) + \lambda(w - p\cdot x)$
que se les suele atribuir sí se leyó en apuntes que los siguen y los citan
—Nolan Miller (Illinois), *Notes on Microeconomic Theory* cap. 3 p. 44, y Simon
Board (UCLA), Eco11 lect. 3 ec. 3.8—, pero **no se cita a MWG ni a Simon y Blume
porque no se leyeron**.

## Qué mide el multiplicador

| # | Afirmación en la página | Fuente | Verificado |
|---|---|---|---|
| 8 | Con $\lambda \ge 0$, el multiplicador es **cuánto mejora el óptimo por unidad que se afloja** la restricción | En un máximo es directo: Ireland §3.1 p. 18, «the envelope theorem tells us that […] $V'(I) = \lambda^*(I)$», el multiplicador como utilidad marginal del ingreso; Varian ec. (7.10) p. 108, igual. En un mínimo el signo respecto del valor óptimo se invierte: Boyd §5.6.3 ec. (5.58), «$\lambda^*_i = -\partial p^*(0,0)/\partial u_i$». Las dos cosas dicen lo mismo: relajar **baja** un mínimo y **sube** un máximo, y $\lambda \ge 0$ en los dos | Sí |
| 9 | Por qué $\lambda$ no puede ser negativo | Osborne §7.1: «Suppose, to the contrary, that $\lambda < 0$. Then we know that a small decrease in $c$ raises the maximal value of $f$. That is, there is a point $x$ inside the constraint for which $f(x) > f(x^*)$, contradicting the fact that $x^*$ is the solution» | Sí |
| 10 | La lectura del término como **castigo por violar** | No aparece con esas palabras en ningún texto canónico. Formulaciones equivalentes sí: Simon Board, Eco11 lect. 3 p. 12, «a **penalty term which punishes the agent for exceeding her budget**»; Boyd §5.1.4 p. 218, «our displeasure grows as the constraint becomes "more violated"» | Sí, como formulación equivalente |
| 11 | Una restricción **activa** puede tener $\lambda = 0$ | Comprobado por construcción, no citado: maximizar $-(x-1)^2$ sujeto a $x \le 1$ tiene óptimo en $x=1$ con la cota activa y $\lambda = 0$, porque el máximo libre ya estaba en la frontera. Es el caso degenerado | Sí |

## Los números del episodio del reactor

Todos con aritmética exacta de fracciones; el guion está en
`docs/superpowers/verificacion-optimizacion/clase3.py` (local).

| # | Afirmación en la página | Cómo se verificó |
|---|---|---|
| 12 | El óptimo sin cota es $(3,5,7)$, con $\lambda = 3$ y rendimiento $173/2 = 86.5$ | Resuelto por enumeración de patrones activos, **sin usar Lagrange**, para poder comprobar que Lagrange acierta en vez de suponerlo |
| 13 | $U^\ast(P) = -\tfrac16P^2 + 8P + 4$, válida **solo** para $P \ge 6$ | Comparada contra el óptimo real en $P = 6\ldots29$; en $P=3$ la fórmula da $53/2$ y el óptimo real es $103/4$ |
| 14 | $\lambda$ es derivada y no diferencia: $\lambda = 3$ contra $U^\ast(16)-U^\ast(15) = 17/6$ | Calculadas las dos |
| 15 | Con la cota $p_3 \le 5$: $(4,6,5)$, $\lambda = 2$, $\mu_3 = 3$, rendimiento $167/2 = 83.5$ | Íd. **Este registro corrigió un número estimado a ojo**: 83.5, no 84.5 |
| 16 | $\mu_3$ es la derivada del valor óptimo respecto de la cota | Moviendo la cota $\pm\varepsilon$ con fracciones, da 3 |
| 17 | La regla da el mismo término se escriba $p_3 - 5 \le 0$ o $5 - p_3 \ge 0$ | Las dos escrituras dan $\mu_3 = 3$ |
| 18 | Los tres pasos del descenso desde $(0,0)$ con $\alpha = 1/10$, y los factores $4/5$ y $1/5$ | Iterados con fracciones; los factores se comprueban en **todos** los pasos, no en los tres que la tabla muestra |
| 19 | El descenso converge exactamente cuando $0 < \alpha < 1/4$ | Comprobado por lo que **hace** la sucesión, no derivando el factor: con $\alpha$ justo por debajo encoge, justo por encima crece, y en $1/4$ la coordenada $y$ se queda a distancia 2 alternando signo mientras la $x$ sí converge |

## Fuentes

- Boyd y Vandenberghe, *Convex Optimization* (Cambridge, 2004) — <https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf>
- Nocedal y Wright, *Numerical Optimization*, 2ª ed. (Springer, 2006)
- Kuhn y Tucker, *Nonlinear Programming* (1951)
- Varian, *Microeconomic Analysis*, 3ª ed.
- Chiang y Wainwright, *Fundamental Methods of Mathematical Economics*, 4ª ed.
- Osborne, *Mathematical methods for economic theory* — <https://mjo.osborne.economics.utoronto.ca/>
- Ireland, *The Kuhn-Tucker and Envelope Theorems* (Boston College) — <http://irelandp.com/econ7720/notes/notes1.pdf>
- Nolan Miller, *Notes on Microeconomic Theory* (Illinois); Simon Board, Eco11 (UCLA)
- Ruye Wang, *Optimization with Inequality Constraints* (Harvey Mudd)
- Wikipedia, «Lagrange multiplier» y «Karush–Kuhn–Tucker conditions»
