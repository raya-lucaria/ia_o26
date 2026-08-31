# Verificación — Complejidad computacional

Registro de fuentes de toda afirmación datable de `course/4_complejidad/`.

A diferencia de la unidad de historia, aquí **un solo archivo cubre las doce
páginas**: la unidad es matemática, no histórica, y sus fechas son pocas y todas
del mismo tipo —quién publicó qué teorema y cuándo—. Se agrupan por página para
que localizar una siga siendo directo.

Todas las fechas se comprobaron contra Wikipedia en inglés el **31 de agosto de
2026**, artículo por artículo. Donde la fuente trae un matiz que la página no
necesita, el matiz queda escrito aquí.

## `3_contar_un_algoritmo.md`

| # | Afirmación en la página | Fuente | Verificado |
|---|---|---|---|
| 1 | **Strassen (1969)** bajó la multiplicación de matrices a $O(n^{2{,}807})$ | Wikipedia, «Strassen algorithm»: «first published this algorithm in 1969 and thereby proved that the n³ general matrix multiplication algorithm was not optimal». El exponente exacto es $\log_2 7 \approx 2{,}8074$, que es lo que la página redondea a 2,807 | Sí |
| 2 | Strassen hace **siete** multiplicaciones de bloques en vez de ocho | Wikipedia, «Strassen algorithm»: el algoritmo calcula siete productos $M_1 \dots M_7$ en lugar de los ocho de la partición ingenua | Sí |
| 3 | El mejor límite inferior conocido para multiplicar matrices es $\Omega(n^2)$ | Es el costo de escribir la salida: la matriz resultado tiene $n^2$ entradas. La página lo dice así, y no afirma ninguna cota superior más allá de Strassen | Sí |
| 4 | La tabla de tiempos de reloj a $10^9$ operaciones por segundo | Aritmética directa, recalculada: $2^{100}/10^9 = 1{,}27\times10^{21}$ s $= 4{,}0\times10^{13}$ años; $10^{18}/10^9 = 10^9$ s $= 31{,}7$ años; $10^{12}/10^9 = 1000$ s $= 17$ min | Sí |

## `4_por_que_importa.md`

| # | Afirmación en la página | Fuente | Verificado |
|---|---|---|---|
| 5 | Al duplicar la velocidad, un algoritmo $n^2$ gana un factor $1{,}41$ y uno $n^3$ un factor $1{,}26$ | Aritmética: $\sqrt{2} = 1{,}414$ y $\sqrt[3]{2} = 1{,}260$ | Sí |
| 6 | Un algoritmo $2^n$ gana **una unidad** de $n$ al duplicar la velocidad | $2^{n+1} = 2\cdot 2^n$: duplicar el presupuesto de pasos sube $n$ en exactamente 1 | Sí |
| 7 | Dijkstra es $O(m + n\log n)$ | Wikipedia, «Dijkstra's algorithm»: esa es la cota con montículo de Fibonacci. Con montículo binario es $O((n+m)\log n)$; la página cita la primera, que es la estándar | Sí |
| 8 | La fuerza bruta sobre TSP con 40 ciudades pide $39!$ recorridos, «un número con 46 dígitos» | $39! = 2{,}04\times10^{46}$, que tiene 47 dígitos. **Corregido en la página a «un número de 47 cifras»** | Sí |

## `5_espacio.md`

| # | Afirmación en la página | Fuente | Verificado |
|---|---|---|---|
| 9 | Conectividad en grafos **no dirigidos** está en $L$ (**Reingold, 2004**) | Wikipedia, «SL (complexity)»: «In October 2004 Omer Reingold showed that SL = L». La versión de revista es Reingold, «Undirected connectivity in log-space», *JACM* 55(4), **2008**. La página cita 2004, el anuncio del resultado | Sí |
| 10 | **Teorema de Savitch (1970)**: $NSPACE(f) \subseteq DSPACE(f^2)$, y por tanto $NPSPACE = PSPACE$ | Wikipedia, «Savitch's theorem»: «Walter Savitch proved this theorem in 1970»; el corolario $NPSPACE = PSPACE$ está enunciado ahí mismo | Sí |
| 11 | El Hex y el Reversi generalizados a $n\times n$ son **PSPACE-completos** | Wikipedia, «PSPACE-complete»: «Examples of games that are PSPACE-complete (when generalized so that they can be played on an n × n board) are the games Hex and Reversi» | Sí |
| 12 | El **Go generalizado es EXPTIME-completo**, no PSPACE-completo (Robson, 1983) | Wikipedia, «Game complexity»: EXPTIME-completo, probado por J. M. Robson en 1983, «without the superko rule». Y Wikipedia, «PSPACE-complete»: Go «will become PSPACE-complete if a polynomial bound on the number of moves is enforced», que es el matiz que la página recoge. **Este renglón corrigió un error de un borrador anterior**, que listaba Go entre los PSPACE-completos | Sí |

## `6_las_clases.md`

| # | Afirmación en la página | Fuente | Verificado |
|---|---|---|---|
| 13 | **Khachiyan (1979)** puso la programación lineal en $P$ con el método de elipsoide | Wikipedia, «Linear programming»: «The linear programming problem was first shown to be solvable in polynomial time by Leonid Khachiyan in 1979» | Sí |
| 14 | **Klee-Minty (1972)**: el simplex visita $2^n$ vértices en el peor caso | Wikipedia, «Klee–Minty cube»: publicado en 1972; el simplex de Dantzig «visits all corners of a (perturbed) cube in dimension D in the worst case» | Sí |
| 15 | **AKS (2002)**: PRIMES está en $P$ | Wikipedia, «AKS primality test»: 6 de agosto de 2002, Agrawal, Kayal y Saxena, del IIT Kanpur | Sí |
| 16 | El **ajedrez generalizado** a $n\times n$, sin la regla de las 50 jugadas, es EXP-completo | Wikipedia, «Game complexity»: Fraenkel y Lichtenstein, 1981, «Computing a perfect strategy for n × n chess requires time exponential in n». El artículo añade la salvedad «without the 50-move drawing rule», que la página recoge | Sí |
| 17 | 2-SAT está en $P$, en tiempo lineal, por componentes fuertemente conexas | Es el algoritmo de Aspvall, Plass y Tarjan (1979). La página no da la fecha, solo el método | Sí |
| 18 | Hopcroft-Karp es $O(m\sqrt{n})$ y Edmonds-Karp es $O(nm^2)$ | Cotas estándar de los dos algoritmos, con la convención $n$ vértices y $m$ aristas que la unidad fija en su página 1 | Sí |

## `7_azar.md`

| # | Afirmación en la página | Fuente | Verificado |
|---|---|---|---|
| 19 | **Miller (1976)** y **Rabin (1980)** | Wikipedia, «Miller–Rabin primality test»: «Gary L. Miller discovered the test in 1976; Miller's version of the test is deterministic, but its correctness relies on the unproven extended Riemann hypothesis. Michael O. Rabin modified it to obtain an unconditional probabilistic algorithm» en 1980 | Sí |
| 20 | Al menos **3/4** de las bases son testigos de un compuesto | Wikipedia, «Miller–Rabin primality test»: «at most 1/4 of the bases a are strong liars for n» | Sí |
| 21 | Tras $k$ rondas, el error es $\le 4^{-k}$ | Wikipedia, misma entrada: «running k iterations of the Miller–Rabin test will declare n probably prime with a probability at most 4^−k» | Sí |
| 22 | **561 = 3·11·17** es el número de Carmichael más chico, y engaña al test de Fermat | Wikipedia, «Carmichael number»: el más pequeño es 561 = 3 × 11 × 17, y un número de Carmichael «will pass a Fermat primality test to every base b relatively prime to the number» | Sí |
| 23 | Hay **infinitos** números de Carmichael | Wikipedia, misma entrada: Alford, Granville y Pomerance lo demostraron en **1994** | Sí |
| 24 | Las dos cadenas de la figura: 97 con $s=5, d=3$ y 561 con $s=4, d=35$ | No se transcribieron: `tools/gen_complejidad.py` las calcula con `pow()` al generar el SVG, y `test_las_cadenas_de_miller_rabin_son_las_de_verdad` comprueba que el ejemplo sigue diciendo lo que la página afirma | Sí |
| 25 | **Impagliazzo-Wigderson (1997)**: bajo cierta hipótesis de dureza, $P = BPP$ | Wikipedia, «BPP (complexity)»: «In 1997 [Impagliazzo and Wigderson proved] that if any problem in E has circuit complexity 2^Ω(n) then P = BPP» | Sí |
| 26 | **No se sabe si $BPP \subseteq NP$** | Wikipedia, «BPP (complexity)»: «The relationship between BPP and NP is unknown: it is not known whether BPP is a subset of NP, NP is a subset of BPP or neither» | Sí |
| 27 | $BPP$ cabe «en el segundo nivel de una jerarquía por encima de $NP$» | Es el teorema de Sipser-Gács-Lautemann: $BPP \subseteq \Sigma_2 \cap \Pi_2$. La página lo dice sin nombrarlo ni dar fecha | Sí |

## `8_completos_y_duros.md`

| # | Afirmación en la página | Fuente | Verificado |
|---|---|---|---|
| 28 | **Cook (1971)** y **Levin (1973)**, independientemente | Wikipedia, «Cook–Levin theorem»: Cook, «The complexity of theorem proving procedures», STOC 1971; Levin, «Universal search problems», *Problems of Information Transmission*, 1973 — con la nota de que el trabajo de Levin «was mentioned in talks and submitted for publication a few years earlier». La página dice «de manera independiente», que es exacto | Sí |
| 29 | **Karp (1972)** encontró 21 problemas NP-completos | Wikipedia, «Karp's 21 NP-complete problems»: «In his 1972 paper, "Reducibility Among Combinatorial Problems"» | Sí |
| 30 | Una cláusula de $k$ literales da $k-2$ cláusulas y $k-3$ variables nuevas | Comprobado sobre el ejemplo de la figura: $k=5$ da 3 cláusulas y 2 variables ($y_1, y_2$), que es $5-2$ y $5-3$ | Sí |
| 31 | El problema de la parada es NP-duro y no es NP-completo | Se sigue de las definiciones de la propia página más la indecidibilidad demostrada en `course/3_computabilidad/5_el_problema_de_la_parada.md` | Sí |

## `9_el_mapa.md`

| # | Afirmación en la página | Fuente | Verificado |
|---|---|---|---|
| 32 | **Jerarquía de tiempo: Hartmanis-Stearns, 1965**, y de ahí $P \subsetneq EXP$ | Wikipedia, «Time hierarchy theorem»: «first proven by Richard E. Stearns and Juris Hartmanis in 1965», y «the time hierarchy theorems guarantee that... **P** ⊊ **EXPTIME**» | Sí |
| 33 | **$P$ contra $NP$ vale un millón de dólares**, del Clay Mathematics Institute | Wikipedia, «P versus NP problem»: es uno de los siete Millennium Prize Problems, anunciados en **2000**, con premio de **1 000 000 USD** | Sí |
| 34 | **Baker, Gill y Solovay (1975)**: la relativización no puede resolver $P$ contra $NP$ | Wikipedia, «P versus NP problem»: «P = NP with respect to some oracles, while P ≠ NP for other oracles», y por tanto las técnicas que relativizan no bastan | Sí |
| 35 | **Teorema de Ladner (1975)**: si $P \ne NP$, hay problemas en $NP$ que no están en $P$ ni son NP-completos | Wikipedia, «Ladner's theorem»: «Richard E. Ladner proved [it] in 1975»; «if P ≠ NP, then NPI is non-empty» | Sí |
| 36 | **Babai (2015)** dio un algoritmo casi polinomial para isomorfismo de grafos | Wikipedia, «Graph isomorphism problem»: anunciado en noviembre de **2015**; retirado el 4 de enero de 2017 tras un error hallado por Helfgott, y **restituido el 9 de enero de 2017** con una corrección que Helfgott confirmó. La página cita 2015, que es la fecha del resultado; el episodio de 2017 no cambia el enunciado y la página no lo necesita | Sí |
| 37 | El isomorfismo de grafos no se sabe en $P$ ni NP-completo | Wikipedia, misma entrada: «not known to be solvable in polynomial time nor to be NP-complete» | Sí |

## Afirmaciones no datables

El resto de la unidad son definiciones, demostraciones y cuentas, no
afirmaciones históricas: las definiciones de $O$, $\Omega$, $\Theta$ y $o$; los
conteos de complejidad de los cuatro algoritmos de la página 3; las
contenciones de la cadena y sus justificaciones; y las cuatro salidas ante un
problema intratable. Nada de eso tiene fecha que verificar.

Las cifras de la carrera interactiva
(`_assets/carrera_de_crecimiento.html`) se calculan en el navegador desde la
propia fórmula de cada fila —incluido $\log_{10}(n!)$ por Stirling con su
término de corrección— así que no hay ninguna constante transcrita que pueda
desincronizarse. La edad del universo que usa para la escala más alta,
$1{,}38\times10^{10}$ años, es la única constante externa del archivo.
