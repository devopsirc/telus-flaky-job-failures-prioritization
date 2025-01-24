"""FlakeRanker CLI tool module."""

import os
import click

from src.flakeranker import labeler, analyzer


@click.group(invoke_without_command=False)
@click.pass_context
def cli(ctx):
    """FlakeRanker CLI tool."""
    if not ctx.invoked_subcommand:
        print("FlakeRanker Hello World!")
    else:
        pass


@cli.command(help="Run the complete FlakeRanker pipeline")
@click.argument(
    "input_file", type=click.Path(exists=True, dir_okay=False, readable=True)
)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(exists=True, file_okay=False, writable=True),
    required=True,
)
def run(input: str, output: str):
    label()
    analyze()
    rank()


@cli.command()
@click.argument(
    "input_file", type=click.Path(exists=True, dir_okay=False, readable=True)
)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(exists=True, file_okay=False, writable=True),
    required=True,
)
def label(input_file: str, output_dir: str):
    """Label an INPUT_FILE .csv dataset of build jobs having required columns:
    `id`, `name`, `status`, `failure_reason`, `commit`, `created_at`, `finished_at`, `duration`, `logs`, `project`
    """
    click.echo("Labeling...")
    input_file_base_name = os.path.basename(input_file)
    output_file_path = os.path.join(output_dir, f"labeled_{input_file_base_name}")
    labeler.label(input_file, output_file_path)


@cli.command()
@click.argument(
    "input_file", type=click.Path(exists=True, dir_okay=False, readable=True)
)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(exists=True, file_okay=False, writable=True),
    required=True,
)
def analyze(input_file: str, output_dir: str):
    """Analyze an INPUT_FILE labeled dataset of build jobs, output from the label sub-command."""
    click.echo("Analyzing...")
    output_file_path = os.path.join(output_dir, "rfm.csv")
    analyzer.analyze(input_file, output_file_path)


@cli.command(help="Rank flaky job failure categories with RFM patterns.")
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(exists=True, file_okay=False, writable=True),
    required=True,
)
def rank():
    click.echo("Ranking...")


if __name__ == "__main__":
    cli()
