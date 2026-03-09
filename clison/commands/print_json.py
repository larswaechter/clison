import click
import json
import shutil

from clison.utils import read_json

COL_PADDING = 2
TOTAL_COL_PADDING = 2 * COL_PADDING

@click.command(name="print")
@click.option('-f', '--file', type=click.Path(exists=True), help="Path to JSON file")
def print_json(file):
    data = read_json(file)

    if isinstance(data, dict):
        data = [data] # Convert to list for uniform processing
    elif isinstance(data, list):
        if(len(data) == 0):
            return

    col_widths = calculate_column_widths(data)

    # Print header
    header_row = dict(zip(data[0].keys(), data[0].keys()))
    print_row(header_row, col_widths)
    click.echo("-" * sum(col_widths.values()))

    # Print body
    for row in data:
        print_row(row, col_widths)

def get_terminal_width():
    """Get the width of the terminal."""
    # return 40
    return shutil.get_terminal_size((80, 20)).columns

def calculate_column_widths(rows):
    """Calculate the width of each column based on its largest cell."""

    max_widths = {}
    for row in rows:
        for col in row:
            val = row[col]
            max_widths[col] = max(max_widths.get(col, 0), get_cell_width(col), get_cell_width(val))

    col_widths_sum = sum(max_widths.values())

    # If total width > terminal width, scale down terminal width
    if(col_widths_sum > get_terminal_width()):
        new_max_widths = {}
        for col, width in max_widths.items():
            new_width = int(width / col_widths_sum * get_terminal_width())
            new_max_widths[col] = new_width
        return new_max_widths

    return max_widths

def print_row(row, col_widths):

    # Only white space in row, break recursion
    if all(len(str(row[col]).strip()) == 0 for col in row):
        return

    overflow_row = {}

    for col in row:
        max_width = col_widths[col]

        cell = str(row[col])
        cell_compressed = cell[:max_width - COL_PADDING]

        click.echo(" " * COL_PADDING, nl=False)
        click.echo(cell_compressed, nl=False)
        click.echo(" " * (max_width - COL_PADDING - len(cell_compressed)), nl=False)

        if len(cell) > max_width:
            overflow_row[col] = cell[max_width:] # Store overflow for next row
        else:
            overflow_row[col] = " " * max_width # Fill with spaces to maintain alignment

    click.echo("")

    return print_row(overflow_row, col_widths)

def get_cell_width(cell):
    return len(str(cell)) + TOTAL_COL_PADDING