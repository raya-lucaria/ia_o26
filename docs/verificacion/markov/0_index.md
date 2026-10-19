# Verificación — Cadenas de Markov

Registro de fuentes de `course/8_markov/`. Como en juegos, **un solo archivo
cubre la unidad**. Lo que hay que respaldar es de dos tipos:

- **Números del corpus y de los juguetes** (la frase «Con la iglesia hemos
  dado, Sancho», el *Quijote*, las simulaciones). No se citan de ninguna
  fuente: se **calculan** en `tools/markov.py` y `tools/test_markov.py`
  comprueba cada número que la prosa cita, en su página y su sección.
- **Hechos externos** (Markov, Nekrásov, Shannon, el corpus), con su fuente
  abajo.

Las fuentes se consultaron el **18 de octubre de 2026**. La investigación
completa, con lo que **no** se debe decir, está en la carpeta de planes de la
unidad (no versionada); aquí queda lo que las páginas citan.

## Hechos externos

| Afirmación | Fuente | Nivel | Matiz |
|---|---|---|---|
| Markov definió por primera vez las cadenas en 1906, en «Extensión de la ley de los grandes números a cantidades que dependen unas de otras» (*Izvestiya* de la Sociedad Físico-Matemática de Kazán, 2.ª serie, t. 15, pp. 135–156) | E. Seneta, «Markov and the Creation of Markov Chains» (2006), §3 y ref. [27], https://www.ime.usp.br/~jmstern/wp-content/uploads/2020/12/Seneta2006.pdf ; B. Hayes, «First Links in the Markov Chain», *American Scientist* 101(2): 92–97 (2013) | Alta | No «1907» (ese año es otro artículo). Bruns publicó casos especiales en 1906: se dice «Markov las definió en 1906», no «fue el único» |
| En 1902, P. A. Nekrásov sostuvo que la independencia era condición necesaria para la ley de los grandes números; Markov respondió en 1906 con variables dependientes que la cumplen | Seneta 2006, §3 («claim in 1902 of P.A. Nekrasov», «pairwise independence of summands was necessary as well as sufficient for the WLLN»); Hayes 2013 | Alta | Es la tesis **como la interpretó Markov** (Seneta). La respuesta es de 1906, no el *Oneguin* de 1913 |
| En 1913 Markov contó las primeras 20 000 letras de *Eugenio Oneguin* (el primer capítulo y dieciséis estrofas del segundo), sin espacios ni puntuación | Markov 1913, *Izvestiya Imp. Akad. Nauk* VI, 7(3): 153–162; trad. inglesa en *Science in Context* 19(4): 591–600 (2006), DOI 10.1017/S0269889706001074 (resumen leído); Hayes 2013 | Alta | Son **letras**, no palabras. Lo presentó el 23 de enero de 1913 (juliano) |
| 8 638 vocales y 11 362 consonantes; 1 104 pares vocal-vocal; Pr(vocal) = 0.432, Pr(vocal ∣ vocal) = 0.128, Pr(vocal ∣ consonante) = 0.663 | Hayes 2013; carta de Markov a Chuprov (15 de enero de 1913) citada en A. Langville y M. von Hilgers, https://langvillea.people.charleston.edu/5greatest.pdf ; aritmética: 1 104 / 8 638 ≈ 0.128 y 7 534 / 11 362 ≈ 0.663 (comprobada en `tools/test_markov.py`) | Alta | No usar las cifras de la réplica de Hayes (7 788 / 0.175 / 0.526): son de la traducción inglesa. No citar conteos de tripletas |
| Shannon (1948), «A Mathematical Theory of Communication», *Bell System Technical Journal* 27: 379–423 y 623–656; parte I, §3 «The Series of Approximations to English»: aproximaciones de orden cero, primer orden (frecuencias de letras), segundo orden (digramas) y tercer orden (trigramas), con un alfabeto de 27 símbolos | Reimpresión en https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf ; DOI 10.1002/j.1538-7305.1948.tb01338.x | Alta | Su «primer orden» es nuestra memoria 0; su «segundo orden», memoria 1. Lo hizo a mano, con tablas de frecuencias y abriendo un libro al azar; no con computadora |

## El corpus

| Afirmación | Fuente | Nivel | Matiz |
|---|---|---|---|
| *Don Quijote*, Project Gutenberg #2000, https://www.gutenberg.org/cache/epub/2000/pg2000.txt ; Cervantes murió en 1616: dominio público en México (LFDA art. 29) y en EE. UU. | Ficha https://www.gutenberg.org/ebooks/2000 ; licencia https://www.gutenberg.org/policy/license.html | Alta | El corte versionado (`tools/datos/quijote/`) quita cabecera, paratexto y pie de Gutenberg, como pide su licencia para derivar un texto de dominio público. Su `README.md` guarda URL, fecha, SHA-256 y las líneas de corte |

## Números calculados

| Afirmación | Dónde se calcula | Prueba |
|---|---|---|
| La frase «Con la iglesia hemos dado, Sancho» (II, 9): 27 letras, 26 transiciones, $N$ = 2, 9, 10, 5 y $\widehat P$ = 2/11, 9/11, 2/3, 1/3 | `frase_a_mano`, `frase_vc`, `matriz_estimada` | `test_la_frase_a_mano_es_la_del_plan` |
| Página 1: el sorteo de 26 posiciones (12/26, 11/26, 2/26, 2/11, 0.195), la regla del producto (14/25 · 9/14 · 7/9 = 7/25), la probabilidad total y las condicionales de memoria 2 del corpus (0.710, 0.624, 0.922); el ejercicio de «En un lugar de la Mancha» | `experimento_posiciones`, `regla_del_producto`, `condicionales_memoria_2`, `matriz_vce` | `test_p1_*` |
| Página 2: aritmética de Markov 1913 (1 104 / 8 638 ≈ 0.128; 7 534 / 11 362 ≈ 0.663); corpus: 1 620 532 letras, Pr(V) = 0.464, $\widehat P$ ≈ (0.181, 0.819; 0.710, 0.290); trayectoria «conla» = 4/33; el ejemplo de tres estados; MUESTREAR-FILA a mano (CVCCVV); rachas reales, geométricas y simuladas (semillas 2026 y 2027) | `aritmetica_markov_1913`, `matriz_corpus`, `probabilidad_trayectoria`, `matriz_vce`, `trayectoria_a_mano`, `rachas_*` | `test_p2_*` |
| Página 3: verosimilitudes (3.88×10⁻⁷, 1.49×10⁻⁸, 3.63×10⁻⁷), la traza de CONTAR, recuperar una matriz conocida (200 réplicas por T, semilla 2028), 784 entradas y 393 ceros, la «k» sin salidas, Laplace en la frase y en «q», la tabla de ceros por memoria | `verosimilitud`, `traza_contar`, `recuperar_p`, `entradas_memoria_1`, `fila_caracteres`, `fraccion_no_vista` | `test_p3_*` |
| Página 4: árbol de dos pasos (34/99), μ₁ a μ₃ de la frase, μₜ del corpus y 10 000 réplicas (semillas 2029 y 2030; mayor diferencia 0.010, unos 2.0 errores estándar), los dos ejercicios | `arbol_dos_pasos`, `mu_t`, `mu_t_corpus`, `diferencia_maxima_mu_t`, `ejercicio_p4_simulacion` | `test_p4_*` |
| Página 5: generar a mano, las salidas con semilla 2032 a 2036, cuánto copian del corpus (6, 10, 11, 13 letras; 0 %, 9 %, 20 %, 42 % de 8-gramas) y lo que la prosa dice de ellas | `generar_a_mano`, `generar`, `subcadena_mas_larga_en_corpus`, `fraccion_ngramas_en_corpus` | `test_p5_*` |
| Cada cifra anterior aparece literal en su página y en su sección | `_cifras()` | `test_cada_cifra_de_las_paginas_sale_de_markov`, `test_cifras_de_la_pagina_en_su_bloque` |
