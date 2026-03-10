import click

from clison.commands.print_json import print_json

@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-f', '--file', type=click.Path(exists=True), help="Path to JSON file")
@click.option('-p', '--path', type=click.STRING, help="JSON path to filter data")
def cli(ctx, file, path):
    """Clison"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(print_json, file=file, path=path)

cli.add_command(print_json)

if __name__ == "__main__":
    cli()