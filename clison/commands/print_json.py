import click
import json
import shutil
import math
import jsonpath_ng as jp

from clison.utils import read_json, distribute_dict

COL_PADDING = 1
TOTAL_COL_PADDING = 2 * COL_PADDING

@click.command(name="print", help="Print JSON data as a formatted table")
@click.option('-f', '--file', type=click.Path(exists=True), required=True, help="Path to JSON file")
@click.option('-p', '--path', type=str, help="JSONPath expression to filter data")
def print_json(file, path):
    data = read_json(file)

    # Unwrap [[...]] -> [...]
    if isinstance(data, list) and len(data) == 1 and isinstance(data[0], list):
        data = data[0]

    # JSONPath
    if path:
        jsonpath_expr = jp.parse(path)
        matches = jsonpath_expr.find(data)
        # Flatten one level; works with match objects or raw values
        data = [item for m in matches for item in (m.value if hasattr(m, 'value') else m)]

    if isinstance(data, dict):
        data = [data]
    elif isinstance(data, list):
        if not data:
            return
    else:
        click.echo("Unsupported data format.")
        return

    # Calculate column widths
    col_widths = calculate_column_widths(data)

    # Print header
    header_row = {key: key for key in data[0].keys()}
    print_row(header_row, col_widths)
    click.echo("-" * sum(col_widths.values()))

    # Print body
    for row in data:
        print_row(row, col_widths)

def get_terminal_width():
    """Get the width of the terminal."""
    return shutil.get_terminal_size((80, 20)).columns

def calculate_column_widths(rows):
    """Calculate the width of each column based on its largest cell."""

    max_widths = {}
    for row in rows:
        for col in row:
            val = row[col]
            max_widths[col] = max(max_widths.get(col, 0), get_cell_width(col), get_cell_width(val))

    col_widths_sum = sum(max_widths.values())

    # If total width > terminal width -> redistribute
    if(col_widths_sum > get_terminal_width()):
        return distribute_dict(max_widths, get_terminal_width(), TOTAL_COL_PADDING)

    return max_widths

def print_row(row, col_widths):
    """Print a single row, handling overflow using recursion if necessary."""

    # Only white space in row, break recursion
    if all(len(str(row[col]).strip()) == 0 for col in row):
        return

    row_overflow = {}
    for col in row:
        max_width = col_widths[col]

        cell = str(row[col])
        cell_fitted = cell[:max_width - TOTAL_COL_PADDING] # Fit cell to max width, leaving space for padding

        click.echo(" " * COL_PADDING, nl=False)
        click.echo(cell_fitted, nl=False)
        click.echo(" " * (max_width - COL_PADDING - len(cell_fitted)), nl=False)

        if len(cell) > max_width:
            row_overflow[col] = cell[max_width - TOTAL_COL_PADDING:] # Store overflow for next row
        else:
            row_overflow[col] = " " * max_width # Fill with spaces to maintain alignment

    click.echo("")

    return print_row(row_overflow, col_widths)

def get_cell_width(cell):
    return len(str(cell)) + TOTAL_COL_PADDING