from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from typing import TypedDict, Annotated, Sequence, Union

from langchain_core.messages import (
    AnyMessage,
    MessageLikeRepresentation,
    RemoveMessage,
    convert_to_messages,
    message_chunk_to_message,
)
Messages = Union[list[MessageLikeRepresentation], MessageLikeRepresentation]


def replace_messages(left: Messages, right: Messages) -> Messages:
    messages = add_messages(left, right)
    return messages[-1:]


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], replace_messages]
