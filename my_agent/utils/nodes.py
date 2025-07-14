import random

import nltk
from langsmith import traceable, tracing_context
from nltk.corpus import words

try:
    word_list = words.words()
except LookupError:
    nltk.download("words")
    word_list = words.words()

data_sizes = [
    100,
    150,
    180,
    200,
    210,
    230,
    250,
    300,
    500,
    800,
    1200,
    1800,
    2352,
    2800,
    3500,
    5000,
    8000,
    12000,
    15566,
    20000,
    50000,
    100000,
    200000,
    364318,
    400000,
    500000,
]

ITERATIONS = 5

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
    messages = [
        {"role": "system", "content": system_prompt, "data": input_data}
    ] + messages

    random_words = ["The", "quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
    simulated_content = " ".join(random.choices(random_words, k=10))
    response = {"role": "assistant", "content": simulated_content, "data": output_data}

    another_trace_method(messages)
    another_trace_method(response)
    del response["data"]

    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


def call_tool_node(state, config):
    # Fake tool node - generate fake output using data_array and random sampling
    input_data = random.choice(data_array)
    output_data = random.choice(data_array)

    # Simulate tool execution with fake response
    fake_tool_response = {
        "role": "tool",
        "content": f"Tool executed successfully. Input: {input_data[:100]}... Output: {output_data[:100]}...",
        "tool_call_id": "123",
        "name": "tavily_search_results_json",
        "args": {"query": input_data},
        "data": output_data,
    }

    for _ in range(ITERATIONS):
        with tracing_context(enabled=True, parent=False):
            another_trace_method(fake_tool_response)
            another_trace_method(fake_tool_response)

    return {"messages": [fake_tool_response]}
