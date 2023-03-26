"""
test demultiplex module
"""
import os
import shutil
import pandas as pd
import yaml

from rna_map_tools.fastq import get_paired_fastqs
from rna_map_tools.tools.demultiplex import (
    NovobarcodeDemultiplexer,
    SabreDemultiplexer,
)
from rna_map_tools.parameters import PY_DIR

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def load_default_params():
    path = PY_DIR + "/resources/default.yml"
    with open(path) as f:
        params = yaml.safe_load(f)
    return params


def setup_test_dir():
    """
    setup test directory
    """
    os.makedirs(f"{TEST_DIR}/test_run", exist_ok=True)
    os.makedirs(f"{TEST_DIR}/test_run/download", exist_ok=True)
    test_data = f"{TEST_DIR}/resources/test_fastqs_gziped/"
    shutil.copy(
        f"{test_data}/C0098_S1_L001_R1_001.fastq.gz",
        f"{TEST_DIR}/test_run/download",
    )
    shutil.copy(
        f"{test_data}/C0098_S1_L001_R2_001.fastq.gz",
        f"{TEST_DIR}/test_run/download",
    )
    shutil.copy(
        f"{test_data}/data.csv",
        f"{TEST_DIR}/test_run/",
    )


def test_novobarcode_demultiplex():
    """
    test demultiplex
    """
    setup_test_dir()
    path = f"{TEST_DIR}/test_run/"
    os.makedirs(f"{path}/demultiplexed", exist_ok=True)
    #setup_applevel_logger(file_name=f"{path}/demultiplexed/demultiplex.log")
    params = load_default_params()
    df = pd.read_csv(f"{path}/data.csv")
    pfqs = get_paired_fastqs(f"{path}/download")
    demultiplexer = NovobarcodeDemultiplexer()
    demultiplexer.setup(params["demultiplex"])
    demultiplexer.run(df, pfqs, path + "/demultiplexed")
    shutil.rmtree(f"{TEST_DIR}/test_run")


def test_sabre_demultiplex():
    """
    test demultiplex
    """
    # TODO make sure to do more file checks
    setup_test_dir()
    path = f"{TEST_DIR}/test_run/"
    os.makedirs(f"{path}/demultiplexed", exist_ok=True)
    #setup_applevel_logger(file_name=f"{path}/demultiplexed/demultiplex.log")
    params = load_default_params()
    df = pd.read_csv(f"{path}/data.csv")
    pfqs = get_paired_fastqs(f"{path}/download")
    demultiplexer = SabreDemultiplexer()
    demultiplexer.setup(params["demultiplex"])
    demultiplexer.run(df, pfqs, path + "/demultiplexed")
    shutil.rmtree(f"{TEST_DIR}/test_run")
