import importlib
import sys


def load_openrouter(monkeypatch):
    monkeypatch.setenv("OPENROUTER_URL", "https://openrouter.test")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    monkeypatch.setenv("OPENROUTER_MODEL", "test-model")
    sys.modules.pop("app.services.openrouter", None)
    return importlib.import_module("app.services.openrouter")


def test_stream_token_reads_content_delta(monkeypatch):
    openrouter = load_openrouter(monkeypatch)
    line = 'data: {"choices":[{"delta":{"content":"hello"}}]}'

    assert openrouter._stream_token(line) == "hello"


def test_stream_token_ignores_comments_and_done(monkeypatch):
    openrouter = load_openrouter(monkeypatch)

    assert openrouter._stream_token(": OPENROUTER PROCESSING") == ""
    assert openrouter._stream_token("data: [DONE]") == ""
