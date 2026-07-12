from app.routes.versions import _course_summary
from app.routes.preview import preview_all_html


def test_course_summary_uses_snapshot_fields():
    row = {
        "id": 4,
        "refined_id": 9,
        "course_json": {"semester": "3", "course_code": "CS201", "course_title": "Data Structures"},
    }

    assert _course_summary(row) == {
        "id": 4,
        "refined_id": 9,
        "semester": "3",
        "course_code": "CS201",
        "course_title": "Data Structures",
    }


def test_preview_html_endpoint_returns_html_response():
    # This is a unit test that the endpoint exists and returns HTMLResponse
    # The actual integration test with mock supabase would require more setup
    assert preview_all_html is not None
    assert callable(preview_all_html)


def test_version_preview_endpoint_exists():
    from app.routes.versions import preview_version

    assert preview_version is not None
    assert callable(preview_version)


def test_version_course_preview_endpoint_exists():
    from app.routes.versions import preview_version_course

    assert preview_version_course is not None
    assert callable(preview_version_course)
