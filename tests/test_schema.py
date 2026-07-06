from pathlib import Path


SCHEMA = Path("docs/schema.sql")


def test_schema_file_is_schema_only():
    text = SCHEMA.read_text().lower()

    assert "alter table" not in text
    assert "insert into" not in text
    assert "drop table" not in text


def test_schema_has_required_tables():
    text = SCHEMA.read_text()
    for table in (
        "submissions",
        "refined_submissions",
        "agent_drafts",
        "agent_document_drafts",
        "finalized_submissions",
        "curriculum_versions",
        "course_revision_history",
        "chat_sessions",
        "chat_messages",
        "chat_attachments",
    ):
        assert f"create table if not exists {table}" in text
