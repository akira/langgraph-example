from functools import lru_cache
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from my_agent.utils.tools import tools
from langgraph.prebuilt import ToolNode
from langsmith import traceable
import random

from nltk.corpus import words
import nltk

try:
    word_list = words.words()
except LookupError:
    nltk.download('words')
    word_list = words.words()

data_sizes = [20, 10240, 25600, 102400, 1048576, 5242880]
data_array = [" ".join(random.choices(word_list, k=(size // 5))) for size in data_sizes]

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
    input_data = random.choice(data_array)
    output_data = random.choice(data_array)

    messages = state["messages"]
    messages = [{"role": "system", "content": system_prompt, "data": input_data}] + messages

    random_words = ["The", "quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
    simulated_content = " ".join(random.choices(random_words, k=10))
    response = {"role": "assistant", "content": simulated_content, "data": output_data}

    another_trace_method(messages)
    another_trace_method(response)
    del response["data"]

    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

# Define the function to execute tools
tool_node = ToolNode(tools)