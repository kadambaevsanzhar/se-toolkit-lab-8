import json
import os
import pathlib
import sys


APP_DIR = pathlib.Path("/app/nanobot")
CONFIG_PATH = APP_DIR / "config.json"
RESOLVED_CONFIG_PATH = APP_DIR / "config.resolved.json"
WORKSPACE_PATH = APP_DIR / "workspace"
NANOBOT_BIN = "/opt/nanobot/.venv/bin/nanobot"


def env_str(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return value


def env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return int(value)


def ensure_dict(parent: dict, key: str) -> dict:
    value = parent.get(key)
    if not isinstance(value, dict):
        value = {}
        parent[key] = value
    return value


def main() -> None:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        config = json.load(f)

    agents = ensure_dict(config, "agents")
    defaults = ensure_dict(agents, "defaults")

    providers = ensure_dict(config, "providers")
    custom = ensure_dict(providers, "custom")

    gateway = ensure_dict(config, "gateway")
    tools = ensure_dict(config, "tools")
    mcp_servers = ensure_dict(tools, "mcpServers")
    channels = ensure_dict(config, "channels")

    defaults["workspace"] = str(WORKSPACE_PATH)
    defaults["provider"] = "custom"

    llm_model = env_str("LLM_API_MODEL")
    if llm_model:
        defaults["model"] = llm_model

    llm_api_key = env_str("LLM_API_KEY")
    llm_api_base = env_str("LLM_API_BASE_URL")

    if llm_api_key:
        custom["apiKey"] = llm_api_key
    if llm_api_base:
        custom["apiBase"] = llm_api_base

    custom.setdefault("extraHeaders", None)

    gateway["host"] = env_str("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
    gateway["port"] = env_int("NANOBOT_GATEWAY_CONTAINER_PORT", 18790)

    heartbeat = ensure_dict(gateway, "heartbeat")
    heartbeat.setdefault("enabled", True)
    heartbeat.setdefault("intervalS", 1800)
    heartbeat.setdefault("keepRecentMessages", 8)

    channels["sendProgress"] = channels.get("sendProgress", True)
    channels["sendToolHints"] = channels.get("sendToolHints", False)
    channels["sendMaxRetries"] = channels.get("sendMaxRetries", 3)

    webchat = ensure_dict(channels, "webchat")
    webchat["enabled"] = True
    webchat["allowFrom"] = ["*"]
    webchat["host"] = env_str("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
    webchat["port"] = env_int("NANOBOT_WEBCHAT_CONTAINER_PORT", 8765)

    access_key = env_str("NANOBOT_ACCESS_KEY")
    if access_key:
        webchat["accessKey"] = access_key

    lms = ensure_dict(mcp_servers, "lms")
    lms["command"] = "python3"
    lms["args"] = ["-m", "mcp_lms"]

    lms_env = ensure_dict(lms, "env")
    lms_backend_url = env_str("NANOBOT_LMS_BACKEND_URL")
    lms_api_key = env_str("NANOBOT_LMS_API_KEY")

    if lms_backend_url:
        lms_env["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
    if lms_api_key:
        lms_env["NANOBOT_LMS_API_KEY"] = lms_api_key

    mcp_webchat = ensure_dict(mcp_servers, "webchat")
    mcp_webchat["command"] = "python3"
    mcp_webchat["args"] = ["-m", "mcp_webchat"]

    webchat_mcp_env = ensure_dict(mcp_webchat, "env")
    ui_relay_url = env_str("NANOBOT_WEBCHAT_UI_RELAY_URL")
    ui_relay_token = env_str("NANOBOT_WEBCHAT_UI_TOKEN", access_key)

    if ui_relay_url:
        webchat_mcp_env["NANOBOT_WEBCHAT_UI_RELAY_URL"] = ui_relay_url
    if ui_relay_token:
        webchat_mcp_env["NANOBOT_WEBCHAT_UI_TOKEN"] = ui_relay_token
    if access_key:
        webchat_mcp_env["NANOBOT_ACCESS_KEY"] = access_key

    with RESOLVED_CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Using config: {RESOLVED_CONFIG_PATH}", flush=True)

    if not os.path.exists(NANOBOT_BIN):
        raise FileNotFoundError(f"Nanobot binary not found: {NANOBOT_BIN}")

    os.environ["NANOBOT_CONFIG_FILE"] = str(RESOLVED_CONFIG_PATH)
    os.execv(
        NANOBOT_BIN,
        [
            NANOBOT_BIN,
            "gateway",
        ],
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[entrypoint] fatal error: {exc}", file=sys.stderr, flush=True)
        raise
