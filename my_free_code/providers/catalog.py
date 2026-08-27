from dataclasses import dataclass

@dataclass(frozen=True)
class Provider:
    id: str
    name: str
    key: str | None
    base_url: str | None

_ROWS = [
("nvidia_nim","NVIDIA NIM","NVIDIA_NIM_API_KEY","https://integrate.api.nvidia.com/v1"),
("open_router","OpenRouter","OPENROUTER_API_KEY","https://openrouter.ai/api/v1"),
("groq","Groq","GROQ_API_KEY","https://api.groq.com/openai/v1"),
("cline_pass","ClinePass","CLINE_API_KEY","https://api.cline.bot/v1"),
("openai","OpenAI","OPENAI_API_KEY","https://api.openai.com/v1"),
("xai","xAI","XAI_API_KEY","https://api.x.ai/v1"),
("qwencloud","QwenCloud Token Plan","QWENCLOUD_API_KEY","https://dashscope-intl.aliyuncs.com/compatible-mode/v1"),
("qwencloud_coding","QwenCloud Coding Plan","QWENCLOUD_CODING_API_KEY","https://coding-intl.dashscope.aliyuncs.com/v1"),
("together","Together AI","TOGETHER_API_KEY","https://api.together.xyz/v1"),
("deepinfra","DeepInfra","DEEPINFRA_API_KEY","https://api.deepinfra.com/v1/openai"),
("siliconflow","SiliconFlow","SILICONFLOW_API_KEY","https://api.siliconflow.com/v1"),
("nebius","Nebius","NEBIUS_API_KEY","https://api.tokenfactory.nebius.com/v1"),
("chutes","Chutes","CHUTES_API_KEY","https://llm.chutes.ai/v1"),
("featherless","Featherless","FEATHERLESS_API_KEY","https://api.featherless.ai/v1"),
("agnes","Agnes AI","AGNES_API_KEY","https://api.agnes-ai.com/v1"),
("zenmux","ZenMux","ZENMUX_API_KEY","https://api.zenmux.ai/v1"),
("wandb","W&B Inference","WANDB_API_KEY","https://api.inference.wandb.ai/v1"),
("azure_openai","Azure OpenAI","AZURE_OPENAI_API_KEY",None),
("gemini","Google AI Studio","GEMINI_API_KEY","https://generativelanguage.googleapis.com/v1beta/openai"),
("vertex","Google Vertex AI",None,None),
("deepseek","DeepSeek","DEEPSEEK_API_KEY","https://api.deepseek.com/v1"),
("mistral","Mistral","MISTRAL_API_KEY","https://api.mistral.ai/v1"),
("mistral_codestral","Mistral Codestral","CODESTRAL_API_KEY","https://codestral.mistral.ai/v1"),
("opencode_zen","OpenCode Zen","OPENCODE_API_KEY","https://opencode.ai/zen/v1"),
("opencode_go","OpenCode Go","OPENCODE_API_KEY","https://opencode.ai/zen/v1"),
("vercel","Vercel AI Gateway","AI_GATEWAY_API_KEY","https://ai-gateway.vercel.sh/v1"),
("bedrock","Amazon Bedrock","AWS_BEARER_TOKEN_BEDROCK",None),
("huggingface","Hugging Face","HUGGINGFACE_API_KEY","https://router.huggingface.co/v1"),
("cohere","Cohere","COHERE_API_KEY","https://api.cohere.com/compatibility/v1"),
("github_models","GitHub Models","GITHUB_MODELS_TOKEN","https://models.inference.ai.azure.com"),
("wafer","Wafer","WAFER_API_KEY","https://api.wafer.ai/v1"),
("kimi","Kimi API","KIMI_API_KEY","https://api.moonshot.ai/v1"),
("kimi_code","Kimi Code","KIMI_CODE_API_KEY","https://api.kimi.com/coding/v1"),
("minimax","MiniMax","MINIMAX_API_KEY","https://api.minimax.io/v1"),
("cerebras","Cerebras","CEREBRAS_API_KEY","https://api.cerebras.ai/v1"),
("sambanova","SambaNova","SAMBANOVA_API_KEY","https://api.sambanova.ai/v1"),
("kilo","Kilo.ai","KILO_API_KEY","https://api.kilo.ai/api/openrouter/v1"),
("fireworks","Fireworks AI","FIREWORKS_API_KEY","https://api.fireworks.ai/inference/v1"),
("novita","Novita AI","NOVITA_API_KEY","https://api.novita.ai/openai"),
("cloudflare","Cloudflare Workers AI","CLOUDFLARE_API_TOKEN",None),
("zai","Z.ai Coding","ZAI_API_KEY","https://api.z.ai/api/coding/paas/v4"),
("zai_api","Z.ai API","ZAI_API_KEY","https://api.z.ai/api/paas/v4"),
("tokenrouter","TokenRouter","TOKENROUTER_API_KEY","https://tokenrouter.io/api/v1"),
("nararoute","NaraRoute","NARAROUTE_API_KEY","https://router.bynara.id/v1"),
("poolside","Poolside","POOLSIDE_API_KEY","https://api.poolside.ai/v1"),
("llm7","LLM7","LLM7_API_KEY","https://api.llm7.io/v1"),
("ollama_cloud","Ollama Cloud","OLLAMA_API_KEY","https://ollama.com/v1"),
("lmstudio","LM Studio",None,"http://127.0.0.1:1234/v1"),
("llamacpp","llama.cpp",None,"http://127.0.0.1:8080/v1"),
("ollama","Ollama",None,"http://127.0.0.1:11434/v1"),
]
PROVIDERS = [Provider(*x) for x in _ROWS]
PROVIDER_MAP = {p.id:p for p in PROVIDERS}
