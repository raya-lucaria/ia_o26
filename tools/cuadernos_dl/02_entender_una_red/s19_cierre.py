# Sección 19 · Cierre. Consume TODAS las corridas que haya en CORRIDAS
# (las de §3 a §17, con la CNN) vía tabla_maestra(). No entrena nada.
# Publica: resumen, variacion. Si el alumno saltó secciones, CORRIDAS
# puede venir corto o vacío: cada celda lo dice y sigue sin tronar.

# %% [texto] s19-intro

# %% [codigo] s19-resumen
# La tabla maestra de la caja (s03): una fila por corrida, con sus números
# en la MEJOR epoch por validation (test no participó en elegirla).
# brecha = acc train − acc validation: cuánto va train por delante.
import numpy as np
import pandas as pd

# §16 guarda el MLP elegido también como CORRIDAS["s16-elegido"]: es el
# MISMO objeto con otro nombre, así que su fila saldría dos veces con su ID
# original. Dejamos una fila por ID.
resumen = tabla_maestra()
if not resumen.empty:
    resumen = resumen.drop_duplicates("id").reset_index(drop=True)
if resumen.empty:
    print("CORRIDAS está vacío: no corriste ninguna sección con experimentos.")
    print("Ejecuta el notebook completo (Entorno de ejecución → Ejecutar todo)")
    print("y vuelve aquí; esta sección solo resume lo que ya se entrenó.")
    resumen = pd.DataFrame(columns=["id", "seccion", "datos", "parametros",
                                    "mejor_epoch", "acc_train",
                                    "acc_validation", "acc_test", "brecha",
                                    "segundos", "divergio"])
else:
    # Orden: los grupos de datos en el orden en que aparecen en el notebook
    # y, dentro de cada grupo, de mejor a peor accuracy de VALIDATION.
    # Nunca se ordena ni se elige con test.
    resumen["divergio"] = resumen["divergio"].astype(bool)
    resumen["_orden"] = resumen.groupby("datos")["seccion"].transform("min")
    resumen = (resumen.sort_values(["_orden", "datos", "acc_validation"],
                                   ascending=[True, True, False])
               .drop(columns="_orden").reset_index(drop=True))
    print(f"{len(resumen)} corridas en {resumen['datos'].nunique()} grupos "
          f"de datos y {resumen['seccion'].nunique()} secciones.")
    print("Corridas por grupo de datos:")
    print(resumen.groupby("datos", sort=False).size().to_string())
    print("Divergieron:", int(resumen["divergio"].sum()))


def presupuesto(ident):
    """El presupuesto PEDIDO en la Config: pasos si los topa, si no epochs."""
    cfg = CORRIDAS[ident].config
    return f"{cfg.max_pasos} pasos" if cfg.max_pasos else f"{cfg.epochs} epochs"


resumen["presupuesto"] = [presupuesto(i) for i in resumen["id"]]
resumen["pasos"] = [int(CORRIDAS[i].historial["pasos"].iloc[-1])
                    for i in resumen["id"]]        # pasos dados de verdad
# Un color por sección, el mismo en la figura y en el recuadro final.
secciones = sorted(resumen["seccion"].unique())
paleta = plt.cm.tab20b(np.linspace(0, 1, max(len(secciones), 2)))
color_de = {s: paleta[i] for i, s in enumerate(secciones)}

# %% [texto] s19-tabla-texto

# %% [codigo] s19-tabla
# La tabla maestra completa, partida por grupo de datos. Solo se comparan
# filas DENTRO de un grupo: con 2000 ejemplos y 20 % de etiquetas
# cambiadas (§10) la accuracy no se puede poner junto a la de 50 000
# limpios. Dentro de cada grupo, el orden lo da validation.
columnas_tabla = ["id", "seccion", "parametros", "presupuesto", "pasos",
                  "mejor_epoch", "loss_train", "loss_validation", "loss_test",
                  "acc_train", "acc_validation", "acc_test", "brecha",
                  "segundos", "divergio"]
if resumen.empty:
    print("Sin corridas: no hay tabla maestra que mostrar.")
for datos_grupo, grupo in resumen.groupby("datos", sort=False):
    print(f"\n=== datos: {datos_grupo} · {len(grupo)} corridas, "
          "ordenadas por accuracy de validation ===")
    display(grupo[columnas_tabla].set_index("id").round(4))

# %% [texto] s19-figura-texto

# %% [codigo] s19-figura
# Una fila de paneles por grupo de datos. Izquierda: accuracy de
# validation en la mejor epoch, una barra por corrida, coloreada por la
# sección que la produjo. Derecha: la brecha train − validation de esa
# misma corrida. Las corridas que divergieron llevan «✕ divergió».
if resumen.empty:
    print("Sin corridas: no hay figura resumen.")
else:
    grupos = list(resumen.groupby("datos", sort=False))
    alturas = [max(len(g), 2) for _, g in grupos]
    alto = 0.32 * sum(alturas) + 1.6 * len(grupos) + 1.0   # +1 in: leyenda
    fig, ejes = plt.subplots(
        len(grupos), 2, figsize=(13, alto),
        gridspec_kw={"height_ratios": alturas, "width_ratios": [3, 2]},
        squeeze=False)
    # Todas las brechas con la misma escala, para compararlas entre grupos.
    lim_br = (min(0.0, resumen["brecha"].min()) - 0.01,
              max(0.0, resumen["brecha"].max()) + 0.01)
    for (datos_grupo, g), (ax_acc, ax_br) in zip(grupos, ejes):
        g = g.iloc[::-1]                       # la mejor queda arriba
        y = np.arange(len(g))
        colores = [color_de[s] for s in g["seccion"]]
        etiquetas = [f"{i}  ✕ divergió" if d else i
                     for i, d in zip(g["id"], g["divergio"])]
        barras = ax_acc.barh(y, g["acc_validation"], color=colores)
        for barra, d in zip(barras, g["divergio"]):
            barra.set_hatch("//" if d else "")      # rayada = divergió
        ax_br.barh(y, g["brecha"], color=colores, alpha=0.6)
        ax_br.axvline(0, color="black", lw=0.8)
        ax_br.set_xlim(*lim_br)
        # Eje de accuracy recortado: si arranca en 0, 0.97 y 0.98 se ven
        # iguales. El piso sale de las corridas que NO divergieron.
        sanas = g.loc[~g["divergio"], "acc_validation"]
        piso = max(0.0, (sanas.min() if len(sanas) else 0.0) - 0.05)
        for yi, v in zip(y, g["acc_validation"]):
            fuera = "  ◀ fuera del eje" if v < piso else ""
            ax_acc.text(max(v, piso) + 0.002, yi, f"{v:.3f}{fuera}",
                        va="center", fontsize=7)
        ax_acc.set_yticks(y, etiquetas, fontsize=8)
        ax_br.set_yticks(y, [""] * len(y))
        ax_acc.set_title(f"datos: {datos_grupo} · accuracy de validation "
                         f"(eje desde {piso:.2f})", fontsize=10)
        ax_acc.set_xlim(piso, 1.0)
        ax_br.set_title("brecha: acc train − acc validation", fontsize=10)
    ejes[-1, 0].set_xlabel("accuracy de validation en la mejor epoch")
    ejes[-1, 1].set_xlabel("brecha (positivo = train va adelante)")
    manijas = [plt.Rectangle((0, 0), 1, 1, color=color_de[s])
               for s in secciones]
    fig.legend(manijas, [f"§{s}" for s in secciones], title="sección",
               loc="upper center", ncol=min(len(secciones), 10),
               bbox_to_anchor=(0.5, 1.0), fontsize=8)
    fig.tight_layout(rect=(0, 0, 1, 1 - 1.0 / alto))   # 1 in libre arriba
    plt.show()

# %% [texto] s19-figura-mira

# %% [texto] s19-movio-texto

# %% [codigo] s19-movio
# «Qué movió de verdad el error»: cuánto varió la accuracy de validation
# entre corridas COMPARABLES: misma sección, mismos datos y mismo
# presupuesto pedido. Rango = máx − mín entre las que no divergieron.
# Rango chico = esa perilla casi no movió nada; grande = sí importa.
# Medida tosca: depende de qué valores se probaron en cada sección.
filas_var = []
for (sec, dat, pres), g in resumen.groupby(["seccion", "datos", "presupuesto"]):
    sanas, n_div = g[~g["divergio"]], int(g["divergio"].sum())
    if len(g) < 2:                       # con una sola corrida no hay rango
        continue
    acc = sanas["acc_validation"]
    filas_var.append({"comparacion": f"§{sec} · {dat} · {pres}", "seccion": sec,
                      "corridas": len(g), "divergieron": n_div,
                      "rango": acc.max() - acc.min() if len(acc) > 1 else 0.0})
# Dos comparaciones que cruzan secciones, si ambas corridas existen:
# dropout (§15) contra su control (§10), y la CNN contra el MLP elegido.
elegido = CORRIDAS["s16-elegido"].id if "s16-elegido" in CORRIDAS else None
for nombre, a, b in [("§15 · dropout vs su control de §10", "s15-dropout",
                      "s10-control"),
                     ("§17 · CNN vs MLP elegido en §16", "s17-cnn", elegido)]:
    par = resumen[resumen["id"].isin([a, b])]
    if len(par) == 2 and not par["divergio"].any():
        acc = par["acc_validation"]
        filas_var.append({"comparacion": nombre, "seccion": par["seccion"].max(),
                          "corridas": 2, "divergieron": 0,
                          "rango": acc.max() - acc.min()})
variacion = pd.DataFrame(filas_var)

if variacion.empty:
    print("No hay ninguna sección con dos o más corridas comparables:")
    print("corre las secciones 4 a 17 para llenar este recuadro.")
else:
    variacion = variacion.sort_values("rango").reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(11, 0.45 * len(variacion) + 1.5))
    ax.barh(variacion["comparacion"], variacion["rango"],
            color=[color_de[s] for s in variacion["seccion"]])
    for yi, (r, n_div) in enumerate(zip(variacion["rango"],
                                        variacion["divergieron"])):
        extra = f"  (+{n_div} divergieron)" if n_div else ""
        ax.text(r, yi, f" {r:.3f}{extra}", va="center", fontsize=8)
    ax.set_xlabel("rango de accuracy de validation entre corridas "
                  "comparables (máx − mín)")
    ax.set_title("Qué movió de verdad el error y qué no movió nada")
    ax.set_xlim(0, variacion["rango"].max() * 1.35 + 1e-3)
    plt.tight_layout()
    plt.show()
    display(variacion.round(4))

# %% [texto] s19-que-viste

# %% [texto] s19-protocolo

# %% [codigo] s19-final
# La lista de todos los experimentos que quedaron registrados, en el orden
# de la tabla maestra (un ID por corrida). CORRIDAS guarda además el alias
# "s16-elegido" (la MISMA corrida con otro nombre), así que se cuentan
# objetos distintos, no llaves. La última línea la busca la prueba.
for ident in resumen["id"]:
    print(ident)
alias = sorted(set(CORRIDAS) - set(resumen["id"]))
if alias:
    print("alias en CORRIDAS (no cuentan aparte):", ", ".join(alias))
try:
    experimentos_unicos                     # lo define la caja (s03)
except NameError:                           # respaldo si la caja es vieja
    def experimentos_unicos():
        return len({id(c) for c in CORRIDAS.values()})
print(f"EXPERIMENTOS COMPLETOS: {experimentos_unicos()}")
