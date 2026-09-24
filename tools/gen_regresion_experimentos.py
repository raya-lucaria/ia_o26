"""Regenera seis gráficas de regresión con datos simulados y ajustes calculados.

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
from numpy.polynomial import Polynomial
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "course/6_optimizacion/_assets"
METRICS = ROOT / ".superpowers/regresion-ampliada/metrics.json"
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


def gallery() -> list[dict[str, object]]:
    rng = np.random.default_rng(672)
    families = [
        ("Lineal", "4 + 2x", lambda z: 4 + 2.0*z, [1, 2, 8], (-0.9, 0.9)),
        ("Cuadrática", "4 + 1.5x + 4x²", lambda z: 4 + 1.5*z + 4*z*z,
         [1, 2, 10], (-0.9, 0.9)),
        ("Cúbica", "4 + 2x − 2x² + 3x³", lambda z: 4 + 2*z - 2*z*z + 3*z**3,
         [1, 3, 12], (-0.9, 0.9)),
        ("Senoidal", "4 + 2sin(5x)", lambda z: 4 + 2*np.sin(5*z),
         [1, 5, 15], (-0.9, 0.9)),
        ("Recíproca", "2 + 5/x", lambda z: 2 + 5/z, [1, 4, 12], (1, 5)),
    ]
    fig, axes = plt.subplots(5, 1, figsize=(7.1, 22), layout="constrained")
    facts = []
    for ax, (name, formula, truth, degrees, domain) in zip(axes, families):
        x = np.linspace(*domain, 27)
        dense = np.linspace(*domain, 450)
        y = truth(x) + rng.normal(0, 0.17, x.size)
        ax.plot(dense, truth(dense), color=WHITE, linestyle="--", linewidth=2,
                label="Generadora")
        for degree, color in zip(degrees, [CYAN, GOLD, PINK]):
            model = Polynomial.fit(x, y, degree)
            ax.plot(dense, model(dense), color=color, linewidth=2.3,
                    label=f"Grado {degree}")
        sns.scatterplot(x=x, y=y, ax=ax, s=35, color=GREEN, edgecolor="none",
                        zorder=6, label="Muestras")
        ax.set(xlabel="Entrada x (u. a.)",
               ylabel="Salida y (u. a.)", xlim=domain)
        ax.set_title(f"{name}: tres ajustes; 27 muestras", pad=13)
        ax.legend(ncol=2, fontsize=16, facecolor=PANEL, edgecolor=GRID,
                  labelcolor=WHITE, loc="upper left")
        facts.append({"family": name, "generating_formula": formula,
                      "x_interval": list(domain), "degrees": degrees,
                      "n_samples": len(x), "noise_sd": 0.17})
    save(fig, "opt-regresion-formas.png")
    return facts


def overfit_data() -> dict[str, dict[str, object]]:
    """Dos experimentos independientes, cada uno con entrenamiento y validación."""
    rng = np.random.default_rng(8182)
    x_train = np.linspace(-1, 1, 21)
    x_val = np.linspace(-1, 1, 101)
    truths = {"linear": lambda z: 4 + 1.5*z,
              "quadratic": lambda z: 4 + 1.2*z + 2.8*z*z}
    result = {}
    for name, truth in truths.items():
        result[name] = {"x_train": x_train, "y_train": truth(x_train) + rng.normal(0, 0.28, 21),
                        "x_val": x_val, "y_val": truth(x_val) + rng.normal(0, 0.28, 101),
                        "truth": truth, "generating_degree": 1 if name == "linear" else 2}
    return result


def overfit_experiments() -> dict[str, dict[str, object]]:
    """Ajusta grados 1–16 en cada entrenamiento y mide validación independiente."""
    datasets = overfit_data()
    for experiment in datasets.values():
        x_train, y_train = experiment["x_train"], experiment["y_train"]
        x_val, y_val = experiment["x_val"], experiment["y_val"]
        models = {degree: Polynomial.fit(x_train, y_train, degree)
                  for degree in range(1, 17)}
        experiment["models"] = models
        experiment["errors_by_degree"] = [
            {"degree": degree,
             "train_rmse": float(np.sqrt(np.mean((model(x_train)-y_train)**2))),
             "validation_rmse": float(np.sqrt(np.mean((model(x_val)-y_val)**2)))}
            for degree, model in models.items()
        ]
    return datasets


def overfit() -> dict[str, object]:
    experiments = overfit_experiments()
    dense = np.linspace(-1, 1, 500)
    fig, axes = plt.subplots(2, 1, figsize=(7.1, 9.1), layout="constrained")
    for ax, (name, experiment) in zip(axes, experiments.items()):
        truth = experiment["truth"]
        x_train, y_train = experiment["x_train"], experiment["y_train"]
        x_val, y_val = experiment["x_val"], experiment["y_val"]
        models = experiment["models"]
        correct_degree = experiment["generating_degree"]
        ax.plot(dense, truth(dense), color=WHITE, linestyle="--", linewidth=2.6,
                label="Relación generadora")
        ax.scatter(x_train, y_train, color=GREEN, s=42, zorder=5,
                   label="21 entren.")
        ax.scatter(x_val[::7], y_val[::7], color=MUTED, s=24, alpha=0.65,
                   label="101 val. (muestra)")
        ax.plot(dense, models[correct_degree](dense), color=CYAN, linewidth=3,
                label=f"Ajuste grado {correct_degree}")
        ax.plot(dense, models[15](dense), color=PINK, linewidth=2.8,
                label="Ajuste grado 15")
        ax.set(xlim=(-1, 1), xlabel="Entrada x (u. a.)",
               ylabel="Salida y (u. a.)")
        ax.set_title(("Relación lineal" if name == "linear" else "Relación cuadrática")
                     + ": grado correcto y grado 15", pad=13)
        ax.legend(loc="upper left", fontsize=15, ncol=2, facecolor=PANEL,
                  edgecolor=GRID, labelcolor=WHITE)
    save(fig, "opt-regresion-sobreajuste.png")

    fig, axes = plt.subplots(2, 1, figsize=(7.1, 9.1), layout="constrained")
    for ax, (name, experiment) in zip(axes, experiments.items()):
        rows = experiment["errors_by_degree"]
        ax.plot([r["degree"] for r in rows], [r["train_rmse"] for r in rows],
                color=CYAN, marker="o", label="Entrenamiento")
        ax.plot([r["degree"] for r in rows], [r["validation_rmse"] for r in rows],
                color=PINK, marker="o", label="Validación independiente")
        degree = experiment["generating_degree"]
        ax.axvline(degree, color=GOLD, linestyle="--", linewidth=2,
                   label=f"Grado generador: {degree}")
        ax.set(xlabel="Grado del polinomio (entero)", ylabel="RMSE (u. a.)",
               xlim=(0.5, 16.5), xticks=list(range(1, 17, 2)))
        ax.set_title(("Datos lineales" if name == "linear" else "Datos cuadráticos")
                     + ": entrenamiento y validación", pad=14)
        ax.legend(facecolor=PANEL, edgecolor=GRID, labelcolor=WHITE, fontsize=16)
    save(fig, "opt-regresion-validacion.png")
    formulas = {"linear": "4 + 1.5x", "quadratic": "4 + 1.2x + 2.8x²"}
    return {name: {"n_train": 21, "n_validation": 101,
                   "generating_formula": formulas[name], "x_interval": [-1, 1],
                   "generating_degree": exp["generating_degree"],
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
    families = gallery()
    overfit_metrics = overfit()
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
        "overfit": {"seed": 8182, "noise_sd": 0.28, "experiments": overfit_metrics},
    }
    METRICS.parent.mkdir(parents=True, exist_ok=True)
    METRICS.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
    print(f"Seis gráficas y métricas: {METRICS}")


if __name__ == "__main__":
    main()
