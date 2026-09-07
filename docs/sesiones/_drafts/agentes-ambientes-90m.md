# Sesión: de predicción a decisión (90 minutos)

**Estado:** borrador docente
**Unidad:** Agentes, ambientes y modelado de decisiones

## Resultado visible al salir

Cada estudiante puede tomar una historia nueva y completar de forma defendible:

1. decisión concreta, frontera, entorno, observación y acciones;
2. una P con horizonte, resultado y al menos una restricción;
3. una E, una A y una S que no se contradicen; y
4. dos propiedades del entorno justificadas por hechos.

No se pide resolver un MDP ni programar. La formalización matemática empieza en
la sesión siguiente, una vez que estas cajas sean habituales.

## Preparación

- Proyectar las figuras de predicción, bucle, PEAS, diagnóstico, capacidades y
  trayectoria de `course/5_agentes_ambientes/_assets/`.
- Pizarrón en tres columnas fijas: **lienzo** a la izquierda, **bucle** al
  centro, **caso vigente** a la derecha. No borrar el lienzo durante la clase.
- Usar una tarjeta de caso ya prellenada para la clínica final; no pedir que
  inventen los diez campos desde cero en los últimos minutos.
- Usar las tres escenas como respiros visuales, no como diapositivas con texto.

## Guion minuto a minuto

| Minutos | Actividad y pregunta | Producción del grupo | Riesgo a vigilar |
|---:|---|---|---|
| 0–10 | **Gancho: portera.** «¿Qué falta para convertir 70% a la izquierda en una decisión?» | Acciones, consecuencias y criterio. | No llamar agente a la predicción sola. |
| 10–22 | **Bucle: plataformas.** «¿Qué existe, qué llega a pantalla y qué queda fuera?» | Frontera, observación, acción, memoria posible. | No equiparar mundo con pantalla. |
| 22–37 | **P: pits.** «¿Qué cuenta como hacerlo bien?» | P con horizonte, resultado, límite y posible atajo. | Meta, desempeño, utilidad y recompensa no son sinónimos. |
| 37–49 | **E/A/S en contraste.** «¿Qué existe, qué puedo mover y qué veo?» | Una fila de cada letra para el mismo caso. | No copiar el mundo a los sensores ni confundir deseo con acción. |
| 49–54 | **Pausa.** | — | No añadir contenido. |
| 54–66 | **Diagnóstico: ajedrez y póker.** «¿Qué evidencia cambia el diseño?» | Dos cadenas hecho → propiedad → implicación. | Ajedrez es estratégico aunque su transición sea determinista. |
| 66–78 | **Capacidades.** «¿Qué no puede resolver el percepto actual?» | Regla, memoria/modelo, objetivo, utilidad o aprendizaje. | No presentar una escalera rígida. |
| 78–88 | **Clínica: museo simulado.** Completar P, E, A y S; marcar un supuesto. | Ficha PEAS breve y coherente. | No intentar taxonomía ni refuerzo todavía. |
| 88–90 | **Salida.** «Una etiqueta sin evidencia no cuenta.» | Recolectar tarjeta. | Cerrar con el método, no definiciones. |

## Lienzo que permanece escrito

1. Decisión: ¿qué verbo y qué opciones?
2. Frontera: ¿qué está dentro del agente?
3. Entorno: ¿qué queda fuera y afecta?
4. Observación: ¿qué llega de verdad?
5. Acciones: ¿qué puede ejecutar?
6. Dinámica: ¿qué cambia después?
7. Oculto o incierto: ¿qué debe inferir?
8. Desempeño: ¿qué trayectoria preferimos y qué no permitimos?
9. Diagnóstico: hecho → propiedad → implicación.
10. Capacidad mínima: ¿qué debe poder hacer el controlador?

## Frases útiles para conducir

- «No me des una etiqueta: dime qué hecho del caso la justifica.»
- «¿Eso lo ve el agente, lo recuerda, o solo lo sabe quien escribió el problema?»
- «¿Es una acción disponible o una meta que te gustaría alcanzar?»
- «Si tu recompensa funcionara perfectamente, ¿qué conducta extraña podría
  seguir siendo rentable?»
- «Declara tu supuesto; no lo escondas.»

## Respuestas aceptables y correcciones breves

| Si aparece... | Responder / redirigir |
|---|---|
| «El agente ve el estado.» | «¿Cuál sensor o interfaz entrega esa variable?» |
| «Póker es estocástico, ajedrez determinista.» | «Sí, y ambos incluyen otros agentes. ¿Qué hace estratégica la decisión?» |
| «La recompensa es ganar.» | «¿Cuándo y cómo la recibe? ¿Qué hace antes del final?» |
| «Necesita RL.» | «¿Qué evidencia descarta primero una regla, memoria o modelo?» |
| «No hay respuesta.» | «Puede haber varias; marca el supuesto que separa una de otra.» |

## Después de los 90 minutos

La sesión introduce P y contrasta E/A/S; no pretende agotar la unidad. La ruta
de estudio sigue con las cuatro páginas PEAS y su clínica integrada, después las
siete propiedades del entorno, y solo entonces capacidades de agente y
refuerzo. El siguiente encuentro puede retomar una ficha real y preguntar qué
capacidad exige su evidencia.
