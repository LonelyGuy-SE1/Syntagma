from app.services.refinement import _books, _units_from_course_contents, build_refined_payload


def test_units_are_read_from_course_contents():
    raw = """
Course Contents
Unit 1: Intro - A, B. 14 Hours
Unit 2: Core - C, D. 14 Hours
Unit 3: Advanced - E, F. 14 Hours
Unit 4: Applications - G, H. 14 Hours
Text Book(s):
1. Book
"""

    units = _units_from_course_contents(raw)

    assert [unit["title"] for unit in units] == ["Unit 1: Intro", "Unit 2: Core", "Unit 3: Advanced", "Unit 4: Applications"]
    assert units[0]["content"] == "A, B."


def test_books_remove_page_noise_and_numbering():
    books = _books("Text Book(s): 1. First Book, 2024.\nP.E.S. University\n2. Second Book, 2025.")

    assert books == ["First Book, 2024.", "Second Book, 2025."]


def test_refined_payload_keeps_deterministic_fields_and_four_units():
    sub = {
        "id": 10,
        "semester": "3",
        "course_title": "data structures",
        "target_department": "CSE",
        "credit_category": "5",
        "raw_course_content": """
Unit 1: Lists - linked lists. 14 Hours
Unit 2: Stacks - stacks. 14 Hours
Unit 3: Trees - trees. 14 Hours
Unit 4: Graphs - graphs. 14 Hours
""",
        "text_books": "1. Data Structures Book.",
        "reference_books": "",
        "preferred_tools": "C",
    }
    out = {
        "course_title": "Data Structures",
        "objectives": ["Use data structures"],
        "course_outcomes": ["Implement data structures"],
        "units": _units_from_course_contents(sub["raw_course_content"]),
        "tools_languages": "C",
    }

    payload = build_refined_payload(sub, out, [])

    assert payload["program"] == "B. TECH"
    assert payload["credits"] == 5
    assert payload["course_type"] == "Core Course-Lab Integrated"
    assert len(payload["units"]) == 4
    assert sum(unit["hours"] for unit in payload["units"]) == 56
