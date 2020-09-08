import re
from pathlib import Path
from typing import Optional

from prettytable import PrettyTable

from eddington import __version__, FitFunctionsRegistry, FitData, fit_to_data

import click


@click.group("eddington")
@click.version_option(version=__version__)
def eddington_cli():
    """Command line for Eddington."""


@eddington_cli.command("list")
@click.option(
    "-r",
    "--regex",
    type=str,
    default=None,
    help="Filter functions by a regular expression",
)
def eddington_list(regex: Optional[str]):
    """Prints all fit functions in a pretty table."""
    table = PrettyTable(field_names=["Function", "Syntax"])
    for func in FitFunctionsRegistry.all():
        if regex is None or re.search(regex, func.name):
            table.add_row([func.signature, func.syntax])
    click.echo(table)


@eddington_cli.command("fit")
@click.pass_context
@click.argument("fit_func", type=str, default="linear")
@click.option(
    "-d",
    "--data-file",
    required=True,
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    help="Data file to read from.",
)
@click.option("-s", "--sheet", type=str, help="Sheet name for excel files.")
def eddington_fit(
    ctx: click.Context, fit_func: Optional[str], data_file: str, sheet: Optional[str]
):
    """Fit data file according to a fitting function."""
    data = __load_data_file(ctx, Path(data_file), sheet)
    func = FitFunctionsRegistry.load(fit_func)
    result = fit_to_data(data, func)
    click.echo(result.pretty_string)


def __load_data_file(ctx: click.Context, data_file: Path, sheet: Optional[str]):
    suffix = data_file.suffix
    if suffix == ".csv":
        return FitData.read_from_csv(filepath=data_file)
    if suffix == ".json":
        return FitData.read_from_json(filepath=data_file)
    if suffix != ".xlsx":
        click.echo(f'Cannot read data with "{suffix}" suffix')
        ctx.exit(1)
    if sheet is None:
        click.echo(f"Sheet name has not been specified!")
        ctx.exit(1)
    return FitData.read_from_excel(filepath=data_file, sheet=sheet)
