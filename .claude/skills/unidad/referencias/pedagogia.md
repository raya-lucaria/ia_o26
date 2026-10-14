# Pedagogía: ejemplos, avance y repetición

**DEBE** = verificable, no negociable · **DEBERÍA** = cotejo del revisor · **CRITERIO** = guía con ejemplo.
Rutas desde la raíz; `J/` = `course/7_juegos/`, `P/` = `course/6_optimizacion/5_practica_de_modelado/`,
`spec` = `docs/superpowers/specs/2026-10-01-juegos-adversarial-design.md` (gitignorado). Ejercicios: ver `ejercicios.md`.

## Ejemplos en tres capas

| Capa | Qué es | Tamaño | Ejemplo |
|---|---|---|---|
| Hilo de unidad | Un objeto que recorre todas las clases | Libre | Hexapawn, `J/0_index.md:35-40` |
| Instancia a mano | Sub-caso del hilo que se calcula en papel | A mano | e1, 11 nodos, `J/2_mirar_todo_y_podar/2_minimax_como_algoritmo.md:502` |
| Juguete para traza | Sin dominio; hojas elegidas para que cada `if` informe | A mano | Árbol T, `J/2_mirar_todo_y_podar/2_minimax_como_algoritmo.md:200-210` |

- **DEBE** haber **un hilo por unidad**, presentado en el índice de unidad (`J/0_index.md:35`).
- **DEBE** volver al hilo después del juguete: T y luego «Ahora en hexapawn: n1» (`J/2_mirar_todo_y_podar/2_minimax_como_algoritmo.md:429`).
- **DEBE** comprobarse con la fuente Python toda afirmación sobre el juguete (ver `codigo.md`). Contraejemplo: `J/2_mirar_todo_y_podar/2_minimax_como_algoritmo.md:210` dice «todas son distintas» y la hoja 2 está bajo C1 y bajo D.
- **CRITERIO** el juguete crece por etapas: T1 de 7 nodos → T de 14 (`J/2_mirar_todo_y_podar/4_alfa_beta.md:252`, `:315`).

## Cuándo entra un ejemplo nuevo

**DEBE** entrar solo por una de tres razones, y explicarse en 3–4 líneas (`spec:180-184`). Si no aplica ninguna, se usa el hilo.

| Razón | Ejemplo |
|---|---|
| Probar transferencia | Tres juegos ajenos para diagnosticar, `J/1_leer_y_escribir/4_diagnosticar_el_juego.md:125` |
| El modelo se rompe | El árbol ya no cabe: peones 4×4 y ajedrez en la clase 3 (`spec:145-148`) |
| El hilo no muestra la idea | Hexapawn no tiene azar: un dado sobre T (`J/2_mirar_todo_y_podar/3_cuando_decide_un_dado.md:434`) |

## Variantes y tamaños

- **DEBE** una variante cambiar **una idea nombrada** y decirlo; lo demás igual, para que la respuesta anterior sirva de referencia: «Lo demás no cambia» (`J/2_mirar_todo_y_podar/3_cuando_decide_un_dado.md:434-436`), «los hijos al revés» (`J/2_mirar_todo_y_podar/2_minimax_como_algoritmo.md:319`). Escalar la instancia está permitido.
- **DEBE** «a mano» = ≤14 nodos, ≤6 datos, ≤4 variables trazadas. «Modelo general» = libre, con la frase puente «La misma definición sirve con más…» (`P/1_salones_practica.md:60`).
- **DEBE** ir los datos grandes solo en gráfica o notebook: seis entregas a mano (`P/4_regresion_practica.md:77`), 120 puntos solo en figura (`P/4_regresion_practica.md:428`).
- **CRITERIO** práctica de modelado (tipo 6.5): **dominio distinto por página**, cada uno con una dificultad nueva (`P/0_index.md:22-24`); el ejercicio final agrega una dimensión al mismo dominio (la hora en salones, `P/1_salones_practica.md:378-379`).

## Avance poco a poco

- **DEBE** cada clase cambiar una cosa, en tabla del índice de unidad (`J/0_index.md:46-53`); cada página, una dificultad.
- **DEBE** cerrar el índice de clase con «Qué no cubre esta clase» (`J/2_mirar_todo_y_podar/0_index.md:158`).
- **DEBE** abrir con «Lo que traes» la clase o página que depende de otra: tabla ≤12 filas con enlace a cada definición (`J/2_mirar_todo_y_podar/0_index.md:32-50`, 10 filas) o cita corta en página (`J/2_mirar_todo_y_podar/4_alfa_beta.md:25`).
- **DEBE** presentar el pseudocódigo que cambia como **delta de líneas**: «La línea 9 es la nueva… todo lo que sigue se corre un lugar» (`J/3_cuando_no_cabe/2_minimax_con_corte.md:168-175`).
- **DEBE** partir las trazas en tramos que cortan en un **evento** y lo nombran: «D corta», «El corte beta en C2» (`J/2_mirar_todo_y_podar/4_alfa_beta.md:282`, `:367`). Topes de filas: ver `lectura.md`; figuras de tramo: ver `figuras.md`.
- **DEBERÍA** explicarse cada símbolo antes de usarse; bloques de 5–8 minutos; ≈1 **Piensa** por `##`.
- **CRITERIO** orden **motivación → ejemplo → definición → general**: relato (`P/1_salones_practica.md:20`), Piensa (`:52`), definición de $x_{cs}$ (`:54`), generalización (`:60`). En algoritmos, el ejemplo a mano va antes del pseudocódigo (`spec:247-257`).

## Hilo narrativo: cada sección nace de la anterior

La página es **un argumento**, no una lista de hechos. Se vio en `course/7_juegos/3_cuando_no_cabe/6_de_donde_sale_el_bono.md`
(2026-10-12): cada sección era correcta por separado y el profesor dijo «se perdió totalmente la narrativa, está fragmentada».

- **DEBE** la página abrir con **una pregunta guía** y cada `##` responder una parte de ella. El primer párrafo de cada
  `##` retoma lo que dejó abierto la anterior («La regla se atora porque no duda; ¿cuánto debería dudar?»), y el último
  deja la pregunta que contesta la siguiente. Si una sección no se puede enlazar así, sobra o está fuera de orden.
- **DEBE** todo símbolo o fórmula nueva traer tres cosas: **de dónde sale** (la cuenta, o un enlace a donde se deriva),
  **qué significa en palabras**, y **un número del hilo**. Contraejemplo: $\bar u=(2G-N)/N$ sin decir que es
  victorias (+1) menos derrotas (−1) entre $N$ (`5_simular_en_vez_de_evaluar.md`, antes de 2026-10-12).
- **DEBE** un objeto que aparece en dos páginas **ligarse en las dos**: la primera anuncia de dónde saldrá y la segunda
  parte de la forma que el alumno ya vio y muestra la equivalencia. Contraejemplo: el puntaje de p5 con $c$ y $N(s)$, y p6
  que llega por $\delta$ sin decir que $c=\sqrt{2k}$ cuando $\delta=N(s)^{-k}$.
- **DEBE** no haber dos frases que el alumno lea como contradicción entre páginas («con $G/N$ cambia la elección» /
  «es la misma regla»). Si las dos son ciertas, la cuenta que las reconcilia va escrita.
- **DEBE** cada concepto con nombre tener su **intuición antes de su fórmula**: qué pregunta contesta y qué haría el
  alumno sin él. Contraejemplo: «techo» definido en una línea, sin decir qué protege ni mostrarlo en números.
- **DEBERÍA** la página cerrar recorriendo el argumento en orden («Lo que hay que llevarse» sigue la pregunta guía,
  no es una lista de cifras sueltas).

## Repetición útil y relleno

- **CRITERIO útil**: «Lo que traes»; «Lo que hay que llevarse» con los números concretos (`J/2_mirar_todo_y_podar/2_minimax_como_algoritmo.md:674-684`); el modelo dos veces, construcción y resumen (`P/1_salones_practica.md:222`); una columna que se repite para verla viajar (`J/2_mirar_todo_y_podar/2_minimax_como_algoritmo.md:228-230`). No cuenta para topes (ver `lectura.md`).
- **CRITERIO relleno**: repetir sin número ni enlace nuevo, re-explicar una definición ya enlazada, un resumen más largo que lo que resume.
- **DEBE (regla del profesor, 2026-10-14): no toda repetición es mala.** Repetir una fórmula o una definición donde se vuelve a usar, o lo que ayuda a comparar sin tener que subir en la página (p. ej. fichas que se comparan lado a lado), **se queda**. Se quita solo lo repetido sin sentido: la misma frase dos veces seguidas, un paso repetido dentro de la misma sección. Ante un hallazgo de «repetición», la pregunta es si ayuda a leer o comparar en ese punto.

## Error típico y «Qué no es»

- **DEBE** llevar **Qué no es:** la definición que tiene un confusor cercano (`J/1_leer_y_escribir/2_escribir_el_juego.md:149`; EVAL frente a $V$, `J/3_cuando_no_cabe/1_cortar_y_evaluar.md:124`). Sin confusor real, no se inventa.
- **DEBERÍA** ir en tabla Error | Qué pasa los errores simétricos (`J/2_mirar_todo_y_podar/3_cuando_decide_un_dado.md:247-251`), y la idea que más confunde, en cita destacada (`J/1_leer_y_escribir/3_el_juego_como_grafo.md:153-157`).

## «Para profundizar» como válvula

- **DEBE** ir en `## Para profundizar`, antes de «Lo que hay que llevarse», lo que el ejercicio final no necesita (memoria, terminación, costo fino); la prosa principal lo anuncia (`J/2_mirar_todo_y_podar/2_minimax_como_algoritmo.md:445-446`, `:583`). Puede llevar micro-ejercicios (`:600`).

## Qué no copiar de unidades viejas

| Patrón viejo | Dónde | En su lugar |
|---|---|---|
| Afirmación falsa sobre el juguete | `J/2_mirar_todo_y_podar/2_minimax_como_algoritmo.md:210` | Verificar con la fuente |
| 20 minutos para 1042 líneas | `P/3_clasificacion_practica.md:7` | `lectura.md` |
| Imagen sin `::: figure` | `P/4_regresion_practica.md:142` | `figuras.md` |
| Pistas y respuestas en páginas distintas | `course/6_optimizacion/4_entero/1_la_bitacora_del_taller.md:174` | `ejercicios.md` |
| «Límite», «revisa tu hoja», «error tentador» | Tareas (`*_tarea.md`) | No se trasladan a páginas |

## Excepciones

- Unidades de lectura o cronología: sin juguete para traza; las capas son hilo e instancia.
- «Lo que traes» se omite en la primera página de la primera clase.
- El hilo completo (hexapawn: 252 nodos) aparece como cifra o en el notebook, nunca trazado a mano.
