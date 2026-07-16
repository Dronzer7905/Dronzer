from prometheus_client import Counter, Gauge, Histogram, Info


class PrometheusMetrics:
    """
    Enterprise Prometheus metrics registry for the AI Gateway.
    Tracks requests, latency, tokens, cost, and provider health.
    """

    def __init__(self):
        # Request Counters
        self.http_requests_total = Counter(
            "dronzer_http_requests_total",
            "Total HTTP requests handled by the Gateway",
            ["method", "endpoint", "status"],
        )

        # Latency Histograms
        self.http_request_duration_seconds = Histogram(
            "dronzer_http_request_duration_seconds",
            "HTTP request latency",
            ["method", "endpoint"],
            buckets=[0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0],
        )

        # Provider Metrics
        self.provider_requests_total = Counter(
            "dronzer_provider_requests_total",
            "Total requests routed to a specific AI provider",
            ["provider", "model", "status"],
        )

        self.provider_latency_seconds = Histogram(
            "dronzer_provider_latency_seconds",
            "Latency of requests sent to upstream providers",
            ["provider", "model"],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 60.0],
        )

        # Token and Cost Tracking
        self.tokens_consumed_total = Counter(
            "dronzer_tokens_consumed_total",
            "Total tokens processed",
            ["provider", "model", "token_type"],  # prompt, completion, total
        )

        self.estimated_cost_usd = Counter(
            "dronzer_estimated_cost_usd",
            "Estimated cost in USD incurred from upstream providers",
            ["provider", "model"],
        )

        # System Health
        self.active_connections = Gauge(
            "dronzer_active_connections", "Number of currently active SSE/WebSocket connections"
        )

        self.gateway_info = Info("dronzer_gateway", "Dronzer AI Gateway Information")
        self.gateway_info.info({"version": "1.0.0", "environment": "production"})

    def record_request(self, method: str, endpoint: str, status: int, duration: float):
        self.http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
        self.http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(
            duration
        )

    def record_provider_call(
        self,
        provider: str,
        model: str,
        status: int,
        duration: float,
        prompt_tokens: int,
        completion_tokens: int,
        cost: float,
    ):
        self.provider_requests_total.labels(provider=provider, model=model, status=status).inc()
        self.provider_latency_seconds.labels(provider=provider, model=model).observe(duration)

        if prompt_tokens > 0:
            self.tokens_consumed_total.labels(
                provider=provider, model=model, token_type="prompt"
            ).inc(prompt_tokens)
        if completion_tokens > 0:
            self.tokens_consumed_total.labels(
                provider=provider, model=model, token_type="completion"
            ).inc(completion_tokens)

        if cost > 0:
            self.estimated_cost_usd.labels(provider=provider, model=model).inc(cost)


# Global singleton
metrics = PrometheusMetrics()
