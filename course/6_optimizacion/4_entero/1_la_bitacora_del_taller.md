---
id: la-bitacora-del-taller
title: La bitácora del taller
nav_title: La bitácora
summary: "Una bitácora nueva y cómo se lee: qué preguntarle, dónde se esconde lo que sobra y lo que falta, y cómo se decide el dominio. El modelo lo escribes tú."
status: ready
estimated_time: 12m
tags: [optimizacion, modelado, entera]
---

# La bitácora del taller

**¿Qué dice exactamente este problema?**

Vienes de [[optimizacion-continua|el reactor]] · Aquí: leer · Sigue: escribir el
modelo.

> **Bitácora — día 214.**
>
> El taller tiene que fabricar el equipo que baja al planeta: **rovers** y
> **sondas de superficie**. Quedan **24 kg de aleación** y **6 horas de
> calibración** antes de la ventana de descenso. El taller consume la misma
> electricidad esté haciendo lo que esté haciendo.
>
> Un rover se lleva 6 kg y 1 hora, y transmite 5 MB al día. Una sonda se lleva
> 4 kg y 2 horas, y transmite 4 MB al día.
>
> El comandante cierra la reunión: «y no me hagan más de cuatro rovers».

**Esta página no escribe el modelo. Lo escribes tú.** Aquí solo están las
preguntas que hay que hacerle a una bitácora, y cómo se contesta cada una.

## 1 · Qué preguntarle, y cómo se escribe la respuesta

| Pregunta | Cómo la contestas | Qué forma tiene la respuesta |
|---|---|---|
| ¿Qué decido? | Busca lo que puedes **contar o repartir**, no lo que ya está decidido | Una variable por cada cosa, con su unidad dicha en voz alta |
| ¿Qué me limita? | Busca lo que **se acaba** | Una desigualdad por recurso: lo que consumes $\le$ lo que hay |
| ¿Qué quiero? | Busca lo único que quieres que **suba** | $\max$ de una suma: coeficiente por variable |
| ¿De qué tipo son los números? | **Pregúntate qué significaría media unidad** de cada variable | Un renglón propio para el dominio |

### El dominio, que es la casilla que casi todos se saltan

Es la pregunta nueva de esta clase, así que va con más detalle. Tres preguntas,
en este orden:

1. **¿Media unidad sirve de algo?** Media hora de trabajo sí significa algo.
   ¿Y medio aparato? Si la mitad no hace nada, la variable no puede valer $3/2$.
2. **¿Puede ser negativa?** Casi nunca, y hay que escribirlo igual.
3. **¿Tiene un tope propio**, independiente de los recursos?

Y ojo con **cómo** se expresa: el dominio va en su **propio renglón**, al final
del modelo, y **no sustituye a** $x \ge 0$. Son dos afirmaciones distintas sobre
la misma variable.

## 2 · Tres cosas que esconde toda bitácora

No las busques al escribir: búscalas **antes**.

| Qué esconde | Cómo se reconoce |
|---|---|
| **Un dato que sobra** | Vale lo mismo en todos los planes posibles, así que no puede cambiar la decisión |
| **Un dato que falta** | Un número que el modelo necesita y nadie dijo. No lo inventes: anótalo como pregunta |
| **Una frase que no aporta** | Suena a restricción, pero otra parte del modelo ya la impone |

Esta bitácora trae una de cada. Cuáles son, se contesta en la página siguiente.

## 3 · Plantéalo tú

Papel y lápiz. Escribe el modelo en forma canónica **antes de pasar de página**.

No lo corrijas contra nada todavía. Revisa solo que tenga sus siete partes:

- Sentido: ¿maximizas o minimizas?
- Función objetivo, con sus coeficientes
- Variables de decisión, con su unidad dicha en voz alta
- Una restricción por recurso
- Lados derechos
- **Dominio de cada variable**
- Nada de la bitácora que sobre, dentro

## 4 · Y ahora cámbialo

Tres avisos que llegan después. **Ninguno es un cambio de número**: los tres
piden algo que las clases anteriores no te enseñaron a escribir.

1. **Encender cuesta.** Poner en marcha la línea de rovers gasta 3 horas de
   calibración, se fabrique uno o se fabriquen cuatro. Si no se fabrica
   ninguno, no se gasta.
2. **O ninguno, o lote completo.** Los rovers se calibran en lote: o no
   fabricas ninguno, o fabricas **al menos tres**.
3. **La antena se comparte.** Los dos primeros rovers transmiten 5 MB cada uno;
   del tercero en adelante, **3 MB**.

Pista, y solo eso: dos de los tres necesitan una **variable nueva que no cuenta
nada** —solo dice sí o no—, y el tercero necesita **partir una variable en
dos**. En los tres, la pregunta difícil es la misma: **cómo se conecta lo nuevo
con lo que ya estaba.**

Las tres respuestas están en la página siguiente, plegadas. No las abras antes
de haber escrito algo, aunque esté mal.

> **Cuidado.** Si un número no está en la bitácora, no lo inventes. Anótalo como
> pregunta y sigue: preguntarlo es parte del trabajo, y la respuesta puede
> cambiar el dominio entero.

## Lo que hay que llevarse

- Modelar empieza leyendo, no escribiendo.
- El dominio no se hereda del problema anterior: se decide preguntando qué
  significaría media unidad.
- Lo que no puedas justificar señalando una frase de la bitácora, no entra al
  modelo.

Cuando ya tengas el tuyo escrito: [[el-modelo-del-taller|el modelo, escrito]].
