import os, shutil, subprocess
from dataclasses import dataclass
from ..config import settings

@dataclass(frozen=True)
class ClientSpec:
    name: str
    executable: str
    base_env: str
    args: tuple[str, ...] = ()

CLIENTS = {
    "claude": ClientSpec("Claude Code", "claude", "ANTHROPIC_BASE_URL"),
    "codex": ClientSpec("Codex", "codex", "OPENAI_BASE_URL"),
    "opencode": ClientSpec("OpenCode", "opencode", "OPENAI_BASE_URL"),
    "cline": ClientSpec("Cline", "cline", "OPENAI_BASE_URL"),
    "pi": ClientSpec("Pi", "pi", "ANTHROPIC_BASE_URL"),
    "hermes": ClientSpec("Hermes", "hermes", "OPENAI_BASE_URL"),
    "deepseek-harness": ClientSpec("DeepSeek Harness", "deepseek-harness", "OPENAI_BASE_URL"),
    "grok": ClientSpec("Grok Build", "grok", "OPENAI_BASE_URL"),
    "muse": ClientSpec("Muse Code", "muse", "OPENAI_BASE_URL"),
}

def launch(client: str, args=None):
    spec = CLIENTS[client]
    exe = shutil.which(spec.executable)
    if not exe:
        raise SystemExit(f"{spec.executable!r} was not found on PATH.")
    env = os.environ.copy()
    base = f"http://{settings.host}:{settings.port}"
    env["ANTHROPIC_BASE_URL"] = base
    env["OPENAI_BASE_URL"] = base + "/v1"
    env["ANTHROPIC_AUTH_TOKEN"] = settings.auth_token
    env["OPENAI_API_KEY"] = settings.auth_token
    env["CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY"] = "1"
    no_proxy = env.get("NO_PROXY", "")
    env["NO_PROXY"] = ",".join(x for x in [no_proxy, "127.0.0.1", "localhost", "::1"] if x)
    env["no_proxy"] = env["NO_PROXY"]
    return subprocess.call([exe, *(args or [])], env=env)
