from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class AI:
    """
    This class represents an AI assistant that can chat with users and provide output based
    on the conversation.
    """

    def __init__(self, transcript: str) -> None:
        """
        Initializes an instance of the class.

        Args:
            transcript (str): The transcript of the video.

        Returns:
            None
        """
        self.chat = ChatOpenAI()
        self.messages = [
            SystemMessage(
                content="The user will provide a transcript. You will provide two documents as output. The first is a list of key takeaways from the video. The second document is the transcript reformatted into an in-depth markdown blog post using sections and section headers."
            ),
            HumanMessage(content=transcript),
        ]

    def print(self) -> None:
        """
        Prints the output generated by the AI assistant based on the conversation with the
        user.
        """
        for chunk in self.chat.stream(self.messages):
            print(chunk.content, end="", flush=True)
        print()
