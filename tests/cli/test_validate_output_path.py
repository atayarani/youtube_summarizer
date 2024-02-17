import pathlib

import pytest
import pytest_mock
import youtube_cheatsheet.cli
from hypothesis import example, given
from hypothesis import strategies as st
from returns.maybe import Maybe


@pytest.mark.parametrize(
    (
        "file_path_exists",
        "dir_path_is_dir",
        "dir_path_exists",
        "expected_result",
    ),
    [
        pytest.param(False, True, True, True, id="function_succeeds"),
        pytest.param(True, True, True, False, id="file_exists_error"),
        pytest.param(False, False, True, False, id="not_a_directory_error"),
        pytest.param(False, True, False, False, id="file_not_found_error"),
    ],
)
def test(
    mocker: pytest_mock.MockerFixture,
    file_path_exists: bool,
    dir_path_is_dir: bool,
    dir_path_exists: bool,
    expected_result: Maybe[bool],
) -> None:
    """
    Test the `validate_output_path` function.

    Args:
        mocker: A pytest mocker fixture used for mocking objects and functions.
        file_path_exists: A boolean indicating whether the file path exists.
        dir_path_is_dir: A boolean indicating whether the directory path is a directory.
        dir_path_exists: A boolean indicating whether the directory path exists.
        expected_result: An integer representing the expected result of the method.


    """
    file_path = mocker.Mock()
    file_path.exists.return_value = file_path_exists
    dir_path = mocker.Mock()
    dir_path.is_dir.return_value = dir_path_is_dir
    dir_path.exists.return_value = dir_path_exists

    result = youtube_cheatsheet.cli.validate_output_path(file_path, dir_path)

    assert type(result) == type(expected_result)


# @pytest.mark.xfail(strict=True, reason="Not idempotent")
@given(file_path=st.from_type(pathlib.Path), dir_path=st.from_type(pathlib.Path))
@example(file_path=pathlib.Path(), dir_path=pathlib.Path()).via("discovered failure")
def test_idempotent_validate_output_path(
    file_path: pathlib.Path, dir_path: pathlib.Path
) -> None:
    """
    Test idempotency of the `validate_output_path` function.

    Args:
        file_path: A `pathlib.Path` object representing the file path to validate.
        dir_path: A `pathlib.Path` object representing the directory path to validate.

    """
    result = youtube_cheatsheet.cli.validate_output_path(
        file_path=file_path, dir_path=dir_path
    )
    repeat = youtube_cheatsheet.cli.validate_output_path(
        file_path=file_path, dir_path=dir_path
    )
    assert result == repeat, (result, repeat)


@given(file_path=st.from_type(pathlib.Path), dir_path=st.from_type(pathlib.Path))
def test_fuzz_validate_output_path(
    file_path: pathlib.Path, dir_path: pathlib.Path
) -> None:
    """
    Test fuzzing the `validate_output_path` function.

    Args:
        file_path: A `pathlib.Path` object representing the file path to be validated.
        dir_path: A `pathlib.Path` object representing the directory path to be validated.

    """
    youtube_cheatsheet.cli.validate_output_path(file_path=file_path, dir_path=dir_path)
