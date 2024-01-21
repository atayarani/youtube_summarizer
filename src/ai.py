import os

from langchain.text_splitter import CharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from functools import cache

from src.exceptions import InvalidTranscript
from src.transcript import Transcript

class AI:
    """
    This class represents an AI assistant that
    can chat with users and provide output based
    on the conversation.
    """

    def __init__(self, transcript: Transcript) -> None:
        """Initializes an instance of the AI class.

        Args:
            transcript (Transcript): The transcript object containing
                the content and metadata.

        Raises:
            KeyError: If the OPENAI_API_KEY environment variable is not set.

        Returns:
            None
        """
        self.transcript = transcript.content
        self.metadata = transcript.metadata

        if self.transcript is None or self.transcript == "":
            raise InvalidTranscript()

        if "OPENAI_API_KEY" not in os.environ:
            raise KeyError("OPENAI_API_KEY environment variable not set.")

    def takeaways(self) -> list:
        """Returns the key takeaways from the transcript provided by the user.

        Returns:
            list: A list of key takeaways.
        """
        output = []
        for transcript in self._split_transcript():
            messages = [
                SystemMessage(
                    content=(
                        "The user will provide a transcript."
                        "From the transcript, you will provide a bulleted list of "
                        "key takeaways. At the top of the list, add a title: "
                        f"'# Key Takeaways — {self.metadata.title}'"
                    )
                ),
                HumanMessage(content=self.transcript),
            ]
            output.append("".join(self._chat(temperature=1.0, messages=messages)))

        return output

    def summary(self) -> list:
        """Generates a summary of the transcript by reformatting it into an
        in-depth markdown blog post using sections and section headers.

        Returns:
            A list of strings representing the generated summary.
        """
        output = []

        for transcript in self._split_transcript():
            messages = [
                SystemMessage(
                    content=(
                        "The user will provide a transcript."
                        "reformat the transcript  into an in-depth "
                        "markdown blog post using sections and section headers."
                        f"The title of the blog post will be {self.metadata.title}."
                    )
                ),
                HumanMessage(content=transcript),
            ]

            output.append("".join(self._chat(temperature=1.0, messages=messages)))

        return output

    @staticmethod
    def _chat(
        model: str = "gpt-3.5-turbo-16k",
        temperature: float = 0.0,
        messages: list = None,
    ) -> list:
        """Perform a chat conversation using the specified model and messages.

        Args:
            model (str): The model to use for the chat conversation.
                Defaults to "gpt-3.5-turbo".
            temperature (float): The temperature parameter for generating
                responses. Defaults to 0.0.
            messages (list): The list of messages in the conversation.
                Must be specified.

        Returns:
            list: The list of generated responses.
        """
        if messages is None:
            raise ValueError("messages must be specified.")
        chat = ChatOpenAI(temperature=temperature, model=model)

        return [chunk.content for chunk in chat.stream(messages)]

    @cache
    def _split_transcript(self) -> list:
        """Split the transcript into chunks using a character-based text splitter.

        Returns:
            A list of transcript chunks.
        """
        transcript_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=10000, chunk_overlap=0
        )

        return transcript_splitter.split_text(self.transcript)
