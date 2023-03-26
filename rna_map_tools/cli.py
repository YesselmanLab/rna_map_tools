import click

from rna_map_tools.logger import  get_logger, setup_applevel_logger
from rna_map_tools import run

log = get_logger("CLI")

@click.group()
def cli():
    pass


@cli.command(help="download a run using bs commandline tool")
@click.argument("run_name")
@click.option(
    "-d",
    "--download-dir",
    default=None,
    help="root directory of where data should be downloaded will default to "
    "$BASESPACE",
)
def download(run_name, download_dir):
    """
    a wrapper around the bs commandline tool to download a sequencing run
    :param run_name:
    :param download_dir:
    :return:
    """
    setup_applevel_logger()
    return run.download(run_name, download_dir)


@cli.command()
@click.argument("csv")
@click.option("--debug", is_flag=True)
def demultiplex(csv, debug):
    """
    demultiplexes paired fastq files given 3' end barcodes
    """
    setup_applevel_logger(file_name="demultiplex.log")
    #return run.demultiplex(csv, debug)


@cli.command()
@click.argument("csv")
@click.argument("data_dir")
@click.argument("seq_path")
@click.option("--hide-dreem-output", is_flag=True)
def runmulti(csv, data_dir, hide_dreem_output, seq_path):
    log = setup_applevel_logger(file_name="run_multi.log")
    log.info("creating processed/ all dreem runs will go here")
    log.info("creating analysis/ all finalized analysis will go here")
    #return run.runmulti(csv, data_dir, seq_path, hide_dreem_output)


@cli.command()
@click.argument("json_file")
@click.argument("yml_file")
def parsedata(json_file, yml_file):
    setup_applevel_logger()
    #return run.parsedata(json_file, yml_file)


@cli.command()
@click.argument("pickle_file")
def replot(pickle_file):
    pass
    #return run.replot(pickle_file)


@cli.command()
@click.argument("csv")
def analysis(csv):
    setup_applevel_logger()
    #return run.analysis(csv)


if __name__ == '__main__':
    cli()
