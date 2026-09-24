"""Regenera gráficas de regresión con datos simulados y ajustes calculados.

Ejecutar desde cualquier directorio: python3 tools/gen_regresion_experimentos.py
Requiere numpy, scipy, matplotlib y seaborn (requirements-regresion.txt).
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from numpy.polynomial import Polynomial
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "course/6_optimizacion/_assets"
METRICS = ROOT / ".superpowers/polinomios-extrapolacion/metrics.json"
BG = "#211033"
PANEL = "#2e1945"
WHITE = "#fff8ed"
MUTED = "#dfd0e8"
GRID = "#665075"
CYAN = "#64dce3"
GOLD = "#ffd166"
PINK = "#ff87ad"
GREEN = "#a9e88f"


def style() -> None:
    sns.set_theme(style="darkgrid")
    plt.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": PANEL, "savefig.facecolor": BG,
        "text.color": WHITE, "axes.labelcolor": WHITE, "axes.edgecolor": MUTED,
        "xtick.color": MUTED, "ytick.color": MUTED, "grid.color": GRID,
        "font.family": "DejaVu Sans", "font.size": 17, "axes.labelsize": 19,
        "axes.titlesize": 20, "xtick.labelsize": 16, "ytick.labelsize": 16,
        "legend.fontsize": 16, "lines.linewidth": 2.8,
    })


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(ASSETS / name, dpi=130, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)


def delivery_data() -> tuple[np.ndarray, np.ndarray, list[int]]:
    rng = np.random.default_rng(20260924)
    x = np.linspace(0.7, 12.0, 101) + rng.uniform(-0.20, 0.20, 101)
    x.sort()
    y = 10.0 + 3.2 * x + rng.normal(0, 2.4, len(x))
    outliers = [63, 69, 75, 81, 87, 93, 99]
    y[outliers] += 25.0
    return x, y, outliers


def mae_fit(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Minimiza la suma de valores absolutos mediante programación lineal."""
    n = len(x)
    objective = np.r_[np.zeros(2), np.ones(n)]
    design = np.column_stack((np.ones(n), x))
    matrix = np.vstack((np.column_stack((design, -np.eye(n))),
                        np.column_stack((-design, -np.eye(n)))))
    bounds = [(None, None), (None, None)] + [(0, None)] * n
    result = linprog(objective, A_ub=matrix, b_ub=np.r_[y, -y],
                     bounds=bounds, method="highs")
    if not result.success:
        raise RuntimeError(f"No se pudo ajustar MAE: {result.message}")
    return result.x[:2]


def score(x: np.ndarray, y: np.ndarray, beta: np.ndarray) -> dict[str, float]:
    residual = y - (beta[0] + beta[1] * x)
    return {"mae_min": float(np.mean(np.abs(residual))),
            "rmse_min": float(np.sqrt(np.mean(residual**2)))}


def axes_delivery(ax: plt.Axes, x: np.ndarray, y: np.ndarray) -> None:
    sns.scatterplot(x=x, y=y, ax=ax, s=32, color=CYAN, edgecolor="none", alpha=0.85)
    ax.set(xlim=(0, 13), ylim=(0, 85), xlabel="Distancia x (km)",
           ylabel="Tiempo de entrega y (min)")
    ax.grid(alpha=0.35)


def plot_delivery(x: np.ndarray, y: np.ndarray, outliers: list[int]) -> None:
    fig, ax = plt.subplots(figsize=(7.1, 5.1), layout="constrained")
    axes_delivery(ax, x, y)
    ax.scatter(x[outliers], y[outliers], s=100, facecolors="none",
               edgecolors=PINK, linewidths=2.3, label="Casos atípicos simulados")
    ax.legend(loc="upper left", facecolor=PANEL, edgecolor=GRID, labelcolor=WHITE)
    ax.set_title("101 entregas simuladas: distancia y tiempo", pad=15)
    save(fig, "opt-regresion-datos.png")


def plot_fits(x: np.ndarray, y: np.ndarray, fits: dict[str, np.ndarray]) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(7.1, 9.3), sharex=True, sharey=True,
                             layout="constrained")
    xline = np.linspace(0, 13, 250)
    for ax, (label, beta), color in zip(axes, fits.items(), [GOLD, PINK]):
        axes_delivery(ax, x, y)
        ax.plot(xline, beta[0] + beta[1] * xline, color=color, linewidth=3.5)
        metric = score(x, y, beta)
        ax.set_title(f"Ajuste por {label}: β₀={beta[0]:.2f}, β₁={beta[1]:.2f}", pad=13)
        ax.text(0.04, 0.94, f"MAE {metric['mae_min']:.2f} min  ·  RMSE {metric['rmse_min']:.2f} min",
                transform=ax.transAxes, va="top", color=WHITE, fontsize=16,
                bbox={"facecolor": BG, "edgecolor": GRID, "boxstyle": "round,pad=0.5"})
    fig.suptitle("Dos criterios; mismos datos y ejes", fontsize=20)
    save(fig, "opt-regresion-ajustes.png")


def plot_slope_slice(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    intercept = 10.0
    slopes = np.linspace(2.0, 5.0, 500)
    mae = np.mean(np.abs(y[:, None] - intercept - x[:, None] * slopes), axis=0)
    rmse = np.sqrt(np.mean((y[:, None] - intercept - x[:, None] * slopes)**2, axis=0))
    # Weighted median is an exact minimizer of sum_i x_i |slope - (y_i-b0)/x_i|.
    breakpoints = (y - intercept) / x
    order = np.argsort(breakpoints)
    slope_mae = float(breakpoints[order[np.searchsorted(np.cumsum(x[order]), x.sum()/2)]])
    slope_rmse = float(np.sum(x * (y - intercept)) / np.sum(x*x))
    fig, ax = plt.subplots(figsize=(7.1, 5.1), layout="constrained")
    ax.plot(slopes, mae, color=GOLD, label="MAE (min)")
    ax.plot(slopes, rmse, color=PINK, label="RMSE (min)")
    for slope, loss, color, label in [(slope_mae, np.mean(np.abs(y-intercept-slope_mae*x)),
                                      GOLD, "mín. MAE"),
                                     (slope_rmse, np.sqrt(np.mean((y-intercept-slope_rmse*x)**2)),
                                      PINK, "mín. RMSE")]:
        ax.scatter([slope], [loss], color=color, edgecolor=BG, linewidth=1, s=130,
                   zorder=5, label=f"{label}: {slope:.2f}")
    ax.set(xlabel="Pendiente β₁ (min/km), con β₀ = 10 min fijo",
           ylabel="Pérdida (min)", xlim=(2, 5))
    ax.set_title("Cambiar solo la pendiente: corte del problema", pad=14)
    ax.legend(loc="upper right", facecolor=PANEL, edgecolor=GRID, labelcolor=WHITE,
              ncol=2, fontsize=16)
    save(fig, "opt-regresion-pendiente.png")
    return {"beta0_fixed_min": intercept, "mae_slice_beta1": slope_mae,
            "rmse_slice_beta1": slope_rmse,
            "mae_slice_min": float(np.mean(np.abs(y-intercept-slope_mae*x))),
            "rmse_slice_min": float(np.sqrt(np.mean((y-intercept-slope_rmse*x)**2)))}


FAMILIES = {
    "linear": {"label": "Lineal", "file": "lineal", "formula": "4 + 2x",
               "truth": lambda z: 4 + 2*z, "degrees": [1, 2, 15],
               "domain": (-1, 1), "extended": (-1.5, 1.5), "seed": 672},
    "quadratic": {"label": "Cuadrática", "file": "cuadratica",
                  "formula": "4 + 1.5x + 4x²", "truth": lambda z: 4 + 1.5*z + 4*z*z,
                  "degrees": [1, 2, 15], "domain": (-1, 1),
                  "extended": (-1.5, 1.5), "seed": 673},
    "cubic": {"label": "Cúbica", "file": "cubica",
              "formula": "4 + 2x − 2x² + 3x³",
              "truth": lambda z: 4 + 2*z - 2*z*z + 3*z**3,
              "degrees": [1, 3, 15], "domain": (-1, 1),
              "extended": (-1.5, 1.5), "seed": 674},
    "sinusoidal": {"label": "Senoidal", "file": "senoidal",
                   "formula": "4 + 2sin(5x)", "truth": lambda z: 4 + 2*np.sin(5*z),
                   "degrees": [1, 5, 15], "domain": (-1, 1),
                   "extended": (-1.5, 1.5), "seed": 675},
    "reciprocal": {"label": "Recíproca", "file": "reciproca",
                   "formula": "2 + 5/x", "truth": lambda z: 2 + 5/z,
                   "degrees": [1, 4, 15], "domain": (1, 5),
                   "extended": (0.5, 6), "seed": 676},
}
NOISE_SD = 0.4
N_TRAIN = 120
N_VALIDATION = 300
SUPERSCRIPT = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def family_data() -> dict[str, dict[str, object]]:
    """Datos fijos; los extremos observados son parte del entrenamiento."""
    result = {}
    for key, spec in FAMILIES.items():
        rng = np.random.default_rng(spec["seed"])
        left, right = spec["domain"]
        outer_left, outer_right = spec["extended"]
        x = np.r_[left, np.sort(rng.uniform(left, right, N_TRAIN - 2)), right]
        truth = spec["truth"]
        y = truth(x) + rng.normal(0, NOISE_SD, N_TRAIN)
        models = {degree: Polynomial.fit(x, y, degree)
                  for degree in range(1, 17)}
        x_val = rng.uniform(left, right, N_VALIDATION)
        y_val = truth(x_val) + rng.normal(0, NOISE_SD, N_VALIDATION)
        x_ext = np.r_[rng.uniform(outer_left, left, N_VALIDATION // 2),
                      rng.uniform(right, outer_right, N_VALIDATION // 2)]
        y_ext = truth(x_ext) + rng.normal(0, NOISE_SD, N_VALIDATION)
        result[key] = {"x_train": x, "y_train": y,
                       "x_val": x_val, "y_val": y_val,
                       "x_exterior": x_ext, "y_exterior": y_ext,
                       "x_ext": x_ext, "y_ext": y_ext,
                       "models": models, "truth": truth, "spec": spec,
                       "generating_degree": {"linear": 1, "quadratic": 2}.get(key)}
    return result


def _axis_number(value: float, _position: float) -> str:
    if value == 0:
        return "0"
    if abs(value) >= 1000:
        return f"{value:.1e}"
    return f"{value:g}"


def gallery(datasets: dict[str, dict[str, object]] | None = None) -> list[dict[str, object]]:
    """Cinco pares de vistas: cada modelo se ajusta una sola vez."""
    datasets = family_data() if datasets is None else datasets
    facts = []
    for key, experiment in datasets.items():
        spec = experiment["spec"]
        left, right = spec["domain"]
        outer_left, outer_right = spec["extended"]
        fig, axes = plt.subplots(2, 1, figsize=(6.0, 14.0))
        fig.subplots_adjust(left=0.17, right=0.97, top=0.93, bottom=0.14, hspace=0.30)
        for index, (ax, interval) in enumerate(zip(axes, [spec["domain"], spec["extended"]])):
            dense = np.linspace(*interval, 750)
            curves = [experiment["truth"](dense)] + [
                experiment["models"][degree](dense) for degree in spec["degrees"]]
            if index == 1:
                ax.axvspan(left, right, color=CYAN, alpha=0.09, zorder=0)
                ax.axvline(left, color=MUTED, linestyle=":", linewidth=2)
                ax.axvline(right, color=MUTED, linestyle=":", linewidth=2)
            ax.plot(dense, curves[0], color=WHITE,
                    linestyle="--", linewidth=2.4, label="Generadora")
            for degree, color, values in zip(spec["degrees"], [CYAN, GOLD, PINK], curves[1:]):
                ax.plot(dense, values, color=color,
                        linewidth=2.5, label=f"Grado {degree}")
            sns.scatterplot(x=experiment["x_train"], y=experiment["y_train"],
                            ax=ax, s=35, color=GREEN, edgecolor="none", alpha=0.75,
                            zorder=6, label="Datos (120)", legend=False)
            ax.set(xlim=interval, xlabel="x (u. a.)", ylabel="y (u. a.)")
            max_abs = max(float(np.max(np.abs(values))) for values in curves)
            if max_abs >= 1000:
                exponent = int(np.floor(np.log10(max_abs)))
                ax.yaxis.set_major_formatter(FuncFormatter(
                    lambda value, _position, scale=10**exponent: f"{value/scale:g}"))
                ax.set_ylabel(f"y (u. a.; ×10{str(exponent).translate(SUPERSCRIPT)})")
            else:
                ax.yaxis.set_major_formatter(FuncFormatter(_axis_number))
            ax.set_title("Intervalo observado" if index == 0 else
                         "Intervalo ampliado", fontsize=19, pad=10)
            if index == 1:
                width = outer_right - outer_left
                for center in ((outer_left + left) / 2, (right + outer_right) / 2):
                    ax.text((center - outer_left) / width, 0.75, "Extrapolación",
                            rotation=90, transform=ax.transAxes, va="center",
                            ha="center", color=MUTED, fontsize=15,
                            bbox={"facecolor": PANEL, "edgecolor": "none", "pad": 1.5})
                ax.text(((left + right) / 2 - outer_left) / width,
                        0.72 if key == "reciprocal" else 0.96,
                        "Observado", transform=ax.transAxes, va="top",
                        ha="center", color=CYAN, fontsize=15)
            ax.grid(alpha=0.3)
        fig.suptitle(f"Relación {spec['label'].lower()}: mismos ajustes", fontsize=20)
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 0.005),
                   ncol=2, facecolor=PANEL, edgecolor=GRID, labelcolor=WHITE,
                   fontsize=17, frameon=True)
        save(fig, f"opt-regresion-forma-{spec['file']}.png")
        facts.append({"family": spec["label"], "key": key,
                      "generating_formula": spec["formula"],
                      "x_interval": list(spec["domain"]),
                      "extended_interval": list(spec["extended"]),
                      "degrees": spec["degrees"], "n_samples": N_TRAIN,
                      "noise_sd": NOISE_SD, "seed": spec["seed"]})
    return facts


def overfit_data(datasets: dict[str, dict[str, object]] | None = None) -> dict[str, dict[str, object]]:
    """Comparación con los mismos datos lineales y cuadráticos de la galería."""
    datasets = family_data() if datasets is None else datasets
    return {name: datasets[name] for name in ("linear", "quadratic")}


def overfit_experiments(datasets: dict[str, dict[str, object]] | None = None) -> dict[str, dict[str, object]]:
    """Mide entrenamiento, validación interior y prueba exterior independientes."""
    datasets = overfit_data(datasets)
    for experiment in datasets.values():
        x_train, y_train = experiment["x_train"], experiment["y_train"]
        x_val, y_val = experiment["x_val"], experiment["y_val"]
        x_ext, y_ext = experiment["x_exterior"], experiment["y_exterior"]
        models = experiment["models"]
        experiment["errors_by_degree"] = [
            {"degree": degree,
             "train_rmse": float(np.sqrt(np.mean((model(x_train)-y_train)**2))),
             "validation_rmse": float(np.sqrt(np.mean((model(x_val)-y_val)**2))),
             "exterior_rmse": float(np.sqrt(np.mean((model(x_ext)-y_ext)**2)))}
            for degree, model in models.items()
        ]
    return datasets


def overfit(datasets: dict[str, dict[str, object]] | None = None) -> dict[str, object]:
    experiments = overfit_experiments(datasets)
    fig, axes = plt.subplots(2, 1, figsize=(6.0, 10.0))
    fig.subplots_adjust(left=0.18, right=0.97, top=0.94, bottom=0.22, hspace=0.38)
    for ax, (name, experiment) in zip(axes, experiments.items()):
        rows = experiment["errors_by_degree"]
        ax.plot([r["degree"] for r in rows], [r["train_rmse"] for r in rows],
                color=CYAN, marker="o", label="Entrenamiento")
        ax.plot([r["degree"] for r in rows], [r["validation_rmse"] for r in rows],
                color=PINK, marker="o", label="Validación independiente")
        degree = experiment["generating_degree"]
        ax.axvline(degree, color=GOLD, linestyle="--", linewidth=2,
                   label="Grado generador")
        ax.set(xlabel="Grado del polinomio", ylabel="RMSE (u. a.)",
               xlim=(0.5, 16.5), xticks=list(range(1, 17, 2)))
        ax.set_title("Datos lineales" if name == "linear" else "Datos cuadráticos", pad=14)
        ax.grid(alpha=0.3)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 0.005),
               ncol=1, facecolor=PANEL, edgecolor=GRID, labelcolor=WHITE, fontsize=15)
    save(fig, "opt-regresion-validacion.png")
    return {name: {"n_train": N_TRAIN, "n_validation": N_VALIDATION,
                   "n_exterior": N_VALIDATION,
                   "n_exterior_each_side": N_VALIDATION // 2,
                   "noise_distribution": "normal", "noise_sd": NOISE_SD,
                   "generating_formula": exp["spec"]["formula"],
                   "x_interval": list(exp["spec"]["domain"]),
                   "exterior_interval": list(exp["spec"]["extended"]),
                   "generating_degree": exp["generating_degree"],
                   "best_validation_degree": min(exp["errors_by_degree"],
                                                   key=lambda row: row["validation_rmse"])["degree"],
                   "errors_by_degree": exp["errors_by_degree"]}
            for name, exp in experiments.items()}


def main() -> None:
    style()
    ASSETS.mkdir(parents=True, exist_ok=True)
    x, y, outliers = delivery_data()
    design = np.column_stack((np.ones(len(x)), x))
    fits = {"MAE": mae_fit(x, y), "RMSE": np.linalg.lstsq(design, y, rcond=None)[0]}
    plot_delivery(x, y, outliers)
    plot_fits(x, y, fits)
    slope = plot_slope_slice(x, y)
    datasets = family_data()
    families = gallery(datasets)
    overfit_metrics = overfit(datasets)
    manifest = {
        "source": "Datos simulados; semilla fija. Ajustes calculados, no observaciones reales.",
        "delivery": {"n": len(x), "seed": 20260924, "outlier_indices_zero_based": outliers,
                     "first_three_rows": [{"distance_km": float(a), "time_min": float(b)}
                                          for a, b in zip(x[:3], y[:3])],
                     "fits": {name: {"beta0_min": float(beta[0]),
                                      "beta1_min_per_km": float(beta[1]),
                                      **score(x, y, beta)} for name, beta in fits.items()},
                     "slope_slice": slope},
        "form_gallery": families,
        "overfit": {"noise_sd": NOISE_SD, "experiments": overfit_metrics},
    }
    METRICS.parent.mkdir(parents=True, exist_ok=True)
    METRICS.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
    print(f"Nueve gráficas y métricas: {METRICS}")


if __name__ == "__main__":
    main()
