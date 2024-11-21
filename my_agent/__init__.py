import os
if os.getenv("ENABLE_OTEL") == "true":
    from traceloop.sdk import Traceloop
    Traceloop.init(app_name="langgraph_example")
    print("ENABLING OTEL")
else:
    print("OTEL NOT ENABLED")
