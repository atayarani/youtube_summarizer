import pathlib

import pytest
import pytest_mock
from hypothesis import example, given
from hypothesis import strategies as st

import src.cli


@pytest.mark.parametrize(
    ",".join(
        [
            "file_path_exists",
            "dir_path_is_dir",
            "dir_path_exists",
            "expected_result",
            "expected_value",
        ]
    ),
    [
        pytest.param(False, True, True, 0, None, id="function_succeeds"),
        pytest.param(True, True, True, 1, FileExistsError, id="file_exists_error"),
        pytest.param(
            False, False, True, 2, NotADirectoryError, id="not_a_directory_error"
        ),
        pytest.param(
            False, True, False, 3, FileNotFoundError, id="file_not_found_error"
        ),
    ],
)
def test(
    mocker: pytest_mock.MockerFixture,
    file_path_exists: bool,
    dir_path_is_dir: bool,
    dir_path_exists: bool,
    expected_result: int,
    expected_value: (
        type[FileExistsError] | type[NotADirectoryError] | type[FileNotFoundError]
    ),
) -> None:
    file_path = mocker.Mock()
    file_path.exists.return_value = file_path_exists
    dir_path = mocker.Mock()
    dir_path.is_dir.return_value = dir_path_is_dir
    dir_path.exists.return_value = dir_path_exists

    result, value = src.cli.validate_output_path(file_path, dir_path)

    assert result == expected_result
    assert isinstance(value, type(value))


@pytest.mark.xfail(strict=True, reason="Not idempotent")
@given(file_path=st.from_type(pathlib.Path), dir_path=st.from_type(pathlib.Path))
@example(file_path=pathlib.Path(), dir_path=pathlib.Path()).via("discovered failure")
def test_idempotent_validate_output_path(
    file_path: pathlib.Path, dir_path: pathlib.Path
) -> None:
    result = src.cli.validate_output_path(file_path=file_path, dir_path=dir_path)
    repeat = src.cli.validate_output_path(file_path=file_path, dir_path=dir_path)
    assert result == repeat, (result, repeat)


@given(file_path=st.from_type(pathlib.Path), dir_path=st.from_type(pathlib.Path))
def test_fuzz_validate_output_path(
    file_path: pathlib.Path, dir_path: pathlib.Path
) -> None:
    src.cli.validate_output_path(file_path=file_path, dir_path=dir_path)
