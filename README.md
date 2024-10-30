# Setup

1. Setup Python

    ```
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    ```

2. Set `$DD_API_KEY` environment variable.

# Execute

```
python3 trace.py
```

Output:

```
doing some work...
doing some nested work...
Global context baggage: {}
Span context baggage: {'foo': 'bar'}
Transient error StatusCode.UNAVAILABLE encountered while exporting traces to trace.agent.datadoghq.com, retrying in 1s.
Transient error StatusCode.UNAVAILABLE encountered while exporting traces to trace.agent.datadoghq.com, retrying in 2s.
Transient error StatusCode.UNAVAILABLE encountered while exporting traces to trace.agent.datadoghq.com, retrying in 4s.
```
