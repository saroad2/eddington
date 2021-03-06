from pytest_cases import parametrize_with_cases

from tests.plot_legacy import cases
from tests.util import assert_calls

EPSILON = 1e-5


@parametrize_with_cases(
    argnames="base_dict, plot_method", cases=[cases.case_plot_residuals]
)
def test_plot_residuals_without_boundaries(base_dict, plot_method, mock_figure):
    fig = plot_method(**base_dict)
    assert (
        fig._raw_figure == mock_figure  # pylint: disable=protected-access
    ), "Figure is different than expected"
    ax = mock_figure.add_subplot.return_value
    assert_calls(
        ax.hlines, [([0], dict(xmin=0.1, xmax=10.9, linestyles="dashed"))], rel=EPSILON
    )
    data = base_dict["data"]
    y_residuals = data.y - cases.FUNC(cases.A, data.x)
    assert_calls(
        ax.errorbar,
        [
            (
                [],
                dict(
                    x=data.x,
                    y=y_residuals,
                    xerr=data.xerr,
                    yerr=data.yerr,
                    markersize=1,
                    marker="o",
                    linestyle="None",
                    label=None,
                    ecolor=None,
                    mec=None,
                ),
            ),
        ],
        rel=EPSILON,
    )


@parametrize_with_cases(
    argnames="base_dict, plot_method", cases=[cases.case_plot_residuals]
)
def test_plot_residuals_with_xmin(base_dict, plot_method, mock_figure):
    xmin = 4
    fig = plot_method(**base_dict, xmin=xmin)
    assert (
        fig._raw_figure == mock_figure  # pylint: disable=protected-access
    ), "Figure is different than expected"
    ax = mock_figure.add_subplot.return_value
    assert_calls(
        ax.hlines, [([0], dict(xmin=xmin, xmax=10.9, linestyles="dashed"))], rel=EPSILON
    )
    data = base_dict["data"]
    y_residuals = data.y - cases.FUNC(cases.A, data.x)
    data_filter = [val >= xmin for val in data.x]
    assert_calls(
        mock_figure.add_subplot.return_value.errorbar,
        [
            (
                [],
                dict(
                    x=data.x[data_filter],
                    y=y_residuals[data_filter],
                    xerr=data.xerr[data_filter],
                    yerr=data.yerr[data_filter],
                    markersize=1,
                    marker="o",
                    linestyle="None",
                    label=None,
                    ecolor=None,
                    mec=None,
                ),
            ),
        ],
        rel=EPSILON,
    )


@parametrize_with_cases(
    argnames="base_dict, plot_method", cases=[cases.case_plot_residuals]
)
def test_plot_residuals_with_xmax(base_dict, plot_method, mock_figure):
    xmax = 7
    fig = plot_method(**base_dict, xmax=xmax)
    assert (
        fig._raw_figure == mock_figure  # pylint: disable=protected-access
    ), "Figure is different than expected"
    ax = mock_figure.add_subplot.return_value
    assert_calls(
        ax.hlines, [([0], dict(xmin=0.1, xmax=xmax, linestyles="dashed"))], rel=EPSILON
    )
    data = base_dict["data"]
    y_residuals = data.y - cases.FUNC(cases.A, data.x)
    data_filter = [val <= xmax for val in data.x]
    assert_calls(
        mock_figure.add_subplot.return_value.errorbar,
        [
            (
                [],
                dict(
                    x=data.x[data_filter],
                    y=y_residuals[data_filter],
                    xerr=data.xerr[data_filter],
                    yerr=data.yerr[data_filter],
                    markersize=1,
                    marker="o",
                    linestyle="None",
                    label=None,
                    ecolor=None,
                    mec=None,
                ),
            ),
        ],
        rel=EPSILON,
    )


@parametrize_with_cases(
    argnames="base_dict, plot_method", cases=[cases.case_plot_residuals]
)
def test_plot_residuals_with_color(base_dict, plot_method, mock_figure):
    color = "blue"
    fig = plot_method(**base_dict, color=color)
    assert (
        fig._raw_figure == mock_figure  # pylint: disable=protected-access
    ), "Figure is different than expected"
    ax = mock_figure.add_subplot.return_value
    assert_calls(
        ax.hlines, [([0], dict(xmin=0.1, xmax=10.9, linestyles="dashed"))], rel=EPSILON
    )
    data = base_dict["data"]
    y_residuals = data.y - cases.FUNC(cases.A, data.x)
    assert_calls(
        mock_figure.add_subplot.return_value.errorbar,
        [
            (
                [],
                dict(
                    x=data.x,
                    y=y_residuals,
                    xerr=data.xerr,
                    yerr=data.yerr,
                    markersize=1,
                    marker="o",
                    linestyle="None",
                    label=None,
                    ecolor=color,
                    mec=color,
                ),
            ),
        ],
        rel=EPSILON,
    )
