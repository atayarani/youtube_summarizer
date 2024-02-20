# import pytest
# from hypothesis import given
# from hypothesis import strategies as st
# from youtube_cheatsheet.cli import get_output


# class TestGetOutput:
#     def test_title_only(self) -> None:
#         """Test for the `get_output` method with only the `title` parameter."""
#         assert get_output("title", None, None, None) == "# title\n\n"

#     def test_title_and_metadata(self) -> None:
#         r"""
#         Test method for the `get_output` function with "title" and "metadata" parameters.

#         Asserts that the returned output of `get_output` with "title" and "metadata" parameters is equal to "# title\n\nmetadata".

#         Returns:
#             None
#         """
#         assert get_output("title", "metadata", None, None) == "# title\n\nmetadata"

#     def test_title_takeaways_and_metadata(self) -> None:
#         """
#         Test method for testing the test_title_takeaways_and_metadata method.

#         Args:
#             self (class): The instance of the class.

#         Returns:
#             None: This method does not return anything.
#         """
#         assert (
#             get_output("title", "metadata", "takeaways", None)
#             == "# title\n\ntakeaways\n---\nmetadata"
#         )

#     def test_all_fields(self) -> None:
#         """
#         Test the 'get_output' method with all field parameters.

#         This method asserts that the output of the 'get_output' method
#         is equal to the expected output string when all field parameters
#         ('title', 'metadata', 'takeaways', and 'summary') are provided.

#         Returns:
#             None
#         """
#         assert (
#             get_output("title", "metadata", "takeaways", "summary")
#             == "# title\n\nsummary\n---\ntakeaways\n---\nmetadata"
#         )

#     @pytest.mark.xfail(strict=True, reason="Not idempotent")
#     @given(
#         title=st.text(),
#         metadata=st.one_of(st.none(), st.text()),
#         takeaways=st.one_of(st.none(), st.text()),
#         summary=st.one_of(st.none(), st.text()),
#     )
#     def test_idempotent_get_output(
#         self,
#         title: str,
#         metadata: str | None,
#         takeaways: str | None,
#         summary: str | None,
#     ) -> None:
#         """
#         Test method for checking the idempotent behavior of the `get_output` function.

#         Args:
#             title: A string representing the title parameter for `get_output`.
#             metadata: Either a string representing the metadata parameter for `get_output`,
#                       or None if metadata is not provided.
#             takeaways: Either a string representing the takeaways parameter for `get_output`,
#                        or None if takeaways is not provided.
#             summary: Either a string representing the summary parameter for `get_output`,
#                      or None if summary is not provided.
#         """
#         result = get_output(
#             title=title, metadata=metadata, takeaways=takeaways, summary=summary
#         )
#         repeat = get_output(
#             title=result, metadata=metadata, takeaways=takeaways, summary=summary
#         )
#         assert result == repeat, (result, repeat)

#     @given(
#         title=st.text(),
#         metadata=st.one_of(st.none(), st.text()),
#         takeaways=st.one_of(st.none(), st.text()),
#         summary=st.one_of(st.none(), st.text()),
#     )
#     def test_fuzz_get_output(
#         self,
#         title: str,
#         metadata: str | None,
#         takeaways: str | None,
#         summary: str | None,
#     ) -> None:
#         """
#         Test method for fuzz testing the `get_output` function.

#         Args:
#             title (str): The title of the test case.
#             metadata (Union[str, None]): The metadata associated with the test case.
#             takeaways (Union[str, None]): The takeaways from the test case.
#             summary (Union[str, None]): The summary of the test case.

#         """
#         get_output(
#             title=title,
#             youtube_data_metadata=metadata,
#             output_takeaways=takeaways,
#             output_summary=summary,
#         )
