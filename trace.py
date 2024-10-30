import os, socket

from opentelemetry import baggage, trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    BatchSpanProcessor
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import Status, StatusCode

provider = TracerProvider(resource=Resource.create({
    "service.name": __name__,
    # "datadog.host.use_as_metadata": True,
    "deployment.environment": "otel",
    "host.name": socket.gethostname(),
}))

# provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
# provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint="localhost:4317", insecure=True)))

exporter = OTLPSpanExporter(
    endpoint="https://trace.agent.datadoghq.com/api/v0.2/traces", # Replace this with the correct endpoint
    headers={
        "dd-protocol": "otlp",
        "dd-api-key": os.environ.get("DD_API_KEY"),
        "dd-otel-span-mapping": "{span_name_as_resource_name: true}",
        "dd-otlp-source": "datadog" # Replace this with the correct site
    },
)
provider.add_span_processor(BatchSpanProcessor(exporter))

tracer = trace.get_tracer("python", tracer_provider=provider)

with tracer.start_as_current_span("parent_span") as parent_span:
    ctx = baggage.set_baggage("foo", "bar")

    parent_span.set_status(Status(StatusCode.OK))
    # do some work that 'parent' tracks
    print("doing some work...")

    # Create a nested span to track nested work
    with tracer.start_as_current_span("child") as child:
        # do some work that 'child' tracks
        print("doing some nested work...")
        # the nested span is closed when it's out of scope

print(f"Global context baggage: {baggage.get_all()}")
print(f"Span context baggage: {baggage.get_all(context=ctx)}")