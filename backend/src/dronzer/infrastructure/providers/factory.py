import importlib

import structlog

from dronzer.domain.sdk.provider import IProvider

logger = structlog.get_logger("dronzer.providers.factory")


class ProviderFactory:
    """
    Factory for instantiating AI Provider SDKs dynamically.
    """

    _registry: dict[str, type[IProvider]] = {}
    _initialized = False

    @classmethod
    def _initialize_registry(cls):
        if cls._initialized:
            return

        # Explicit mapping of common provider IDs to their module paths and class names
        provider_map = {
            "anthropic": ("dronzer.infrastructure.providers.anthropic", "AnthropicProvider"),
            "cerebras": ("dronzer.infrastructure.providers.cerebras", "CerebrasProvider"),
            "cloudflare-workers-ai": (
                "dronzer.infrastructure.providers.cloudflare",
                "CloudflareProvider",
            ),
            "cohere": ("dronzer.infrastructure.providers.cohere", "CohereProvider"),
            "deepseek": ("dronzer.infrastructure.providers.deepseek", "DeepSeekProvider"),
            "fireworks": ("dronzer.infrastructure.providers.fireworks", "FireworksProvider"),
            "gemini": ("dronzer.infrastructure.providers.gemini", "GeminiProvider"),
            "google": ("dronzer.infrastructure.providers.gemini", "GeminiProvider"),  # Alias
            "google-ai-studio": (
                "dronzer.infrastructure.providers.gemini",
                "GeminiProvider",
            ),  # Alias
            "generic": ("dronzer.infrastructure.providers.generic", "GenericOpenAIProvider"),
            "groq": ("dronzer.infrastructure.providers.groq", "GroqProvider"),
            "lmstudio": ("dronzer.infrastructure.providers.lmstudio", "LMStudioProvider"),
            "mistral": ("dronzer.infrastructure.providers.mistral", "MistralProvider"),
            "mock": ("dronzer.infrastructure.providers.mock", "MockProvider"),
            "nvidia-nim": ("dronzer.infrastructure.providers.nvidia", "NvidiaNIMProvider"),
            "ollama": ("dronzer.infrastructure.providers.ollama", "OllamaProvider"),
            "openai": ("dronzer.infrastructure.providers.openai", "OpenAIProvider"),
            "openrouter": ("dronzer.infrastructure.providers.openrouter", "OpenRouterProvider"),
            "perplexity": ("dronzer.infrastructure.providers.perplexity", "PerplexityProvider"),
            "together": ("dronzer.infrastructure.providers.together", "TogetherProvider"),
            "vllm": ("dronzer.infrastructure.providers.vllm", "VLLMProvider"),
            "xai": ("dronzer.infrastructure.providers.xai", "XAIProvider"),
        }

        for provider_id, (module_path, class_name) in provider_map.items():
            try:
                module = importlib.import_module(module_path)
                provider_class = getattr(module, class_name)
                cls._registry[provider_id] = provider_class
            except (ImportError, AttributeError) as e:
                logger.warning(f"Failed to load provider SDK for {provider_id}: {e}")

        cls._initialized = True

    @classmethod
    def get_provider(cls, provider_id: str) -> IProvider:
        """
        Instantiates and returns the Provider SDK for the given ID.
        """
        cls._initialize_registry()

        provider_id = provider_id.lower()
        provider_class = cls._registry.get(provider_id)

        if not provider_class:
            raise ValueError(f"Provider SDK for '{provider_id}' is not implemented or registered.")

        return provider_class()
