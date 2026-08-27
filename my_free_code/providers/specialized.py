from .adapters import OpenAIChatAdapter, AnthropicMessagesAdapter

class NIMAdapter(OpenAIChatAdapter):
    """NVIDIA NIM profile. NIM uses OpenAI-compatible chat semantics."""

class DeepSeekAdapter(OpenAIChatAdapter):
    """DeepSeek profile; reasoning fields are mapped by the request policy."""

class MistralAdapter(OpenAIChatAdapter):
    """Mistral/Codestral profile."""

class KimiAdapter(OpenAIChatAdapter):
    """Kimi profile."""

class ZAIAdapter(OpenAIChatAdapter):
    """Z.ai profile."""

class OpenRouterAdapter(OpenAIChatAdapter):
    """OpenRouter profile."""

SPECIALIZED = {
    "nvidia_nim": NIMAdapter,
    "deepseek": DeepSeekAdapter,
    "mistral": MistralAdapter,
    "mistral_codestral": MistralAdapter,
    "kimi": KimiAdapter,
    "kimi_code": KimiAdapter,
    "zai": ZAIAdapter,
    "zai_api": ZAIAdapter,
    "open_router": OpenRouterAdapter,
}
