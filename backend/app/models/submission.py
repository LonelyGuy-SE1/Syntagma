from typing import Literal

from pydantic import BaseModel, Field, field_validator


class CourseSubmission(BaseModel):
    course_title: str = Field(min_length=3, max_length=150)

    offering_department: str = Field(min_length=2, max_length=120)

    target_department: str = Field(min_length=2, max_length=120)

    semester: int = Field(ge=1, le=8)

    credit_category: Literal[0, 2, 4, 5]

    raw_course_content: str = Field(min_length=50)

    text_books: str = Field(min_length=5)

    reference_books: str = ""

    preferred_tools: str = ""

    @field_validator(
        "course_title",
        "offering_department",
        "target_department",
        "raw_course_content",
        "text_books",
        "reference_books",
        "preferred_tools",
        mode="before",
    )
    @classmethod
    def strip_text_fields(cls, value):
        if isinstance(value, str):
            return value.strip()

        return value