"""
This module contains the runmulti function.
"""
import os
import yaml
import pandas as pd
from pathlib import Path

from rna_map_tools.dataframe import check_if_columns_exist
from rna_map_tools.logger import get_logger
from rna_map_tools.fastq import get_paired_fastqs
from rna_map_tools.exceptions import RNAMapToolsInputException

from rna_map.run import (
    validate_fastq_file,
    validate_fasta_file,
    validate_csv_file,
)
from rna_map.run import run as run_rna_map
from rna_map.mutation_histogram import (
    get_dataframe,
    get_mut_histos_from_json_file,
)

log = get_logger("RUNMULTI")


def valid_fastq_files(df: pd.DataFrame, data_path: str) -> bool:
    """
    Check that the fastq files exist
    :param df: pandas dataframe that contains the barcode information
    :param data_path: path to the data directory
    :return: True if the fastq files exist, False otherwise
    """
    expects = ["barcode", "barcode_seq", "construct"]
    check_if_columns_exist(df, expects)
    msg = f"\n{data_path} directory structure should be as follows:"
    msg += "each BARCODE directory should be the sequence of the barcode as "
    msg += "it appears in the data.csv\n"
    msg += "--DATA_PATH/\n"
    msg += "  |--BARCODE_1/\n"
    msg += "     |--test_S1_L001_R1_001.fastq\n"
    msg += "     |--test_S1_L001_R2_001.fastq\n"
    for _, row in df.iterrows():
        fastq_path = os.path.join(data_path, row["barcode_seq"])
        # check to see if the fastq directory exists
        if not os.path.exists(fastq_path):
            log.error(f"barcode directory: {fastq_path} does not exist")
            log.error(msg)
            return False
        # check to see if the fastq files exist in the barcode directory
        try:
            pfq = get_paired_fastqs(fastq_path + "/test_S1*")
        except FileNotFoundError:
            log.error(
                f"no fastqs do not exist in barcode directory: {fastq_path}"
            )
            log.error(msg)
            return False
        for fq in [pfq.read_1, pfq.read_2]:
            if not validate_fastq_file(fq.path):
                log.error(f"fastq file: {fq.path} is not a valid fastq")
                log.error(msg)
                return False
    return True


def valid_fasta_files(df: pd.DataFrame, fasta_path: str) -> bool:
    """
    Check that the fasta files exist
    :param df:
    :param fasta_path:
    :return:
    """
    msg = f"\n{fasta_path} directory structure should be as follows:\n"
    msg += "each fasta files should be named code.fasta\n"
    msg += "--FASTA_PATH/\n"
    msg += "  |--code_1.fasta\n"
    msg += "  |--code_2.fasta\n"
    fasta_path = Path(fasta_path)
    check_if_columns_exist(df, ["code"])
    for _, row in df.iterrows():
        fasta = Path(fasta_path) / f'{row["code"]}.fasta'
        if not os.path.exists(fasta):
            log.error(f"fasta file: {fasta} does not exist")
            log.error(msg)
            return False
        if not validate_fasta_file(fasta):
            log.error(f"fasta file: {fasta} is not a valid fasta")
            log.error(msg)
            return False
    return True


def valid_csv_files(df: pd.DataFrame, csv_path: str) -> bool:
    check_if_columns_exist(df, ["code"])
    for _, row in df.iterrows():
        csv = Path(csv_path) / row["code"] + ".csv"
        if not os.path.exists(csv):
            log.error(f"csv file: {csv} does not exist")
            return False
        if not validate_csv_file(csv):
            log.error(f"csv file: {csv} is not a valid csv")
            return False
    return True




def runmulti(df, run_path, data_path, seq_data_path, params):
    # TODO add option to hide rna-map output
    # TODO add some processing before to remove katie's constructs
    # TODO add validation for csvs
    # TODO give links to instructions for how to setup data and google drive
    # check everything is setup properly and exists
    if not os.path.exists(run_path):
        log.error(f"{run_path} does not exist cannot run multi")
        exit()
    # check all the data is valid before starting the run!
    # check to make sure fastqs actually exist and are valid
    if not valid_fastq_files(df, data_path):
        exit()
    # check to make sure fasta exists
    if not valid_fasta_files(df, Path(seq_data_path) / "fasta"):
        exit()
    # check to make sure csv exists
    if not valid_csv_files(df, Path(seq_data_path) / "rna"):
        exit()

    os.chdir(run_path)
    # catch old column names
    if "name" in df:
        df = df.rename({"name": "construct"}, axis="columns")
        log.warning("renaming 'name' column to 'construct'")
    if "type" in df:
        df = df.rename({"type": "data_type"}, axis="columns")
    os.makedirs("processed", exist_ok=True)
    os.makedirs("analysis", exist_ok=True)
    os.chdir("processed")
    dfs = []
    for i, row in df.iterrows():
        # TODO add option to skip processing
        dir_name = row["construct"] + "_" + row["code"] + "_" + row["data_type"]
        os.chdir(dir_name)
        fa_path = f"{seq_data_path}/fasta/{row['code']}.fasta"
        # notice the switch of fastq1 and fastq2 since we are working with RNA
        fastq1_path = (
            f"{data_path}/{row['barcode_seq']}/test_S1_L001_R2_001.fastq"
        )
        fastq2_path = (
            f"{data_path}/{row['barcode_seq']}/test_S1_L001_R1_001.fastq"
        )
        dot_bracket_path = f"{seq_data_path}/rna/{row['code']}.csv"
        params_path = params["rna_map_params_file"]
        rna_map_params = yaml.safe_load(open(params_path))
        run_rna_map(
            fa_path, fastq1_path, fastq2_path, dot_bracket_path, rna_map_params
        )
