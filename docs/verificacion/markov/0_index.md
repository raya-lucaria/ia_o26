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
| Brin y Page (1998), «The Anatomy of a Large-Scale Hypertextual Web Search Engine», *Computer Networks and ISDN Systems* 30: 107–117. Escriben PR(A) = (1−d) + d(PR(T1)/C(T1) + … + PR(Tn)/C(Tn)) y «We usually set d to 0.85» | Espejo de infolab.stanford.edu/~backrub/google.html en https://gwern.net/doc/www/infolab.stanford.edu/6f7c60d7e3beb371d089d6b926d4f523a4bdcd5c.html ; ficha https://research.google/pubs/pub334/ | Alta | Su $d$ es nuestra $\alpha$. Su fórmula **no está normalizada** (los valores suman el número de páginas, no 1), aunque el texto dice que forman una distribución. Consultado el 21 de octubre de 2026 |
| Page, Brin, Motwani y Winograd, «The PageRank Citation Ranking: Bringing Order to the Web», Stanford InfoLab Technical Report 1999-66: el navegante al azar que «se aburre» y salta; los enlaces colgantes se quitan, se calcula y se reinsertan | Copia en https://www.informatik.uni-leipzig.de/~jtiepmar/lehre/ads/ss19/literature/Page%20et.al.%201998.pdf (§2.5, §2.7) | Alta | Sustituir cada fila sin salidas por $v$ ($\overline P$) es la convención de los libros posteriores, no la del informe |
| Serpientes y escaleras viene de una familia de juegos de dados de la India (*gyan chaupar*, *moksha patam*); F. H. Ayres lo publicó en Londres en 1892; Milton Bradley lo vendió como *Chutes and Ladders* en 1943 | Topsfield, «The Indian Game of Snakes and Ladders», *Artibus Asiae* 46(3), 1985; V&A, https://collections.vam.ac.uk/item/O26344/snakes-and-ladders-board-game/ ; Slesin, *The New York Times*, 15 de julio de 1993 | Media | **Sin fechas antiguas** («siglo II», «siglo XIII»): no tienen respaldo serio. El tablero de 100 casillas de la página es nuestro, no histórico |
| Los teoremas ergódicos generales: G. D. Birkhoff, «Proof of the ergodic theorem», *Proc. Natl. Acad. Sci.* 17 (1931): 656–660 (puntual); J. von Neumann, «Proof of the quasi-ergodic hypothesis», *Proc. Natl. Acad. Sci.* 18 (1932): 70–82 (medio) | https://encyclopediaofmath.org/wiki/Birkhoff_ergodic_theorem ; C. C. Moore, «Ergodic theorem, ergodic theory, and statistical mechanics», *PNAS* 112(7): 1907–1911 (2015), https://pmc.ncbi.nlm.nih.gov/articles/PMC4343160 | Alta | Se publicaron casi a la vez y hubo disputa de prioridad (Moore 2015): la página no dice quién fue primero. El teorema ergódico de las cadenas finitas es un caso particular, no su origen. Consultado el 21 de octubre de 2026 |
| Perron (1907) probó el teorema para matrices positivas y Frobenius (1912) lo extendió a no negativas irreducibles; el «teorema ergódico» de las cadenas, como se enuncia hoy, es una síntesis posterior (Kolmogorov, Doeblin, años treinta) | Perron, *Math. Ann.* 64 (1907) 248–263; Frobenius, *Sitzungsber. Preuss. Akad. Wiss.* (1912) 456–477; Seneta 2006 | Alta | No atribuir el teorema ergódico a un solo artículo |

## El corpus

| Afirmación | Fuente | Nivel | Matiz |
|---|---|---|---|
| *Don Quijote*, Project Gutenberg #2000, https://www.gutenberg.org/cache/epub/2000/pg2000.txt ; Cervantes murió en 1616: dominio público en México (LFDA art. 29) y en EE. UU. | Ficha https://www.gutenberg.org/ebooks/2000 ; licencia https://www.gutenberg.org/policy/license.html | Alta | El corte versionado (`tools/datos/quijote/`) quita cabecera, paratexto y pie de Gutenberg, como pide su licencia para derivar un texto de dominio público. Su `README.md` guarda URL, fecha, SHA-256 y las líneas de corte |

## Números calculados

| Afirmación | Dónde se calcula | Prueba |
|---|---|---|
| La frase «Con la iglesia hemos dado, Sancho» (II, 9): 27 letras, 26 transiciones, $N$ = 2, 9, 10, 5 y $\widehat P$ = 2/11, 9/11, 2/3, 1/3 | `frase_a_mano`, `frase_vc`, `matriz_estimada` | `test_la_frase_a_mano_es_la_del_plan` |
| Lo que necesitas de probabilidad: el sorteo de 26 posiciones (12/26, 11/26, 2/26, 2/11, 0.195), la regla del producto (14/25 · 9/14 · 7/9 = 7/25), la probabilidad total y las condicionales de memoria 2 del corpus (0.710, 0.624, 0.922); el ejercicio de «En un lugar de la Mancha» | `experimento_posiciones`, `regla_del_producto`, `condicionales_memoria_2`, `matriz_vce` | `test_p1_*` |
| El problema de Markov: aritmética de Markov 1913 (1 104 / 8 638 ≈ 0.128; 7 534 / 11 362 ≈ 0.663); corpus: 1 620 532 letras, Pr(V) = 0.464, $\widehat P$ ≈ (0.181, 0.819; 0.710, 0.290); trayectoria «conla» = 4/33; el ejemplo de tres estados; MUESTREAR-FILA a mano (CVCCVV); rachas reales, geométricas y simuladas (semillas 2026 y 2027) | `aritmetica_markov_1913`, `matriz_corpus`, `probabilidad_trayectoria`, `matriz_vce`, `trayectoria_a_mano`, `rachas_*` | `test_p2_*` |
| Ajustar contando: verosimilitudes (3.88×10⁻⁷, 1.49×10⁻⁸, 3.63×10⁻⁷), la traza de CONTAR, recuperar una matriz conocida (200 réplicas por T, semilla 2028), 784 entradas y 393 ceros, la «k» sin salidas, Laplace en la frase y en «q», la tabla de ceros por memoria | `verosimilitud`, `traza_contar`, `recuperar_p`, `entradas_memoria_1`, `fila_caracteres`, `fraccion_no_vista` | `test_p3_*` |
| Predecir: árbol de dos pasos (34/99), μ₁ a μ₃ de la frase, μₜ del corpus y 10 000 réplicas (semillas 2029 y 2030; mayor diferencia 0.010, unos 2.0 errores estándar), los dos ejercicios | `arbol_dos_pasos`, `mu_t`, `mu_t_corpus`, `diferencia_maxima_mu_t`, `ejercicio_p4_simulacion` | `test_p4_*` |
| Generar texto: generar a mano, las salidas con semilla 2032 a 2036, cuánto copian del corpus (6, 10, 11, 13 letras; 0 %, 9 %, 20 %, 42 % de 8-gramas) y lo que la prosa dice de ellas | `generar_a_mano`, `generar`, `subcadena_mas_larga_en_corpus`, `fraccion_ngramas_en_corpus` | `test_p5_*` |
| Cada cifra anterior aparece literal en su página y en su sección | `_cifras()` | `test_cada_cifra_de_las_paginas_sale_de_markov`, `test_cifras_de_la_pagina_en_su_bloque` |

## Clase 3 · Decidir

Consultado el 26 de octubre de 2026.

| Afirmación | Fuente | Nivel | Matiz |
|---|---|---|---|
| Richard Bellman, *Dynamic Programming*, Princeton University Press, 1957 | Ficha CiNii https://ci.nii.ac.jp/ncid/BA02237591 (Princeton, 1957, xxv + 340 p.) | Alta | — |
| Según su autobiografía, Bellman eligió el nombre «programación dinámica» en RAND para ocultar que hacía matemáticas: «dinámico» no admite sentido peyorativo | Bellman, *Eye of the Hurricane* (World Scientific, 1984), p. 159, citado en S. Dreyfus, *Operations Research* 50(1): 48–51 (2002), https://web.cs.miami.edu/home/odelia/teaching/csc317_fall19/syllabus/dy_birth.pdf | Media | Es el relato de Bellman, no un hecho comprobado: sitúa la elección en el otoño de 1950 y culpa al secretario Wilson, que lo fue del 28 de enero de 1953 al 8 de octubre de 1957 (https://history.defense.gov/Multimedia/Biographies/Article-View/Article/571268/charles-e-wilson/). Decir «según su autobiografía» |
| Ronald A. Howard, *Dynamic Programming and Markov Processes* (1960): cap. 3, iteración de valores; cap. 4, «The Policy-Iteration Method» | Portada y contenido, https://gwern.net/doc/statistics/decision/1960-howard-dynamicprogrammingmarkovprocesses.pdf | Alta | Editorial: «The Technology Press of the MIT and John Wiley & Sons», no «MIT Press». Viene de su tesis Sc.D. del MIT (1958). No atribuirle la iteración de valores |
| Manne (1960) formuló el problema de decisión markoviano como programa lineal (costo promedio); d'Epenoux (1963), con descuento | Manne, *Management Science* 6(3): 259–267, DOI 10.1287/mnsc.6.3.259; d'Epenoux, *Management Science* 10(1): 98–108, DOI 10.1287/mnsc.10.1.98 (resúmenes en IDEAS/RePEc) | Alta | No se encontró el supuesto original francés de d'Epenoux (1960): citar solo el de 1963 |
| Bertsekas y Tsitsiklis (1991), «An Analysis of Stochastic Shortest Path Problems», *Math. Oper. Res.* 16(3): 580–595: si existe una política propia y toda impropia tiene costo infinito desde algún estado, la ecuación de Bellman tiene solución única y VI y PI dan una política óptima propia | DOI 10.1287/moor.16.3.580; supuestos según Bertsekas y Yu, «Stochastic Shortest Path Problems Under Weak Conditions», https://www.mit.edu/~dimitrib/SSP_Weak_Conditions.pdf | Alta | Propia = estacionaria y llega al destino con probabilidad 1 desde todo estado. Admite costos de cualquier signo. Supuestos leídos en fuente secundaria de uno de los autores, no en el PDF original |
| Sutton y Barto, *Reinforcement Learning: An Introduction*, 2.ª ed., MIT Press, 2018: cap. 3 «Finite Markov Decision Processes», cap. 4 «Dynamic Programming»; ej. 4.3 = ecuaciones de evaluación para q; ej. 4.4 = la iteración de políticas que oscila entre políticas igual de buenas | http://incompleteideas.net/book/RLbook2020.pdf (ISBN 9780262039246) | Alta | Citar el ejercicio por su contenido, no solo por el número |
