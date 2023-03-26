"""

"""
import os
import shutil
import glob

from rna_map_tools.logger import get_logger
from rna_map_tools.fastq import get_paired_fastqs

log = get_logger("RUN")


def does_program_exist(prog_name: str) -> bool:
    """
    Check if a program exists
    :prog_name: name of the program
    """
    if shutil.which(prog_name) is None:
        return False
    else:
        return True


def download(run_name, download_dir, params):
    """
    Download a run from basespace
    :param run_name:
    :param download_dir:
    :return:
    """
    # check that bs program exists before starting
    if not does_program_exist("bs"):
        log.error("cannot find program 'bs', please install it")
        exit()
    # if download_dir is not set assume we are using $BASESPACE
    if download_dir is None:
        log.info("-d/--dir was not suppled will use $BASESPACE")
        if os.getenv("BASESPACE") is None:
            log.error("$BASESPACE is not set! set it or use -d/--dir")
        log.info("$BASESPACE -> " + os.getenv("BASESPACE"))
        download_dir = os.getenv("BASESPACE")
    os.chdir(download_dir)
    log.debug(f"download_dir: {download_dir}")
    if os.path.exists(run_name):
        log.error(f"directory {run_name} already exists")
        exit()
    os.makedirs(run_name)
    os.chdir(run_name)
    log.info(f"running: `bs download project --name {run_name}`")
    # do not use subprocess here because then we cant see progress
    os.system(
        f"bs download project --name {run_name}",
    )
    # get the only directory in the current directory with other files
    current_dir = os.getcwd()
    dirs = [
        d
        for d in os.listdir(current_dir)
        if os.path.isdir(os.path.join(current_dir, d))
    ]
    if len(dirs) != 1:
        raise Exception("Expected only one directory in the current directory")
    if params["rename_dir"]:
        log.info(f"renaming {dirs[0]} to {params['dir_name']}")
        shutil.move(dirs[0], params["dir_name"])
        fpath = os.path.join(current_dir, params["dir_name"])
    else:
        fpath = os.path.join(current_dir, dirs[0])
    return get_paired_fastqs(fpath)
