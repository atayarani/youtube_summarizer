import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.metadata import Metadata


class AI:
    """
    This class represents an AI assistant that
    can chat with users and provide output based
    on the conversation.
    """

    def __init__(self, transcript_chunks: list[str], metadata: Metadata) -> None:
        """Initializes an instance of the AI class.

        Args:
            transcript (Transcript): The transcript object containing
                the content and metadata.
            youtube_data (YouTubeData): The YouTubeData object containing
                the metadata of the YouTube video.

        Returns:
            None
        """
        self.transcript_chunks = transcript_chunks
        self.metadata: Metadata = metadata

    def takeaways(self) -> str:
        """Returns the key takeaways from the transcript provided by the user.

        Returns:
            list: A list of key takeaways.
        """

        content = (
            "The user will provide a transcript.From the transcript, you will provide a bulleted list of "
            f"key takeaways. At the top of the list, add a title: '# Key Takeaways — {self.metadata.title}'"
        )

        return self._chat(
            system_message=SystemMessage(content=content), temperature=1.0
        )

    def summary(self) -> str:
        """Generates a summary of the transcript by reformatting it into an
        in-depth markdown blog post using sections and section headers.

        Returns:
            A list of strings representing the generated summary.
        """

        content = (
            "The user will provide a transcript. Reformat the transcript into an in-depth "
            "markdown blog post using sections and section headers. The title of the blog "
            f"post will be {self.metadata.title}."
        )

        return self._chat(
            system_message=SystemMessage(content=content), temperature=1.0
        )

    def _chat(
        self,
        system_message: SystemMessage,
        model: str = "gpt-3.5-turbo-16k",
        temperature: float = 0.0,
    ) -> str:
        """Perform a chat conversation using the specified model and messages.

        Args:
            model (str): The model to use for the chat conversation.
                Defaults to "gpt-3.5-turbo-16k".
            temperature (float): The temperature parameter for generating
                responses. Defaults to 0.0.
            messages (list): The list of messages in the conversation.
                Must be specified.

        Returns:
            list: The list of generated responses.
        """
        if system_message is None:
            raise ValueError("messages must be specified.")
        if system_message.content == "" or system_message.content is None:
            raise ValueError("system_message.content must be specified.")

        output = []

        if not self.check_openai_api_key():
            raise self.OpenAIKeyNotFoundError

        for transcript in self.transcript_chunks:
            messages = [system_message, HumanMessage(content=transcript)]
            chat = ChatOpenAI(temperature=temperature, model=model)
            output.append("".join([chunk.content for chunk in chat.stream(messages)]))  # type: ignore

        return output[0]

    def check_openai_api_key(self) -> bool:
        return "OPENAI_API_KEY" in os.environ

    class OpenAIKeyNotFoundError(Exception):
        """Raised when the OPENAI_API_KEY environment variable is not found."""

        def __init__(self) -> None:
            """Initializes the OpenAIKeyNotFoundError exception."""
            super().__init__("OPENAI_API_KEY environment variable not set.")
