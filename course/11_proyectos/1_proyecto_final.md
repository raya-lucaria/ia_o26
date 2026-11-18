---
id: proyecto-final
title: "El proyecto final"
nav_title: "Proyecto final"
summary: "Un proyecto completo y de inteligencia artificial, en un repo público con Docker, que se presenta con demo en vivo el día del examen final."
status: ready
estimated_time: 12m
tags: [proyectos, proyecto-final, docker, entrega, evidencia]
prerequisites: [proyectos]
---

# El proyecto final

**Equipo de 1 o 2 · se entrega el día del examen final · se presenta con demo en vivo.**

Si quieres un equipo de otro tamaño, lo hablas conmigo y yo decido.

> [!NOTE]
> **Se entrega en el repositorio de entregas:**
> **[github.com/raya-lucaria/ia_o26_proyecto_final](https://github.com/raya-lucaria/ia_o26_proyecto_final)**.
> Las direcciones y los pasos, del fork al pull request de la entrega, están en [[proyecto-final-entrega|Cómo se entrega el proyecto final]]. Si algo difiere, manda el repositorio.

## Qué puede ser

Cualquier tema **de inteligencia artificial, relevante para la clase**: un agente que juega o que resuelve un ambiente, benchmarks de algoritmos de búsqueda u optimización, un modelo entrenado con su evaluación, un dashboard, un harness. Tiene que estar bien pensado, ser interesante y estar completo de punta a punta.

**No se vale algo hecho con vibe coding el día antes de entregar.** Antes de empezar, vienes a hablar conmigo para que yo autorice el proyecto. Si lo suben, se asume que lo hablamos; si no, lo veo yo y ajusto.

## Requisitos

- Todo el proyecto vive en **su carpeta del [repositorio de entregas](https://github.com/raya-lucaria/ia_o26_proyecto_final)**, que es público: open source, con licencia.
- **Docker o Docker Compose**, con instrucciones cortas y directas en el README para correrlo.
- Accesible desde la web, o que corra fácil en cualquier máquina. Los videojuegos, en línea.
- La demo puede vivir **fuera de GitHub** (Supabase, un plan gratuito, otro hosting), o como acordemos si no aplica. Si el hosting sale caro, buscamos juntos una opción gratis.
- Evita los datos simulados, salvo que sean necesarios: por ejemplo, un dashboard para comparar muchas bases de datos.
- Un harness no tiene que estar en la web, pero sí funcionar dentro de un contenedor.

## Qué entregas (dos pull requests)

Cada equipo tiene **una carpeta**, `estudiantes/<tu_equipo>/`, copiada de la plantilla del repositorio, con todo su proyecto: código, Docker, README, licencia y bitácora. Sus datos van en `proyecto.toml`:

```toml
estado = "propuesta"          # "entrega" en el segundo pull request
titulo = "Título del proyecto"
tema = "Una línea: qué hace y qué parte del curso usa"
equipo = ["usuario-a", "usuario-b"]
demo = ""                     # la URL, en la entrega; puede estar fuera de GitHub
```

1. **La propuesta.** Después de hablarlo conmigo, abren un pull request con la carpeta y `estado = "propuesta"`. **Cuando le hago merge, el tema queda autorizado.**
2. **La entrega.** El día del examen final, otro pull request con todo el proyecto, `estado = "entrega"` y la demo.

Cada integrante trabaja y hace sus commits **con su propia cuenta de GitHub**, para que su trabajo quede a su nombre. Los datos, los modelos y las llaves se quedan en su computadora: la plantilla ya los ignora y el check no deja subirlos. Sin presentación en GitHub.

El paso a paso, con los comandos, la carpeta y lo que revisa el check, está en [[proyecto-final-entrega|Cómo se entrega el proyecto final]].

## Evidencia de que trabajaron

Quiero ver que cada integrante trabajó, sin que sea complicado. Lo que GitHub ya sabe (commits, pull requests, issues, reviews) se toma de GitHub y no lo escribes a mano.

Para lo que no deja commits (un robot, hardware, diseño, pruebas), lleva la `BITACORA.md` de tu carpeta, con una línea por entrada: fecha, quién, qué hizo y un **link o un archivo commiteado** (foto, video). Sin link ni archivo, la línea no cuenta como evidencia. No subas caras ni datos personales: el repo es público.

## Qué se revisa

- Que tu carpeta pase el check del pull request: licencia, README, bitácora y Docker que se construye.
- Que el Compose sea válido y la demo responda, si declaras una.
- Que cada integrante tenga evidencia de trabajo por algún canal.

Los reportes dicen hechos verificables, por ejemplo cuántos commits tiene cada quien. Nunca acusan a nadie.

## Cómo se presenta

Demo en vivo y platicar todo el proceso, **entre 8 y 12 minutos**. Son muchos equipos, así que el tiempo puede ser menor: se anuncia antes de presentar, y **el reloj es exacto**. Al llegar al límite se corta. **No se muestra código.** Las diapositivas se recomiendan, pero no son obligatorias. Prepárala para que quepa en el tiempo y cuenta, en este orden:

1. Qué es, a grandes rasgos (1 minuto).
2. Cómo funciona y su arquitectura (2 a 3 minutos).
3. Qué se les hizo difícil y qué problemas tuvieron (1 a 2 minutos).
4. La demo, funcionando (3 a 4 minutos).
5. El proceso completo: qué hay detrás de lo que se ve (1 a 2 minutos).

Si te avisan que el tiempo es de 8 minutos, recorta la arquitectura y el proceso, no la demo. Ten la demo abierta y lista antes de que te toque: cargarla no se descuenta del reloj de nadie más.
