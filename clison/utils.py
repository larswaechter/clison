import click
import sys
import json

def read_json(file_path):
    """
    Read JSON data from a file or stdin.
    """
    try:
        if  file_path:
            with open(file_path, 'r') as f:
                return json.load(f)
        else:
            # Read from stdin
            return json.load(sys.stdin)
    except json.JSONDecodeError as e:
        click.echo(f"Invalid JSON: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

def distribute_dict(dictionary, X, k_padding):
    """Distribute values in a dict proportionally to fit within X, with a minimum padding."""

    mins = {k: len(k) + k_padding for k in dictionary}
    min_total = sum(mins.values())

    if min_total > X:
        raise ValueError("Impossible")

    remaining = X - min_total
    orig_sum = sum(dictionary.values())

    # proportional shares
    shares = {k: remaining * dictionary[k] / orig_sum for k in dictionary}

    # floor allocation
    result = {k: mins[k] + int(shares[k]) for k in dictionary}

    # compute leftover due to flooring
    left = X - sum(result.values())

    # sort by largest fractional remainder
    remainders = sorted(dictionary.keys(), key=lambda k: shares[k] % 1, reverse=True)

    for k in remainders[:left]:
        result[k] += 1

    return result