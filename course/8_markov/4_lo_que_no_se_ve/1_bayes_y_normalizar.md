---
id: mkv-bayes-y-normalizar
title: "Lo que necesitas: Bayes y normalizar"
nav_title: "Bayes y normalizar"
summary: "La regla de Bayes y normalizar, con un número del paraguas: lo único que se necesita de probabilidad para filtrar."
status: ready
estimated_time: 12m
tags: [markov, ocultas, bayes]
---

# Lo que necesitas: Bayes y normalizar

**¿Cómo cambia lo que crees de algo que no ves cuando ves una señal?**

Al terminar tendrás:

- **La regla de Bayes:** pasar de la probabilidad de la señal dado el estado a la del estado dada la señal. Sirve con cualquier número de estados.
- **Normalizar:** dividir pesos no negativos entre su suma y reconocer cuándo no se puede.
- **Cuatro nombres:** prior, verosimilitud, evidencia y posterior, cada uno con su valor en el ejemplo del paraguas.

## Lo que traes

De [[mkv-lo-que-necesitas|Lo que necesitas de probabilidad]], en la clase 1:

- **Condicional:** $\Pr(A\mid B)=\Pr(A\cap B)/\Pr(B)$, con $\Pr(B)>0$ (@mkv-c1-prob-condicional).
- **Producto:** $\Pr(A\cap B)=\Pr(B)\Pr(A\mid B)$ (@mkv-c1-teo-producto).
- **Probabilidad total:** $\Pr(A)=\sum_j\Pr(A\mid B_j)\Pr(B_j)$ sobre una partición (@mkv-c1-teo-total).
- **Una distribución como vector fila:** $\mu_0$ en [[mkv-cadena-en-general|La cadena en general]].

Aquí basta con eso. Aún no usamos $P$ ni seguimos cambios en el tiempo: un día, un estado oculto y una señal.

---

## 1 · Invertir la condicional con Bayes

**Piensa: cuando llueve, tu compañero trae paraguas 9 de cada 10 veces. Si llega con paraguas, ¿qué tan probable es que llueva?**

Todavía no puedes decirlo: faltan el prior y la probabilidad de paraguas con sol.

Trabajas en un sótano sin ventanas. No ves el estado $S$: lluvia o sol. Sí ves la señal $O$: paraguas o sin paraguas. Las mayúsculas representan variables aleatorias. Las minúsculas $s$ y $o$ son valores concretos. El conjunto de estados es $\mathcal S$.

::: table {#mkv-c4-tabla-bayes title="Las cuatro cantidades de Bayes, en el paraguas"}
| Símbolo | Nombre | Qué es | En el paraguas |
|---|---|---|---|
| $\Pr(S=s)$ | prior | lo que crees antes de ver la señal | $1/2$ lluvia, $1/2$ sol |
| $\Pr(O=o\mid S=s)$ | verosimilitud | qué tan probable es la señal en cada estado | $9/10$ con lluvia, $2/10$ con sol |
| $\Pr(O=o)$ | evidencia | la probabilidad de la señal al considerar todos los estados | $11/20$ |
| $\Pr(S=s\mid O=o)$ | posterior | lo que crees después de ver la señal | $9/11$ lluvia |
:::

- **El prior es un vector fila**, como $\mu_0$: $(1/2,\ 1/2)$, en el orden (lluvia, sol).
- **Aviso de letra.** La página 2 llama $B(s,o)$, la emisión, a $\Pr(O=o\mid S=s)$. Aquí la escribimos completa.

::: theorem {#mkv-c4-teo-bayes title="Regla de Bayes"}
**Condición.** $\mathcal S$ es finito, $\Pr(S=s)>0$ y la evidencia es positiva: $\Pr(O=o)>0$. La suma recorre solo los estados con prior positivo; en los demás, $\Pr(O=o\mid S=s')$ no está definida.

$$
\begin{aligned}
\Pr(S=s\mid O=o)
&=\frac{\Pr(O=o\mid S=s)\,\Pr(S=s)}{\Pr(O=o)},\\
\Pr(O=o)&=\sum_{s':\,\Pr(S=s')>0}\Pr(O=o\mid S=s')\\
&\qquad\times\Pr(S=s').
\end{aligned}
$$

**Lectura.** Multiplica el prior de cada estado por su verosimilitud. Divide cada producto entre la suma de todos los productos.

**Casos nulos.** Un estado con prior 0 no entra en la suma, y su posterior vale 0: $\Pr(S=s,\ O=o)\le\Pr(S=s)=0$. Si la evidencia vale 0, la señal es imposible en el modelo. La posterior no se define.
:::

::: proof {#mkv-c4-dem-bayes of="mkv-c4-teo-bayes"}
Aplica la condicional, el producto y la probabilidad total, en ese orden:

$$
\begin{aligned}
\Pr(S=s\mid O=o)
&=\frac{\Pr(S=s,\ O=o)}{\Pr(O=o)}\\
&=\frac{\Pr(O=o\mid S=s)\,\Pr(S=s)}{\Pr(O=o)}.
\end{aligned}
$$

El primer renglón requiere $\Pr(O=o)>0$, y el segundo, $\Pr(S=s)>0$. La evidencia se desarrolla con la probabilidad total, que omite los casos de prior 0.
:::

**Ejemplo del paraguas.** Usa el prior $(1/2,\ 1/2)$:

$$
\begin{aligned}
\Pr(\text{lluvia}\mid\text{paraguas})
&=\frac{\tfrac{9}{10}\cdot\tfrac12}{\tfrac{9}{10}\cdot\tfrac12+\tfrac{2}{10}\cdot\tfrac12}\\
&=\frac{9/20}{11/20}=\frac{9}{11}\approx0.818.
\end{aligned}
$$

- **El numerador, $9/20$,** es la fracción de días con lluvia y paraguas.
- **El denominador, $11/20$,** incluye todos los días con paraguas: $9/20$ de lluvia más $2/20$ de sol.
- **Qué significa:** de cada 11 días con paraguas, 9 son de lluvia. La página 3 usará este $9/11$ como primer paso del filtro.

> [!TIP]
> **Ejemplo y contraejemplo de la condición.**
>
> - **Lo cumple.** Con lluvia, paraguas tiene probabilidad $9/10$; con sol, $2/10$. Las verosimilitudes son $\begin{pmatrix}9/10 & 2/10\end{pmatrix}$ y la evidencia es $\tfrac{9}{20}+\tfrac{2}{20}=\tfrac{11}{20}>0$.
> - **No lo cumple.** La señal «nieve» tiene verosimilitudes $\begin{pmatrix}0 & 0\end{pmatrix}$. La evidencia es $0\cdot\tfrac12+0\cdot\tfrac12=0$. Por eso, $\Pr(\text{lluvia}\mid\text{nieve})$ no se define.

> [!WARNING]
> **Error típico: voltear la barra.** $\Pr(\text{paraguas}\mid\text{lluvia})=9/10$ no es $\Pr(\text{lluvia}\mid\text{paraguas})=9/11$. **La lectura correcta: después de la barra va lo que ya sabes.** Aquí lo que sabes es la señal: tu compañero trae paraguas.

::: exercise {#mkv-c4-bn-ej-sin-paraguas title="Calcula con la otra señal"}
Con el mismo prior $(1/2,\ 1/2)$, tu compañero llega **sin** paraguas. ¿Cuánto vale $\Pr(\text{lluvia}\mid\text{sin paraguas})$?
:::

::: hint {#mkv-c4-bn-pista-sin-paraguas of="mkv-c4-bn-ej-sin-paraguas" title="Las verosimilitudes de la otra señal"}
¿Cuánto vale $\Pr(\text{sin paraguas}\mid S=s)$ en cada estado? Para paraguas, las probabilidades eran $9/10$ y $2/10$.
:::

::: answer {#mkv-c4-bn-resp-sin-paraguas of="mkv-c4-bn-ej-sin-paraguas"}
**$1/9\approx0.111$.** Las verosimilitudes son $1/10$ y $8/10$. Los productos son $1/20$ y $8/20$. La evidencia es $9/20$. Al dividir, obtienes $\tfrac{1/20}{9/20}=\tfrac19$.
:::

---

## 2 · Normalizar al final

**Piensa: el denominador de Bayes es igual para todos los estados. ¿Necesitas calcularlo primero?**

No. Calcula los numeradores, uno por estado. Al final, divide cada numerador entre la suma.

::: definition {#mkv-c4-def-normalizar title="Normalizar"}
$$
\begin{aligned}
&w(s)\ge0\ \text{para } s\in\mathcal S,\qquad \sum_{s'}w(s')>0,\\
&\operatorname{normalizar}(w)(s)=\frac{w(s)}{\sum_{s'\in\mathcal S}w(s')}.
\end{aligned}
$$

- **Qué es:** dividir los pesos no negativos del vector $w$ entre su suma.
- **Cómo se calcula:** suma las entradas y divide cada una entre esa suma. Si la suma es 0, no puedes normalizar.
- **Qué significa:** obtienes una distribución que suma 1 y conserva las proporciones entre estados.
- **Qué no es:** normalizar solo las verosimilitudes. Como $9/10+2/10=11/10$, no forman una distribución sobre estados. Normalizarlas da la posterior solo con prior uniforme.
:::

- **Por qué puedes dejar la evidencia al final:** dividir entre el mismo número conserva las proporciones. Aquí la razón es $9:2$.
- **La evidencia sale de la suma:** los pesos suman $11/20$.

::: table {#mkv-c4-tabla-normalizar title="Pesos y posterior con paraguas y prior uniforme"}
| Estado | Prior × verosimilitud | Peso | Posterior |
|---|---|---:|---:|
| lluvia | $\tfrac12\cdot\tfrac{9}{10}$ | $9/20=0.45$ | $9/11\approx0.818$ |
| sol | $\tfrac12\cdot\tfrac{2}{10}$ | $2/20=0.10$ | $2/11\approx0.182$ |
| suma | | $11/20=0.55$ | $1$ |
:::

**El prior influye.** Con prior $(3/4,\ 1/4)$, los pesos son $27/40=0.675$ y $2/40=0.05$. Suman $29/40$. La posterior de lluvia sube a $27/29\approx0.931$.

> [!TIP]
> **Ejemplo y contraejemplo de normalizar.**
>
> - **Lo cumple.** $w=\begin{pmatrix}0.45 & 0.10\end{pmatrix}$ tiene suma $0.55>0$. Al normalizar, obtienes $\begin{pmatrix}9/11 & 2/11\end{pmatrix}$, que suma 1.
> - **No lo cumple.** $w=\begin{pmatrix}0 & 0\end{pmatrix}$ contiene los pesos de «nieve». Su suma es 0, y no hay entre qué dividir.

**Con Python.** Calcula los pesos y normaliza con fracciones exactas:

```python
from fractions import Fraction as F

def normalizar(w):
    total = sum(w.values())
    if total == 0:
        raise ValueError("la suma de los pesos es 0")
    return {s: x / total for s, x in w.items()}

prior = {"lluvia": F(1, 2), "sol": F(1, 2)}
verosimilitud = {"lluvia": F(9, 10), "sol": F(2, 10)}
pesos = {s: verosimilitud[s] * prior[s] for s in prior}
print({s: str(x) for s, x in pesos.items()})
print({s: str(x) for s, x in normalizar(pesos).items()})
```

```text
{'lluvia': '9/20', 'sol': '1/10'}
{'lluvia': '9/11', 'sol': '2/11'}
```

- **$1/10$ es $2/20$:** `Fraction` simplifica.

::: exercise {#mkv-c4-bn-ej-prior-seco title="Encuentra la posterior con un prior seco"}
En una ciudad seca, el prior es $(1/10,\ 9/10)$. Tu compañero llega con paraguas. ¿Cuánto vale la posterior de lluvia?
:::

::: hint {#mkv-c4-bn-pista-prior-seco of="mkv-c4-bn-ej-prior-seco" title="Primero los pesos"}
Antes de dividir, ¿cuánto vale cada producto prior × verosimilitud?
:::

::: answer {#mkv-c4-bn-resp-prior-seco of="mkv-c4-bn-ej-prior-seco"}
**$1/3$.** Los pesos son $9/100$ y $18/100$. Suman $27/100$. La posterior de lluvia es $9/27=1/3$. Aun con paraguas, lo más probable es que haya sol.
:::

---

## Ejercicios

::: exercise {#mkv-c4-bn-ej-tres-estados title="Calcula la posterior con tres climas"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

**Cambia una idea:** ahora hay tres estados en lugar de dos. Agregamos «nublado» al modelo. El prior es $(1/4,\ 1/4,\ 1/2)$ en el orden (lluvia, nublado, sol). Las verosimilitudes de paraguas son $9/10$, $1/2$ y $2/10$. Tu compañero llega con paraguas.

1. **Escribe** los tres pesos sin normalizar.
2. **Calcula** la evidencia $\Pr(\text{paraguas})$.
3. **Normaliza** y comprueba que la posterior suma 1.
4. **Compara** la posterior de lluvia con el $9/11$ de dos estados. Explica la diferencia.
5. **Revisa el modelo:** las tres verosimilitudes suman más de 1; ¿es un error?
:::

::: hint {#mkv-c4-bn-pista-tres-estados-1 of="mkv-c4-bn-ej-tres-estados" title="Pista 1 · ¿Qué cambia en la suma del denominador?"}
¿Cuántos términos tiene ahora la suma sobre $\mathcal S$? ¿Qué estado nuevo también explica el paraguas?
:::

::: hint {#mkv-c4-bn-pista-tres-estados-2 of="mkv-c4-bn-ej-tres-estados" title="Pista 2 · ¿Cómo revisas tu borrador?"}
¿Tus tres posteriores suman 1? Para cada estado, ¿las verosimilitudes de las dos señales suman 1?
:::

::: answer {#mkv-c4-bn-resp-tres-estados of="mkv-c4-bn-ej-tres-estados" title="Respuesta · La lluvia baja a 1/2"}
**1. Pesos.** $\tfrac14\cdot\tfrac{9}{10}=\tfrac{9}{40}$, $\tfrac14\cdot\tfrac12=\tfrac{5}{40}$ y $\tfrac12\cdot\tfrac{2}{10}=\tfrac{4}{40}$.

**2. Evidencia.** $\tfrac{9+5+4}{40}=\tfrac{18}{40}=\tfrac{9}{20}$.

**3. Normaliza.**

$$
\begin{aligned}
&\Pr(S\mid\text{paraguas})=\bigl(\tfrac{9}{18},\ \tfrac{5}{18},\ \tfrac{4}{18}\bigr)\\
&\quad=\bigl(\tfrac12,\ \tfrac{5}{18},\ \tfrac29\bigr)\approx(0.5,\ 0.278,\ 0.222).
\end{aligned}
$$

Suma $\tfrac{9+5+4}{18}=1$.

**4. Compara.** La posterior de lluvia baja de $9/11\approx0.818$ a $1/2$. Su prior bajó de $1/2$ a $1/4$. Además, nublado explica el paraguas con probabilidad $1/2$ y recibe parte del peso.

**5. Revisa el modelo.** No es un error. Las verosimilitudes de paraguas corresponden a estados distintos. No tienen por qué sumar 1. Para cada estado, las probabilidades de sus dos señales suman 1: $9/10+1/10$, $1/2+1/2$ y $2/10+8/10$.
:::

---

**Punto de control:** deberías poder calcular una posterior con Bayes para dos o más estados, y decir qué es prior, verosimilitud, evidencia y posterior. También, normalizar pesos al final y reconocer cuándo no se puede: suma 0.

---

## Lo que hay que llevarse

- **Bayes invierte la condicional:** multiplica prior por verosimilitud y divide entre la evidencia. Con prior $(1/2,\ 1/2)$ y paraguas, $\Pr(\text{lluvia}\mid\text{paraguas})=9/11\approx0.818$.
- **No voltees la barra:** $\Pr(\text{paraguas}\mid\text{lluvia})=9/10$ responde otra pregunta.
- **Normalizar al final:** divide los pesos $0.45$ y $0.10$ entre su suma $11/20$, que es la evidencia. Sin suma positiva no hay posterior.
- **El prior influye:** con $(3/4,\ 1/4)$ la misma señal da $27/29\approx0.931$.

Aquí el clima fue uno solo y no cambió. ¿Y si el estado cambia de un día a otro?

Continúa con [[mkv-el-modelo-oculto|El modelo oculto]].
