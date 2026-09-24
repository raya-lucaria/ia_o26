"""Comprueba los ajustes que sustentan las nuevas gráficas de regresión."""

import numpy as np
from numpy.polynomial import Chebyshev

import gen_regresion_experimentos as gen


def test_mae_permite_coeficientes_negativos():
    x = np.array([0., 1., 2., 3., 4.])
    y = -3. - 2. * x
    np.testing.assert_allclose(gen.mae_fit(x, y), [-3., -2.], atol=1e-9)


def test_mae_coincide_con_minimo_independiente_entre_rectas_candidatas():
    """Una solución L1 de rango dos existe en un cruce de dos residuos cero."""
    x, y, _ = gen.delivery_data()
    first, second = np.triu_indices(len(x), 1)
    slopes = (y[second] - y[first]) / (x[second] - x[first])
    intercepts = y[first] - slopes * x[first]
    losses = np.mean(np.abs(y - intercepts[:, None] - slopes[:, None] * x), axis=1)
    beta = gen.mae_fit(x, y)
    actual = np.mean(np.abs(y - beta[0] - beta[1] * x))
    np.testing.assert_allclose(actual, losses.min(), rtol=1e-9, atol=1e-9)


def test_cada_criterio_prefiere_su_ajuste_sobre_los_mismos_datos():
    x, y, _ = gen.delivery_data()
    design = np.column_stack([np.ones(len(x)), x])
    least_squares = np.linalg.lstsq(design, y, rcond=None)[0]
    least_absolute = gen.mae_fit(x, y)
    np.testing.assert_allclose(design.T @ (y - design @ least_squares), 0, atol=1e-9)
    mae = gen.score(x, y, least_absolute)
    rmse = gen.score(x, y, least_squares)
    assert mae['mae_min'] < rmse['mae_min']
    assert rmse['rmse_min'] < mae['rmse_min']


def test_mismos_modelos_estables_dentro_y_fuera_del_entrenamiento():
    for experiment in gen.family_data().values():
        x, y = experiment['x_train'], experiment['y_train']
        evaluation_x = np.r_[experiment['x_val'], experiment['x_exterior']]
        model = experiment['models'][15]
        independent, diagnostics = Chebyshev.fit(x, y, 15, full=True)
        assert diagnostics[1] == 16
        np.testing.assert_allclose(
            model(evaluation_x), independent(evaluation_x), rtol=1e-7, atol=1e-6,
        )


def test_muestras_abundantes_y_evaluaciones_en_regiones_separadas():
    for experiment in gen.family_data().values():
        x = experiment['x_train']
        left, right = experiment['spec']['domain']
        interior, exterior = experiment['x_val'], experiment['x_exterior']
        assert len(x) >= 100
        assert len(np.unique(x)) == len(x)
        assert x.min() == left and x.max() == right
        assert np.std(np.diff(np.sort(x))) > 0.01
        assert np.all((interior > left) & (interior < right))
        assert np.all((exterior < left) | (exterior > right))
        assert np.count_nonzero(exterior < left) == np.count_nonzero(exterior > right)
        # Validación son observaciones con ruido propio, no la curva exacta.
        assert np.std(experiment['y_val'] - experiment['truth'](interior)) > 0.1
        assert np.std(experiment['y_exterior'] - experiment['truth'](exterior)) > 0.1


def test_evaluar_no_reajusta_y_las_perdidas_usan_la_region_correcta():
    datasets = gen.family_data()
    coefficients = {
        name: {degree: model.coef.copy() for degree, model in data['models'].items()}
        for name, data in datasets.items()
    }
    experiments = gen.overfit_experiments(datasets)
    for name, experiment in experiments.items():
        assert experiment is datasets[name]
        errors = experiment['errors_by_degree']
        assert np.all(np.diff([r['train_rmse'] for r in errors]) <= 1e-9)
        for row in errors:
            degree = row['degree']
            model = experiment['models'][degree]
            np.testing.assert_array_equal(model.coef, coefficients[name][degree])
            for x_key, y_key, loss in [
                ('x_train', 'y_train', 'train_rmse'),
                ('x_val', 'y_val', 'validation_rmse'),
                ('x_exterior', 'y_exterior', 'exterior_rmse'),
            ]:
                residual = experiment[y_key] - model(experiment[x_key])
                np.testing.assert_allclose(row[loss], np.linalg.norm(residual) / np.sqrt(len(residual)))
