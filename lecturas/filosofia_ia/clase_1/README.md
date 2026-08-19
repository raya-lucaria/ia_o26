# Módulo 1 — ¿Accelerate What?

**Filosofía de la IA · Aceleracionismo, de Marx al valle**

Seis lecturas, 57 páginas, entre 3.5 y 4 horas. Encadenan con la sección de
[aceleracionismos y TESCREAL](../../../course/1_introduccion/2_historia_ia/7_ia_y_sociedad.md)
de la unidad de historia: aquí están los textos que ese mapa ideológico resume.

## Cuadernillo

**[`lecturas/filosofia_ia_clase_1_cuadernillo.pdf`](lecturas/filosofia_ia_clase_1_cuadernillo.pdf)**
— **57 páginas, las seis lecturas completas**, cada una con su portadilla y la
razón por la que se lee.

| # | Lectura | Autor | Año | Fuente | Estado |
|---|---|---|---|---|---|
| 1 | Fragmento sobre las máquinas | Marx | 1858 | [Grundrisse, MIA](https://www.marxists.org/archive/marx/works/1857/grundrisse/ch13.htm) | ✅ en el cuadernillo |
| 2 | *El Anti-Edipo*, pp. 239–240 | Deleuze y Guattari | 1972 | ed. Paidós, p. 247 | ✅ en el cuadernillo |
| 3 | Meltdown | Land | 1994 | [ccru.net](http://www.ccru.net/swarm1/1_melt.htm) | ✅ en el cuadernillo |
| 4 | «Terminator vs Avatar», pp. 335–346 | Fisher | 2012 | extracto de *#Accelerate* | ✅ en el cuadernillo |
| 5 | Swarmachines | CCRU | 1996 | [ccru.net](http://www.ccru.net/swarm1/1_swarm.htm) | ✅ en el cuadernillo |
| 6 | La ideología californiana | Barbrook y Cameron | 1995 | [imaginaryfutures.net](http://www.imaginaryfutures.net/2007/04/17/the-californian-ideology-2/) | ✅ en el cuadernillo |

### Sobre las dos que llegaron como PDF

Ambas se reproducen de la edición que las tiene, y el pipeline las recorta por
página. Dos avisos que importan al citarlas en clase:

- **El Anti-Edipo es la edición española de Paidós**, no la Minnesota de 1983 que
  cita el temario. El pasaje equivalente a sus pp. 239–240 **cabe entero en la
  p. 247** de esta edición, que es más densa. Cortar 239–240 aquí habría dado un
  pasaje distinto: lo verifiqué buscando «acelerar el proceso» en el texto, no
  confiando en el número.
- **El archivo de Fisher ya es el extracto** de la antología: 12 páginas, las
  335–346, así que se usa entero.

Qué se versiona y qué no: los dos PDF conseguidos —los archivos completos en
`fuentes/`— están en `.gitignore` y viven solo en tu disco. Los recortes de los
pasajes (`lecturas/deleuze-guattari-antiedipo.pdf`,
`lecturas/fisher-terminator-avatar.pdf`) y el cuadernillo que los contiene sí
están versionados, y el cuadernillo se publica en el sitio del curso.

## Verificación contra la edición original

Los dos textos de CCRU se comprobaron contra el folleto donde se publicaron,
*Abstract Culture* (serie completa, 258 pp., vía [Monoskop](https://monoskop.org/CCRU)):

| Texto | Lo que tenemos | Folleto original | Diferencia |
|---|---|---|---|
| Meltdown | 3 554 palabras | 3 560 (pp. 14–26 de *swarm1*) | 0.2 % |
| Swarmachines | 1 866 palabras | 1 775 (pp. 72–78 de *swarm1*) | 5.1 % |

**Ambos están íntegros.** Swarmachines son 7 páginas en el original, no 11: la
diferencia con el temario es la introducción que los editores de la antología le
anteponen. El texto de ccru.net no está recortado.

## Dos avisos sobre lo que sí está

**La paginación no coincide.** El temario cuenta páginas de la antología
*#Accelerate*; el cuadernillo toma los textos de sus fuentes primarias. El texto
es el mismo, la numeración no. Marx quedó recortado a las ~4 600 palabras que
corresponden al fragmento antologizado, que en el Grundrisse cruza dos cuadernos.

**«La ideología californiana» está completa.** El temario pide pp. 44–53, que es
la versión abreviada de la antología; la de imaginaryfutures es el ensayo íntegro
de los autores, más largo. Si prefieres la versión corta, dímelo y la recorto.

## Cómo se reconstruye

```bash
python3 tools/bajar_lecturas.py filosofia_ia/clase_1   # descarga y verifica
python3 tools/lecturas.py       filosofia_ia/clase_1   # recorta y maqueta
```

El descargador comprueba que cada archivo contenga lo que dice contener antes de
guardarlo. Agregar una lectura es agregar una entrada a `LECTURAS` en
`tools/lecturas.py`, con su recorte y la razón por la que se lee.

Las fuentes quedan en `fuentes/` tal como se descargaron, para que el recorte
sea auditable.

`introduccion.md` es la fuente de la introducción general del cuadernillo; la
página del curso (`course/2_filosofia_ia/1_aceleracionismo/0_index.md`) lleva una copia
literal de este texto, bajo guarda de `tools/test_lecturas.py`
(`test_la_introduccion_no_ha_derivado`), que falla si ambos divergen.
