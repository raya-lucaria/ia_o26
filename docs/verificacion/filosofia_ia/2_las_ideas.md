# Verificación — Las ideas del módulo

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
| 1858, fecha del *Fragmento sobre las máquinas* de Marx | Cuadernillo, portadilla de la lectura 1: «Fragmento sobre las máquinas · Karl Marx · 1858» | p. 3 | Sí — `pdftotext -f 3 -l 3` |
| 1972, fecha de *El Anti-Edipo* de Deleuze y Guattari | Cuadernillo, portadilla de la lectura 2: «El Anti-Edipo, pp. 239–240 · Gilles Deleuze y Félix Guattari · 1972» | p. 12 | Sí — `pdftotext -f 12 -l 12` |
| 1994, fecha de *Meltdown* de Land | Cuadernillo, portadilla de la lectura 3: «Meltdown · Nick Land · 1994» | p. 14 | Sí — `pdftotext -f 14 -l 14` |
| 1995, fecha de *La ideología californiana* de Barbrook y Cameron | Cuadernillo, portadilla de la lectura 6: «La ideología californiana · Richard Barbrook y Andy Cameron · 1995» | p. 43 | Sí — `pdftotext -f 43 -l 43` |
| 1996, fecha de *Swarmachines* del CCRU | Cuadernillo, portadilla de la lectura 5: «Swarmachines · CCRU · 1996» | p. 37 | Sí — `pdftotext -f 37 -l 37` |
| 2012, fecha de *Terminator vs Avatar* de Fisher | Cuadernillo, portadilla de la lectura 4: «Terminator vs Avatar · Mark Fisher · 2012» | p. 24 | Sí — `pdftotext -f 24 -l 24` |
| 2013, fecha del manifiesto aceleracionista de Srnicek y Williams | Ya verificada en `docs/verificacion/7_ia_y_sociedad.md`: Williams y Srnicek, «#Accelerate: Manifesto for an Accelerationist Politics», 14 de mayo de 2013, *Critical Legal Thinking* | — | Sí (reutilizada) |
| 2022, año de nacimiento de e/acc | Ya verificada en `docs/verificacion/7_ia_y_sociedad.md`: el movimiento nace pseudónimo en mayo de 2022 (@BasedBeffJezos y coautores); la identidad de Guillaume Verdon se revela en diciembre de 2023 | — | Sí (reutilizada) |
