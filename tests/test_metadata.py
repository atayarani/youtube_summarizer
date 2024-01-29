import pytest

from src.metadata import Metadata


@pytest.fixture
def valid_metadata():
    return Metadata(
        title="Title",
        publish_date="2022-01-01",
        author="Author",
        url="www.example.com",
        description="Description",
        video_id="12345",
    )


@pytest.fixture
def valid_output():
    return "Title: Title\nPublish Date: 2022-01-01\nAuthor: Author\nURL: www.example.com\nDescription: Description\n"


class TestMetadata:
    def test_returns_metadata_as_string(self, valid_metadata, valid_output):
        metadata = valid_metadata
        expected_output = valid_output
        assert str(metadata) == expected_output
