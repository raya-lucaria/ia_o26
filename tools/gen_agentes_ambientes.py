"""Genera los diagramas SVG de agentes y ambientes."""

from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/5_agentes_ambientes/_assets"
FONDO = "#211033"
DIAGRAMAS = {
    "aa-prediccion-vs-decision": ("Predecir no basta para decidir", "Una predicción termina en una estimación; un agente cierra un bucle de observación, acción y consecuencias.", ["entrada", "predictor", "estimación", "observación", "agente", "acción", "entorno", "nueva observación"]),
    "aa-lienzo-modelado": ("El lienzo de modelado en diez pasos", "Un recorrido de decisión, frontera, observación, acción, dinámica, información oculta, desempeño, diagnóstico y capacidades.", ["1 Decisión", "2 Frontera", "3 Entorno", "4 Observa", "5 Actúa", "6 Cambia", "7 No ve", "8 Evalúa", "9 Diagnostica", "10 Diseña"]),
    "aa-mundo-observacion-creencia": ("Mundo, observación, creencia y estado de decisión", "El mundo puede tener aspectos ocultos; el agente recibe un percepto, actualiza su estado interno y decide.", ["mundo", "percepto", "creencia", "estado de decisión"]),
    "aa-peas": ("Especificar una tarea con PEAS", "La medida de desempeño, el entorno, los actuadores y los sensores rodean a un estratega de carrera.", ["P desempeño", "E entorno", "A actuadores", "S sensores"]),
    "aa-perillas-entorno": ("Siete preguntas para diagnosticar un task environment", "Cada eje pregunta qué información, azar, tiempo, dinámica, continuidad, agentes y conocimiento importan.", ["¿ve todo?", "¿azar o rival?", "¿afecta después?", "¿cambia al pensar?", "¿discreto o continuo?", "¿otros deciden?", "¿conoce reglas?"]),
    "aa-capacidades-agente": ("Capacidades de decisión, no una escalera obligatoria", "Un controlador puede reaccionar, mantener modelo, usar objetivos o utilidad; el aprendizaje puede mejorar todas esas capacidades.", ["reflejo", "modelo", "objetivo", "utilidad", "aprendizaje atraviesa"]),
    "aa-trayectoria": ("Política, recompensa inmediata y retorno", "La política elige una acción; el entorno produce una recompensa inmediata y un siguiente estado; el retorno agrega consecuencias futuras.", ["estado u observación", "política", "acción", "recompensa inmediata", "siguiente estado", "retorno futuro"]),
}


def svg(titulo, descripcion, etiquetas):
    total = len(etiquetas)
    paso = 1040 / total
    tarjetas = []
    for indice, etiqueta in enumerate(etiquetas):
        x = 80 + indice * paso
        color = "#ff4fd8" if indice % 2 == 0 else "#55ddff"
        tarjetas.append(f'<rect x="{x:.0f}" y="245" width="{paso - 12:.0f}" height="96" rx="16" fill="#35164d" stroke="{color}" stroke-width="3"/>')
        tarjetas.append(f'<text x="{x + (paso - 12) / 2:.0f}" y="288" text-anchor="middle" fill="#f7f2ff" font-size="18" font-weight="700">{escape(etiqueta)}</text>')
        if indice < total - 1:
            flecha_x = x + paso - 8
            tarjetas.append(f'<path d="M {flecha_x:.0f} 293 h 18" stroke="#f7c948" stroke-width="4" marker-end="url(#flecha)"/>')
    contenido = "".join(tarjetas)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="560" viewBox="0 0 1200 560" role="img" aria-label="{escape(titulo)}">
<title>{escape(titulo)}</title>
<desc>{escape(descripcion)}</desc>
<defs><marker id="flecha" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#f7c948"/></marker></defs>
<rect width="1200" height="560" fill="{FONDO}"/>
<text x="600" y="92" text-anchor="middle" fill="#f7f2ff" font-family="system-ui, sans-serif" font-size="34" font-weight="800">{escape(titulo)}</text>
<text x="600" y="140" text-anchor="middle" fill="#c8b9d8" font-family="system-ui, sans-serif" font-size="18">{escape(descripcion)}</text>
<path d="M100 188 H1100" stroke="#6a3d8d" stroke-width="2"/>
{contenido}
<text x="600" y="445" text-anchor="middle" fill="#c8b9d8" font-family="system-ui, sans-serif" font-size="17">Primero modela el caso; después nombra la herramienta.</text>
</svg>'''


def generar():
    ASSETS.mkdir(parents=True, exist_ok=True)
    for nombre, (titulo, descripcion, etiquetas) in DIAGRAMAS.items():
        (ASSETS / f"{nombre}.svg").write_text(svg(titulo, descripcion, etiquetas), encoding="utf-8")


if __name__ == "__main__":
    generar()
