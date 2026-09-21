---
id: optimizacion-entera
title: "Clase 4 · Cuando las piezas no se parten"
nav_title: Entero
summary: "De los datos y las decisiones a cuatro modelos enteros completos. Después, enumeración y ramificación y cotas para resolver el taller original."
status: ready
estimated_time: 125m
tags: [optimizacion, modelado, entera]
prerequisites: [optimizacion-lineal]
---

# Clase 4 · Cuando las piezas no se parten

**Empieza con papel y lápiz:** vas a convertir las condiciones de un taller
en cuatro modelos enteros completos. Sigue la ruta **datos → variables →
reglas → ecuaciones → modelo completo**. Después aprenderás dos algoritmos
para resolver el taller original.

En las clases anteriores podíamos repartir cantidades continuas. Aquí contamos
aparatos que deben entregarse completos. Esa condición cambia las soluciones
permitidas, aunque el objetivo y las restricciones sigan siendo lineales.

## El problema 1 · Taller original

El taller fabrica **rovers** y **sondas de superficie**. Quiere transmitir la
mayor cantidad de datos al día con los recursos disponibles.

::: table {#opt-el-taller title="Recursos y rendimiento del taller"}
| Equipo | Aleación por equipo | Calibración por equipo | Transmisión por equipo |
|---|---:|---:|---:|
| Rover | 6 kg | 1 h | 5 MB/día |
| Sonda | 4 kg | 2 h | 4 MB/día |
| **Disponible** | **24 kg** | **6 h** | **Maximizar el total** |
:::

La bitácora agrega una orden del comandante: fabricar como máximo cuatro
rovers. Este es el **problema 1 · Taller original**, al que volveremos para
aprender los dos algoritmos.

## Cuatro problemas con nombres propios

| Problema | Qué cambia respecto del taller original |
|---|---|
| **1 · Taller original** | Ningún cambio: usamos los datos de la bitácora |
| **2 · Preparar la línea de ensamble de rovers** | Preparar las máquinas consume 3 horas una sola vez, además de la hora de calibración de cada rover |
| **3 · Fabricar cero rovers o un lote de al menos tres** | Se permite fabricar 0, 3 o 4 rovers; no hay horas de preparación adicionales |
| **4 · Compartir la antena entre los rovers** | Los primeros dos rovers transmiten 5 MB/día cada uno; el tercero y el cuarto, 3 cada uno |

**Los problemas 2, 3 y 4 son variantes independientes del problema 1.** Cada
uno cambia una condición del taller original; los cambios no se acumulan.
Primero formularemos los cuatro, conservando todas las condiciones de cada
enunciado y los dominios de sus variables. El objetivo de esta primera parte
es aprender a construir modelos, incluso cuando haya miles de variables.
Después resolveremos el **problema 1** por enumeración y por ramificación y
cotas.

## La ruta de trabajo

| Etapa | Qué harás | Qué debes poder explicar al terminar |
|---|---|---|
| 1 · La bitácora | Separar datos y variables; describir reglas y casos; construir ecuaciones | Qué es un dato, qué se decide y cómo una condición se convierte en una expresión |
| 2 · Los modelos | Revisar cuatro formulaciones completas, con parámetros antes de los datos | Cómo se construye cada renglón y dónde queda cada condición del relato |
| 3 · Enumerar | Generar, filtrar y comparar candidatos | Por qué encuentra un óptimo y cuánto trabajo requiere |
| 4 · Ramificar y acotar | Resolver relajaciones y cerrar subproblemas | Qué permite descartar candidatos sin enumerarlos individualmente |

1. [[la-bitacora-del-taller|Leer la bitácora y plantear los ejercicios]].
2. [[el-modelo-del-taller|Comprobar los modelos]].
3. [[enumerar|Resolver por enumeración]].
4. [[ramificar-y-acotar|Resolver por ramificación y cotas]].

## Cómo usar estas páginas

Intenta cada formulación antes de abrir sus pistas o leer las soluciones.
Primero expresa las condiciones en palabras y por casos; después construye
las ecuaciones con parámetros y sustituye los datos. Termina cada intento
reuniendo el objetivo, todas las restricciones y los dominios en un solo
modelo. En esta etapa conserva las condiciones explícitas del enunciado;
la búsqueda de un óptimo viene después.

En las tablas de los algoritmos sigue dos cosas: **qué se está revisando** y
**qué solución se guarda**.

Si pierdes el hilo, vuelve al comienzo del bloque: ahí se indica el problema
activo y el paso pendiente. Los problemas 2, 3 y 4 se trabajan por
separado; para aprender los algoritmos regresamos al **problema 1 · Taller
original**.

Como orientación, reserva **unos 125 minutos** para el recorrido principal con
intentos breves: 20 para plantear, 30 para comparar modelos, 30 para enumerar y
45 para ramificar. Es una estimación de trabajo, no una prueba contra reloj.
Las ampliaciones y el notebook pueden hacerse después. Hay un punto de parada
al terminar cada página.

## Práctica en el notebook

El cuaderno permite ejecutar **enumeración** sobre el taller y las tres
variantes, comparar sus resultados con `scipy.optimize.milp` y experimentar con
el número de variables y restricciones. Úsalo después de hacer el recorrido a
mano. La llamada a `milp` comprueba resultados; no muestra los pasos del árbol
que construirás en la última página.

El cuaderno incluye representaciones simplificadas para esos contrastes. Las
mismas decisiones físicas pueden representarse con distintas variables y
restricciones: comprueba siempre qué significa cada una. En particular, la
formulación de la antena que construiremos en estas páginas usa una binaria
para imponer el orden de los tramos en toda asignación permitida; al comparar
con el cuaderno, distingue esa garantía del resultado que se obtiene al
maximizar.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/6_optimizacion/_assets/04_taller_entero.ipynb)

El archivo local es `course/6_optimizacion/_assets/04_taller_entero.ipynb`.
Necesita `numpy`, `scipy` y `matplotlib` si lo ejecutas en tu equipo.

En esta clase buscamos **una solución óptima** de problemas lineales enteros
con cotas finitas. Las variables mixtas, los planos de corte y las heurísticas
de los solucionadores quedan para otro momento.
