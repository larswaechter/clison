import click

from clison.commands.print_json import print_json

@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-f', '--file', type=click.Path(exists=True), help="Path to JSON file")
def cli(ctx, file):
    """Clison"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(print_json, file=file)

cli.add_command(print_json)

if __name__ == "__main__":
    cli()