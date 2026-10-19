---
id: proyecto-torneo-adversarial
title: "Proyecto: un bot para Breakthrough de combate"
nav_title: Proyecto
summary: "El proyecto de la unidad: en equipos de 2, un bot que juega Breakthrough de combate en una liga todos contra todos. Qué es, cómo empezar, qué se entrega y cómo se califica; las instrucciones completas están en su repositorio."
status: ready
estimated_time: 6m
tags: [juegos, proyecto, torneo]
---

# Proyecto: un bot para Breakthrough de combate

**¿Qué tan lejos llega lo que aprendiste en esta unidad contra un juego que
nadie ha resuelto?**

En equipos de 2, programas un bot que juega **Breakthrough de combate** y
compite en una **liga** contra los bots de tus compañeros y los nuestros.

> [!NOTE]
> **Todo lo oficial está en el repositorio del torneo:**
> **[github.com/raya-lucaria/ia_o26_torneo_adversarial](https://github.com/raya-lucaria/ia_o26_torneo_adversarial)**.
> Ahí vienen las reglas completas, el motor, el árbitro, los comandos, la
> entrega y la calificación. Esta página solo presenta lo importante; si algo
> difiere, manda el repositorio.

---

## El juego en un minuto

- **Tablero y peones.** 9 × 9, 18 peones por bando. Blancas empiezan en las
  filas 1 y 2; Negras, en las 8 y 9.
- **Mover.** Un peón avanza una casilla: recto a una vacía, o en diagonal a
  una vacía o atacando a un rival. Nunca hacia atrás ni de lado.
- **Combate con dado.** El **apoyo** de un peón es cuántos peones propios
  tiene en sus dos diagonales de atrás (0, 1 o 2). El atacante gana con
  probabilidad

  $$
  \begin{aligned}
  p&=0.5+0.15\,\Delta,\\
  \Delta&=a_{\text{ataca}}-a_{\text{defiende}},
  \end{aligned}
  $$

  con $a$ el apoyo de cada peón.

  Si gana, ocupa la casilla; si pierde, sale **su** peón.
- **Ganar.** Un peón que llega a la última fila rival anota 1 punto y sale.
  Gana quien llega a **3 puntos** o deja al rival **sin jugadas**. No hay
  empates.

## Lo que ya tienes de la unidad

- **El dado** convierte cada ataque en un nodo de azar, como en
  [[cuando-decide-un-dado|Cuando decide un dado]].
- **El árbol no cabe.** Hace falta cortar y evaluar
  ([[cortar-y-evaluar|Cortar y evaluar]]) y administrar el reloj
  ([[jugar-contra-el-reloj|Hasta dónde mirar]]).
- **Simular.** El participante `montecarlo` es el Monte Carlo plano de
  [[simular-en-vez-de-evaluar|Simular partidas]]; MCTS con UCT está en
  [[monte-carlo-en-un-arbol-grande|MCTS con UCT]].
- **Elegir.** [[elegir-el-algoritmo|Elegir el algoritmo]] ayuda a decidir qué
  combinar.

## Tu bot: dos funciones

```python
def preparar(config):
    # una vez por partida,
    # 10 s fuera del reloj
    ...

def jugar(estado,
          tiempo_restante):
    # te toca: devuelve una
    # de estado.jugadas()
    ...
```

Recibes el estado completo y tu reloj; regresas una jugada legal. Lo de en
medio es tuyo: búsqueda, evaluación, manejo del azar y del reloj,
precomputación.

## Empezar

1. **Crea tu repo privado** desde el repositorio del torneo con *Use this
   template* (un *fork* sería público).
2. **Copia el participante `montecarlo`** a `estudiantes/<tu_equipo>/` y
   llena `equipo.toml` e `INFORME.md`.
3. **Juega contra él:** `./torneo jugar <tu_equipo> montecarlo`, y mejora tu
   `strategy.py` partida a partida.

## Reglas que no se rompen

- **Límites:** 30 s de reloj por partida, 1 núcleo, 1024 MB de memoria.
- **Prohibido:** redes neuronales, código ofuscado o nativo propio, adivinar
  o manipular los dados, compartir código o datos entre equipos.
  **Trampa = 0 para todo el equipo.**
- **Obligatorio:** `INFORME.md` completo y `equipo.toml` válido; sin ellos no
  hay calificación.

## Entrega

1. **Antes de la hora límite**, registras el SHA de tu último commit; tu
   código sigue privado.
2. **En las 24 horas siguientes**, abres un *pull request* con tu carpeta tal
   como estaba en ese SHA. Solo puede cambiar archivos de
   `estudiantes/<tu_equipo>/`.

La fecha y la hora las anuncia el profesor.

## Cómo se califica

> [!WARNING]
> **La calificación todavía puede ajustarse.** Aquí va la idea; la versión
> vigente es la del repositorio.

Liga todos contra todos: 4 partidas contra cada participante, 1 punto por
victoria. Tu calificación es la del **mejor bot de referencia al que le
ganas**, y «ganarle» es terminar con **estrictamente más puntos** que él.

::: table {#jue-proyecto-calificacion title="Calificación según el mejor bot al que le ganas"}
| Mejor bot de referencia al que le ganas | Calificación |
|---|---:|
| ninguno | 0 |
| `random` (juega al azar) | 1 |
| `montecarlo` (Monte Carlo plano) | 3 |
| Tier 1 | 5 |
| Tier 2 | 6 |
| Tier 3 | 7 |
| Tier 4 | 8.5 |
| Tier 5 | 10 |
| **Lugares 1, 2 y 3 entre equipos de alumnos** | **10** |
:::

Los tiers son bots nuestros, de menor a mayor fuerza; su código no se
publica y juegan con las mismas reglas y límites que tú.

**Un consejo del repositorio:** usa un agente de IA para programar, pero la
estrategia es tuya. Lo que gana es tu idea, medida con partidas.

Regresa a [[juegos|la unidad]].
