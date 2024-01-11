from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.transcript import Transcript


class AI:
    """
    This class represents an AI assistant that
    can chat with users and provide output based
    on the conversation.
    """

    def __init__(self, transcript: Transcript) -> None:
        """
        Initializes an instance of the class.

        Args:
            transcript (str): The transcript of the video.

        Returns:
            None
        """
        self.transcript = transcript.content
        self.metadata = transcript.metadata

    def print_takeaways(self) -> None:
            """
            Prints the key takeaways from the transcript provided by the user.

            The method uses the ChatOpenAI class to generate a bulleted list of key takeaways
            from the transcript. It starts by adding a title to the list, which is formatted as
            '# Key Takeaways — {self.metadata.title}'. Then, it adds the transcript as a
            HumanMessage to the list of messages. Finally, it iterates over the messages using
            the chat.stream() method and prints each chunk of content.

            Note: The transcript should be set before calling this method.

            Returns:
                None
            """
            chat = ChatOpenAI(temperature=0)
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
            for chunk in chat.stream(messages):
                print(chunk.content, end="", flush=True)
            print()
            print("---")

    def print_summary(self) -> None:
            """
            Prints a summary of the transcript as a markdown blog post.

            The summary is generated using the ChatOpenAI model with a temperature of 1.
            The transcript is copy edited for clarity, accuracy, and basic errors.
            The reformatted transcript is then printed as an in-depth markdown blog post
            with sections and section headers. The title of the blog post is based on
            the metadata's title attribute.
            """
            chat = ChatOpenAI(temperature=1)
            messages = [
                SystemMessage(
                    content=(
                        "The user will provide a transcript.Copy edit the transcript "
                        "for clarity, accuracy, and basic errors. "
                        "reformat the transcript  into an in-depth "
                        "markdown blog post using sections and section headers."
                        f"The title of the blog post will be {self.metadata.title}."
                    )
                ),
                HumanMessage(content=self.transcript),
            ]
            for chunk in chat.stream(messages):
                print(chunk.content, end="", flush=True)
            print()
            print("---")
