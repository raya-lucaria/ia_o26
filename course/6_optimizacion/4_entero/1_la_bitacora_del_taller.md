---
id: la-bitacora-del-taller
title: La bitácora del taller
nav_title: La bitácora
summary: "Una bitácora nueva y el trabajo de siempre: separar lo que decides, lo que te limita y lo que mides. Aquí no se resuelve nada."
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

## 1 · Las tres trampas

Toda bitácora trae tres. Cázalas antes de escribir nada.

| Trampa | Cuál es aquí | Qué hago |
|---|---|---|
| Un dato que sobra | La electricidad del taller | Fuera: es igual en todos los planes |
| Un dato que falta | **¿Sirve de algo media sonda?** Nadie lo dijo | Preguntar. Respuesta: no transmite |
| Una frase que no aporta | «No más de cuatro rovers» | Fuera: la aleación ya lo impide |

La segunda es la importante. Todo lo que hace distinta a esta clase cuelga de esa
respuesta.

## 2 · Lo que sí entra

| Parte | En la bitácora |
|---|---|
| Lo que decides | Cuántos rovers y cuántas sondas fabricar |
| Lo que te limita | 24 kg de aleación · 6 horas de calibración |
| Lo que mides | MB transmitidos al día, y los quieres al máximo |
| Qué clase de números | **Cantidades completas.** Media sonda no es media respuesta: es nada |

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

Dos avisos que llegan después. Replantea cada uno **sin volver a empezar**: di
qué renglón se mueve y cuál se queda igual.

1. **Llega un cargamento**: habrá 30 kg de aleación, no 24.
2. **Cada rover necesita su propia antena**, y solo hay 3 antenas.

Las dos respuestas están en la página siguiente, plegadas. No las abras antes de
haber escrito algo.

> **Cuidado.** La frase del comandante suena a restricción y no lo es.
> Escribirla te deja un renglón que no hace nada — y en un modelo grande, un
> renglón que no hace nada es un renglón que nadie vuelve a revisar.

## Lo que hay que llevarse

- La bitácora trae siempre un dato de más, uno de menos y una frase inútil.
- El dato que falta suele ser el que fija **de qué tipo son los números**.
- Un modelo bien escrito se revisa por su forma, no por su resultado.

Ahora sí, con nombre y símbolos: [[el-modelo-del-taller|el modelo, escrito]].
