# Plan de sesión — Computabilidad e incompletitud

**Fecha:** miércoles 26 de agosto de 2026, 16:00–18:00
**Unidad:** `course/3_computabilidad/`
**Preparación que traen:** el video de Veritasium (34 min) y las ocho preguntas
de `0_index.md`. Tarea `ver-video-computabilidad`, `due: 2026-08-26`.

---

## El principio que ordena la sesión

**El video ya contó la historia. La sesión hace lo que el video no puede: derivar
en vivo y ponerlos a trabajar.** Y las páginas de repaso —que se publican
después— hacen lo que la sesión no puede: cubrirlo todo con calma.

De ahí el reparto. Dos derivaciones se hacen **en el pizarrón, con ellos
diciendo el siguiente paso**: la traza de la máquina de juguete y la
demostración del problema de la parada. Todo lo demás va a ritmo de vocabulario,
rápido, sin detenerse — porque lo van a tener escrito.

No intentes cubrir en 120 minutos lo que las ocho páginas cubren en tres horas.
Si algo se cae, que se caiga de los bloques 1, 5 y 8, nunca del 2 ni del 6.

## Minutado

| Min | Bloque | Qué pasa | Pizarrón |
|---:|---|---|---|
| 0–12 | **0 · Aterrizar el video** | Las ocho preguntas, una por una: «¿quién se atoró en ésta?» a mano alzada. Ajusta el énfasis del resto según dónde estén las manos | Las 8 numeradas, en la orilla. Se quedan toda la sesión |
| 12–20 | **1 · Vocabulario mínimo** | $\Sigma$, cadena, $\Sigma^*$, lenguaje. Y el giro: **un problema de decisión *es* un lenguaje**. Rápido | Pizarrón A |
| 20–50 | **2 · La máquina de Turing** ⭐ | La 7-tupla. La máquina de $0^n1^n$. **Trazar `0011` en vivo**, pidiéndoles el siguiente paso cada vez | Pizarrón B (fijo) + C |
| 50–60 | **3 · Ejercicio en parejas** | Trazar `001`. ¿En qué paso rechaza y por qué? Luego alguien lo pasa al pizarrón | C |
| 60–65 | *Descanso* | | |
| 65–78 | **4 · Los tres desenlaces** | Acepta / rechaza / **cicla**. Decidible vs. reconocible: la promesa de detenerse. Por qué «córrelo y espera» no sirve | A (se borra el 1) |
| 78–82 | **5 · Todo es un número** | Shortlex, $\langle M\rangle$, la máquina universal. Bisagra, rápido | Orilla de A |
| 82–100 | **6 · El problema de la parada** ⭐ | $H$, $D$, y la tabla de dos casos. En vivo | Pizarrón C (se borra) |
| 100–115 | **7 · Gödel con el `for`** | El programa $P$. Tres pasos. Y $\text{Con}(F)$ como programa | C |
| 115–120 | **8 · El mismo truco** | La tabla de tres columnas y el cierre para IA | A |

⭐ = los dos bloques que justifican que la sesión sea presencial. Protégelos.

## Orden de pizarrón

Tres zonas, y **B no se borra nunca**:

- **A — izquierda, rotativa.** Vocabulario, luego las tres clases, luego la
  síntesis. Se borra dos veces.
- **B — centro, FIJA TODA LA SESIÓN.** La 7-tupla y la tabla de $\delta$ de la
  máquina de juguete. Se escriben una vez a los 20 minutos y se quedan hasta el
  final: los bloques 3, 4 y 6 apuntan a ella constantemente. Si la borras, el
  bloque 6 se queda sin el objeto del que habla.
- **C — derecha, de trabajo.** Las trazas, y luego las dos demostraciones.

En la orilla, desde el minuto 0: **las ocho preguntas del video**, numeradas.
Cada vez que la sesión contesta una, se palomea. Al final deben estar las ocho —
y es el cierre visual de la clase.

## Bloque 2, con detalle — la máquina de juguete

Es media hora y es el corazón. **El orden importa: español primero, símbolos
después.**

1. **Qué contesta** (2 min). «¿Lo que me diste son unos cuantos ceros seguidos de
   exactamente la misma cantidad de unos?» Acepta `01`, `0011`, `000111`.
   Rechaza `001`, `00111`, `0101`, y la vacía.
   Ancla: **es el caso más simple de paréntesis balanceados**, con un solo nivel
   de anidamiento. *(No digas que **es** el problema de los paréntesis
   balanceados: `()()` = `0101` está balanceado y esta máquina lo rechaza.)*
2. **La estrategia, sin notación** (3 min). «No puede contar: no tiene dónde
   guardar un número. Lo que hace es **emparejar**.» Tacha un cero, busca un uno,
   lo tacha, regresa, repite.
   **Esta frase es la que se tienen que llevar**, porque explica por qué la
   cinta es indispensable: la memoria no está en los estados, está en las marcas.
3. **La 7-tupla** (5 min), en el pizarrón B. Y el contraste que *es* la máquina:
   **la tabla de reglas es finita, la cinta no.**
4. **La tabla de $\delta$** (5 min), también en B. Con los estados nombrados en
   español: $q_0$ busca el siguiente cero sin tachar, $q_1$ va a la derecha
   buscando un uno, $q_2$ regresa, $q_3$ verifica que solo queden marcas.
5. **La traza de `0011`** (15 min), en C, **preguntándoles el siguiente paso cada
   vez**. Trece configuraciones, doce transiciones. Es lento a propósito: es la
   única media hora del semestre en que van a ver una máquina de Turing correr.

Notación en el pizarrón: configuración $u\,q\,v$, con el cabezal sobre el primer
símbolo de $v$. Dibuja la flechita bajo el símbolo leído las primeras tres veces
y luego déjala.

**Dos cosas que van a preguntar, con la respuesta corta:**

- *¿Por qué hay celdas vacías en $\delta$?* Porque son inalcanzables. $\delta$ es
  total —va a $q_{\text{rej}}$— pero esas combinaciones nunca ocurren. Está
  verificado por simulación exhaustiva.
- *¿Y si el cabezal se sale por la izquierda?* La cinta es infinita **hacia la
  derecha**; si $\delta$ ordena moverse a la izquierda en la casilla 0, se queda.
  A esta máquina no le pasa nunca.

## Los dos ejercicios de salón

**Ejercicio 1 (min 50–60), en parejas.** Trazar `001` con la tabla de $\delta$
que está en el pizarrón B. ¿En qué paso rechaza y por qué?

> **Respuesta:** ocho pasos. En el paso 8 está en $q_1$ —buscando un uno— y
> encuentra el final de la cinta. Rechaza porque **había más ceros que unos**.
> Ojo: las seis primeras *reglas* son las mismas que en `0011`, pero las
> configuraciones son distintas desde el paso 1, porque la entrada es otra. No
> los dejes comparar tablas renglón a renglón.

Que uno lo pase al pizarrón. Si sobra tiempo: *¿qué pasa con `0101`?* (rechaza en
5 pasos, y es el caso que rompe la analogía de los paréntesis).

**Ejercicio 2 (min 98–100), rápido y en voz alta.** *Si HALT es reconocible —lo
simulas y si para, contestas—, ¿por qué eso no lo vuelve decidible?*

> **Respuesta:** porque si la máquina **no** para, nunca te enteras. No hay un
> momento en el que puedas rendirte con derecho. Reconocible te da la respuesta
> cuando es «sí»; no te la da cuando es «no».

Es la pregunta que separa a quien entendió de quien repite el video.

## Bloque 6, con detalle — el problema de la parada

En el pizarrón, en este orden, sin apurarse:

1. **Qué sería $H$**: recibe $\langle M,w\rangle$, **siempre se detiene**, y
   responde SÍ o NO. Dibuja la caja.
2. **Construye $D$** alrededor de $H$: con entrada $\langle M\rangle$, le
   pregunta a $H$ si $M$ se detiene con su propio código, y **hace lo
   contrario**. Dibuja $H$ *dentro* de $D$ — que se vea que $D$ está hecha con
   $H$ es medio argumento.
3. **La pregunta**: ¿qué hace $D$ con su propio código? Deja que la contesten.
4. **La tabla de dos casos**, en el pizarrón:

| Si suponemos que… | $H$ contestó… | y entonces $D$… | lo cual |
|---|---|---|---|
| $D$ **se detiene** con $\langle D\rangle$ | SÍ | cicla | contradice lo supuesto |
| $D$ **cicla** con $\langle D\rangle$ | NO | se detiene | contradice lo supuesto |

5. **El cierre**: no hay una tercera rama. Luego $H$ no existe.

Y señala **dónde está la diagonal**: máquinas en las filas, sus códigos en las
columnas, $D$ construida para diferir de cada $M_i$ en la casilla $(i,i)$. Es
Cantor con máquinas en lugar de reales — que es lo que el video ya les enseñó
como dibujo.

## Bloque 7, con detalle — Gödel sin maquinaria

La ruta es la computacional, no la de la numeración de Gödel. Escribe el
programa en el pizarrón:

```
P(x):                                        # x es el código de un programa
    for p in shortlex:
        if EsDemostracion(p, NoPara(x, x)):
            halt
```

En español: **P busca una demostración de que no termina, y si la encuentra,
termina.**

Luego los tres pasos, preguntándoles cada uno:

1. *¿Puede terminar $P(\langle P\rangle)$?* No: si terminara, es que encontró una
   demostración de que no termina, y F solo demuestra verdades. **Luego no
   termina.**
2. *Entonces, ¿es verdad que no termina?* Sí.
3. *¿Lo demuestra F?* No: si lo demostrara, el `for` encontraría esa demostración
   y $P$ terminaría.

**Hay una verdad que F no demuestra.** Eso es el primer teorema.

Di en voz alta la honestidad: usamos «**F solo demuestra verdades**», que es más
fuerte que «F no se contradice». Eso es exactamente lo que hace que quepa en seis
líneas — y es la razón por la que la demostración original de Gödel es larga.

Para el segundo: **el buscador de contradicciones**. El programa que enumera
demostraciones de F y se detiene si encuentra una de $0=1$. F consistente ⟺ ese
programa nunca para. Y el segundo teorema dice: **F no puede demostrar que ese
programa no para.**

## Cierre (bloque 8)

La tabla, en tres columnas:

| | Cantor | Gödel | Turing |
|---|---|---|---|
| La diagonal | dígito $n$ del real $n$ | $P$ con entrada $\langle P\rangle$ | $M_i$ con entrada $\langle M_i\rangle$ |
| El giro | cambiar cada dígito | terminar si se demuestra que no termina | lo contrario de lo que $H$ predice |

Y la moraleja, dicha con cuidado: **el núcleo común no es la autorreferencia, es
la diagonalización.** En Cantor no hay autorreferencia — los reales no hablan de
sí mismos. En Gödel y en Turing la lista es de objetos que sí pueden hablar de sí
mismos, y ahí la diagonal se vuelve autorreferencia.

Y para la IA, dos frases: el límite **no** prohíbe que una máquina sea
inteligente; sí prohíbe el verificador perfecto de programas arbitrarios, que es
donde muerde en alineación. **La computabilidad fija el techo del edificio; casi
todo el trabajo ocurre en los primeros pisos.**

Palomea la octava pregunta.

## Qué anunciar antes de que se vayan

- Las páginas de repaso de la unidad **se publican después de esta sesión**, y
  ahí va todo con calma, con ejercicios y soluciones.
- **No hay tarea nueva.** La del video ya cubrió esta sesión.

## Si te quedas sin tiempo

En este orden de sacrificio:

1. Bloque 8 → una frase y se acabó.
2. Bloque 5 → «se puede numerar todo, y hay una máquina que corre a las demás».
3. Bloque 1 → dilo mientras escribes la 7-tupla.
4. Bloque 7 → hasta el primer teorema; el segundo queda enunciado sin más.

**Nunca los bloques 2, 3 y 6.** Si se cae el 6, la unidad se queda sin su
resultado central y no hay página que lo repare, porque nadie va a leer una
demostración que no vio nacer.
