"""
testing downloading from basespace
"""
import os
import shutil

import yaml

from rna_map_tools.run import download
from rna_map_tools.parameters import PY_DIR

TEST_DIR = os.path.dirname(os.path.realpath(__file__))

def load_default_params():
    path = PY_DIR + "/resources/default.yml"
    with open(path) as f:
        params = yaml.safe_load(f)
    return params

def test_download():
    """
    test downloading a run from basespace
    :return:
    """
    params = load_default_params()
    params["download"]["rename_dir"] = True
    run_name = "2023_01_11_mtt6_uucg_2_seq"
    download_dir = TEST_DIR
    pfqs = download(run_name, download_dir, params["download"])
    # not sure if this is always the same name?
    path = f"{TEST_DIR}/{run_name}/download"
    assert os.path.isdir(path)
    assert pfqs.is_compressed() == True
    assert pfqs.read_1.path == f"{path}/C0098_S1_L001_R1_001.fastq.gz"
    assert pfqs.read_2.path == f"{path}/C0098_S1_L001_R2_001.fastq.gz"
    shutil.rmtree(f"{TEST_DIR}/{run_name}")


