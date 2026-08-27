import os
import shutil
import subprocess
from ..config import settings

def main():
    claude = shutil.which("claude")
    if not claude:
        raise SystemExit("Claude Code CLI was not found on PATH.")
    env = os.environ.copy()
    env["ANTHROPIC_BASE_URL"] = f"http://{settings.host}:{settings.port}"
    env["ANTHROPIC_AUTH_TOKEN"] = settings.auth_token
    env["CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY"] = "1"
    raise SystemExit(subprocess.call([claude, *os.sys.argv[1:]], env=env))

if __name__ == "__main__":
    main()
