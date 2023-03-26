"""
testing structured data module
"""
import os
import pytest

from rna_map_tools.fastq import FastqFile, get_paired_fastqs

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def test_fastq():
    path = TEST_DIR + "/resources/test_fastqs/C0098_S1_L001_R1_001.fastq"
    fq = None
    try:
        fq = FastqFile(path)
    except:
        pytest.fail("FastqFile failed to initialize not a valid file")

    assert fq.path == path
    assert fq.is_compressed() is False
    assert fq.is_r1() is True
    assert fq.is_r2() is False


def test_fastq_compressed():
    path = (
        TEST_DIR + "/resources/test_fastqs_gziped/C0098_S1_L001_R1_001.fastq.gz"
    )
    fq = None
    try:
        fq = FastqFile(path)
    except:
        pytest.fail("FastqFile failed to initialize not a valid file")

    assert fq.path == path
    assert fq.is_compressed() is True
    assert fq.is_r1() is True
    assert fq.is_r2() is False

def test_fastq_messes():
    path = TEST_DIR + "/resources/test_fastqs_messed/C0098.fastq"
    with pytest.raises(ValueError):
        FastqFile(path)



def test_get_paired_fastqs():
    """
    test getting paired fastq files from a directory
    :return:
    """
    path = TEST_DIR + "/resources/test_fastqs"
    pfqs = get_paired_fastqs(path)
