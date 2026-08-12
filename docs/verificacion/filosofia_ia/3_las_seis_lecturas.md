# Verificación — Las seis lecturas, en claro

Fuente de cada cita y de cada fecha de `course/2_filosofia_ia/2_repaso_y_discusion.md`.
Las citas se copiaron del PDF del cuadernillo con `pdftotext`; la columna «Página»
es la del cuadernillo, no la de la edición original.

Cada cita se extrajo con `pdftotext -f N -l N lecturas/filosofia_ia/clase_1/lecturas/filosofia_ia_clase_1_cuadernillo.pdf -`
sobre la página N que indica la tabla, y se comprobó como subcadena literal del
texto de esa página tras normalizar los saltos de línea a espacios. Ninguna
palabra se cambió; lo único que se hizo fue unir las líneas.

Nota sobre la numeración: en las páginas que el cuadernillo compone él mismo, el
folio impreso coincide con el número de página del PDF (p. ej. la página 11
lleva impreso «11»). Las páginas reproducidas tal cual de los PDF originales
—Deleuze y Guattari, y Fisher— no llevan folio del cuadernillo (la de Deleuze y
Guattari conserva el «247» de la edición de Paidós). En esos dos casos la columna
«Página» es el número de página del PDF del cuadernillo, que es por el que
navega quien lo lee.

| Afirmación o cita | Fuente | Página | Verificado |
|---|---|---|---|
| «The development of fixed capital indicates to what degree general social knowledge has become a direct force of production, and to what degree, hence, the conditions of the process of social life itself have come under the control of the general intellect and been transformed in accordance with it.» | Cuadernillo, lectura 1 (Marx, *Fragmento sobre las máquinas*, Grundrisse, 1858; traducción de Marxists Internet Archive, dominio público) | p. 11 | Sí — `pdftotext -f 11 -l 11`; el folio impreso de la página dice «11» |
| «No retirarse del proceso, sino ir más lejos, «acelerar el proceso», como decía Nietzsche: en verdad, en esta materia todavía no hemos visto nada.» | Cuadernillo, lectura 2 (Deleuze y Guattari, *El Anti-Edipo*, pp. 239–240) | p. 13 | Sí — `pdftotext -f 13 -l 13`; página reproducida del PDF original, sin folio del cuadernillo (conserva el «247» de la edición de Paidós). Las comillas angulares interiores son las del original y se reproducen sin cambio |
| «Logistically accelerating techno-economic interactivity crumbles social order in auto-sophisticating machine runaway.» | Cuadernillo, lectura 3 (Land, *Meltdown*, 1994) | p. 14 | Sí — `pdftotext -f 14 -l 14`; el folio impreso de la página dice «14» |
| «markets may or may not be the self-organising meshworks described by Fernand Braudel and Manuel Delanda, but what is certain is that capitalism, dominated by quasi-monopolies such as Microsoft and Wal-Mart, is an anti-market.» | Cuadernillo, lectura 4 (Fisher, *Terminator vs Avatar*, 2012, según se reproduce en *#Accelerate: The Accelerationist Reader*). La cita empieza a media oración: en el original va precedida de «Similarly,» | p. 35 | Sí — `pdftotext -f 35 -l 35`; página reproducida del PDF original, sin folio del cuadernillo |
| «Only multiplicities, decolonized ants, swarms without strategies, insectoid freeways burrowed through the screens of spectacular time.» | Cuadernillo, lectura 5 (CCRU, *Swarmachines*, 1996; ccru.net) | p. 38 | Sí — `pdftotext -f 38 -l 38`; el folio impreso de la página dice «38» |
| «the Californian Ideology promiscuously combines the free-wheeling spirit of the hippies and the entrepreneurial zeal of the yuppies.» | Cuadernillo, lectura 6 (Barbrook y Cameron, *The Californian Ideology*, 1995). La cita empieza a media oración: en el original va precedida de «Promoted in magazines, books, TV programmes, websites, newsgroups and Net conferences,» | p. 44 | Sí — `pdftotext -f 44 -l 44`; el folio impreso de la página dice «44» |
