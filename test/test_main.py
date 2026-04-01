import os
import subprocess
import tempfile

import pytest
from click.testing import CliRunner

from sequana_pipelines.depletion.main import main

from . import test_dir

input_dir = os.sep.join((test_dir, "data"))
reference = f"{input_dir}/measles.fa"


def test_standalone_subprocess():
    directory = tempfile.TemporaryDirectory()
    cmd = ["test", "--input-directory", input_dir, "--working-directory", directory.name, "--force"]
    subprocess.call(cmd)


@pytest.mark.parametrize("mode", ["selection", "depletion"])
def test_standalone_script_paired(mode):
    directory = tempfile.TemporaryDirectory()
    args = [
        "--input-directory", input_dir,
        "--working-directory", directory.name,
        "--force",
        "--mode", mode,
        "--reference-file", reference,
    ]
    runner = CliRunner()
    results = runner.invoke(main, args)
    assert results.exit_code == 0


@pytest.mark.parametrize("mode", ["selection", "depletion"])
def test_standalone_script_single(mode):
    directory = tempfile.TemporaryDirectory()
    args = [
        "--input-directory", input_dir,
        "--input-readtag", "_R1_",
        "--working-directory", directory.name,
        "--force",
        "--mode", mode,
        "--reference-file", reference,
    ]
    runner = CliRunner()
    results = runner.invoke(main, args)
    assert results.exit_code == 0


def test_version():
    cmd = ["sequana_depletion", "--version"]
    subprocess.call(cmd)

