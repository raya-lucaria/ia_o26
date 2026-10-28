---
id: mkv-decidir-sin-ver
title: "Decidir sin ver el estado"
nav_title: "Decidir sin ver"
summary: "Del MDP con el estado visible al problema con estado oculto: decidir con la creencia, el valor de mirar y la creencia como estado."
status: ready
estimated_time: 40m
tags: [markov, ocultas, decidir, pomdp]
---

# Decidir sin ver el estado

**Si no ves el estado, ¿qué haces? ¿Y cuánto vale poder verlo?**

Al terminar tendrás:

- **El repaso:** política, valor y costo al decidir sobre el paraguas con el clima visible.
- **El problema de un día:** qué eliges, en qué orden y cuándo termina.
- **Una regla:** elegir con la creencia $b$ la acción de menor costo esperado. En el paraguas, llevar si $b>1/4$.
- **Un precio y un valor:** cuándo conviene pagar $1/2$ por mirar. Por qué el precio difiere del valor de ver el clima.
- **Un puente:** la creencia como estado de un MDP y la relación entre Viterbi y Bellman.

## Lo que traes

- **Decidir viendo.** En [[mkv-el-mdp|El proceso de decisión de Markov]] el agente veía $s$, elegía una acción y recibía $r(s,a)$. La política $\pi$ indica qué hacer en cada estado.
- **El máximo.** En [[mkv-bellman|La ecuación de Bellman]] eliges desde $s$ considerando la recompensa inmediata y el mejor valor futuro esperado.
- **Bayes.** En [[mkv-bayes-y-normalizar|Bayes y normalizar]], partiste del prior $(1/2,1/2)$. Con paraguas, la probabilidad de lluvia quedó en $9/11$; sin paraguas, en $1/9$.
- **La creencia.** En [[mkv-filtrar|Filtrar y predecir]] calculaste $b_t(s)=\Pr(S_t=s\mid O_{0:t})$ cada día: $b_0(\text{lluvia})=9/11$ y, con otro paraguas, $b_1(\text{lluvia})=621/703$.
- **Viterbi.** En [[mkv-decodificar|Decodificar]], $\operatorname{mejor}_t(s)$ guardó la probabilidad de la mejor trayectoria que termina en $s$.
- **Qué significan $b$ y $V$ aquí.** $b$ es la creencia de hoy. Para el paraguas basta un número: $b=b(\text{lluvia})$. $V^*$ y $Q^*$ son los de la clase 3, con estado visible.

---

## 1 · Repasar la decisión con el estado a la vista

**Piensa: si ves por la ventana que llueve, ¿qué haces con el paraguas?**

Lo llevas. Si ves el estado, puedes elegir una acción para cada estado. Ese fue el problema de la clase 3; aquí lo repasamos en corto.

Un proceso de decisión de Markov (MDP) tiene cuatro piezas: estados, acciones, transiciones y recompensas. La tabla las muestra para el paraguas, con clima visible y un solo día.

::: table {#mkv-c4-ds-tabla-repaso title="El MDP de la clase 3, pieza por pieza, en el paraguas visible"}
| Pieza | Símbolo | Qué es | En el paraguas visible |
|---|---|---|---|
| Estado | $s\in\mathcal S$ | Lo que ves al decidir | lluvia o sol |
| Acción | $a\in\mathcal A$ | Lo que eliges | llevar o no llevar |
| Transición | $P(s'\mid s,a)$ | A dónde llegas | El día termina |
| Costo | $\operatorname{costo}(s,a)=-r(s,a)$ | Lo que pagas al usar $a$ en $s$ | Llevar 1; no llevar 4 con lluvia, 0 con sol |
| Política | $\pi(s)$ | Una acción por estado | Llevar si llueve |
| Valor | $V^*(s)$ | Lo que vale $s$ con la mejor política | $V^*(\text{lluvia})=-1$, $V^*(\text{sol})=0$ |
| Valor de acción | $Q^*(s,a)$ | Usar $a$ y luego lo mejor | $Q^*(\text{lluvia},\text{no llevar})=-4$ |
:::

- **Aviso de signo.** En la clase 3 maximizaste recompensas $r\le0$. Aquí usamos costos: $\operatorname{costo}(s,a)=-r(s,a)$. Maximizar recompensa equivale a minimizar costo.
- **Aviso de letra.** $\operatorname{costo}(s,a)$ es lo que pagas en un paso. En la escalera, $\operatorname{costo}(s)$ era todo lo que faltaba pagar.
- **Aviso de diccionarios.** En el modelo oculto, `P[s][s2]` y `B[s][o]` son diccionarios anidados por estado. En el MDP de la clase 3, `P[(s, a)]` daba la transición por pareja.

**La política óptima.** El día termina al actuar, así que $Q^*(s,a)=r(s,a)$. Con lluvia, llevar cuesta 1 y no llevar cuesta 4: conviene llevar. Con sol, llevar cuesta 1 y no llevar cuesta 0. Conviene no llevar. La política óptima es **llevar si llueve**.

**Lo que cuesta no ver.** Sin más información, asignas a la lluvia una probabilidad de $1/2$. Llevar cuesta 1 y no llevar tiene costo esperado $\tfrac12\cdot4+\tfrac12\cdot0=2$. Conviene llevar: 1.

**Lo que costaría ver gratis.** Si vieras el clima gratis, seguirías la política óptima:

$$
\tfrac12\cdot1+\tfrac12\cdot0=\tfrac12.
$$

Ver el clima te ahorraría $1-\tfrac12=\tfrac12$. Ese ahorro es el valor de saber el estado. Depende de tu creencia inicial.

::: exercise {#mkv-c4-ds-ej-ver-gratis title="Calcula lo que ahorra ver"}
Ahora asignas a la lluvia una probabilidad de $1/3$. ¿Cuánto cuesta la mejor acción sin ver? ¿Y viendo gratis? ¿Cuánto ahorras?
:::

::: hint {#mkv-c4-ds-pista-ver-gratis of="mkv-c4-ds-ej-ver-gratis" title="Dos promedios"}
Sin ver, promedia los costos de cada acción con $1/3$ y $2/3$. Viendo, promedia los costos de la política óptima.
:::

::: answer {#mkv-c4-ds-resp-ver-gratis of="mkv-c4-ds-ej-ver-gratis"}
Sin ver, llevar cuesta 1 y no llevar cuesta $\tfrac13\cdot4=\tfrac43$. Conviene llevar: 1. Viendo gratis: $\tfrac13\cdot1+\tfrac23\cdot0=\tfrac13$. Ahorras $\tfrac23$.
:::

Desde el sótano no puedes ver gratis. ¿Cómo decides sin ver?

---

## 2 · Plantear el problema de un día

**Piensa: si no ves el clima, ¿qué puedes elegir y con qué información?**

Puedes elegir una acción a partir de tu creencia. Primero planteamos el problema: qué ocurre, en qué orden y cuándo termina.

::: remark {#mkv-c4-obs-un-dia title="El problema de un día"}
**En general.** Hay conjuntos finitos de estados $\mathcal S$ y acciones $\mathcal A$. Cada pareja tiene un costo $\operatorname{costo}(s,a)\ge0$. La creencia $b$ es una distribución sobre $\mathcal S$. El estado es uno solo y **no cambia durante el día**.

1. **Eliges** con $b$, sin ver $s$: una acción $a\in\mathcal A$ o **mirar**.
2. **Si eliges $a$,** pagas $\operatorname{costo}(s,a)$ según el $s$ real.
3. **Si eliges mirar,** pagas un precio y ves $s$. **Luego** eliges $a$ sabiendo $s$.
4. **El día termina.** No hay transición: $P$ no se aplica dentro del día.

**En el paraguas.** $\mathcal S=\{\text{lluvia},\text{sol}\}$ y $\mathcal A=\{\text{llevar},\text{no llevar}\}$. Llevar cuesta 1. No llevar cuesta 4 si llueve y 0 si no. Mirar cuesta $1/2$: subes al vestíbulo y ves el cielo.
:::

> **Dado:** la creencia $b=\Pr(\text{lluvia})$, los costos y el precio de mirar.
>
> **Encontrar:** la decisión inicial de menor costo esperado: llevar, no llevar o mirar. Si miras, también necesitas una regla para después.

- **Mirar es una macroacción.** Junta dos pasos: pagar por ver y decidir con esa información. Después de mirar, tienes el MDP visible de la sección 1.
- **La acción no puede depender de $s$.** No lo ves. Sin mirar, eliges una sola acción para los dos climas.
- **Por qué un día.** No hay decisiones futuras que valorar. La creencia de mañana entra en la sección 5.

::: exercise {#mkv-c4-ds-ej-planes title="Cuenta los planes del día"}
Un plan indica qué haces hoy y, si miras, qué haces en cada clima. ¿Cuántos planes hay? ¿Qué regla tras mirar gana en los dos climas?
:::

::: hint {#mkv-c4-ds-pista-planes of="mkv-c4-ds-ej-planes" title="Después de mirar"}
Al mirar ves lluvia o sol. ¿De cuántas formas puedes asignar llevar o no llevar a cada clima?
:::

::: answer {#mkv-c4-ds-resp-planes of="mkv-c4-ds-ej-planes"}
Seis: llevar, no llevar y mirar con una de $2\times2=4$ reglas. La regla «llevar si llueve, no llevar si hay sol» minimiza el costo: 1 con lluvia y 0 con sol. Es la política óptima de la sección 1. En adelante, mirar incluye seguir esa regla.
:::

¿Qué conviene hacer sin mirar?

---

## 3 · Decidir con la creencia

**Piensa: si crees que llueve con $b$, ¿cuánto esperas pagar por cada acción?**

Esperas pagar el promedio de los costos, ponderado por tu creencia. Gana la acción con el menor promedio.

Con cualquier creencia $b$, el costo esperado de una acción y el mínimo sin mirar son:

$$
\begin{aligned}
\operatorname{costo}(b,a)&=\sum_{s\in\mathcal S}b(s)\operatorname{costo}(s,a),\\
\operatorname{actuar}(b)&=\min_{a\in\mathcal A}\operatorname{costo}(b,a).
\end{aligned}
$$

- **De dónde sale:** usas las probabilidades de cada clima como pesos, como en la probabilidad total de la clase 1.
- **Qué significa:** decides con la información disponible. La misma $b$ da la misma decisión, llueva o no.
- **Aviso de letra.** $\operatorname{costo}(b,a)$ recibe una creencia; $\operatorname{costo}(s,a)$ recibe un estado.

**En el paraguas.** Con $b(\text{lluvia})=b$ y $b(\text{sol})=1-b$:

$$
\begin{aligned}
\operatorname{costo}(b,\text{llevar})&=b\cdot1+(1-b)\cdot1=1,\\
\operatorname{costo}(b,\text{no llevar})&=b\cdot4+(1-b)\cdot0=4b.
\end{aligned}
$$

Así, $\operatorname{actuar}(b)=\min(1,4b)$. Llevar gana si $4b>1$, es decir, si $b>1/4$.

- **El umbral es un cociente:** $1/4$ resulta de dividir el costo de llevar entre el de mojarse. Si mojarse costara más, el umbral bajaría.
- **El empate:** en $b=1/4$ ambas acciones cuestan 1. Cualquiera es óptima.
- **No es $1/2$.** Puede convenir llevar aunque el sol sea más probable. Mojarse cuesta cuatro veces lo que cuesta cargarlo.

**La creencia viene del filtro.** Si observas paraguas el día 0, $b_0=9/11\approx0.818$. Como $9/11>1/4$, llevas, con costo esperado 1. No llevar costaría $4\cdot\tfrac9{11}=\tfrac{36}{11}\approx3.27$. Si observas a tu compañero sin paraguas, $b=1/9<1/4$. No llevas, con costo $4/9$.

> [!WARNING]
> **Error típico:** «llevo el paraguas si es más probable que llueva». **La regla compara costos esperados, no probabilidades.** El umbral es $1/4$, no $1/2$.

::: exercise {#mkv-c4-ds-ej-dia-uno title="Decide con dos días de señales"}
Tu compañero llegó con paraguas el día 0 y sin paraguas el día 1. El filtro da $b_1=69/397\approx0.174$. Sin mirar, ¿llevas el paraguas? ¿Cuánto esperas pagar?
:::

::: hint {#mkv-c4-ds-pista-dia-uno of="mkv-c4-ds-ej-dia-uno" title="Compara con el umbral"}
¿$69/397$ queda arriba o abajo de $1/4$?
:::

::: answer {#mkv-c4-ds-resp-dia-uno of="mkv-c4-ds-ej-dia-uno"}
$69/397\approx0.174<1/4$: no llevas. El costo esperado es $4\cdot\tfrac{69}{397}=\tfrac{276}{397}\approx0.695$. Llevar cuesta 1.
:::

Ese $0.695$ es caro para quien casi seguro tiene sol. ¿Cuánto ayudaría salir de dudas?

---

## 4 · Pagar por mirar

**Piensa: con $b=1/4$, ¿cuánto pagarías por ver el cielo antes de decidir?**

Hasta $3/4$. Sin mirar pagas 1, y si vieras gratis pagarías en promedio $b=1/4$. La diferencia es el valor de ver. Calculemos primero el costo de mirar.

**El costo de mirar, en general.** Pagas el precio y ves $s$. Luego eliges la acción de menor costo en ese estado:

$$
\operatorname{costo}(b,\text{mirar})=\text{precio}+\sum_{s}b(s)\min_{a}\operatorname{costo}(s,a).
$$

**En el paraguas.** El costo mínimo es 1 con lluvia y 0 con sol. Entonces:

$$
\operatorname{costo}(b,\text{mirar})=\tfrac12+b.
$$

**Antes de la gráfica.** Contesta qué acción cuesta menos según lo que crees. Cada punto de una línea es el costo esperado de una acción con una creencia. El eje horizontal es $b$, de 0 a 1. El vertical muestra el costo esperado del día.

::: figure {#mkv-c4-fig-ds-costos title="Los tres costos según la creencia, y dónde gana cada uno"}
![Gráfica con la creencia b = Pr(lluvia) de 0 a 1 en el eje horizontal y el costo esperado del día en el vertical. Tres rectas: llevar, horizontal en 1; no llevar, 4b, que sube desde 0; mirar, 1/2 + b, que sube desde 1/2. Una recta punteada, b, marca ver gratis. Abajo, tres regiones: no llevar de 0 a 1/6, mirar entre 1/6 y 1/2, llevar de 1/2 a 1. Puntos marcados: en 1/6, no llevar y mirar valen 2/3; en 1/4, llevar y no llevar valen 1 y mirar 3/4; en 1/2, mirar y llevar valen 1. Una marca en b = 9/11 dice llevar.](../_assets/mkv-c4-ds-costos.svg)
:::

- **Mirar contra no llevar:** $\tfrac12+b<4b$ si $b>1/6$. En $b=1/6$ las dos valen $2/3$.
- **Mirar contra llevar:** $\tfrac12+b<1$ si $b<1/2$. En $b=1/2$ las dos valen 1.
- **Mirar conviene estrictamente** para $1/6<b<1/2$. En los extremos empata con la mejor acción sin mirar.
- **En $b=1/4$:** llevar y no llevar empatan en 1, y mirar cuesta $3/4$. Ahí el ahorro es máximo.
- **Fuera del rango,** mirar no reduce el costo. Con $b=9/11$ mirar cuesta $\tfrac12+\tfrac9{11}=\tfrac{29}{22}\approx1.32$, más que llevar.

**El valor de la información perfecta.** Es cuánto bajaría el costo si vieras $s$ gratis:

$$
\operatorname{info}(b)=\operatorname{actuar}(b)-\sum_{s}b(s)\min_{a}\operatorname{costo}(s,a).
$$

En el paraguas, $\operatorname{info}(b)=\min(1,4b)-b$. En la gráfica, mide la distancia vertical entre la recta más baja sin mirar y la punteada. Vale $3/4$ en $b=1/4$ y $1/2$ en $b=1/6$ y en $b=1/2$.

::: theorem {#mkv-c4-teo-mirar title="Cuándo conviene pagar por mirar"}
**Condición.** Usamos el problema de un día de @mkv-c4-obs-un-dia. $\mathcal S$ y $\mathcal A$ son finitos, $b$ es una distribución sobre $\mathcal S$ y el precio es $\ge0$. Mirar revela el estado **exacto**. Después eliges la acción de menor costo para ese estado.

$$
\operatorname{costo}(b,\text{mirar})<\operatorname{actuar}(b)
\iff\operatorname{info}(b)>\text{precio}.
$$

**Lectura.** Paga por mirar si el ahorro esperado supera el precio.

**Casos nulos.** Si $b$ concentra toda la probabilidad en un estado, $\operatorname{info}(b)=0$. Mirar no mejora el costo. Con precio 0, mirar nunca pierde, porque $\operatorname{info}(b)\ge0$.
:::

::: proof {#mkv-c4-dem-mirar of="mkv-c4-teo-mirar"}
Resta $\operatorname{actuar}(b)$ a ambos lados de la definición del costo de mirar:

$$
\begin{aligned}
\operatorname{costo}(b,\text{mirar})-\operatorname{actuar}(b)
&=\text{precio}-\operatorname{info}(b).
\end{aligned}
$$

La diferencia es negativa si y solo si $\operatorname{info}(b)>\text{precio}$. Además, $\operatorname{info}(b)\ge0$: para cada $a$, $\operatorname{costo}(s,a)\ge\min_{a'}\operatorname{costo}(s,a')$. La desigualdad se conserva al promediar con $b$ y tomar el mínimo. Revelar el estado exacto permite pagar $\min_a\operatorname{costo}(s,a)$ después de mirar.
:::

> [!TIP]
> **Ejemplo y contraejemplo.**
>
> - **Lo cumple:** $b=1/3$ y mirar revela el clima. Con lluvia ($1/3$) llevas y pagas 1; con sol ($2/3$), pagas 0. Mirar cuesta $\tfrac12+\tfrac13=\tfrac56<1$. El teorema coincide: $\operatorname{info}=1-\tfrac13=\tfrac23>\tfrac12$.
> - **No lo cumple:** $b=1/3$. La ventana empañada solo deja ver si el vecino trae paraguas, con $B=\begin{pmatrix}9/10&1/10\\2/10&8/10\end{pmatrix}$. Lo trae con probabilidad $13/30$: la probabilidad de lluvia sube a $9/13$ y llevas: 1. No lo trae con $17/30$: la probabilidad de lluvia baja a $1/17$ y no llevas: $4/17$. Mirar cuesta $\tfrac12+\tfrac{13}{30}+\tfrac{4}{30}=\tfrac{16}{15}>1$. La fórmula del teorema diría «mira», pero aquí no aplica: mirar pierde.

::: figure {#mkv-c4-fig-ej-decidir title="Ejemplo y contraejemplo: pagar por mirar"}
![Dos árboles de decisión con b = 1/3 y precio 1/2. Arriba, el que cumple: mirar revela el clima; rama lluvia con probabilidad 1/3 lleva a llevar, costo 1; rama sol con 2/3 lleva a no llevar, costo 0; total 1/2 + 1/3 = 5/6, menor que actuar ya, 1. Abajo, el que no: la ventana empañada muestra solo una señal; rama paraguas con 13/30 deja la lluvia en 9/13 y lleva a llevar, costo 1; rama sin paraguas con 17/30 deja la lluvia en 1/17 y lleva a no llevar, costo 4/17; total 16/15, mayor que 1.](../_assets/mkv-c4-ej-decidir.svg)
:::

> [!WARNING]
> **Error típico:** confundir valor y precio. **$\operatorname{info}(b)$ es el ahorro de ver gratis; el precio es lo que pagas por mirar.** Conviene mirar si el ahorro supera el precio. En $b=1/2$ ambos valen $1/2$: mirar empata con llevar.

**La creencia no es el clima.** Mirar cambia lo que sabes. Antes de mirar, $b=1/4$. Después, $b$ vale 1 o 0. La creencia es un **estado de información**; el clima es el **estado físico**. El filtro y mirar actualizan la creencia. Solo $P$ cambia el clima.

**En Python.** La misma función decide con cualquier creencia. Los costos se guardan por pareja $(s,a)$, como $r(s,a)$ en la clase 3. En un empate elige la primera acción de la lista.

```python
from fractions import Fraction as F

costo = {("lluvia", "llevar"): F(1),
         ("lluvia", "no llevar"): F(4),
         ("sol", "llevar"): F(1),
         ("sol", "no llevar"): F(0)}
ACCIONES = ["llevar", "no llevar"]
PRECIO = F(1, 2)                          # mirar

def costo_creencia(b, a):                 # costo(b, a)
    return sum(b[s] * costo[(s, a)] for s in b)

def costo_mirar(b):                       # ver s, elegir bien
    return PRECIO + sum(
        b[s] * min(costo[(s, a)] for a in ACCIONES)
        for s in b)

def decidir(b):                           # empate: el primero
    tabla = {a: costo_creencia(b, a) for a in ACCIONES}
    tabla["mirar"] = costo_mirar(b)
    mejor = min(tabla.values())
    return [a for a in tabla if tabla[a] == mejor][0], tabla

for x in [F(1, 9), F(1, 6), F(69, 397), F(1, 4),
          F(1, 2), F(9, 11)]:
    b = {"lluvia": x, "sol": 1 - x}
    a, tabla = decidir(b)
    cifras = [str(v).ljust(7) for v in tabla.values()]
    print(str(x).ljust(7), *cifras, a)
```

```text
1/9     1       4/9     11/18   no llevar
1/6     1       2/3     2/3     no llevar
69/397  1       276/397 535/794 mirar
1/4     1       1       3/4     mirar
1/2     1       2       1       llevar
9/11    1       36/11   29/22   llevar
```

- **Columnas:** creencia, costos de llevar, no llevar y mirar, y decisión.
- **$1/6$ y $1/2$:** hay empate. El código elige la primera acción óptima de la lista.
- **$69/397$:** observaste paraguas y luego sin paraguas. Está apenas arriba de $1/6$. Mirar cuesta $535/794\approx0.674$; no llevar, $0.695$.

::: exercise {#mkv-c4-ds-ej-un-quinto title="Compara mirar con un quinto"}
Con $b=1/5$, calcula los tres costos. ¿Qué eliges? Comprueba con $\operatorname{info}(1/5)$ y el teorema.
:::

::: hint {#mkv-c4-ds-pista-un-quinto of="mkv-c4-ds-ej-un-quinto" title="Tres números y una resta"}
Usa $1$, $4b$ y $\tfrac12+b$. Para el valor, resta $b$ al menor de $1$ y $4b$.
:::

::: answer {#mkv-c4-ds-resp-un-quinto of="mkv-c4-ds-ej-un-quinto"}
Llevar cuesta 1; no llevar, $4/5$; mirar, $7/10$. Conviene mirar. $\operatorname{info}(1/5)=\tfrac45-\tfrac15=\tfrac35>\tfrac12$, como pide el teorema.
:::

El problema terminaba hoy. ¿Qué cambia si mañana decides otra vez?

---

## 5 · Tomar la creencia como estado

**Piensa: si decides todos los días, ¿qué tienes que recordar de los días pasados?**

Solo tu creencia de hoy. El filtro la actualiza con la acción y la nueva señal. No necesitas guardar el resto de la historia.

Cuando el problema se repite, decides en cada paso $t$ con $b_t$. La creencia funciona como estado del MDP. Este es un **proceso de decisión de Markov parcialmente observable** (*partially observable Markov decision process*, POMDP).

::: remark {#mkv-c4-obs-creencia-estado title="La creencia como estado"}
**En general.** Tienes un MDP con estado oculto: $\mathcal S$, $\mathcal A$, $P(s'\mid s,a)$, $r(s,a)$ y señales descritas por $B(s,o)$. En cada paso:

1. **Decides** con $b_t$ y ejecutas $a$. Recibes, en promedio, $r(b_t,a)=\sum_s b_t(s)\,r(s,a)$.
2. **El estado cambia** según $P(\cdot\mid s,a)$ y emite una señal $o$ según $B$.
3. **Actualizas** con el filtro de la página 3: predices con $P$, corriges con $B(s',o)$ y normalizas.

$$
\begin{aligned}
b_{t+1}(s')&=\frac{B(s',o)\sum_s b_t(s)P(s'\mid s,a)}{\Pr(o\mid b_t,a)}.
\end{aligned}
$$

El denominador suma el numerador sobre $s'$. **Qué significa:** la nueva creencia depende solo de $b_t$, de $a$ y de $o$. La creencia es el estado de este MDP.
:::

- **En el paraguas,** llevar no cambia el clima: $P(s'\mid s,a)=P(s'\mid s)$. Usas el filtro de la página 3.
- **Aviso de estado.** $b_t$ es el estado de información del MDP. El clima sigue oculto.

**La ecuación tiene el mismo aspecto.** Usamos recompensas como en la clase 3; $b'$ es la creencia después de $a$ y $o$:

$$
\begin{aligned}
V(b)&=\max_{a\in\mathcal A}\Bigl[r(b,a)\\
&\qquad+\sum_{o}\Pr(o\mid b,a)\,V(b')\Bigr].
\end{aligned}
$$

- **El problema de un día** no tiene decisiones futuras. El segundo término vale 0 y queda $V(b)=\max_a r(b,a)=-\operatorname{actuar}(b)$. La sección 3 resolvió justo eso.
- **Límite del teorema.** El teorema de la clase 3 exigía estados finitos. Aquí $b$ toma un continuo de valores. Ese teorema no garantiza una solución única ni que la política codiciosa sea óptima.

**Viterbi y Bellman.** Ambas usan programación dinámica con un máximo. Construyen la mejor solución a partir de soluciones óptimas de problemas más cortos.

$$
\begin{aligned}
\operatorname{mejor}_t(s')&=\max_{s}\operatorname{mejor}_{t-1}(s)\,P(s'\mid s)\,B(s',o_t),\\
V^*(s)&=\max_{a}\Bigl[r(s,a)+\sum_{s'}P(s'\mid s,a)V^*(s')\Bigr].
\end{aligned}
$$

::: table {#mkv-c4-ds-tabla-viterbi-bellman title="Viterbi y Bellman: la misma recursión, dos preguntas"}
| | Viterbi | Bellman |
|---|---|---|
| Qué maximiza | La probabilidad conjunta de una trayectoria con las señales vistas | La recompensa esperada |
| Sobre qué | Hipótesis de lo que pasó: trayectorias de estados | Decisiones: acciones |
| Qué está dado | El modelo y las señales $o_{0:T}$ | El MDP: $P$ y $r$ |
| Cómo combina | Multiplica probabilidades | Suma recompensas y promedia el azar |
| Hacia dónde | Del día 0 al día $T$ | Desde el final hacia atrás, o como punto fijo si hay ciclos |
:::

- **Viterbi no decide nada.** Busca la trayectoria más probable dadas las señales.
- **Bellman sí decide.** Elige una acción y promedia sus posibles consecuencias.
- **Con logaritmos se parecen más.** El logaritmo convierte el producto de Viterbi en una suma, como en Bellman.

::: exercise {#mkv-c4-ds-ej-cuantas-creencias title="Cuenta las creencias del paraguas"}
Empiezas con $\mu_0=(1/2,1/2)$. ¿Cuántos valores puede tomar $b_0$? ¿Y $b_1$? ¿Cuántos como máximo el día $t$?
:::

::: hint {#mkv-c4-ds-pista-cuantas-creencias of="mkv-c4-ds-ej-cuantas-creencias" title="Una rama por señal"}
Cada día llega una de dos señales. ¿Cuántas secuencias de señales hay hasta el día $t$?
:::

::: answer {#mkv-c4-ds-resp-cuantas-creencias of="mkv-c4-ds-ej-cuantas-creencias"}
$b_0$: dos, $9/11$ y $1/9$. $b_1$: cuatro, $621/703$, $69/397$, $279/397$ y $31/503$. El día $t$, como máximo $2^{t+1}$. Otra $\mu_0$ produce otras creencias. El conjunto completo no es una lista finita fija.
:::

---

## Ejercicios

::: exercise {#mkv-c4-ds-ej-mojarse-tres title="Encuentra la nueva frontera de mirar"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

**Cambia una idea:** mojarse cuesta 3, no 4. Llevar cuesta 1 y mirar, $1/2$. El resto del problema sigue igual.

1. **Escribe** los tres costos esperados en función de $b$.
2. **Encuentra** el umbral de llevar sin mirar. ¿Qué ocurre en el umbral?
3. **Encuentra** el rango de $b$ donde mirar conviene estrictamente. Indica los empates en los extremos.
4. **Generaliza:** expresa el umbral y la condición para mirar usando los costos de llevar y mojarse, y el precio. Comprueba que 1, 4 y $1/2$ dan $1/4$ y $(1/6,1/2)$.
5. **Calcula** $\operatorname{info}(b)$ y su máximo. Indica dónde lo alcanza. ¿Desde qué precio mirar deja de convenir estrictamente?
:::

::: hint {#mkv-c4-ds-pista-mojarse-tres-1 of="mkv-c4-ds-ej-mojarse-tres" title="Pista 1 · ¿Qué rectas se cruzan?"}
¿Qué costo cambia y cuáles siguen iguales? ¿Dónde se cruza cada par de rectas?
:::

::: hint {#mkv-c4-ds-pista-mojarse-tres-2 of="mkv-c4-ds-ej-mojarse-tres" title="Pista 2 · ¿Tu fórmula recupera el paraguas original?"}
Con 1, 4 y $1/2$, ¿tus fórmulas dan $1/4$, $1/6$ y $1/2$? ¿El máximo de $\operatorname{info}$ está en el umbral?
:::

::: answer {#mkv-c4-ds-resp-mojarse-tres of="mkv-c4-ds-ej-mojarse-tres" title="Respuesta · El umbral sube a 1/3 y mirar empieza en 1/4"}
**1. Costos.** Llevar: 1. No llevar: $3b$. Mirar: $\tfrac12+b$. El costo de mirar sigue igual: después de ver, nunca te mojas.

**2. Umbral.** $3b>1$ si $b>1/3$: llevas. En $b=1/3$ llevar y no llevar cuestan 1. Mirar cuesta $5/6$ y gana.

**3. Rango.** Mirar contra no llevar: $\tfrac12+b<3b$ si $b>1/4$. Contra llevar: $\tfrac12+b<1$ si $b<1/2$. Conviene para $1/4<b<1/2$. En $b=1/4$, mirar y no llevar valen $3/4$; en $b=1/2$, mirar y llevar valen 1.

**4. Generaliza.** Llevar conviene si

$$
b>\frac{\text{costo de llevar}}{\text{costo de mojarse}}.
$$

Mirar cuesta $\text{precio}+b\cdot\text{costo de llevar}$. Abrevia cada costo con su acción. Compara con el mínimo sin mirar:

$$
\begin{aligned}
&\text{precio}+b\cdot\text{llevar}\\
&\quad<\min(\text{llevar},\ b\cdot\text{mojarse}).
\end{aligned}
$$

Al despejar, $\dfrac{\text{precio}}{\text{mojarse}-\text{llevar}}<b<1-\dfrac{\text{precio}}{\text{llevar}}$. Con 1, 4 y $1/2$, el umbral es $1/4$ y el rango, $(1/6,\ 1/2)$. Con 1, 3 y $1/2$, son $1/3$ y $(1/4,\ 1/2)$.

**5. El valor.** $\operatorname{info}(b)=\min(1,3b)-b$. Sube como $2b$ hasta el umbral. Después baja como $1-b$. Su máximo está en $b=1/3$ y vale $2/3$. Si el precio es $2/3$ o más, mirar nunca gana estrictamente.

```python
from fractions import Fraction as F
for x in [F(1, 4), F(1, 3), F(1, 2)]:
    print(x, 1, 3 * x, F(1, 2) + x, min(1, 3 * x) - x)
```

```text
1/4 1 3/4 3/4 1/2
1/3 1 1 5/6 2/3
1/2 1 3/2 1 1/2
```
:::

**Punto de control:** debes dominar estas cuatro cosas.

- **Plantear** el problema de un día: decisiones, orden, información que revela mirar y momento de terminar.
- **Decidir** con una creencia: comparar costos esperados y obtener el umbral $1/4$.
- **Separar** precio y valor de la información. Usar el teorema para decidir si conviene pagar.
- **Explicar** por qué la creencia funciona como estado y en qué difieren Viterbi y Bellman.

---

## Lo que hay que llevarse

- **Con el estado a la vista:** lleva si llueve. Sin más información ($b=1/2$), el costo mínimo es 1; viendo gratis sería $1/2$.
- **El problema de un día:** con $b$ eliges llevar, no llevar o mirar. Si miras, pagas $1/2$ y eliges según el clima. El día termina sin aplicar $P$ (@mkv-c4-obs-un-dia).
- **Decidir con la creencia:** $\operatorname{costo}(b,a)=\sum_s b(s)\operatorname{costo}(s,a)$. El mínimo es $\min(1,4b)$: llevas si $b>1/4$. Con $b_0=9/11$, llevas.
- **Mirar:** cuesta $\tfrac12+b$ y conviene estrictamente para $1/6<b<1/2$. Empates: $2/3$ en $1/6$, 1 en $1/2$. En $1/4$, llevar y no llevar cuestan 1; mirar, $3/4$.
- **Valor frente a precio:** $\operatorname{info}(b)=\min(1,4b)-b$. Mirar conviene si $\operatorname{info}(b)>\text{precio}$. Esta regla exige ver el estado exacto (@mkv-c4-teo-mirar).
- **La creencia como estado:** el POMDP es un MDP sobre creencias. Bellman conserva su forma. El teorema de la clase 3 no aplica porque las creencias forman un continuo.
- **Viterbi y Bellman:** ambas usan programación dinámica con un máximo. Viterbi busca la trayectoria más probable; Bellman, las acciones con mayor recompensa esperada.

Aquí conocías $P$, $B$ y los costos. ¿Cómo decides si tienes que aprenderlos al actuar?

Continúa con [[mkv-hacia-refuerzo|Hacia el aprendizaje por refuerzo]].
