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


def test_el_sobreajuste_no_es_un_artefacto_de_la_base_polinomica():
    for experiment in gen.overfit_experiments().values():
        x, y = experiment['x_train'], experiment['y_train']
        validation_x, validation_y = experiment['x_val'], experiment['y_val']
        assert x.min() <= validation_x.min() < validation_x.max() <= x.max()
        model = experiment['models'][15]
        independent, diagnostics = Chebyshev.fit(x, y, 15, full=True)
        assert diagnostics[1] == 16
        np.testing.assert_allclose(model(validation_x), independent(validation_x), atol=1e-7)
        errors = experiment['errors_by_degree']
        assert np.all(np.diff([r['train_rmse'] for r in errors]) <= 1e-9)
        reference = experiment['models'][experiment['generating_degree']]
        error_reference = np.mean((reference(validation_x) - validation_y)**2)
        error_flexible = np.mean((model(validation_x) - validation_y)**2)
        assert error_flexible > error_reference
