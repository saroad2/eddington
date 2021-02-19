import numpy as np
import pytest
from pytest_cases import fixture, parametrize

from eddington.consts import (
    DEFAULT_MAX_COEFF,
    DEFAULT_MEASUREMENTS,
    DEFAULT_MIN_COEFF,
    DEFAULT_XMAX,
    DEFAULT_XMIN,
    DEFAULT_XSIGMA,
    DEFAULT_YSIGMA,
)
from eddington.random_util import random_array, random_data, random_error, random_sigma
from tests.dummy_functions import dummy_func1
from tests.util import assert_calls, assert_numpy_array_equal

EPSILON = 1e-5
N = 35
RETURNED = np.random.uniform(size=N)


@fixture
def uniform(mocker):
    return mocker.patch("numpy.random.uniform")


@fixture
def exponential(mocker):
    return mocker.patch("numpy.random.exponential")


@fixture
def normal(mocker):
    return mocker.patch("numpy.random.normal")


def generate_values_dict(n, measurements=DEFAULT_MEASUREMENTS):
    values = dict()
    values["a"] = np.arange(1, n + 1)
    values["x"] = np.arange(1, measurements + 1)
    values["xerr"] = np.arange(1, measurements + 1) * 0.1
    values["xerr_actual"] = np.arange(1, measurements + 1) * 0.05
    values["yerr"] = np.arange(1, measurements + 1) * 0.01
    values["yerr_actual"] = np.arange(1, measurements + 1) * 0.005
    values["y"] = (
        dummy_func1(values["a"], values["x"] + values["xerr_actual"])
        + values["yerr_actual"]  # noqa: W503
    )
    return values


def set_side_effects(uniform_mock, exponential_mock, normal_mock, values):
    uniform_mock.side_effect = [values["a"], values["x"]]
    exponential_mock.side_effect = [values["xerr"], values["yerr"]]
    normal_mock.side_effect = [values["xerr_actual"], values["yerr_actual"]]


def assert_data_values(data, values):
    assert_numpy_array_equal(data.x, values["x"], rel=EPSILON)
    assert_numpy_array_equal(data.xerr, values["xerr"], rel=EPSILON)
    assert_numpy_array_equal(data.y, values["y"], rel=EPSILON)
    assert_numpy_array_equal(data.yerr, values["yerr"], rel=EPSILON)


def assert_uniform_calls(
    mock_obj,
    n,
    min_coeff=DEFAULT_MIN_COEFF,
    max_coeff=DEFAULT_MAX_COEFF,
    xmin=DEFAULT_XMIN,
    xmax=DEFAULT_XMAX,
    measurements=DEFAULT_MEASUREMENTS,
):
    assert_calls(
        mock_obj,
        [
            ([min_coeff, max_coeff], dict(size=n)),
            ([xmin, xmax], dict(size=measurements)),
        ],
        rel=EPSILON,
    )


def assert_exponential_calls(
    mock_obj,
    xsigma=DEFAULT_XSIGMA,
    ysigma=DEFAULT_YSIGMA,
    measurements=DEFAULT_MEASUREMENTS,
):
    assert_calls(
        mock_obj,
        [([xsigma], dict(size=measurements)), ([ysigma], dict(size=measurements))],
        rel=EPSILON,
    )


def assert_normal_calls(mock_obj, xerr, yerr):
    assert_calls(
        mock_obj,
        [([], dict(scale=xerr)), ([], dict(scale=yerr))],
        rel=EPSILON,
    )


def test_random_array(uniform):
    min_val = 1
    max_val = 5
    uniform.return_value = RETURNED

    actual = random_array(min_val=min_val, max_val=max_val, size=N)

    assert actual == pytest.approx(RETURNED), "Random array returned unexpected array"
    uniform.assert_called_once_with(min_val, max_val, size=N)


def test_random_sigma(exponential):
    average_sigma = 0.5
    exponential.return_value = RETURNED

    actual = random_sigma(average_sigma=average_sigma, size=N)

    assert actual == pytest.approx(RETURNED), "Random sigma returned unexpected array"
    exponential.assert_called_once_with(average_sigma, size=N)


def test_random_error(normal):
    scales = np.arange(0, N)
    normal.return_value = RETURNED

    actual = random_error(scales=scales)

    assert actual == pytest.approx(RETURNED), "Random error returned unexpected array"
    normal.assert_called_once_with(scale=scales)


def test_random_data_defaults(uniform, exponential, normal):
    values = generate_values_dict(n=dummy_func1.n)
    set_side_effects(
        uniform_mock=uniform,
        exponential_mock=exponential,
        normal_mock=normal,
        values=values,
    )

    data = random_data(fit_func=dummy_func1)

    assert_data_values(data=data, values=values)
    assert_uniform_calls(uniform, n=dummy_func1.n)
    assert_exponential_calls(exponential)
    assert_normal_calls(normal, xerr=values["xerr"], yerr=values["yerr"])


def test_random_data_change_number_of_measurements(uniform, exponential, normal):
    measurements = 10
    values = generate_values_dict(n=dummy_func1.n, measurements=measurements)
    set_side_effects(
        uniform_mock=uniform,
        exponential_mock=exponential,
        normal_mock=normal,
        values=values,
    )

    data = random_data(fit_func=dummy_func1, measurements=measurements)

    assert_data_values(data=data, values=values)
    assert_uniform_calls(uniform, n=dummy_func1.n, measurements=measurements)
    assert_exponential_calls(exponential, measurements=measurements)
    assert_normal_calls(normal, xerr=values["xerr"], yerr=values["yerr"])


@parametrize(
    argnames="kwargs",
    argvalues=[
        dict(xmin=2),
        dict(xmax=10),
        dict(xmin=2, xmax=10),
        dict(min_coeff=-4),
        dict(max_coeff=6),
        dict(min_coeff=-4, max_coeff=6),
    ],
)
def test_random_data_with_uniform_kwargs(uniform, exponential, normal, kwargs):
    values = generate_values_dict(n=dummy_func1.n)
    set_side_effects(
        uniform_mock=uniform,
        exponential_mock=exponential,
        normal_mock=normal,
        values=values,
    )

    data = random_data(fit_func=dummy_func1, **kwargs)

    assert_data_values(data=data, values=values)
    assert_uniform_calls(uniform, n=dummy_func1.n, **kwargs)
    assert_exponential_calls(exponential)
    assert_normal_calls(normal, xerr=values["xerr"], yerr=values["yerr"])


@parametrize(
    argnames="kwargs",
    argvalues=[dict(xsigma=0.4), dict(ysigma=0.04), dict(xsigma=0.4, ysigma=0.04)],
)
def test_random_data_with_sigmas(uniform, exponential, normal, kwargs):
    values = generate_values_dict(n=dummy_func1.n)
    set_side_effects(
        uniform_mock=uniform,
        exponential_mock=exponential,
        normal_mock=normal,
        values=values,
    )

    data = random_data(fit_func=dummy_func1, **kwargs)

    assert_data_values(data=data, values=values)
    assert_uniform_calls(uniform, n=dummy_func1.n)
    assert_exponential_calls(exponential, **kwargs)
    assert_normal_calls(normal, xerr=values["xerr"], yerr=values["yerr"])


def test_random_data_with_predefined_x(uniform, exponential, normal):
    measurements = 10
    values = generate_values_dict(n=dummy_func1.n, measurements=measurements)

    uniform.side_effect = [values["a"]]
    exponential.side_effect = [values["xerr"], values["yerr"]]
    normal.side_effect = [values["xerr_actual"], values["yerr_actual"]]

    data = random_data(fit_func=dummy_func1, x=values["x"])

    assert_data_values(data=data, values=values)
    assert_calls(
        uniform,
        [
            ([DEFAULT_MIN_COEFF, DEFAULT_MAX_COEFF], dict(size=dummy_func1.n)),
        ],
        rel=EPSILON,
    )
    assert_exponential_calls(exponential, measurements=measurements)
    assert_normal_calls(normal, xerr=values["xerr"], yerr=values["yerr"])


def test_random_data_with_predefined_a(uniform, exponential, normal):
    values = generate_values_dict(n=dummy_func1.n)

    uniform.side_effect = [values["x"]]
    exponential.side_effect = [values["xerr"], values["yerr"]]
    normal.side_effect = [values["xerr_actual"], values["yerr_actual"]]

    data = random_data(fit_func=dummy_func1, a=values["a"])

    assert_data_values(data=data, values=values)
    assert_calls(
        uniform,
        [
            ([DEFAULT_XMIN, DEFAULT_XMAX], dict(size=DEFAULT_MEASUREMENTS)),
        ],
        rel=EPSILON,
    )
    assert_exponential_calls(exponential)
    assert_normal_calls(normal, xerr=values["xerr"], yerr=values["yerr"])
