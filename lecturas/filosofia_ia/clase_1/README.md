# Módulo 1 — ¿Accelerate What?

**Filosofía de la IA · Aceleracionismo, de Marx al valle**

Seis lecturas, 63 páginas, entre 3.5 y 4 horas. Encadenan con la sección de
[aceleracionismos y TESCREAL](../../../course/1_introduccion/2_historia_ia/7_ia_y_sociedad.md)
de la unidad de historia: aquí están los textos que ese mapa ideológico resume.

## Cuadernillo

**[`lecturas/filosofia_ia_clase_1_cuadernillo.pdf`](lecturas/filosofia_ia_clase_1_cuadernillo.pdf)**
— 47 páginas con las cuatro lecturas que existen en fuentes primarias abiertas,
maquetadas en un solo archivo con la razón de cada una.

| # | Lectura | Autor | Año | Fuente | Estado |
|---|---|---|---|---|---|
| 1 | Fragmento sobre las máquinas | Marx | 1858 | [Grundrisse, MIA](https://www.marxists.org/archive/marx/works/1857/grundrisse/ch13.htm) | ✅ en el cuadernillo |
| 2 | Swarmachines | CCRU | 1996 | [ccru.net](http://www.ccru.net/swarm1/1_swarm.htm) | ✅ en el cuadernillo |
| 3 | Meltdown | Land | 1994 | [ccru.net](http://www.ccru.net/swarm1/1_melt.htm) | ✅ en el cuadernillo |
| 4 | La ideología californiana | Barbrook y Cameron | 1995 | [imaginaryfutures.net](http://www.imaginaryfutures.net/2007/04/17/the-californian-ideology-2/) | ✅ en el cuadernillo |
| 5 | *El Anti-Edipo*, pp. 239–240 | Deleuze y Guattari | 1972 | — | ⚠️ de la edición Minnesota |
| 6 | «Terminator vs Avatar», pp. 335–346 | Fisher | 2012 | — | ⚠️ de *#Accelerate* |

Las dos últimas siguen en derechos y no tienen copia abierta verificable.

**Si consigues sus PDF**, déjalos en `fuentes/` con estos nombres exactos y la
siguiente construcción los recorta por página y los une al cuadernillo:

| Archivo esperado en `fuentes/` | Páginas que se recortan |
|---|---|
| `deleuze_guattari_anti_oedipus_minnesota_1983.pdf` | 239–240 |
| `accelerate_reader_urbanomic_2014.pdf` | 335–346 |

Los rangos son los de tu temario. Si el PDF tiene menos páginas de las pedidas,
la construcción se detiene y avisa que probablemente sea otra edición, en vez de
recortar el pasaje equivocado en silencio. Si el archivo no está, el cuadernillo
se arma sin él y lo reporta.

Esos PDF están en `.gitignore`: se quedan en tu disco, no en el repositorio.

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
