import typing

import pytest
from hypothesis import given
from hypothesis import strategies as st

from src.cli import get_output


class TestGetOutput:
    def test_title_only(self):
        assert get_output("title", None, None, None) == "# title\n\n"

    def test_title_and_metadata(self):
        assert get_output("title", "metadata", None, None) == "# title\n\nmetadata"

    def test_title_takeaways_and_metadata(self):
        assert (
            get_output("title", "metadata", "takeaways", None)
            == "# title\n\ntakeaways\n---\nmetadata"
        )

    def test_all_fields(self):
        assert (
            get_output("title", "metadata", "takeaways", "summary")
            == "# title\n\nsummary\n---\ntakeaways\n---\nmetadata"
        )

    @pytest.mark.xfail(strict=True, reason="Not idempotent")
    @given(
        title=st.text(),
        metadata=st.one_of(st.none(), st.text()),
        takeaways=st.one_of(st.none(), st.text()),
        summary=st.one_of(st.none(), st.text()),
    )
    def test_idempotent_get_output(
        self,
        title: str,
        metadata: typing.Union[str, None],
        takeaways: typing.Union[str, None],
        summary: typing.Union[str, None],
    ) -> None:
        result = get_output(
            title=title, metadata=metadata, takeaways=takeaways, summary=summary
        )
        repeat = get_output(
            title=result, metadata=metadata, takeaways=takeaways, summary=summary
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
        metadata: typing.Union[str, None],
        takeaways: typing.Union[str, None],
        summary: typing.Union[str, None],
    ) -> None:
        get_output(title=title, metadata=metadata, takeaways=takeaways, summary=summary)
