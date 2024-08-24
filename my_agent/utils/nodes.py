from functools import lru_cache
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from my_agent.utils.tools import tools
from langgraph.prebuilt import ToolNode
from langsmith import traceable
import random


# Define the function that determines whether to continue or not
def should_continue(state):
    messages = state["messages"]

    # Randomly decide whether to continue or end
    if random.random() < 0.25:
        return "end"
    else:
        return "continue"

@traceable(name="method_1", run_type="chain")
def another_trace_method(messages):
    one_more_trace_method(messages)

@traceable(name="method_2", run_type="llm")
def one_more_trace_method(messages):
    pass

system_prompt = """Be a helpful assistant"""

# Define the function that calls the model
def call_model(state, config):
    messages = state["messages"]
    messages = [{"role": "system", "content": system_prompt}] + messages

    random_words = ["The", "quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
    simulated_content = " ".join(random.choices(random_words, k=10))
    response = {"role": "assistant", "content": simulated_content}

    another_trace_method(messages)

    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

# Define the function to execute tools
tool_node = ToolNode(tools)