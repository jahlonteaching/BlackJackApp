import os
import pytest

from importlib.resources import files
from pathlib import Path


def invoke_tests():
    directory = str(files('juego').joinpath(Path('submissions')))
    file_list = os.listdir(directory)

    for file in file_list:
        if not file.startswith("__"):
            pytest.main(["test_module.py", "--module-file", f"{directory}{os.sep}{file}", "--name", file])


if __name__ == "__main__":
    invoke_tests()
