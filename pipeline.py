#!/usr/bin/env python3
from dataclasses import dataclass

from langchain_community.document_loaders import YoutubeLoader
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

@dataclass
class Transcript:
    content: str
    metadata: dict

def get_transcript(url) -> Transcript:
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        output = loader.load()[0]
        return Transcript(output.page_content, {**output.metadata, url: url})


def ai_chat(chat: ChatOpenAI, content: str) -> list:
    messages = [
        SystemMessage(
            content="The user will provide a transcript. You will provide two documents as output. The first is a list of key takeaways from the video. The second document is the transcript reformatted into an in-depth markdown blog post using sections and section headers."
        ),
        HumanMessage(content=content),
    ]

    return messages


def get_metadata(metadata, url):
    return {
        "Title": metadata["title"],
        "Publish Date": metadata["publish_date"],
        "Author": metadata["author"],
        "URL": url,
    }


url = "https://www.youtube.com/watch?v=Z4WupQQdMsQ"
transcript = get_transcript(url)
chat = ChatOpenAI()
for chunk in chat.stream(ai_chat(chat, transcript.content)):
    print(chunk.content, end="", flush=True)

print()
print(transcript.metadata)
