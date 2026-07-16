import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


class OpenTelemetryTracer:
    """
    Enterprise OpenTelemetry distributed tracing setup.
    Exports traces via OTLP to collectors like Jaeger, DataDog, or New Relic.
    """

    def __init__(self, service_name: str = "dronzer-gateway"):
        self.service_name = service_name
        self.provider = None
        self.tracer = None

    def setup(self):
        """Initializes the OpenTelemetry TracerProvider."""
        resource = Resource.create(
            {SERVICE_NAME: self.service_name, "environment": os.getenv("ENVIRONMENT", "production")}
        )

        self.provider = TracerProvider(resource=resource)

        # Configure OTLP Exporter (Defaults to localhost:4317 if OTEL_EXPORTER_OTLP_ENDPOINT is not set)
        otlp_exporter = OTLPSpanExporter()

        # Use BatchSpanProcessor for high-throughput production environments
        span_processor = BatchSpanProcessor(otlp_exporter)
        self.provider.add_span_processor(span_processor)

        trace.set_tracer_provider(self.provider)
        self.tracer = trace.get_tracer(self.service_name)

    def get_tracer(self):
        if not self.tracer:
            self.setup()
        return self.tracer


# Global singleton
tracing = OpenTelemetryTracer()


def trace_function(name: str):
    """Decorator to easily trace any function call in the gateway."""

    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            tracer = tracing.get_tracer()
            with tracer.start_as_current_span(name) as span:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    span.record_exception(e)
                    span.set_status(trace.Status(trace.StatusCode.ERROR))
                    raise

        def sync_wrapper(*args, **kwargs):
            tracer = tracing.get_tracer()
            with tracer.start_as_current_span(name) as span:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    span.record_exception(e)
                    span.set_status(trace.Status(trace.StatusCode.ERROR))
                    raise

        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
