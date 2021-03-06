import numpy as np

from eddington import linear, plot_data, plot_fitting, plot_residuals
from eddington.random_util import random_data

FUNC = linear
X = np.arange(1, 11)
A = np.array([1, 2])
TITLE_NAME = "Title"


def case_plot_data():
    fit_data = random_data(FUNC, x=X, a=A, measurements=X.shape[0])
    return dict(data=fit_data, title_name=TITLE_NAME), plot_data


def case_plot_fitting():
    fit_data = random_data(FUNC, x=X, a=A, measurements=X.shape[0])
    return dict(func=FUNC, data=fit_data, a=A, title_name=TITLE_NAME), plot_fitting


def case_plot_residuals():
    fit_data = random_data(FUNC, x=X, a=A, measurements=X.shape[0])
    return dict(func=FUNC, data=fit_data, a=A, title_name=TITLE_NAME), plot_residuals
