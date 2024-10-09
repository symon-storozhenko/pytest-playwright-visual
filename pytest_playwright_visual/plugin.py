import sys
import os
import shutil
from io import BytesIO
from pathlib import Path
from typing import Any, Callable
import pytest
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch


@pytest.fixture
def assert_snapshot(pytestconfig: Any, request: Any, browser_name: str) -> Callable:
    test_name = f"{str(Path(request.node.name))}[{str(sys.platform)}]"
    test_dir = str(Path(request.node.name)).split('[', 1)[0]

    def compare(img: bytes, *, threshold: float = 0.1, name=f'{test_name}.png', fail_fast=False) -> None:
        update_snapshot = pytestconfig.getoption("--update-snapshots")
        test_file_name = str(os.path.basename(Path(request.node.fspath))).strip('.py')
        filepath = (
                Path(request.node.fspath).parent.resolve()
                / 'snapshots'
                / test_file_name
                / test_dir
        )
        filepath.mkdir(parents=True, exist_ok=True)
        file = filepath / name
        # Create a dir where all snapshot test failures will go
        results_dir_name = (Path(request.node.fspath).parent.resolve()
                            / "snapshot_tests_failures")
        test_results_dir = (results_dir_name
                            / test_file_name / test_name)
        # Remove a single test's past run dir with actual, diff and expected images
        if test_results_dir.exists():
            shutil.rmtree(test_results_dir)
        if update_snapshot:
            file.write_bytes(img)
            pytest.fail("--> Snapshots updated. Please review images")
        if not file.exists():
            file.write_bytes(img)
            # pytest.fail(
            pytest.fail("--> New snapshot(s) created. Please review images")
        img_a = Image.open(BytesIO(img))
        img_b = Image.open(file)
        img_diff = Image.new("RGBA", img_a.size)
        mismatch = pixelmatch(img_a, img_b, img_diff, threshold=threshold, fail_fast=fail_fast)
        if mismatch == 0:
            return
        else:
            # Create new test_results folder
            test_results_dir.mkdir(parents=True, exist_ok=True)
            img_diff.save(f'{test_results_dir}/Diff_{name}')
            img_a.save(f'{test_results_dir}/Actual_{name}')
            img_b.save(f'{test_results_dir}/Expected_{name}')
            pytest.fail("--> Snapshots DO NOT match!")

    return compare


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("playwright-snapshot", "Playwright Snapshot")
    group.addoption(
        "--update-snapshots",
        action="store_true",
        default=False,
        help="Update snapshots.",
    )
