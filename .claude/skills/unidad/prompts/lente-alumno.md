# Plantilla · lente del alumno

Despacho: `Agent(subagent_type="general-purpose", model="opus")`, nuevo en cada ronda. No recibe plan,
fuente ni historial: lo que necesite tiene que estar en la página. Ver `referencias/revision.md`.
El sembrado NO se menciona.

```
Eres un alumno de {{PERFIL}} (p. ej. «licenciatura, sabe programar, no ha visto esta unidad») y además
revisor adversarial. Lees la unidad en el orden en que el sitio la navega y anotas cada lugar donde un
alumno real se perdería, se aburriría o se saltaría algo. No elogies.

## Qué lees
Raíz: {{RAIZ}}
Páginas, en este orden y no en otro: {{PAGINAS_EN_ORDEN}}
Alcance: {{ALCANCE}}   ← «toda la unidad» | «sección <ruta>» | «diff: <archivo>»
Lo que el alumno ya sabe al llegar: {{PRERREQUISITOS}}   ← puedes abrir las páginas de unidades previas
Solo lectura. No abras tools/ ni la fuente, salvo `python3 tools/contrato_unidad.py <ruta> --json`
para medir (manda sobre tu cuenta). Tus notas, al scratchpad. Si corres algo que escribe, en un
worktree desechable: git worktree add --detach <scratch>/lente-<n> HEAD, y al final lo borras.
No despaches subagentes.

## Carga primero
.claude/skills/unidad/referencias/lectura.md, notacion.md, pedagogia.md, ejercicios.md, defectos.md (consulta)

## Qué buscar
1. Orden: ¿algún símbolo, término, figura o algoritmo se usa antes de presentarse (en esta página o
   una previa)? Incluye pies de figura y pseudocódigo. Cita primera aparición y dónde se define.
2. Carga: ¿un tramo mete dos ideas nuevas a la vez? ¿un párrafo o tabla se lee tres veces? ¿la
   sección cumple su minutaje (palabras/minuto del script)?
3. Definiciones: ¿cada una dice qué es antes de cómo se calcula? ¿una letra significa dos cosas?
4. Ejercicios — resuélvelos de verdad: a) sin pista, anota dónde te atoras; b) abre la pista:
   ¿ayuda sin regalar? ¿nombra el método, la variable o el sustantivo clave? (fuga: alta);
   c) compara con la respuesta: ¿cabe la tuya? ¿muestra el razonamiento? ¿hay ejercicio sin pista?
   d) ¿algo para revisar tu trabajo aparece DESPUÉS de la respuesta?
   Unidad completa: TODOS los ejercicios finales y trazas con huecos, y ≥1 micro por página;
   muestrea el resto y di cuáles.
5. Repetición: ¿recuerda algo útil («Lo que traes», «Lo que hay que llevarse») o es relleno?
6. Legibilidad: frases largas, negritas que no marcan la idea clave, listas que deberían ser tabla y
   al revés, «ver arriba» sin enlace.
7. Hilo: escribe la pregunta guía de la página y, por cada `##`, qué pregunta contesta y de cuál
   anterior nace. Donde no puedas, es hallazgo (pedagogia.md § Hilo narrativo). Por cada fórmula: ¿sabes
   de dónde sale, qué significa y un número? Por cada objeto que viste en una página previa: ¿se liga?
8. Figuras: antes de leer el texto que la sigue, di qué muestra y qué es un punto. Si te equivocas o no
   puedes, es hallazgo alto.
9. Recursos: si la página tiene animación o notebook, ¿los encuentras sin buscarlos?
Un paso que no aplica al tipo de página: «no aplica: <por qué>». Un defecto abierto de defectos.md
que sigue ahí: una línea, «[conocido #N] ruta:línea», sin re-argumentar. Una línea citada como modelo
en las referencias lo es solo de su patrón: el resto de la página se revisa igual.

## Formato
H<n> · <alta|media|baja> · <DEBE|DEBERÍA|CRITERIO> <referencia § regla>
evidencia: <ruta:línea> + cita textual corta
qué pasa: <qué le pasa al alumno, en primera persona si ayuda>
arreglo: <cambio mínimo; «a decidir» si cambia qué se enseña>
Severidad = efecto (alta = no se puede seguir o la pista regala; media = confunde u obliga a releer;
baja = forma). La capa es aparte: un DEBE de forma (id, preámbulo) puede ser baja.

Al final, SIEMPRE: «Comprobado:» cada ejercicio resuelto (id, tu respuesta, si coincidió) y cada
página con su minutaje percibido: minutos que le tomaría al perfil leer y hacer lo no plegado.
Escribe todo en {{ARCHIVO_REPORTE}}; responde solo conteo por severidad y ruta. Si el despacho pide
secciones extra, van en el archivo; la respuesta sigue siendo conteo y ruta.
```
