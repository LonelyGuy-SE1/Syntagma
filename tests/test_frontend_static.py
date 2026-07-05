import shutil
import subprocess
from pathlib import Path

import pytest


LIVE_EDITOR = Path("frontend/live-editor.html")


def test_live_editor_script_parses():
    node = shutil.which("node")
    if not node:
        pytest.skip("node is not installed")
    script = """
const fs = require('fs');
const html = fs.readFileSync('frontend/live-editor.html', 'utf8');
const match = html.match(/<script>([\\s\\S]*)<\\/script>/);
new Function(match[1]);
"""
    subprocess.run([node, "-e", script], check=True)


def test_live_editor_uses_safe_message_rendering():
    text = LIVE_EDITOR.read_text()

    assert "function renderMessageContent" in text
    assert ".innerHTML" not in text
