---
id: proyecto-final-entrega
title: "Cómo se entrega el proyecto final"
nav_title: "Cómo se entrega"
summary: "El repositorio de entregas paso a paso: el fork, la carpeta del equipo copiada de la plantilla, los dos pull requests (propuesta y entrega), la bitácora y qué revisa el check."
status: ready
estimated_time: 10m
tags: [proyectos, proyecto-final, entrega, github, docker]
prerequisites: [proyecto-final]
---

# Cómo se entrega el proyecto final

Todo el proyecto vive en **una carpeta por equipo** dentro de un repositorio público de GitHub, y se entrega con **dos pull requests**: la propuesta y la entrega. Esta página junta las direcciones y los pasos. Qué puede ser el proyecto y cómo se presenta está en [[proyecto-final|El proyecto final]].

> [!NOTE]
> **Lo oficial es el README del repositorio de entregas:**
> **[github.com/raya-lucaria/ia_o26_proyecto_final](https://github.com/raya-lucaria/ia_o26_proyecto_final)**.
> Esta página resume lo mismo. Si algo difiere, manda el repositorio.

## Las direcciones

- **El repositorio de entregas**, donde va tu carpeta y abres tus pull requests: [github.com/raya-lucaria/ia_o26_proyecto_final](https://github.com/raya-lucaria/ia_o26_proyecto_final).
- **El README**, con todos los pasos: [README.md](https://github.com/raya-lucaria/ia_o26_proyecto_final/blob/main/README.md).
- **La plantilla** que copias a tu carpeta: [plantilla/](https://github.com/raya-lucaria/ia_o26_proyecto_final/tree/main/plantilla).
- **El revisor**, el mismo script que corre el check, para usarlo en tu computadora: [herramientas/revisar.py](https://github.com/raya-lucaria/ia_o26_proyecto_final/blob/main/herramientas/revisar.py).
- **Los pull requests** de todos, abiertos y aceptados: [pulls](https://github.com/raya-lucaria/ia_o26_proyecto_final/pulls?q=is%3Apr).
- **Tu fork**, después del paso 1: `https://github.com/<tu-login>/ia_o26_proyecto_final`.
- **Tu carpeta**, dentro del repositorio: `estudiantes/<tu_equipo>/`.

## Cómo funciona

```text
1. Hablas conmigo del tema
2. PR «Propuesta: <tu_equipo>»
   → merge = tema autorizado
3. Trabajan en su fork
4. PR «Entrega: <tu_equipo>»
   → merge, el día del examen final
```

1. **La propuesta.** Después de hablarlo conmigo, abres un pull request con tu carpeta y `estado = "propuesta"`. **Cuando le hago merge, el tema queda autorizado.**
2. **La entrega.** El día del examen final de IA, otro pull request con todo el proyecto, `estado = "entrega"` y la demo. A la hora que anuncie, se deja de hacer merge: lo aceptado es lo que se presenta.

Cada pull request lo revisa un check automático, **revisar-entrega**. Si sale ❌, abre el check, lee el resumen, arregla lo que diga y vuelve a hacer `push`: el check corre solo otra vez.

## Paso a paso

**1. Una persona del equipo hace el fork.** En el [repositorio de entregas](https://github.com/raya-lucaria/ia_o26_proyecto_final): **Fork → Create fork**. Si son dos, en **tu fork** ve a **Settings → Collaborators → Add people** y agrega a tu compañero; acepta la invitación desde su correo.

**2. Los dos clonan el fork.**

```bash
git clone https://github.com/<login-del-fork>/ia_o26_proyecto_final.git
cd ia_o26_proyecto_final
# Debe ser el correo de TU cuenta de GitHub:
git config user.email
```

Si el correo no es el de tu cuenta, tus commits no cuentan como tuyos. Se arregla con `git config --global user.email "tu-correo-de-github"`.

**3. Copia la plantilla a tu carpeta.** El nombre es el del proyecto: de 3 a 30 caracteres, minúsculas sin acentos, dígitos y `_` (por ejemplo, `agente_snake`).

```bash
cp -r plantilla estudiantes/<tu_equipo>
```

**4. Llena `proyecto.toml`.**

```toml
estado = "propuesta"
titulo = "Un agente que juega Snake"
tema = "Q-learning en un ambiente propio"
# Logins de GitHub; si vas solo, uno:
equipo = ["usuario-a", "usuario-b"]
demo = ""
```

**5. Revisa en tu computadora.** Es el mismo revisor del check:

```bash
python3 herramientas/revisar.py estudiantes/<tu_equipo>
```

**6. Sube y abre el pull request de la propuesta.**

```bash
git add estudiantes/<tu_equipo>
git commit -m "Propuesta: <tu_equipo>"
git push
```

En tu fork en GitHub: **Contribute → Open pull request**, con el título `Propuesta: <tu_equipo>`.

**7. Trabajen.** Commits en su fork, cada quien con su cuenta, y la bitácora al día. No hace falta abrir otro pull request hasta la entrega.

**8. El pull request de la entrega.** En `proyecto.toml` cambia `estado = "entrega"` y pon `demo = "https://…"` (o `"no aplica"`, si así lo acordamos). Prueba `docker compose up --build` en tu carpeta, corre otra vez el revisor, haz `commit` y `push`, y abre otro pull request: `Entrega: <tu_equipo>`.

## Tu carpeta

La [plantilla](https://github.com/raya-lucaria/ia_o26_proyecto_final/tree/main/plantilla) ya trae todo esto. Cambia lo que haga falta, pero no quites ninguno:

```text
estudiantes/<tu_equipo>/
├── proyecto.toml   tus datos
├── README.md       con «Cómo correrlo»
├── BITACORA.md     tu evidencia
├── LICENSE         MIT
├── Dockerfile
├── compose.yaml    docker compose up --build
├── .gitignore      datos/, modelos/, .env
├── .env.example    variables, sin valores
└── …               tu código
```

El `main.py`, `requirements.txt` y el `Dockerfile` de la plantilla son un ejemplo que funciona: responde en `http://localhost:8000`. Cámbialos por los tuyos.

## Datos, modelos y llaves

El repositorio es **público**, así que:

- **Datos y modelos** van en `datos/` y `modelos/` dentro de tu carpeta. Están en `.gitignore` y no se suben. En tu README pon de dónde se bajan y el comando para conseguirlos.
- **Ningún archivo de más de 5 MB**, y la carpeta completa, máximo 50 MB.
- **Las llaves** (OpenAI, Anthropic, Hugging Face…) van en `.env`, que no se sube; sube `.env.example` sin valores. Si una llave se sube por error, **revócala** en el sitio que la dio: ya quedó en el historial.
- Nada de caras ni datos personales.

## La bitácora

Lo que GitHub ya sabe (commits, pull requests, issues) no se copia. La bitácora es para lo que no deja commits: pruebas, diseño, entrenamientos largos. Una fila por entrada:

```markdown
| fecha | login | qué hice | evidencia |
|---|---|---|---|
| 2026-11-20 | usuario-a | Entrené 2 h | evidencia/curva.png |
| 2026-11-22 | usuario-b | Probé la demo | https://youtu.be/… |
```

La fecha va como `AAAA-MM-DD`, el login es uno del equipo, y la evidencia es un link o un archivo de tu carpeta. Sin evidencia, la fila no cuenta.

## Qué revisa el check

En cada pull request:

- Que solo cambie **una** carpeta `estudiantes/<tu_equipo>/`, con nombre válido.
- Que quien lo abre esté en `equipo`. Una carpeta ya aceptada solo la cambia su equipo.
- Que estén `proyecto.toml` bien llenado, `README.md` con «Cómo correrlo», `LICENSE` y `BITACORA.md` con su formato.
- Que no haya archivos de más de 5 MB, `datos/`, `modelos/`, `node_modules/`, `.venv/`, `.env` ni llaves.

Y en la entrega, además:

- Que haya `Dockerfile` o `compose.yaml`, y que **la imagen se construya**.
- Que `demo` tenga una URL, o `"no aplica"` si así lo acordamos.

## Si algo falla

- **«El PR toca archivos fuera de…»**: cambiaste algo fuera de tu carpeta. El resumen del check dice qué archivo; regrésalo a como estaba, haz `commit` y `push`.
- **«Quien abre el PR no está en `equipo`»**: agrega tu login en `proyecto.toml`.
- **El check dice que hay una llave**: bórrala del archivo, ponla en `.env` y revócala.
- **El check no corre**: si es tu primer pull request, puede que tenga que aprobarlo yo primero.
