---
id: complejidad
title: Complejidad computacional
nav_title: Complejidad
summary: La unidad anterior preguntó qué puede calcular una máquina. Ésta pregunta cuánto cuesta, que resulta ser la pregunta que de verdad decide qué se puede hacer.
status: ready
estimated_time: 2h30m
tags: [complejidad, algoritmos, np, clases]
---

# Complejidad computacional

[[computabilidad|La unidad anterior]] cerró con una advertencia que ahora hay que cobrar.
Demostró que hay problemas que **ninguna máquina puede resolver nunca**, y
luego dijo, casi de pasada, que ése no es el problema con el que te vas a topar
en la práctica. El problema real es otro:

> Casi todo lo que quieres calcular **sí se puede** calcular. Lo que pasa es que
> tardaría más que la edad del universo.

Eso no es indecidibilidad. Es **complejidad**, y es de lo que trata esta unidad.

::: figure {#ilus-portada-complejidad title="Lo que se puede calcular, y lo que se puede pagar"}
![Una figura solitaria de espaldas frente a una ciudad nocturna cuyas torres se prolongan hacia arriba sin terminar](_assets/ilus-portada-complejidad.png)
:::

*(Esta imagen es una ilustración generada, no una fotografía ni un dato real.)*

## Por qué esto está en un curso de inteligencia artificial

Porque es la restricción que de verdad muerde. Ningún método de los que vienen
después —búsqueda, inferencia, planificación, entrenamiento— se topa con el
problema de la parada. Todos, sin excepción, se topan con esto: existe el
algoritmo correcto, y no lo puedes correr.

Casi cada decisión de diseño en IA es una respuesta a esta unidad. Por qué se
usa una heurística en vez de buscar la solución óptima. Por qué se aproxima en
vez de resolver. Por qué un modelo probabilístico se muestrea en vez de
integrarse. En los tres casos la respuesta es la misma: *el cálculo exacto es
intratable, y sabemos exactamente en qué sentido lo es.*

## Qué vas a poder hacer al terminar

- Decir qué es $n$ para una entrada dada —y no equivocarte con grafos ni con
  números enteros, que es donde todos se equivocan.
- Leer y escribir $O$, $\Omega$, $\Theta$ y $o$ sabiendo qué promete cada una.
- Contar el costo de un algoritmo sencillo mirando sus ciclos.
- Explicar qué son $P$, $NP$, $BPP$ y $EXP$, y ubicar un problema en la clase
  que le toca.
- Distinguir **NP-duro** de **NP-completo**, y saber por qué un solo algoritmo
  polinomial para SAT tumbaría toda la lista.
- Decir qué está demostrado y qué está abierto, sin confundir las dos cosas.

## Recorrido

Nueve páginas y dos hojas de consulta, en este orden. Cada página se sostiene
sola y declara cuánto toma leerla; el total ronda las **dos horas y media**.

| | Página | Qué resuelve | |
|---|---|---|---:|
| 1 | [[cuanto-cuesta|Cuánto cuesta un algoritmo]] | Qué es $n$, qué se cuenta como un paso, y por qué siempre el peor caso | 20m |
| 2 | [[o-grande|O grande, y su familia]] | $O$, $\Omega$, $\Theta$ y $o$ con su definición por límites | 20m |
| 3 | [[contar-un-algoritmo|Contar un algoritmo]] | Cuatro algoritmos contados línea por línea, de $\log n$ a $2^n$ | 25m |
| 4 | [[por-que-importa|Por qué esto importa]] | La frontera entre tratable e intratable, y por qué se traza donde se traza | 15m |
| 5 | [[complejidad-de-espacio|Contar memoria]] | Qué cambia cuando la medida es el espacio y no el tiempo | 15m |
| 6 | [[las-clases|P, NP y EXP]] | La máquina no determinista y las tres clases de tiempo | 25m |
| 7 | [[azar-y-bpp|Máquinas que tiran monedas]] | BPP, y Miller-Rabin explicado desde cero | 25m |
| 8 | [[completos-y-duros|Reducciones, duros y completos]] | Qué es una reducción, qué es NP-completo, y SAT contra 3-SAT | 25m |
| 9 | [[el-mapa-de-las-clases|El mapa completo]] | La cadena entera, qué se demostró y qué sigue abierto | 15m |

Y dos hojas para consultar, no para leer de corrido:

- [[notacion-complejidad|Toda la notación, en una hoja]] — cada símbolo, cómo se
  lee y en qué página salió.
- [[zoologico-de-problemas|El zoológico de problemas]] — cada problema que
  aparece en la unidad, su enunciado en una línea y su clase.

**Si vas con poco tiempo**, la ruta mínima es 1, 2, 3, 6 y 8: qué es $n$, la
notación, cómo se cuenta, las clases, y qué significa NP-completo. Las páginas
4, 5, 7 y 9 completan el cuadro.

## El examen

**Miércoles 2 de septiembre**, sobre **dos** unidades que van juntas: ésta y
[[computabilidad|Computabilidad e incompletitud]]. Se responde solo y en el momento, sin apuntes.

De esta unidad se pide poder:

- **Calcular la complejidad de un algoritmo sencillo** y justificarla contando,
  no de memoria.
- **Enunciar las definiciones con precisión.** $O$ y $\Theta$; $P$, $NP$, $BPP$;
  NP-duro y NP-completo. La diferencia entre las dos últimas se pregunta.
- **Ubicar un problema en su clase** y decir por qué.
- **Distinguir indecidible de intratable.** Es el error más común al salir de
  las dos unidades, y por eso se pregunta desde los dos lados.

> [!WARNING]
> **Indecidible e intratable no son lo mismo, y no se parecen.** Un problema
> indecidible no tiene algoritmo: ninguno, nunca, ni con todo el tiempo del
> universo. Un problema intratable tiene algoritmo —lo puedes escribir en diez
> líneas— y lo que no tienes es el tiempo para correrlo. El primero es un
> teorema sobre lo que existe; el segundo, sobre lo que cabe en una vida.
