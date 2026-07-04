import io
import sys
import zipfile
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "backend"))

from app.services.attachments import MAX_FILE_BYTES, extract_text


def test_extract_text_file():
    text, status, error = extract_text("notes.txt", "text/plain", b"hello\n\nworld")

    assert text == "hello\n\nworld"
    assert status == "ready"
    assert error == ""


def test_extract_docx_file():
    data = io.BytesIO()
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body><w:p><w:r><w:t>first</w:t></w:r></w:p><w:p><w:r><w:t>second</w:t></w:r></w:p></w:body>"
        "</w:document>"
    )
    with zipfile.ZipFile(data, "w") as docx:
        docx.writestr("word/document.xml", xml)

    text, status, error = extract_text("notes.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", data.getvalue())

    assert text == "first\nsecond"
    assert status == "ready"
    assert error == ""


def test_reject_large_file():
    text, status, error = extract_text("large.txt", "text/plain", b"x" * (MAX_FILE_BYTES + 1))

    assert text == ""
    assert status == "failed"
    assert "8 MB" in error
