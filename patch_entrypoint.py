#!/usr/bin/env python3
"""Patch entrypoint.py to copy config to ~/.nanobot."""
import pathlib

entrypoint = pathlib.Path('/home/uniuser/se-toolkit-lab-8/nanobot/entrypoint.py')
text = entrypoint.read_text()

# Добавляем копирование после write_runtime_config
old_func = '''def write_runtime_config(cfg: dict) -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    RUNTIME_CONFIG.write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )'''

new_func = '''def write_runtime_config(cfg: dict) -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    RUNTIME_CONFIG.write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    # Also copy to ~/.nanobot/config.json for nanobot gateway
    import shutil
    home_nanobot = pathlib.Path.home() / ".nanobot" / "config.json"
    home_nanobot.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(RUNTIME_CONFIG, home_nanobot)'''

text = text.replace(old_func, new_func)
entrypoint.write_text(text)
print('Updated entrypoint.py')
