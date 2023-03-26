"""

"""
import os
import shutil
import pytest
from pathlib import Path

import pandas as pd

from rna_map_tools.logger import setup_applevel_logger
from rna_map_tools.exceptions import RNAMapToolsInputException

from rna_map_tools.tools.runmulti import (
    runmulti,
    valid_fastq_files,
    valid_fasta_files,
)

TEST_DIR = Path(__file__).parent


def setup_test_dir():
    os.makedirs(TEST_DIR / "test_run")
    shutil.copytree(
        TEST_DIR / "resources/demultiplexed",
        TEST_DIR / "test_run/demultiplexed",
    )
    shutil.copy(
        TEST_DIR / "resources/test_fastqs/data.csv", TEST_DIR / "test_run/"
    )
    shutil.copytree(
        TEST_DIR / "resources/test_fastas",
        TEST_DIR / "test_run/fastas"
    )


def test_valid_fastq_files():
    """
    test the valid_fastq_files function
    """
    #setup_test_dir()
    df = pd.read_csv(TEST_DIR / "test_run/data.csv")
    path = TEST_DIR / "test_run/demultiplexed"
    assert valid_fastq_files(df, path) == True
    # with pytest.raises(RNAMapToolsInputException) as exec_info:
    assert valid_fastq_files(df, "test/") == False
    # print(exec_info)
    # setup_test_dir()


def test_valid_fasta_files():
    """
    test the valid_fasta_files function
    """
    #setup_test_dir()
    setup_applevel_logger(is_debug=True)
    df = pd.read_csv(TEST_DIR / "test_run/data.csv")
    path = TEST_DIR / "test_run/fastas"
    assert valid_fasta_files(df, path) == True
    # with pytest.raises(RNAMapToolsInputException) as exec_info:
    assert valid_fasta_files(df, "test/") == False
    # print(exec_info)

    # setup_test_dir()
