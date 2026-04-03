"""Patch nanobot-ai ChannelManager to register the lab's nanobot-webchat plugin.

PyPI nanobot-ai does not list webchat in ChannelsConfig or _init_channels, so the
WebSocket server on port 8765 never starts and Caddy returns 502 for /ws/chat.
Idempotent: skips if marker already present.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

MARKER = "# nanobot-lab: webchat-plugin (do not remove)"

INSERT_AFTER = 'logger.warning(f"QQ channel not available: {e}")'

PATCH_BLOCK = (
    "\n        "
    + MARKER
    + """
        try:
            import json
            from pathlib import Path as _Path

            _cfg_path = _Path.home() / ".nanobot" / "config.json"
            _webchat_cfg: dict = {}
            if _cfg_path.exists():
                _raw = json.loads(_cfg_path.read_text(encoding="utf-8"))
                _webchat_cfg = dict(_raw.get("channels", {}).get("webchat") or {})
            if _webchat_cfg.get("enabled"):
                from nanobot_webchat import WebChatChannel

                self.channels["webchat"] = WebChatChannel(_webchat_cfg, self.bus)
                logger.info("WebChat channel enabled")
        except ImportError as e:
            logger.warning(f"WebChat channel not available: {e}")
        except Exception as e:
            logger.warning(f"WebChat channel init failed: {e}")

"""
)


def main() -> None:
    spec = importlib.util.find_spec("nanobot.channels.manager")
    if spec is None or not spec.origin:
        raise SystemExit("nanobot.channels.manager not found — run inside venv with nanobot-ai installed")
    path = Path(spec.origin)
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"Already patched: {path}", flush=True)
        return
    if INSERT_AFTER not in text:
        raise SystemExit(f"Patch anchor not found in {path} — nanobot-ai layout changed?")
    path.write_text(text.replace(INSERT_AFTER, INSERT_AFTER + PATCH_BLOCK), encoding="utf-8")
    print(f"Patched WebChat into {path}", flush=True)


if __name__ == "__main__":
    main()
