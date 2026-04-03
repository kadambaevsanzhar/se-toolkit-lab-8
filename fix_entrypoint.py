#!/usr/bin/env python3
"""Fix entrypoint.py gateway command."""
import pathlib

f = pathlib.Path('/home/uniuser/se-toolkit-lab-8/nanobot/entrypoint.py')
t = f.read_text()

# Заменяем команду запуска
old_cmd = '''    os.execv(
        NANOBOT_BIN,
        [
            NANOBOT_BIN,
            "gateway",
            "--config",
            str(RESOLVED_CONFIG_PATH),
            "--workspace",
            str(WORKSPACE_PATH),
        ],
    )'''

new_cmd = '''    os.environ["NANOBOT_CONFIG_FILE"] = str(RESOLVED_CONFIG_PATH)
    os.execv(
        NANOBOT_BIN,
        [
            NANOBOT_BIN,
            "gateway",
        ],
    )'''

t = t.replace(old_cmd, new_cmd)
f.write_text(t)
print('Fixed gateway command')
