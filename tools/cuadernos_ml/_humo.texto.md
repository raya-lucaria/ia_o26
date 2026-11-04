<!-- Guion del notebook de humo. No se publica; prueba el generador. -->

### celda: portada

# Notebook de humo · El cargador de ml_lab

Este notebook no acompaña ninguna página: comprueba que la celda de arranque
carga `ml_lab` y que `requiere` acepta la versión con que se generó.

### celda: idea

La celda de arranque prueba tres fuentes en orden: la copia local, la del
repositorio y el respaldo que trae el propio notebook. Se queda con la primera
que tenga la misma versión mayor y una menor igual o más nueva.

### celda: bloque-1-predice

**Predice.** Si corres el notebook sin red, ¿qué versión de `ml_lab` queda
cargada: ninguna, la del repositorio o la del respaldo?

### celda: bloque-1-mira

**Mira.** La línea impresa dice la versión cargada y la parte en sus dos
números: la versión mayor $X$ y la menor $Y$.

### celda: bloque-1-explica

<details><summary>Explicación</summary>

La del respaldo: sin red falla la descarga y la celda escribe el `ml_lab.py`
que viene incrustado, que es justo la versión con que se generó el notebook.

</details>

### celda: taller-intro

**Taller.** Pide una versión con otra $X$ (por ejemplo `"9.0"`) y mira el
mensaje de error de `requiere`.

### celda: cierre

Si todas las celdas corrieron, el generador y el cargador funcionan.
