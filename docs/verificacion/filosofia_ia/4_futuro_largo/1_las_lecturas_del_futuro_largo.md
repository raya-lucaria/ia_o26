# Verificación — Las seis lecturas, en claro

Fuente de cada cita y de cada afirmación datable de
`course/2_filosofia_ia/4_futuro_largo/1_las_lecturas_del_futuro_largo.md`, y de las dos
figuras que esa página usa (`v26-mapa-de-la-sesion-modulo-4.svg` y
`v27-de-moloch-al-futuro-largo.svg`).

Cada cita se extrajo con
`pdftotext -f N -l N course/2_filosofia_ia/_assets/cuadernillo_modulo_4_long_future.pdf -`
sobre la página N que indica la tabla, y se comprobó como subcadena literal del
texto de esa página tras normalizar los saltos de línea y los espacios múltiples
a un solo espacio. Ninguna palabra se cambió; lo único que se hizo fue unir las
líneas.

La columna «Página» es la del cuadernillo publicado —78 páginas—, no la de la
fuente original. Cuando la fuente tiene paginación propia y el temario la cita,
la fila lo dice: es el caso de Bostrom, que se publicó en *Utilitas* 15(3),
2003, pp. 308–314, y del artículo de Greaves y MacAskill, del que en el
cuadernillo van solo las secciones 1 a 4 y la 10.

Cinco de las seis lecturas están en derechos de sus autores y se reproducen como
material de clase, con la fuente al pie de cada una; la cuarta es un apunte
escrito para el curso. El detalle está en
`lecturas/filosofia_ia/clase_4/README.md`.

Una trampa que conviene conocer al reproducir estas comprobaciones: el PDF
justifica y parte palabras con guion suave (U+2010), así que una cita que cruce
un corte de línea no coincide como subcadena hasta normalizar ese carácter. Las
catorce citas de esta página se eligieron de modo que no dependan de eso, y se
volvieron a comprobar todas juntas después del último rearmado del cuadernillo.

| Afirmación o cita | Fuente | Página | Verificado |
|---|---|---|---|
| «In some competition optimizing for X, the opportunity arises to throw some other value under the bus for improved X. Those who take it prosper. Those who don’t take it die out.» | Cuadernillo, lectura 1 (Alexander, «Meditations on Moloch», 2014), parte I | p. 13 | Sí — `pdftotext -f 13 -l 13`, subcadena literal |
| «But coordination only works when you have 51% or more of the force on the side of the people doing the coordinating, and when you haven’t come up with some brilliant trick to make coordination impossible.» | Cuadernillo, lectura 1 (Alexander, «Meditations on Moloch», 2014), parte III | p. 26 | Sí — `pdftotext -f 26 -l 26`, subcadena literal |
| «The opposite of a trap is a garden. The only way to avoid having all human values gradually ground down by optimization-competition is to install a Gardener over the entire universe who optimizes for human values.» | Cuadernillo, lectura 1 (Alexander, «Meditations on Moloch», 2014), parte VII | p. 36 | Sí — `pdftotext -f 36 -l 36`, subcadena literal |
| «Instrumental rationality, on the other hand, is about steering reality—sending the future where you want it to go.» | Cuadernillo, lectura 2 (Yudkowsky, «What Do We Mean By “Rationality”?», 2009) | p. 41 | Sí — `pdftotext -f 41 -l 41`, subcadena literal |
| «Similarly, if you find yourself saying, “The (instrumentally) rational thing for me to do is X, but the right thing for me to do is Y,” then you are almost certainly using some other meaning for the word “rational” or the word “right.”» | Cuadernillo, lectura 2 (Yudkowsky, «What Do We Mean By “Rationality”?», 2009), cierre | p. 44 | Sí — `pdftotext -f 44 -l 44`, subcadena literal |
| «We envision the possibility of broadening human potential by overcoming aging, cognitive shortcomings, involuntary suffering, and our confinement to planet Earth.» | Cuadernillo, lectura 3 (Humanity+, «The Transhumanist Declaration»), proposición 1 | p. 46 | Sí — `pdftotext -f 46 -l 46`, subcadena literal |
| «We advocate the well-being of all sentience, including humans, non-human animals, and any future artificial intellects, modified life forms, or other intelligences to which technological and scientific advance may give rise.» | Cuadernillo, lectura 3 (Humanity+, «The Transhumanist Declaration»), proposición 7 | p. 46 | Sí — `pdftotext -f 46 -l 46`, subcadena literal |
| «People are still minors, half-beings, whereas the fulness of personal existence, personal perfection, is possible.» | Cuadernillo, lectura 4 (apunte del curso), fragmento de Fedorov, *What Was Man Created For?*, trad. Koutaissoff y Minto, Honeyglen, 1990, parte II, p. 76 | p. 48 | Sí — `pdftotext -f 48 -l 48`, subcadena literal |
| «Eventually we will be able to resurrect the dead by "copying them to the future".» | Cuadernillo, lectura 4 (apunte del curso), fragmento de Goertzel, *A Cosmist Manifesto*, Humanity+ Press, 2010, «Ten Cosmist Convictions», pp. 10–11 | p. 50 | Sí — `pdftotext -f 50 -l 50`, subcadena literal |
| «What matters for present purposes is not the exact numbers but the fact that they are huge.» | Cuadernillo, lectura 5 (Bostrom, «Astronomical Waste», 2003), sección I | p. 54 | Sí — `pdftotext -f 54 -l 54`, subcadena literal |
| «So long as the evaluation function is aggregative (does not count one person’s welfare for less just because there are many other persons in existence who also enjoy happy lives) and is not relativized to a particular point in time (no time-discounting), the conclusion will hold.» | Cuadernillo, lectura 5 (Bostrom, «Astronomical Waste», 2003), sección II | p. 55 | Sí — `pdftotext -f 55 -l 55`, subcadena literal |
| «For a rough upper bound on near-future expected benefits in the context of a society spending money, we consider the distribution of long-lasting insecticide-treated bednets in malarial regions, which saves a life on average for around $4000.» | Cuadernillo, lectura 6 (Greaves y MacAskill, «The Case for Strong Longtermism», 2021), sección 4 | p. 64 | Sí — `pdftotext -f 64 -l 64`, subcadena literal |
| «Even a 50% credence that the number of future beings will be zero would decrease the expected number by only a factor of two.» | Cuadernillo, lectura 6 (Greaves y MacAskill, 2021), sección 3 | p. 67 | Sí — `pdftotext -f 67 -l 67`, subcadena literal |
| «In our own view, the weakest points in the case for axiological strong longtermism are the assessment of numbers for the cost-effectiveness of particular attempts to benefit the far future, the appropriate treatment of cluelessness, and the question of whether an expected value approach to uncertainty is too “fanatical” in this context.» | Cuadernillo, lectura 6 (Greaves y MacAskill, 2021), sección 10 | p. 78 | Sí — `pdftotext -f 78 -l 78`, subcadena literal |
| Ficha 1: la entrada es del 30 de julio de 2014, en Slate Star Codex, y va completa, partes I a VIII | Fecha y sitio en la portadilla de la lectura; el recorte va del poema de Ginsberg al pie del blog, documentado en `lecturas/filosofia_ia/clase_4/README.md` | pp. 4–39 | Sí — portadilla en la p. 4; extensión comprobada contra el índice del PDF |
| Ficha 1: catorce mil trescientas palabras | 14 321 palabras en `fuentes/alexander_moloch_en.txt`, contadas con `wc -w`. El temario dice 14 955; la diferencia es el marcado de la página, no texto faltante | — | Sí — `wc -w` sobre la fuente versionada |
| Ficha 1: los cuatro frenos son tres malas razones y una buena | Cuadernillo, lectura 1: «I can think of three bad reasons – excess resources, physical limitations, and utility maximization – plus one good reason – coordination» | p. 16 | Sí — `pdftotext -f 16 -l 16`, subcadena literal |
| Ficha 1: Alexander dice que Land recorrió el 99.9 % del camino | Cuadernillo, lectura 1: «he has gone 99.9% of the path and then missed the very last turn, the one marked ORTHOGONALITY THESIS» | p. 32 | Sí — `pdftotext -f 32 -l 32`, subcadena literal |
| Ficha 2: el post es del 16 de marzo de 2009 en LessWrong, y va completo | `postedAt` de la API pública de LessWrong para el post `RcZCwxFiZzE6X7nsv`, consultada al descargar la fuente. **El temario lo fecha en 2012**, que es la fecha de la recopilación en libro | pp. 40–44 | Sí — respuesta de la API y portadilla del cuadernillo |
| Ficha 2: mil ochocientas palabras | 1 783 palabras en `fuentes/yudkowsky_rationality_en.txt`, `wc -w` | — | Sí — `wc -w` sobre la fuente versionada |
| Ficha 3: ocho proposiciones, cuatrocientas dieciocho palabras | 418 palabras en `fuentes/humanityplus_declaracion_transhumanista_en.txt`; las ocho proposiciones numeradas van completas | pp. 45–46 | Sí — `wc -w` y lectura completa de la fuente |
| Ficha 3: redactada en 1998 por veintidós personas y adoptada por la mesa directiva de Humanity+ en marzo de 2009 | Cuadernillo, lectura 3, párrafo de procedencia: «originally crafted in 1998 by an international group of authors» seguido de los veintidós nombres, y «It was adopted by the Humanity+ Board in March, 2009» | p. 45 | Sí — `pdftotext -f 45 -l 45`, subcadena literal; los nombres se contaron uno por uno y son 22 |
| Ficha 3: Bostrom, que firma la lectura 5, está entre los redactores de 1998 | Su nombre cierra la lista de veintidós en el mismo párrafo | p. 45 | Sí — `pdftotext -f 45 -l 45` |
| Ficha 4: el apunte se escribió para el curso en agosto de 2026 con ayuda de un modelo de lenguaje | Primera línea del propio apunte, y `lecturas/filosofia_ia/clase_4/README.md` | p. 47 | Sí — declarado en el texto publicado |
| Ficha 4: Fiódorov, bibliotecario en Moscú, muerto en 1903 | Apunte, sección 1, que cita la Internet Encyclopedia of Philosophy y señala que su año de nacimiento discrepa entre fuentes (1828 en la edición inglesa citada, 1829 en la IEP) | p. 48 | Sí — el apunte declara la discrepancia en vez de resolverla en silencio |
| Ficha 4: la revista *Extropy* desde 1988 y el ensayo de 1990 donde se acuña el sentido moderno de «transhumanismo» | Apunte, sección 2: *Extropy* #1, otoño de 1988; Max More, «Transhumanism: Towards a Futurist Philosophy», *Extropy* #6, verano de 1990, p. 6. El apunte anota que el año de fundación del Extropy Institute se da como 1988, 1990 o 1991 según la fuente | pp. 48–49 | Sí — fechas y paginación tomadas del escaneo de la revista citado en el apunte |
| Ficha 4: Kurzweil publica la curva en 2001 y le pone fecha en 2005 — 2045 | Apunte, sección 3: «The Law of Accelerating Returns», KurzweilAI.net, 7 de marzo de 2001, y *The Singularity Is Near*, Viking, 2005, cap. 3, sección «Setting a Date for the Singularity». El apunte cita por capítulo y sección, no por página, porque el número de página que suele circular no coincide con esa edición | pp. 49–50 | Sí — el sitio original está muerto y se consulta por el Internet Archive, como dice el apunte |
| Ficha 4: cosmismo contemporáneo de Goertzel y Prisco, 2009–2010 | Apunte, sección 4: las «Ten Cosmist Convictions» las redactó Giulio Prisco y las editó Ben Goertzel; versión de blog del 31 de enero de 2009, y libro *A Cosmist Manifesto*, Humanity+ Press, 2010 | pp. 50–51 | Sí — fechas tomadas de las dos fuentes que el apunte cita |
| Ficha 4: altruismo eficaz, Oxford, 2009–2011 | Apunte, sección 5: Giving What We Can se lanza en noviembre de 2009, 80,000 Hours en febrero de 2011, y el nombre «effective altruism» se elige por votación el 5 de diciembre de 2011 | pp. 51–52 | Sí — según el recuento del propio MacAskill que el apunte cita |
| Ficha 4: el acrónimo TESCREAL es de Gebru y Torres | Apunte, sección 6: primera exposición pública en Torres, *Truthdig*, 15 de junio de 2023; artículo en *First Monday* 29(4), 14 de abril de 2024 | p. 52 | Sí — las dos referencias van en el apunte |
| Ficha 5: publicado en *Utilitas* 15(3), 2003, pp. 308–314 | La propia página del autor lo declara: «Originally published in Utilitas Vol. 15, No. 3 (2003): pp. 308-314». Es una afirmación sobre la fuente, no sobre el cuadernillo: la lectura ocupa las pp. 53–59 del PDF y reproduce la versión del autor, sin esa paginación | — | Sí — subcadena literal de `nickbostrom.com/astronomical/waste`, tal como se descargó |
| Ficha 5: dos mil seiscientas palabras, cuatro secciones | 2 653 palabras en `fuentes/bostrom_astronomical_waste_en.txt`; las secciones I a IV van completas | pp. 53–59 | Sí — `wc -w` sobre la fuente versionada |
| Ficha 5: la cuenta de 10³⁸ son tres multiplicaciones — 10¹³ estrellas, 10⁴² operaciones por segundo cada una, entre ~10¹⁷ por vida simulada | Cuadernillo, lectura 5, sección I: «the Virgo Supercluster contains 10 13 stars», «is 10 42 operations per second», «roughly 10 17 operations per second or less», y «the potential for approximately 10 38 human lives is lost every century» | p. 54 | Sí — `pdftotext -f 54 -l 54`, las cuatro subcadenas literales |
| Ficha 5: la variante conservadora da 10²³ humanos biológicos y más de diez billones de vidas por segundo | Cuadernillo, lectura 5: «the Virgo Supercluster could contain 10 23 biological humans» y «the potential for over ten trillion potential human beings is lost for every second» | pp. 54–55 | Sí — `pdftotext -f 54 -l 55`, subcadenas literales (la segunda cae ya en la p. 55). *Trillion* se traduce por *billón* (10¹²), que es su equivalente en español |
| Ficha 6: GPI Working Paper 5-2021, junio de 2021, y en el cuadernillo van solo las secciones 1 a 4 y la 10 | Portada del documento de trabajo del Global Priorities Institute; el recorte está documentado en `lecturas/filosofia_ia/clase_4/README.md` y declarado en la portadilla de la lectura | pp. 60–78 | Sí — portadilla en la p. 60 y contenido del PDF |
| Ficha 6: la estimación principal es 10²⁴, la baja 10¹⁸ y la restringida 10¹⁴ | Cuadernillo, lectura 6, sección 3: «Expected number of future beings Main estimate 1024 Low estimate 1018 Restricted estimate 1014» | p. 69 | Sí — `pdftotext -f 69 -l 69`, subcadena literal |
| Ficha 6: un 0.01 % de crédito en la Vía Láctea aporta 10³² | Cuadernillo, lectura 6, sección 3: «Even a 0.01% credence that biological humanity settles the Milky Way at carrying capacity, for example, contributes at least 1032 to the expected number of future beings» | p. 69 | Sí — `pdftotext -f 69 -l 69`, subcadena literal |
| Ficha 6: con la estimación restringida, dos de sus tres ejemplos dejan de funcionar | Cuadernillo, lectura 6, sección 4: cada 100 dólares aumentaría el número de seres futuros «by 200 million (respectively, 200, 0.02) on our main (resp., low, restricted) estimate», y los beneficios superan a los de corto plazo «on our main and low estimates» — es decir, no en la restringida | p. 73 | Sí — `pdftotext -f 73 -l 73`, subcadenas literales |
| Figura «Las dos horas de la sesión…» (`v26`) | Diagrama propio. Los minutos de la hora 1 suman 60 con los cinco de entrada; las seis lecturas y sus años salen de las portadillas del cuadernillo | — | Sí — **material del curso**, acreditado en `_assets/CREDITOS.md` |
| Figura «De Moloch al futuro largo» (`v27`) | Diagrama propio. **Lectura del curso**: los seis eslabones son una reconstrucción del argumento del módulo, no una cita de ninguna lectura. Cada eslabón lleva en la figura el nombre de la lectura de la que sale | — | Sí — **material del curso**, acreditado en `_assets/CREDITOS.md` |
Esta página no tiene fecha de corte propia: no afirma nada sobre el estado del
mundo en 2026, ni adscripciones laborales en presente de ninguno de los autores
vivos. Lo único que caducaría es la cifra de páginas del cuadernillo, y esa la
comprueba `tools/test_lecturas.py` contra el PDF publicado.
