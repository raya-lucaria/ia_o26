# Ejercicios en la página

**DEBE** = verificable, no negociable · **DEBERÍA** = cotejo del revisor · **CRITERIO** = guía con ejemplo.
`J/` = `course/7_juegos/2_mirar_todo_y_podar/`, `P/` = `course/6_optimizacion/5_practica_de_modelado/`.
Directivas `exercise`/`hint`/`answer` y su render: ver CLAUDE.md § Authoring contract. Tareas (`*_tarea.md`, `_official/`): fuera de alcance.

## Cuatro niveles

| Nivel | Para qué | Forma | Ejemplo |
|---|---|---|---|
| 1 · **Piensa** | Ritmo, no recuperación | Pregunta en negrita; la responde el párrafo siguiente | `P/1_salones_practica.md:36-38` |
| 2 · Micro plegado | Recuperación real de lo recién visto | 0–1 pista; respuesta ≤120 palabras | `J/1_minimax.md:152-176` |
| 3 · Traza con huecos | Correr el algoritmo sin ver la solución | Misma tabla que la resuelta, con «?» | `J/2_minimax_como_algoritmo.md:319-420` |
| 4 · Ejercicio final | Transferir la idea de la página | Preámbulo, 2 pistas, respuesta | `P/4_regresion_practica.md:570-663` |

- **DEBE** haber ≥1 micro por `##` explicativo; lo antecede «**Estamos aquí:**» si hay que ubicar el estado (`J/1_minimax.md:152`). La respuesta no está en el párrafo anterior.
- **DEBE** la traza con huecos poner «?» solo en celdas que se deducen; su respuesta reimprime la tabla con **en negrita lo que faltaba** y lo dice: «En negrita, lo que era «?»» (`J/2_minimax_como_algoritmo.md:378`, `J/4_alfa_beta.md:525`).
- **DEBE** el orden de directivas ser **exercise → hint → hint → answer**, contiguas y en la misma página (no como `course/6_optimizacion/4_entero/1_la_bitacora_del_taller.md:174`, que deja las respuestas en otra).

## Ejercicio final: preámbulo y enunciado

- **DEBE** el preámbulo ser este texto, literal (`P/3_clasificacion_practica.md:878`, `P/4_regresion_practica.md:570`):

  ```
  **Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
  pedir ayuda a ChatGPT.**
  ```
  Las otras tres redacciones (`P/1_salones_practica.md:370`, `P/2_panaderia_practica.md:404`, `P/3_clasificacion_practica.md:652`) no se copian.
- **DEBE** el enunciado traer: relato con datos precisos y **simplificaciones explícitas** («No se puede trasladar el proyector», `P/1_salones_practica.md:383`); qué queda fuera («no ha establecido preferencias», `:387`); **una idea nueva nombrada** respecto del ejemplo resuelto (la hora ya no está fijada, `:378-379`; escalar la instancia está permitido); entregables **numerados, ≤6** (`P/4_regresion_practica.md:582-588`).
- **CRITERIO** si hay varias respuestas válidas, dilo en el enunciado: «La respuesta desarrolla una opción» (`P/3_clasificacion_practica.md:905-906`).

## Arco de entregables por tipo de página

| Tipo | Arco | Ejemplo |
|---|---|---|
| Modelado | datos/decisiones → modelo → variante → método y costo | `P/2_panaderia_practica.md:428-435` |
| Algoritmo | traza → variante de una regla → costo | `J/4_alfa_beta.md:492-515` (traza, filas que faltan, nodos generados) |
| Concepto | clasificar o contraejemplo → justificar | `course/7_juegos/1_leer_y_escribir/4_diagnosticar_el_juego.md:125` |
| Lectura | tesis → evidencia → objeción | Sin ejemplo en página todavía |

## Pistas

- **DEBE** haber exactamente 2, tituladas «Pista 1 · …» y «Pista 2 · …», **formuladas como preguntas**. La 1 **organiza** (qué es dato, qué se decide, qué índice falta); la 2 **revisa el borrador** («Comprueba tu propuesta con dos preguntas»). Modelo: `P/2_panaderia_practica.md:438-449`.
- **DEBE** pasar la **prueba de fuga**: ninguna pista contiene el título de la respuesta ni su sustantivo clave. Contraejemplo: en calibración, la pista 1 nombra el histograma y la 2 dice «reunir mensajes con scores similares» (`P/3_clasificacion_practica.md:910`, `:916`): es el *histogram binning* que la respuesta titula «Usar frecuencias dentro de intervalos» (`:922`).
- **DEBERÍA** evitar la pista que afirma el paso en vez de preguntarlo (`J/2_minimax_como_algoritmo.md:530-533`).

## Respuesta

- **DEBE** titularse «Respuesta · …» (no como `P/2_panaderia_practica.md:451`), con **pasos en negrita numerados que espejan los entregables** (`P/1_salones_practica.md:412`, `:447`, `:484`, `:509`).
- **DEBE** llevar, según el tipo: tabla `Símbolo | Qué representa`; modelo `aligned` con dominios de cada variable; comprobación de la instancia si el enunciado da datos (`P/1_salones_practica.md:484-507`); el razonamiento, no solo el resultado.
- **DEBE** medir ≤2× el enunciado o ≤400 palabras de prosa, lo que sea mayor. Regresión cumple (`P/4_regresion_practica.md:604-663`); salones lo triplica (`P/1_salones_practica.md:411-527`).
- **CRITERIO** «Límite» y autoverificación son **opcionales**: vienen de las tareas. Solo si el modelo tiene un límite real que decir.

## Desvanecimiento

**DEBE** seguir el orden **completo → con huecos → variante o desde cero** sobre el mismo objeto: traza de T resuelta (`J/2_minimax_como_algoritmo.md:232-316`), la misma con «?» y los hijos al revés (`:319`), e1 «sin la página anterior abierta» (`:499-514`).

## Ids y cierre

- **DEBE** `<prefijo>-ej-<slug>`, `<prefijo>-pista-<slug>-1` / `-2`, `<prefijo>-resp-<slug>`. No copiar `-p1`/`-resp` como sufijo (`P/1_salones_practica.md:397`) ni `-pista-<slug>-a` (`J/2_minimax_como_algoritmo.md:525`).
- **DEBERÍA** cerrar la página con «**Punto de control:** deberías poder…», luego `## Para profundizar` si hay, «Lo que hay que llevarse» y «Continúa con» (`J/2_minimax_como_algoritmo.md:578`, `:583`, `:674`).

## Anti-fórmula

- **DEBERÍA** variar el verbo de los títulos: hoy 31 de los 47 ejercicios de juegos se titulan «Decide…» (`grep -rho 'title="Decide' course/7_juegos`). Calcula, Señala, Corrige, Compara, Encuentra…
- **DEBERÍA** no repetir pasos en negrita idénticos de relleno entre respuestas, ni añadir un «Límite» que no diga nada propio del ejercicio.

## Excepciones

- Micro sin pista cuando la pregunta es un cálculo de un paso (`course/7_juegos/4_sin_turnos/1_jugar_a_la_vez.md:119-135`).
- `##` sin micro: motivación, resumen, «Lo que hay que llevarse», y secciones cubiertas por una traza con huecos del mismo tramo.
- Página de concepto o lectura sin traza con huecos: el nivel 3 no aplica.
- La página de cierre de un bloque de práctica puede no tener ejercicio final (`P/0_index.md:77`: el juego no lleva).
