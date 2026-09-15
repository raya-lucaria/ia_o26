---
id: resolver-paso-a-paso
title: Resolver, paso a paso
nav_title: Resolver
summary: "Qué sistema hay que resolver cuando hay desigualdades, por qué se resuelve abriendo casos, y el reactor entero resuelto con uno de los dos casos descartado."
status: ready
estimated_time: 24m
tags: [optimizacion, kkt, procedimiento]
---

# Resolver, paso a paso

**¿Y cómo se resuelve esto, con lápiz?**

La página anterior deja el lagrangeano escrito y las cuatro condiciones
enunciadas. Con una igualdad sola, resolverlas fue
[[el-multiplicador|un sistema de cuatro por cuatro]]. Con desigualdades deja de
ser un sistema: pasa a ser **un sistema por cada caso**.

## 1 · Qué hay que resolver, exactamente

::: table {#opt-sistema-kkt title="El sistema completo, y qué aporta cada condición"}
| Condición | Qué aporta | Cuántas |
|---|---|---|
| Estacionariedad | ecuaciones | una por variable |
| Factibilidad de las igualdades | ecuaciones | una por igualdad |
| Factibilidad de las desigualdades | **desigualdades** | una por desigualdad |
| Signo del multiplicador | **desigualdades** | una por desigualdad |
| Holgura complementaria | ecuaciones, pero **con producto** | una por desigualdad |
:::

**Una igualdad aporta una ecuación limpia; una desigualdad aporta un trío**, y de
los tres solo uno es ecuación — y encima con un producto dentro. Ésa es toda la
diferencia, y es la razón de que no se pueda resolver de corrido: las
desigualdades no se despejan ni se sustituyen.

**La salida es la propia holgura complementaria.** Como obliga a que uno de los
dos factores sea cero, se puede **suponer cuál** y ver qué pasa:

- si supones que la restricción **está activa**, escribes $g(x) = d$ y con eso
  tienes una ecuación: el sistema vuelve a ser un sistema;
- si supones que **está inactiva**, escribes $\mu = 0$, que es la otra ecuación
  posible, y el multiplicador se va del sistema.

En los dos casos vuelves a tener tantas ecuaciones como incógnitas. Lo que no
puedes es saber de antemano cuál de los dos es el bueno: **por eso hay que probar
los dos y descartar.**

## 2 · El procedimiento

::: remark {#opt-procedimiento-kkt title="Resolver con KKT, en siete pasos"}
1. **Deja el problema canónico**: cada restricción contra cero.
2. **Escribe el lagrangeano** con el signo que le toca a cada término.
3. **Deriva respecto de cada variable** e iguala a cero: la estacionariedad.
4. **Abre los casos.** Para cada desigualdad, supón activa ($g = d$) o inactiva
   ($\mu = 0$). Con $m$ desigualdades son $2^m$ combinaciones.
5. **Resuelve cada caso** como el sistema de ecuaciones que ahora es.
6. **Descarta.** Tira los casos cuyo punto no sea factible, y los que den un
   multiplicador con el signo prohibido.
7. **Decide.** Lo que sobrevive son candidatos. Si el problema es convexo,
   **todos** los supervivientes son óptimos globales, y normalmente hay uno solo;
   si no es convexo, hay que comparar sus valores y quedarse con el mejor.
:::

> [!WARNING]
> **El paso 4 es el que hace que esto no escale.** Con 3 desigualdades son 8
> casos; con 20, más de un millón; con 100, unos $1.3\times10^{30}$: a un millón
> de casos por segundo, tres millones de veces la edad del universo. A mano solo se
> resuelven juguetes, y por eso los métodos que se usan de verdad **no abren
> casos**: simplex camina por vértices. El procedimiento de aquí es para
> **entender** qué caracteriza al óptimo, no para encontrarlo cuando el problema
> es grande.

## 3 · El reactor, resuelto entero

El problema con la cota, ya canónico:

$$\begin{aligned}
\max \;&\sum_i \left(b_i p_i - \tfrac12 p_i^2\right), \qquad b = (6,8,10) \\
\text{s.a.}\;\; &p_1+p_2+p_3 - 15 = 0, \qquad p_3 - 5 \le 0, \qquad p \ge 0.
\end{aligned}$$

**Pasos 1 a 3.** Es un máximo y la cota quedó $\le 0$, así que los dos términos
restan:

$$\mathcal{L} = \sum_i u_i(p_i) - \lambda\,(p_1+p_2+p_3-15) - \mu\,(p_3-5).$$

Derivando: $b_i - p_i - \lambda = 0$ para $i = 1,2$, y
$b_3 - p_3 - \lambda - \mu = 0$ para el tercero, que es el único que carga las
dos restricciones. Con la igualdad son cinco incógnitas ($p_1$, $p_2$, $p_3$,
$\lambda$ y $\mu$) y cuatro ecuaciones. **Falta una, y la pone el caso.**

**Paso 4. Abre los casos.** Desigualdades hay cuatro: la cota y las tres de no
negatividad. Pero las de no negatividad **se tratan aparte y no entran al
lagrangeano**, como declaró [[los-signos-del-lagrangeano|la página anterior]]; lo
que se hace con ellas es comprobarlas al final, en el paso 6. Así que a efectos
de casos hay **una** desigualdad, y por tanto **dos casos**.

### Caso A: la cota no aprieta

Supón inactiva, o sea $\mu = 0$. Entonces el tercer sistema queda igual que los
otros dos y el problema es el de
[[el-multiplicador|la página del multiplicador]], resuelto ahí: $\lambda = 3$ y

$$p = (3,\,5,\,7).$$

**Y aquí se cae.** La suposición era que la cota no apretaba, pero el punto que
sale tiene $p_3 = 7$, y la cota decía $p_3 \le 5$. **El caso se descarta por
infactible**: el paso 6, haciendo su trabajo.

### Caso B: la cota aprieta

Supón activa, o sea $p_3 = 5$. Ésa es la quinta ecuación, y ahora el sistema
cierra.

**Paso 5.** Con $p_3$ fijo, los otros dos se reparten $15 - 5 = 10$, y siguen
cumpliendo $p_i = b_i - \lambda$:

$$(6-\lambda) + (8-\lambda) = 10
\qquad\Longrightarrow\qquad 14 - 2\lambda = 10
\qquad\Longrightarrow\qquad \lambda = 2,$$

de donde $p_1 = 4$ y $p_2 = 6$. El multiplicador de la cota sale de la tercera
ecuación, que es la única que lo contiene:

$$\mu = b_3 - p_3 - \lambda = 10 - 5 - 2 = 3.$$

**Paso 6. Descarta, o no.** El punto $(4,6,5)$ suma 15, cumple $p_3 \le 5$ con
igualdad, no tiene coordenadas negativas, y $\mu = 3 \ge 0$, que es el signo
permitido. **No hay nada que descartar: este caso sobrevive.**

**Paso 7. Decide.** Es el único superviviente, el objetivo es cóncavo y las
restricciones son afines, así que es el **máximo global**.

::: table {#opt-dos-casos title="Los dos casos, y por qué solo uno sobrevive"}
| | Caso A: $\mu = 0$ | Caso B: $p_3 = 5$ |
|---|---|---|
| Qué se supone | la cota no aprieta | la cota aprieta |
| Punto que sale | $(3,5,7)$ | $(4,6,5)$ |
| ¿Factible? | **no**: $p_3 = 7 > 5$ | sí |
| ¿Signo correcto? | — | sí: $\mu = 3 \ge 0$ |
| Veredicto | **descartado** | **el óptimo** |
:::

Fíjate en cómo se cayó el caso A: no por el signo del multiplicador, sino por
**factibilidad**. Los dos filtros del paso 6 son distintos y hacen falta los dos.

## 4 · Qué garantiza lo que encontraste

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

Por eso el paso 7 dice «decide» y no «ya está»: el procedimiento entrega
candidatos, y quien los convierte en respuesta es la convexidad.

## Lo que hay que llevarse

- Una igualdad aporta una ecuación; una desigualdad aporta un trío, y solo por
  eso hace falta abrir casos.
- El método es: **suponer cuál factor se anula, resolver, y descartar** por
  factibilidad y por signo. Los dos filtros hacen falta.
- $2^m$ casos es una condena: esto sirve para entender el óptimo, no para
  encontrarlo cuando el problema es grande.

Y cuando ni siquiera un caso se puede resolver a mano:
[[bajar-la-pendiente|la página siguiente]].
