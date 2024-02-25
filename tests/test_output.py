import pathlib

import pytest
import youtube_cheatsheet.output
from hypothesis import given
from hypothesis import strategies as st
from jinja2 import Environment, Template
from pytest_mock import MockerFixture


@pytest.fixture()
def jinja_env() -> Environment:
    return youtube_cheatsheet.output.setup_jinja_env()


class TestTemplateOutput:
    # Returns an instance of jinja2 Environment.
    def test_returns_instance_of_jinja2_environment(self, jinja_env) -> None:
        assert isinstance(jinja_env, Environment)

    # Returns a Jinja2 Template object when given an Environment object and a template name
    def test_returns_template_object(self, jinja_env):
        template = youtube_cheatsheet.output.get_template(jinja_env)
        assert isinstance(template, Template)


def test_get_output_returns_string_with_valid_inputs():
    # Arrange
    title = "Test Title"
    youtube_data_metadata = "Test Metadata"
    output_takeaways = "Test Takeaways"
    output_summary = "Test Summary"

    # Act
    result = youtube_cheatsheet.output.get_output(
        title, youtube_data_metadata, output_takeaways, output_summary
    )

    # Assert
    assert isinstance(result, str)


class TestGetOutput:
    @given(
        title=st.text(),
        youtube_data_metadata=st.one_of(st.none(), st.text()),
        output_takeaways=st.one_of(st.none(), st.text()),
        output_summary=st.one_of(st.none(), st.text()),
    )
    def test_idempotent_get_output(
        self,
        title: str,
        youtube_data_metadata: str | None,
        output_takeaways: str | None,
        output_summary: str | None,
    ) -> None:
        result = youtube_cheatsheet.output.get_output(
            title=title,
            youtube_data_metadata=youtube_data_metadata,
            output_takeaways=output_takeaways,
            output_summary=output_summary,
        )
        repeat = youtube_cheatsheet.output.get_output(
            title=title,
            youtube_data_metadata=youtube_data_metadata,
            output_takeaways=output_takeaways,
            output_summary=output_summary,
        )
        assert result == repeat, (result, repeat)

    @given(
        title=st.text(),
        metadata=st.one_of(st.none(), st.text()),
        takeaways=st.one_of(st.none(), st.text()),
        summary=st.one_of(st.none(), st.text()),
    )
    def test_fuzz_get_output(
        self,
        title: str,
        metadata: str | None,
        takeaways: str | None,
        summary: str | None,
    ) -> None:
        youtube_cheatsheet.output.get_output(
            title=title,
            youtube_data_metadata=metadata,
            output_takeaways=takeaways,
            output_summary=summary,
        )


# class TestWriteFile:


class TestWriteFile:
    def test_create_file_path(self):
        file_path = youtube_cheatsheet.output.create_file_path(
            "bar", pathlib.Path("foo")
        )
        assert str(file_path) == "foo/bar.md"

    def test_sanitize_filename(self, mocker):
        validation = mocker.patch(
            "youtube_cheatsheet.output.validate_output_path", return_value=True
        )
        mocker.patch.object(pathlib.Path, "write_text")
        youtube_cheatsheet.output.write_file(
            "file?name*", "test_string", pathlib.Path("foo")
        )
        validation.assert_called_once_with(
            pathlib.Path("foo/filename.md"), pathlib.Path("foo")
        )

    def test_failed_validate_raises_error(self, mocker):
        mocker.patch(
            "youtube_cheatsheet.output.validate_output_path", return_value=False
        )
        with pytest.raises(
            youtube_cheatsheet.exceptions.OutputPathValidationError,
            match="Output path validation error",
        ):
            youtube_cheatsheet.output.write_file(
                "file?name*", "test_string", pathlib.Path("foo")
            )

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
    def test_validate_output_path(
        self,
        mocker: MockerFixture,
        file_path_exists: bool,
        dir_path_is_dir: bool,
        dir_path_exists: bool,
        expected_result: bool,
    ) -> None:
        file_path = mocker.Mock()
        file_path.exists.return_value = file_path_exists
        dir_path = mocker.Mock()
        dir_path.is_dir.return_value = dir_path_is_dir
        dir_path.exists.return_value = dir_path_exists

        result = youtube_cheatsheet.output.validate_output_path(file_path, dir_path)

        assert type(result) == type(expected_result)
