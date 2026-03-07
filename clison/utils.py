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
